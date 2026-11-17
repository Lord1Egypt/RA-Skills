"""
智汇简报 IndustryRadar — FastAPI 应用入口。

本地运行：
    cd project/backend
    python3 -m uvicorn main:app --host 0.0.0.0 --port 8000

同时托管前端静态页（project/frontend），因此浏览器直接访问 http://localhost:8000 即可。

云端对应关系（见《方案设计.md》）：
    FastAPI 路由  <->  APIG + FunctionGraph
    store.py      <->  RDS MySQL
    BRIEF_DIR     <->  OBS 对象
"""
from __future__ import annotations

import hashlib
import ipaddress
import json
import logging
import sqlite3
import time
from urllib.parse import urlparse
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import Body, FastAPI, Header, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import collector
import generator
import net_guard
import store
from config import (
    ALLOW_CUSTOM_SOURCES, BASE_DIR, CUSTOM_DISABLE_AFTER_FAILS, CUSTOM_MAX_PER_SUB,
    CUSTOM_MAX_PER_USER, CUSTOM_PROBE_TIMEOUT, DEMO_PASS, DEMO_USER, USE_LLM,
)
from sources import all_source_meta

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
)
log = logging.getLogger("industryradar")

app = FastAPI(title="智汇简报 IndustryRadar", version="1.1.0")
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
)

# 演示用极简会话（生产应换成 JWT + Redis，见方案设计「安全」小节）
_SESSIONS: Dict[str, Dict[str, Any]] = {}


# ------------------------------------------------------------------ 认证
def _hash(pw: str) -> str:
    return hashlib.sha256(("ir_salt_" + pw).encode("utf-8")).hexdigest()


def _token_for(user: Dict) -> str:
    tok = hashlib.sha1(f"{user['id']}-{user['username']}-{time.time()}".encode()).hexdigest()
    _SESSIONS[tok] = {"user_id": user["id"], "username": user["username"], "ts": time.time()}
    return tok


def current_user(authorization: Optional[str]) -> Dict[str, Any]:
    if not authorization:
        raise HTTPException(401, "未登录")
    tok = authorization.replace("Bearer ", "").strip()
    sess = _SESSIONS.get(tok)
    if not sess:
        raise HTTPException(401, "登录已失效，请重新登录")
    return sess


def _own_subscription(sub_id: int, me: Dict[str, Any]) -> Dict[str, Any]:
    """取订阅并校验归属。

    不存在与「不属于当前用户」都返回 404：不泄露资源是否存在，
    也避免调用方通过状态码枚举他人订阅。
    """
    sub = store.get_subscription(sub_id)
    if not sub or sub.get("user_id") != me["user_id"]:
        raise HTTPException(404, "订阅不存在")
    return sub


def _own_briefing(briefing_id: int, me: Dict[str, Any]) -> Dict[str, Any]:
    """取简报并顺着 subscription_id 校验归属；同样用 404 统一口径。"""
    b = store.get_briefing(briefing_id)
    if not b:
        raise HTTPException(404, "简报不存在")
    sub = store.get_subscription(b["subscription_id"])
    if not sub or sub.get("user_id") != me["user_id"]:
        raise HTTPException(404, "简报不存在")
    return b


# ------------------------------------------------------ 自定义源（RSS/Atom）
def _require_custom_enabled() -> None:
    if not ALLOW_CUSTOM_SOURCES:
        raise HTTPException(403, "当前部署已关闭自定义源功能")


def _own_custom_source(cs_id: int, me: Dict[str, Any]) -> Dict[str, Any]:
    """取自定义源并校验归属；非本人一律 404，避免枚举。"""
    cs = store.get_custom_source(cs_id)
    if not cs or cs.get("user_id") != me["user_id"]:
        raise HTTPException(404, "自定义源不存在")
    return cs


def _clean_source_url(raw: str) -> str:
    """录入前的地址清洗：只放行公网域名上的 http/https 标准端口。

    真正的访问控制仍由 net_guard 在每次抓取时执行（含重定向逐跳校验），
    这里提前拦住明显不合规的输入，给出可读错误而不是静默抓空。
    """
    url = (raw or "").strip()
    if not url:
        raise HTTPException(400, "源地址不能为空")
    if len(url) > 500:
        raise HTTPException(400, "源地址过长（上限 500 字符）")
    try:
        p = urlparse(url)
    except ValueError as exc:
        raise HTTPException(400, "源地址格式不合法") from exc
    if p.scheme.lower() not in ("http", "https"):
        raise HTTPException(400, "仅支持 http/https 订阅源")
    if p.username or p.password:
        raise HTTPException(400, "源地址不允许携带用户名密码")
    host = (p.hostname or "").strip()
    if not host:
        raise HTTPException(400, "源地址缺少域名")
    try:
        ipaddress.ip_address(host.strip("[]"))
    except ValueError:
        pass
    else:
        raise HTTPException(400, "请填写域名，不支持直接填写 IP 地址")
    try:
        net_guard.check_url(url)
    except net_guard.UnsafeUrlError as exc:
        raise HTTPException(400, f"源地址不可用：{exc}") from exc
    return url


def _probe_custom_source(url: str) -> int:
    """录入/自检时实际抓一次，必须能解析出条目才算有效订阅源。"""
    items, err = collector.fetch_source_checked(
        {"name": "probe", "url": url, "category": "自定义", "_strict_xml": True},
        timeout=CUSTOM_PROBE_TIMEOUT,
    )
    if err:
        raise HTTPException(400, f"无法解析为订阅源：{err}")
    return len(items)


def _sanitize_sources(ids: List[str], user_id: int) -> List[str]:
    """订阅只能引用内置源与自己的、已启用的自定义源；越界项静默剔除。"""
    valid = {m["id"] for m in all_source_meta()}
    own = {f"cs:{c['id']}" for c in store.list_custom_sources(user_id) if c.get("enabled")}
    out: List[str] = []
    custom_used = 0
    for sid in ids:
        if sid in valid:
            out.append(sid)
        elif sid in own and custom_used < CUSTOM_MAX_PER_SUB:
            out.append(sid)
            custom_used += 1
    return out


def _detach_custom_source(user_id: int, cs_id: int) -> None:
    """删除自定义源前，把它从该用户所有订阅的 sources_json 中摘掉。"""
    token = f"cs:{cs_id}"
    for sub in store.list_subscriptions(user_id):
        try:
            ids = json.loads(sub.get("sources_json") or "[]")
        except (ValueError, TypeError):
            continue
        if not isinstance(ids, list) or token not in ids:
            continue
        store.update_subscription(
            sub["id"],
            {"sources_json": json.dumps([i for i in ids if i != token], ensure_ascii=False)},
        )


def _ensure_demo_user() -> Dict[str, Any]:
    u = store.get_user_by_name(DEMO_USER)
    if not u:
        uid = store.create_user(DEMO_USER, _hash(DEMO_PASS), "demo@example.com")
        u = store.get_user_by_name(DEMO_USER)
        # 预置一个示例订阅，首次进入即可看到效果
        store.create_subscription(
            uid, "新能源汽车 × 固态电池", "新能源汽车,汽车", "固态电池,电池,续航",
            "量产,车企", json.dumps(["36kr", "zhihu_daily", "techcrunch"]),
        )
    return u


@app.on_event("startup")
def _startup() -> None:
    store.init_db()
    _ensure_demo_user()
    log.info("IndustryRadar started. LLM=%s", "on" if USE_LLM else "off(fallback)")


# ------------------------------------------------------------------ 模型
class LoginIn(BaseModel):
    username: str
    password: str


class SubIn(BaseModel):
    name: str
    industry_kw: str
    tech_kw: str
    extra_kw: str = ""
    sources: List[str] = []
    frequency: str = "weekly"
    style: str = "standard"      # standard 标准周报 / curated 编辑精选


class SubPatch(BaseModel):
    name: Optional[str] = None
    industry_kw: Optional[str] = None
    tech_kw: Optional[str] = None
    extra_kw: Optional[str] = None
    sources: Optional[List[str]] = None
    frequency: Optional[str] = None
    style: Optional[str] = None
    enabled: Optional[int] = None


class PreviewIn(BaseModel):
    industry_kw: str
    tech_kw: str
    extra_kw: str = ""
    sources: List[str] = []


class CustomSourceIn(BaseModel):
    name: str
    url: str


class CustomSourcePatch(BaseModel):
    name: Optional[str] = None
    url: Optional[str] = None
    enabled: Optional[int] = None


# ------------------------------------------------------------------ API
@app.post("/api/login")
def login(body: LoginIn) -> Dict[str, Any]:
    u = store.get_user_by_name(body.username)
    if not u or u["password_hash"] != _hash(body.password):
        raise HTTPException(401, "用户名或密码错误")
    return {"token": _token_for(u), "username": u["username"], "user_id": u["id"]}


@app.get("/api/sources")
def list_sources() -> Dict[str, Any]:
    return {"sources": all_source_meta()}


@app.get("/api/config")
def get_config() -> Dict[str, Any]:
    """前端展示当前运行模式（LLM 在线 / 离线降级）。"""
    return {
        "llm_enabled": USE_LLM,
        "mode": "在线大模型" if USE_LLM else "离线规则引擎（可配置 LLM）",
        "version": app.version,
    }


@app.get("/api/custom-sources")
def list_custom_sources(authorization: Optional[str] = Header(None)) -> Dict[str, Any]:
    """当前用户的自定义源列表（含抓取健康状态与引用次数）。"""
    me = current_user(authorization)
    usage = store.custom_source_usage(me["user_id"])
    items = []
    for cs in store.list_custom_sources(me["user_id"]):
        cs["used_by"] = usage.get(cs["id"], 0)
        items.append(cs)
    return {
        "enabled": ALLOW_CUSTOM_SOURCES,
        "sources": items,
        "limits": {"max_per_user": CUSTOM_MAX_PER_USER, "max_per_sub": CUSTOM_MAX_PER_SUB},
    }


@app.post("/api/custom-sources")
def create_custom_source(body: CustomSourceIn,
                         authorization: Optional[str] = Header(None)) -> Dict[str, Any]:
    me = current_user(authorization)
    _require_custom_enabled()

    name = (body.name or "").strip()
    if not name:
        raise HTTPException(400, "请填写源名称")
    if len(name) > 60:
        raise HTTPException(400, "源名称过长（上限 60 字符）")

    if store.count_custom_sources(me["user_id"]) >= CUSTOM_MAX_PER_USER:
        raise HTTPException(400, f"自定义源数量已达上限（{CUSTOM_MAX_PER_USER} 个）")

    url = _clean_source_url(body.url)
    if any(c["url"] == url for c in store.list_custom_sources(me["user_id"])):
        raise HTTPException(400, "该源已存在，无需重复添加")

    # 先探活：解析不出条目的地址不入库，避免留下永远抓不到的垃圾源
    count = _probe_custom_source(url)
    try:
        cs_id = store.create_custom_source(me["user_id"], name, url)
    except sqlite3.IntegrityError as exc:
        raise HTTPException(400, "该源已存在，无需重复添加") from exc
    return {"id": cs_id, "items": count, "message": f"已添加，首次抓取到 {count} 条"}


@app.put("/api/custom-sources/{cs_id}")
def update_custom_source(cs_id: int, body: CustomSourcePatch,
                         authorization: Optional[str] = Header(None)) -> Dict[str, Any]:
    me = current_user(authorization)
    _require_custom_enabled()
    cs = _own_custom_source(cs_id, me)

    fields: Dict[str, Any] = {}
    if body.name is not None:
        name = body.name.strip()
        if not name:
            raise HTTPException(400, "请填写源名称")
        if len(name) > 60:
            raise HTTPException(400, "源名称过长（上限 60 字符）")
        fields["name"] = name

    if body.url is not None:
        url = _clean_source_url(body.url)
        if url != cs["url"]:
            if any(c["url"] == url and c["id"] != cs_id
                   for c in store.list_custom_sources(me["user_id"])):
                raise HTTPException(400, "该源已存在，无需重复添加")
            count = _probe_custom_source(url)
            fields.update(url=url, status="ok", fail_count=0,
                          last_status="ok", last_error=None)
            fields["_probe_items"] = count

    if body.enabled is not None:
        fields["enabled"] = 1 if body.enabled else 0
        # 重新启用时清空失败计数，给它一次干净的重试机会
        if fields["enabled"] and cs.get("status") == "disabled":
            fields.update(status="ok", fail_count=0, last_error=None)

    probe_items = fields.pop("_probe_items", None)
    store.update_custom_source(cs_id, fields)
    resp: Dict[str, Any] = {"message": "更新成功"}
    if probe_items is not None:
        resp["items"] = probe_items
    return resp


@app.delete("/api/custom-sources/{cs_id}")
def delete_custom_source(cs_id: int,
                         authorization: Optional[str] = Header(None)) -> Dict[str, Any]:
    me = current_user(authorization)
    _own_custom_source(cs_id, me)
    # 先摘掉订阅里的引用，避免订阅指向已删除的源
    _detach_custom_source(me["user_id"], cs_id)
    store.delete_custom_source(cs_id)
    return {"message": "已删除"}


@app.post("/api/custom-sources/{cs_id}/test")
def test_custom_source(cs_id: int,
                       authorization: Optional[str] = Header(None)) -> Dict[str, Any]:
    """手动复检：重新走一遍出站校验与抓取，并把结果写回健康状态。"""
    me = current_user(authorization)
    _require_custom_enabled()
    cs = _own_custom_source(cs_id, me)

    try:
        net_guard.check_url(cs["url"])
    except net_guard.UnsafeUrlError as exc:
        store.record_custom_source_result(cs_id, False, f"地址不再允许访问：{exc}")
        raise HTTPException(400, f"源地址不可用：{exc}") from exc

    items, err = collector.fetch_source_checked(
        {"name": cs["name"], "url": cs["url"], "category": "自定义", "_strict_xml": True},
        timeout=CUSTOM_PROBE_TIMEOUT,
    )
    store.record_custom_source_result(cs_id, not err, err)
    if err:
        return {"ok": False, "items": 0, "error": err}
    return {"ok": True, "items": len(items), "error": ""}


@app.get("/api/subscriptions")
def get_subscriptions(authorization: Optional[str] = Header(None)) -> Dict[str, Any]:
    me = current_user(authorization)
    return {"subscriptions": store.list_subscriptions(me["user_id"])}


@app.post("/api/subscriptions")
def post_subscription(body: SubIn, authorization: Optional[str] = Header(None)) -> Dict[str, Any]:
    me = current_user(authorization)
    if not body.name or not body.industry_kw or not body.tech_kw:
        raise HTTPException(400, "名称 / 行业词 / 技术词 均为必填")
    sid = store.create_subscription(
        me["user_id"], body.name, body.industry_kw, body.tech_kw,
        body.extra_kw,
        json.dumps(_sanitize_sources(body.sources, me["user_id"]), ensure_ascii=False),
        body.frequency,
        style=(body.style or "standard"),
    )
    return {"id": sid, "message": "创建成功"}


@app.put("/api/subscriptions/{sub_id}")
def put_subscription(sub_id: int, body: SubPatch,
                     authorization: Optional[str] = Header(None)) -> Dict[str, Any]:
    me = current_user(authorization)
    _own_subscription(sub_id, me)
    fields = body.model_dump(exclude_none=True)
    if "sources" in fields:
        fields["sources_json"] = json.dumps(
            _sanitize_sources(fields.pop("sources"), me["user_id"]), ensure_ascii=False,
        )
    store.update_subscription(sub_id, fields)
    return {"message": "更新成功"}


@app.delete("/api/subscriptions/{sub_id}")
def del_subscription(sub_id: int, authorization: Optional[str] = Header(None)) -> Dict[str, Any]:
    me = current_user(authorization)
    _own_subscription(sub_id, me)
    store.delete_subscription(sub_id)
    return {"message": "已删除"}


@app.post("/api/subscriptions/{sub_id}/run")
def run_subscription(sub_id: int, authorization: Optional[str] = Header(None)) -> Dict[str, Any]:
    """手动触发一次简报生成（等价于云端 TIMER 触发）。"""
    me = current_user(authorization)
    sub = _own_subscription(sub_id, me)
    try:
        result = generator.run_pipeline(sub, save=True)
    except Exception as exc:  # noqa: BLE001
        log.exception("pipeline failed")
        raise HTTPException(500, f"生成失败：{exc}") from exc
    return {
        "briefing_id": result["briefing_id"],
        "title": result["title"],
        "stats": result["stats"],
        "message": "简报生成完成",
    }


@app.post("/api/preview")
def preview(body: PreviewIn, authorization: Optional[str] = Header(None)) -> Dict[str, Any]:
    """关键词预览：跑一遍 pipeline 但不落库，方便控制台即时看效果。"""
    me = current_user(authorization)
    sub = {
        "id": 0,
        "name": f"{body.industry_kw} × {body.tech_kw}",
        "industry_kw": body.industry_kw,
        "tech_kw": body.tech_kw,
        "extra_kw": body.extra_kw,
        "sources_json": json.dumps(
            _sanitize_sources(body.sources, me["user_id"]), ensure_ascii=False,
        ),
        "user_id": me["user_id"],
    }
    result = generator.run_pipeline(sub, save=False)
    return {"markdown": result["markdown"], "stats": result["stats"]}


@app.get("/api/articles")
def get_articles(subscription_id: int = Query(...), limit: int = 100,
                 authorization: Optional[str] = Header(None)) -> Dict[str, Any]:
    me = current_user(authorization)
    _own_subscription(subscription_id, me)
    return {"articles": store.list_articles(subscription_id, limit)}


@app.get("/api/briefings")
def get_briefings(subscription_id: int = Query(...),
                  authorization: Optional[str] = Header(None)) -> Dict[str, Any]:
    me = current_user(authorization)
    _own_subscription(subscription_id, me)
    items = store.list_briefings(subscription_id)
    for b in items:
        b.pop("md_path", None)
    return {"briefings": items}


@app.get("/api/briefings/{briefing_id}")
def get_briefing(briefing_id: int, authorization: Optional[str] = Header(None)) -> Dict[str, Any]:
    me = current_user(authorization)
    b = _own_briefing(briefing_id, me)
    b["markdown"] = _read_md(b.get("md_path", ""))
    return b


@app.get("/api/briefings/{briefing_id}/export", response_class=PlainTextResponse)
def export_briefing(briefing_id: int, fmt: str = "md",
                    authorization: Optional[str] = Header(None)) -> PlainTextResponse:
    me = current_user(authorization)
    b = _own_briefing(briefing_id, me)
    md = _read_md(b.get("md_path", ""))
    filename = f"briefing_{briefing_id}.md"
    return PlainTextResponse(
        md, media_type="text/markdown; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@app.get("/api/trend")
def get_trend(subscription_id: int = Query(...),
              authorization: Optional[str] = Header(None)) -> Dict[str, Any]:
    me = current_user(authorization)
    _own_subscription(subscription_id, me)
    return store.trend_data(subscription_id)


@app.get("/api/dashboard")
def dashboard(authorization: Optional[str] = Header(None)) -> Dict[str, Any]:
    """控制台总览：订阅数 / 简报数 / 文章数。"""
    me = current_user(authorization)
    subs = store.list_subscriptions(me["user_id"])
    briefings = sum(s.get("briefing_count", 0) for s in subs)
    articles = 0
    for s in subs:
        articles += len(store.list_articles(s["id"], limit=1000))
    return {
        "subscription_count": len(subs),
        "briefing_count": briefings,
        "article_count": articles,
        "llm_enabled": USE_LLM,
    }


def _read_md(path: str) -> str:
    try:
        p = Path(path)
        if p.exists():
            return p.read_text(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass
    return ""


# ------------------------------------------------------------ 静态前端托管
_FRONTEND = BASE_DIR / "frontend"
if _FRONTEND.exists():
    app.mount("/", StaticFiles(directory=str(_FRONTEND), html=True), name="frontend")