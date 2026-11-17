"""OwlWrite MCP 服务器（S5）。

把 owl-gateway 的核心 API 包成 MCP 工具，让 Agent 终端（WorkBuddy / Claude 等）
用自然语言跑完「检索 → 写作 → 查重 → 核验」闭环。

配置（环境变量，均为 MCP 客户端里配置，不落仓库）：
  OWL_BASE     网关地址，默认 http://127.0.0.1:8787
  OWL_API_KEY  用户 API key（owl_sk_...，必填）

在 MCP 客户端里的配置示例（claude_desktop_config.json / workbuddy mcp.json）：
  {
    "mcpServers": {
      "owlwrite": {
        "command": "python",
        "args": ["C:/path/to/owl-gateway/mcp_server.py"],
        "env": {"OWL_BASE": "https://owl.skillsutra.cn", "OWL_API_KEY": "owl_sk_..."}
      }
    }
  }

设计原则：
  - 工具返回**结构化 JSON 文本**，字段名与服务端一致，Agent 可直接消费；
  - 错误透传服务端的 code/message（402 余额不足、422 参数错、401 key 错），
    绝不吞掉——Agent 需要根据 code 决定是提示用户充值还是改参数；
  - 计费语义原样暴露：搜索返回 points_charged，写作/查重走 quote→run 两步，
    Agent 必须先报价给用户看，再执行（技能文档里写死了这条礼仪）。
"""

import asyncio
import json
import os
import urllib.parse
from contextvars import ContextVar

import httpx
from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

OWL_BASE = os.environ.get("OWL_BASE", "http://127.0.0.1:8787").rstrip("/")
# 对外可访问基址（2026-10-30 缺陷修复）：远程 MCP 场景由 mcp_remote 注入公网域名；
# stdio 场景未设置时回退 OWL_BASE —— 行为与修复前逐字节一致。
# 严禁把 _call() 里的自调地址改成 PUBLIC_BASE：自调必须走 loopback（计费闸门依赖它）。
PUBLIC_BASE = (os.environ.get("OWL_PUBLIC_BASE") or OWL_BASE).rstrip("/")
OWL_API_KEY = os.environ.get("OWL_API_KEY", "")
# 技能版本随包发布，网关据此判断是否强制更新（meta.json 的 min_supported_version）。
# 必须在每次请求里带上，否则网关无法识别旧版客户端（缺头时网关一律放行，避免误伤 API 用户）。
# ⚠️ 发布前必须与 SKILL.md 的 version / connector-meta.version / meta.json latest_version
#    四处对齐（preflight A30 守门），否则装的是最新版也会被自己判成旧版——每次开工都
#    提示「有新版本」，而更新完还是同一句（假提示，严重时 426 全停）。
OWL_SKILL_VERSION = "1.3.2"

mcp = MCPServer(
    "owlwrite",
    instructions=(
        "OwlWrite（夜猫子论文写作）：文献检索、论文写作、查重、引文核验一站式服务。"
        "典型工作流：1) owl_search 检索文献；2) owl_quote 对写作/查重/核验/排版报价；"
        "3) 把报价告诉用户；4) owl_run 执行；5) owl_run_status 轮询到结束。"
        "所有工具返回 JSON；points_charged 是本次消耗的积分（1 积分=0.01 元）。"
        "任何工具返回里出现 _notice_tip 时，必须按它的要求把活动/公告转告用户。"
    ),
)

_TIMEOUT = httpx.Timeout(120.0, connect=10.0)


# 远程 MCP（/mcp）下的**每次请求**的用户 token：由鉴权中间件按请求注入。
# stdio 场景无中间件，恒为空 → 回退到模块级 OWL_API_KEY，行为与改造前逐字节一致。
_request_token: ContextVar[str] = ContextVar("owl_request_token", default="")


def _bearer() -> str:
    return _request_token.get() or OWL_API_KEY


def _headers() -> dict:
    tok = _bearer()
    if not tok:
        raise ToolError(
            "未配置 OWL_API_KEY。请在 MCP 客户端配置里加 env: {\"OWL_API_KEY\": \"owl_sk_...\"}；"
            "还没有账号请到 paper.skillsutra.cn 注册。")
    return {"Authorization": f"Bearer {tok}",
            "Content-Type": "application/json",
            "X-Owl-Skill-Version": OWL_SKILL_VERSION}


async def _call(method: str, path: str, body: dict | None = None, params: dict | None = None,
                timeout: float | None = None) -> dict:
    async with httpx.AsyncClient(timeout=timeout or _TIMEOUT) as c:
        r = await c.request(method, OWL_BASE + path,
                            json=body, params=params, headers=_headers())
    try:
        data = r.json()
    except Exception:
        data = {"raw": r.text[:500]}
    # 错误结构化透传，不包装不吞——Agent 按 code 分支处理；
    # ToolError → 客户端收到 is_error=True + JSON 消息，无 traceback 污染流
    _raise_if_error(r, data)
    # 活动/公告透传（2026-11-04）：网关把当前活动挂在响应顶层 owl_notice，
    # 这里补 _notice_tip 让 Agent 一定转告用户，不依赖它有没有先调 owl_meta。
    return _notices_tip(data)


_NOTICE_SEEN_PATH = os.path.expanduser("~/.owl_notice_seen.json")


def _notices_tip(data):
    """把网关挂在响应里的活动公告（owl_notice）转成给 Agent 的硬提示。

    网关从 2026-11-04 起在 /v1/* 响应顶层带 owl_notice；这里再补一步：
    未看过的公告 → 附 `_notice_tip` 明确要求转告用户，并记下 id 避免每次调用都重复。
    **写不了本地文件也照常提示**——宁可重复，不可漏发（这正是本功能的初衷）。
    """
    try:
        if not isinstance(data, dict):
            return data
        items = data.get("owl_notice")
        if not items:
            return data
        seen: set = set()
        try:
            with open(_NOTICE_SEEN_PATH, encoding="utf-8") as f:
                seen = set(json.load(f) or [])
        except Exception:
            seen = set()
        fresh = [n for n in items
                 if isinstance(n, dict) and n.get("id") and n["id"] not in seen]
        if not fresh:
            return data
        texts = "；".join(str(n.get("text") or "").strip() for n in fresh)
        data["_notice_tip"] = (
            "【请转告用户】" + texts +
            "。把这件事用一两句话顺口告诉用户即可，不要打断正在进行的任务，也不要替他做选择。")
        try:
            with open(_NOTICE_SEEN_PATH, "w", encoding="utf-8") as f:
                json.dump(sorted(seen | {n["id"] for n in fresh}), f)
        except Exception:
            pass
    except Exception:  # noqa: BLE001 — 公告透传绝不影响主流程
        pass
    return data


def _dump(d) -> str:
    return json.dumps(d, ensure_ascii=False, indent=1)


def _raise_if_error(r, data) -> None:
    """统一错误透传：服务端 code/message/extra 原样抛给 Agent，不包装不吞。

    非结构化错误体（HTML 维护页/代理错误页等）不外泄内部细节，只给人话兜底——
    与 CLI（owl_api.request）同一口径。
    """
    if r.status_code < 400:
        return
    err = data.get("detail") if isinstance(data.get("detail"), dict) else data
    code = str((err or {}).get("code") or "").strip()
    msg = str((err or {}).get("message") or "").strip()
    if not (code or msg):
        raise ToolError(json.dumps(
            {"error": f"http_{r.status_code}",
             "message": f"服务暂时不可用（HTTP {r.status_code}），请稍后重试；"
                        "若持续出现请把当前操作反馈给客服",
             "http_status": r.status_code}, ensure_ascii=False))
    extra = {k: v for k, v in (err or {}).items()
             if k not in ("code", "message") and k not in ("detail",)}
    raise ToolError(json.dumps(
        {"error": code or f"http_{r.status_code}", "message": msg, "http_status": r.status_code, **extra},
        ensure_ascii=False))


# ---------------- 工具定义 ----------------

@mcp.tool()
async def owl_search(query: str, limit: int = 5, lang: str = "all", expand: bool = False) -> str:
    """文献检索（同步返回）。返回题名/作者/期刊/年份/DOI/摘要，并按相关性重排。

    返回字段里值得转告用户的：
      - score：相关性得分（题名命中 > 摘要命中 > 核心刊 > 有 DOI > 年份新）
      - core / core_tags：是否核心期刊（core_tags 是官方权威标记，如 BDHX 北大核心 / CSCD / CSSCI / SCI）
      - is_oa：是否为开放获取（外文命中时可直接用 owl_oa 免费取全文）

    Args:
        query: 检索词。自然语言即可；中文查中文库、英文查全球库，自动路由。
        limit: 返回条数，1-50，默认 5。
        lang: all / zh / en，默认 all（按 query 自动判断）。
        expand: 是否强制关键词扩展（同义词替换再检一轮）。结果 <3 条时会自动扩一次。

    计费：命中 2 积分，缓存命中 1 积分，无结果 0 积分。
    """
    body = {"query": query, "limit": limit, "lang": lang}
    if expand:
        body["expand"] = True
    return _dump(await _call("POST", "/v1/search", body))


@mcp.tool()
async def owl_products() -> str:
    """全平台价目表（积分体系，1 积分=0.01 元）。含写作/检索/全文/核验 + 21 个检测商品。
    任何报价、价格说明前必调；价格以本工具实时返回为准（勿引用文档里的静态数字）。"""
    return _dump(await _call("GET", "/v1/prices"))


@mcp.tool()
async def owl_meta() -> str:
    """技能版本与平台公告。**每次会话开工时必调一次**，按三级判定处理返回：

    1) required_update=true 且本地版本 < min_supported_version → **必须停止后续付费动作**，
       先让用户更新技能（只有两个官方入口：SkillHub https://skillhub.cn/skills/user_164f4c1f/owlwrite-paper
       或 ClawHub https://clawhub.ai/j-levee/skills/owlwrite-paper，余额与数据不受影响），
       并把 required_reason 原话说给用户听；
    2) 仅 latest_version 更高 → 一句话提示可更新，**不阻塞**本次任务；
    3) 版本一致 → 静默，不打扰用户。
    notices 里有新公告时按相关度转告。活动类公告同时会随任意工具返回的
    owl_notice / _notice_tip 送达，看到就转告，不必等本工具。

    检测类任务开工前看 channels.weipu_ready：它是检测服务的**真实连通性**检查结果（不是「凭据填没填」）。
    为 false 时读同级 channels.weipu_detail（一句人话）转告用户，别把 weipu_state 的内部码念给他；
    只有 true 才去报价，否则白跑一趟。"""
    return _dump(await _call("GET", "/v1/meta"))


@mcp.tool()
async def owl_disciplines() -> str:
    """斟知学科码表（智评 class_id 用）。

    何时调：用户要做**斟知智评**（商品 1026/1029/1030）检测且要指定学科时；
    查重/大学生版（1034 等）**不需要** class_id，别多调。

    返回 dims 五个维度：1-1 研究生专硕 / 1-2 研究生学硕 / 2-1 本科 / 2-2 高职本科 /
    2-3 高职专科。**礼仪**：先问用户是哪类（本科/研究生），再只展开对应维度逐级
    筛选让用户选，不要把 5000 条直接甩出来。503 weipu_unavailable = 检测服务暂未
    开通，请如实告知用户「检测服务暂不可用，非你的操作问题」，并先做写作/检索。
    """
    return _dump(await _call("GET", "/v1/disciplines"))


@mcp.tool()
async def owl_quote(action: str, params: dict) -> str:
    """对写作/查重/核验/排版报价（不扣费）。返回 quote_id，供 owl_run 使用。

    Args:
        action: "write" | "check" | "verify"
          - write: params = {"topic": 题目, "mode": standard|guided, "target_chars": 目标字数}
          - check: params = {"file_id": 已上传文件编号, "product": 商品 code, "hanzi": 汉字数,
                             "title": 题名, "author": 作者}
                    纯文本可直接用 {"content": 全文, "product": ...}（服务端落成 docx 走真实解析）；
                    图像 / 格式检测必须给 file_id（先 owl_upload 上传本机文件）。
                    product 先调 owl_products 获取，去掉 `wp.` 前缀只留裸编码。
          - verify: params = {"refs_text": 参考文献编号列表文本(GB/T 7714), "lang": zh|en|auto}
          - typeset: 排版报价（mode: latex|docx + 页数等，跟 owl_typeset 流程走，一般直接用 owl_typeset 不必手拼）
        params: 上述参数字典。

    礼仪（技能文档强制）：拿到报价先告知用户价格，经同意再 owl_run。不要默默扣费。
    写作与检测都是**后付费**（billing_mode=postpaid）：积分估算仅作参考，以实际扣除为准
    （按实际成文字数 / 解析出的真实字符数精确结算，无冻结、无上限）。
    """
    return _dump(await _call("POST", "/v1/quote", {"action": action, "params": params}))


def _docx_hanzi(path: str) -> int:
    """数 .docx 正文汉字数，口径与网关一致（800 汉字 ≈ 1 页）。

    报价要先于执行给出，而 docx 的页数只能从正文来：网关在 /v1/typeset 里会自己再数一遍
    （客户端申报不可信），这里数是为了让「先告诉用户多少钱」这一步的数字与最终扣费一致。
    """
    try:
        import re as _re
        import zipfile
        with zipfile.ZipFile(path) as z:
            if z.getinfo("word/document.xml").file_size > 64 * 1024 * 1024:  # 防 zip 炸弹
                return 0
            xml = z.read("word/document.xml").decode("utf-8", "ignore")
        return len(_re.findall(r"[\u4e00-\u9fff]", _re.sub(r"<[^>]+>", "", xml)))
    except Exception:  # noqa: BLE001 — 读不出来就让调用方回退到用户申报的页数
        return 0


async def _upload_local(file_path: str, max_mb: int = 60) -> dict:
    """把本机文件传上去。排版包（含图/字体）天然比单个文档大，上限抬到 60MB。

    网关侧按扩展名再判一次上限：.zip=60MB，其它=30MB；这里只是提前给出可读的报错，
    避免用户传了 55MB 的 zip 才发现服务端不认。
    """
    p = os.path.expanduser(str(file_path or "").strip().strip('"').strip("'"))
    if not os.path.isfile(p):
        raise ToolError(json.dumps({"error": "file_not_found",
                                    "message": f"本机找不到这个文件：{p}"}, ensure_ascii=False))
    size = os.path.getsize(p)
    limit = max_mb if p.lower().endswith(".zip") else 30
    if size > limit * 1024 * 1024:
        raise ToolError(json.dumps({"error": "file_too_large",
                                    "message": f"文件 {size / 1024 / 1024:.1f}MB 超过 {limit}MB 上限；"
                                               f"请删掉工程里的 PDF 成品与 build 目录后重新打包"},
                                   ensure_ascii=False))
    name = urllib.parse.quote(os.path.basename(p))
    async with httpx.AsyncClient(timeout=httpx.Timeout(300.0, connect=10.0)) as c:
        with open(p, "rb") as f:
            r = await c.post(OWL_BASE + "/v1/files", content=f.read(),
                             headers={**_headers(), "X-Filename": name,
                                      "Content-Type": "application/octet-stream"})
    try:
        data = r.json()
    except Exception:
        data = {"raw": r.text[:500]}
    _raise_if_error(r, data)
    return data


@mcp.tool()
async def owl_upload(file_path: str) -> str:
    """上传本机文件到服务端，返回 file_id（检测 / 图像 / 排版必用）。

    为什么需要：服务在云端，读不到你本机的 D:/… 路径。先上传拿 file_id，
    再把它放进 owl_quote 的 check 参数（同时给 hanzi 汉字数才能出价）。
    只传纯文本的可以用 content 直传，不必上传。

    Args:
        file_path: 本机文件的绝对路径（docx / doc / pdf / txt / png / jpg / tif / zip）。
            zip 只用于论文排版工程包，上限 60MB；其它格式上限 30MB。
    """
    data = await _upload_local(file_path)
    return _dump({**data, "next": "把这个 file_id 放进 owl_quote 的 params.file_id，"
                                  "同时给 hanzi（汉字数）才能出价；"
                                  "排版请直接用 owl_typeset（本工具只是它的前置步骤）"})


@mcp.tool()
async def owl_run(quote_id: str) -> str:
    """按 quote_id 执行任务（写作/查重/核验）。返回 run_id，用 owl_run_status 轮询。

    检索是同步的（用 owl_search），本工具只处理异步任务。
    """
    return _dump(await _call("POST", "/v1/runs", {"quote_id": quote_id}))


@mcp.tool()
async def owl_run_status(run_id: str) -> str:
    """查询任务状态与进度。status: queued/running/succeeded/failed/cancelled/pending_upstream。

    pending_upstream = 检测机构已收单、报告仍在生成（**不是失败**），稍后再查即可，别重建单。
    建议 3-5 秒轮询一次；succeeded 后 result 里是成品（写作正文截断在 2000 字，
    完整全文用 owl_run_content 取回后落盘；核验/检测报告用 owl_run_report）。
    """
    return _dump(await _call("GET", f"/v1/runs/{run_id}"))


@mcp.tool()
async def owl_run_report(run_id: str, part: str = "") -> str:
    """获取任务报告。核验（verify）给逐条判定摘要；检测（check）给结论 + 多份报告链接。

    part 仅对检测类有效，可选：main（默认，综合报告 HTML）、compare（比对报告 HTML）、
    simple（简洁版 PDF）、fulltext（原文对照 PDF）。
    返回的 report_url 自带 24 小时签名，浏览器可直接打开；要把报告写进文档/交付给用户时，
    按 part 取对应链接（例如需要 PDF 就用 simple 或 fulltext）。
    """
    data = await _call("GET", f"/v1/runs/{run_id}")
    status, action = data.get("status"), data.get("action")
    result = data.get("result") or {}
    # 签名 query 由 REST /v1/runs/{run_id} 读取时动态签发（见 app/main.py read_run）。
    # ⚠️ 必须取 data（整个返回体）而不是 result（其子字段）—— signed_query 在返回体顶层。
    _sq = data.get("signed_query") or ""
    base = f"{PUBLIC_BASE}/v1/runs/{run_id}/report" + (f"?{_sq}" if _sq else "")

    # 检测类：4 份报告 + 结论摘要（原来这里一律返回「尚无核验结果」，等于对检测单失明）
    if action == "check":
        rep = result.get("report") or {}
        files = rep.get("files") or []
        parts = {f.get("kind"): f.get("file") for f in files
                 if f.get("kind") and not str(f.get("kind")).startswith("other")}
        if not parts:
            parts = {"main": "", "compare": "", "simple": "", "fulltext": ""}
        pick = (part or "main").strip().lower()
        if pick not in parts:
            return _dump({"run_id": run_id, "status": status, "error": "unknown_part",
                          "available_parts": sorted(parts)})
        # 红队审查 4.1：_sq 为空时 base 不含 "?"，连接符必须回退成 "?"，
        # 否则拼出 `/report&part=compare` 这类畸形 URL（浏览器当路径 → 404 且难排查）。
        _sep = "&" if _sq else "?"
        url_of = lambda k: base if k == "main" else f"{base}{_sep}part={k}"
        return _dump({
            "run_id": run_id, "status": status, "action": "check",
            "headline": result.get("headline"),
            "result_mode": result.get("result_mode"),
            "repeat_rate": result.get("repeat_rate"),
            "grade": result.get("grade"),
            "error_count": result.get("error_count"),
            "word_count": result.get("word_count"),
            "num": result.get("num"),
            "report_status": rep.get("status") or "unknown",
            "report_url": url_of(pick),
            "available_parts": {k: url_of(k) for k in sorted(parts)},
            "report_tip": "检测类共 4 份：综合(HTML)/比对(HTML)/简洁(PDF)/原文对照(PDF)",
        })

    items = result.get("items") or []
    summary = result.get("summary") or {}
    if not items:
        return _dump({"run_id": run_id, "status": data.get("status"),
                      "note": "任务尚无核验结果（未完成或非 verify 任务）",
                      "report_url": base})
    s = summary
    head = (f"共 {s.get('total')} 条：已证实 {s.get('verified')}，元数据不符 "
            f"{s.get('metadata_mismatch')}，疑似匹配 {s.get('likely')}，存疑 "
            f"{s.get('suspect')}，未找到 {s.get('not_found')}，失败 {s.get('error')}")
    lines = [head]
    for i in items:
        diffs = "；".join(
            f"{d['field']}：引用「{d['cited']}」→ 实际「{d['actual']}」"
            for d in (i.get("diffs") or []))
        note = f"  ← {i['note']}" if i.get("note") else ""
        diff_txt = f"  ← 可修正：{diffs}" if diffs else ""
        lines.append(f"[{i['idx']}] {i['verdict']}  {str(i['title'])[:48]}{diff_txt}{note}")
    _sq2 = data.get("signed_query") or ""
    return _dump({"run_id": run_id, "summary": summary, "digest": lines,
                  "report_url": f"{PUBLIC_BASE}/v1/runs/{run_id}/report"
                                + (f"?{_sq2}" if _sq2 else ""),
                  "report_tip": "report_url 自带 24 小时签名，浏览器可直接打开（带判定徽标的完整 HTML）"})


@mcp.tool()
async def owl_run_content(run_id: str) -> str:
    """获取写作任务的完整正文与参考文献（配合本地产物资产库落盘）。

    返回：{content, references, chars, aigc}。落盘到用户本地论文文件夹
    （03-稿件/正文-draft<N>.md 与 references.md），元数据 aigc 块原样保留。
    其他动作返回 404。
    """
    return _dump(await _call("GET", f"/v1/runs/{run_id}/content"))


@mcp.tool()
async def owl_figure(mode: str, description: str, count: int = 1,
                     data: str = "", file_id: str = "",
                     figure_type: str = "") -> str:
    """生成论文用的科研配图，图片落盘后返回下载地址（25 积分/张，未交付不收费）。

    Args:
        mode: 三种方式，按内容选，不要乱猜——
            tikz  = 矢量示意图：模型/算法框架、流程图、技术路线、网络拓扑、序列切分、
                    时间轴、张量维度变化、函数曲线。返回 svg 与可直接粘贴的 tikz_code。
            chart = 数据图表：折线/散点/柱状/箱线/热力/子图，**必须有真实数据**。
            image = AI 科研配图：机制图、细胞示意、反应机理、催化循环、晶体结构、图形摘要。
        description: 图的内容说明（chart 模式写图表说明；tikz 可给 tikz_code 代替）。
        count: 张数 1–4，仅 image 模式可大于 1。tikz / chart 每次 1 张。
        data: chart 模式的内联 CSV（首行列名），如 "epoch,A,B\\n1,0.61,0.58"。
        file_id: chart 模式的已有数据文件 id（与 data 二选一，需先在网页端上传）。
        figure_type: 仅 image 模式：auto/roadmap/mechanism/experiment/comparison/
            graphical-abstract/overview/cover。

    计费：25 积分/张（¥0.25），按**实际交付张数**扣，生成失败或没出图不扣。
    调用前请先告诉用户「本次生成 N 张，消耗 N×25 积分」，得到同意再调。
    chart 模式没有真实数据时不要编数据——如实问用户要数据或改用 tikz。
    返回 figures[].download_url 自带 24 小时签名，可直接下载，存到 04-图/<序号>-<说明>.png。
    """
    params = {"mode": mode, "description": description, "count": count}
    if data:
        params["data"] = data
    if file_id:
        params["file_id"] = file_id
    if figure_type:
        params["figure_type"] = figure_type
    q = await _call("POST", "/v1/quote", {"action": "figure", "params": params})
    if not (isinstance(q, dict) and q.get("quote_id")):
        return _dump(q)
    r = await _call("POST", "/v1/runs", {"quote_id": q["quote_id"]})
    rid = (r or {}).get("run_id")
    if not rid:
        return _dump(r)
    final = {}
    for _ in range(60):                       # 最长约 180 秒，与 CLI（owl.py figure --timeout 180）一致
        await asyncio.sleep(3)
        g = await _call("GET", f"/v1/runs/{rid}")
        if isinstance(g, dict) and g.get("status") in ("succeeded", "failed", "cancelled"):
            final = g
            break
    if not final:
        return _dump({"run_id": rid, "status": "running",
                      "message": "仍未完成，用 owl_run_status 继续查；积分按实际交付张数结算"})
    res = final.get("result") or {}
    # 签名在 final（/v1/runs/{run_id} 返回体）顶层，不在 result 子字段里
    _sq3 = final.get("signed_query") or ""
    for f in res.get("figures") or []:
        f["download_url"] = PUBLIC_BASE + f["url"] + (f"?{_sq3}" if _sq3 else "")
        f["hint"] = "链接自带 24 小时签名，可直接下载（也可带 Authorization 头）；存 04-图/"
    return _dump({"run_id": rid, "status": final.get("status"),
                  "points_charged": final.get("points_settled"),
                  "figures": res.get("figures") or [],
                  "tikz_code": res.get("tikz_code") or "",
                  "warnings": res.get("warnings") or [],
                  "error": final.get("error_msg")})


@mcp.tool()
async def owl_typeset(file_path: str = "", mode: str = "latex", template_path: str = "",
                      entry: str = "", pages: int = 0, hanzi: int = 0, title: str = "",
                      file_id: str = "", template_file_id: str = "",
                      author: str = "", student_id: str = "", college: str = "",
                      major: str = "", advisor: str = "", date: str = "",
                      blind: bool = False, refs_std: str = "2015") -> str:
    """按学校模板排版一篇论文，一次调用拿回 PDF（Word 模式另附样式化 Word + 体检单）。

    **开工前必须先调 owl_meta 看 channels.typeset_ready。** 为 false 时不要调用本工具，
    只如实告诉用户「排版功能还在灰度中」，并把 channels.typeset_detail 转成人话说，
    不要报价、不要让用户先打包 —— 那是让人白忙一场。

    Args:
        mode:
            docx  = 用户手里是 Word 稿（绝大多数人的情况）。需要同时给模板。
            latex = 用户手里是 LaTeX 工程（Overleaf 下载的那种）。
        file_path: 本机文件路径。docx 模式给草稿 .docx；latex 模式给工程包 .zip
            （打包时把 .tex/.cls/.bib/图片/bib 一起放进去，不要带 build 目录与 PDF 成品）。
            **工程可以放在文件夹里**（如 论文/main.tex），服务端会自动找主文件。
        template_path: 学校模板 .docx（学校研究生院官网下载的那种），docx 模式必填。
        entry: 仅 latex 模式：主文件名，如 "main.tex"。工程里只有一个 .tex 时可省略。
        pages: 整本 PDF 的页数（latex 必给：填你本地编出来的 PDF 总页数，含封面/目录/附录；
               docx 给了也以网关从正文数出的为准）。
        hanzi: 全文汉字数（docx 可不给：本工具会直接从 .docx 正文里数）。
        title: 论文题目（会印在封面，不给则用文件里的）。
        author / student_id / college / major / advisor / date: 封面信息（仅 docx，可选）。
              不问也能出稿，但学位论文封面要这些字段，能问就顺口问一次。
        blind: 盲审版（仅 docx 模式，默认 false）。true 时封面作者/学号/导师脱敏为 ***、
              致谢整节隐藏。**用户说「盲审」「送盲审」「匿名评审」时必须开**；
              LaTeX 模式不适用（传了会被拒）。
        refs_std: 参考文献著录标准（仅 docx 模式）："2015"（默认）或 "2025"
              （GB/T 7714—2025，2026-07-01 起实施）。用户学校明确要求 2025 版、
              或稿子要投 2026 年之后的期刊/送审时选 2025；不确定就用默认 2015。
              LaTeX 模式不适用（工程自带样式，传了会被拒）。
        file_id / template_file_id: 已经用 owl_upload 传过的文件编号（与路径二选一）。

    计费：按篇一口价，按页数分档，**具体积分一律以 owl_quote 实时返回的 est_points 为准**
    （本工具不写死任何价格数字，你也不要凭印象报价）。
    报价即最终价，不会事后补扣：如果实排页数超出申报档位，网关会**拒单并让你重新报价，
    本次不扣费**——所以页数请如实填。
    72 小时内同一篇稿（标题相同、含同一模板）改格式重排只收 1 积分工本，改多少次都算同一篇。
    排版失败不收费。调用前请先把价格告诉用户并得到同意，不要默默扣费。

    返回：pdf_url / docx_url（7 天有效直链，可直接下载）、checklist（格式体检单：
    逐项「期望 vs 实测」，只有真测过的项才出现；状态「—」= 本稿测不了，不是不合格）、
    needs_confirm（模板里没看准的几项，拿去问用户，**不要**把 profile 全部字段甩给用户）、
    content_gaps（**内容没搬过去的部分，非空必须转告**）、doctor（系统替你改了什么）、
    skipped（工程里被忽略的非排版文件，如 CI 配置/构建脚本，必须转告，否则用户会怀疑文件被改）。
    """
    mode = (mode or "latex").strip().lower()
    if mode not in ("latex", "docx"):
        return _dump({"error": "bad_params", "message": "mode 只能是 latex 或 docx"})

    # 灰度守卫必须在上传之前：先传 60MB 工程包、再被 503 拒，等于让用户白等一场
    try:
        meta = await _call("GET", "/v1/meta")
        ch = (meta or {}).get("channels") or {}
        if ch.get("typeset_ready") is not True:
            return _dump({"error": "typeset_disabled",
                          "message": (ch.get("typeset_detail")
                                      or "排版功能还在灰度中，暂未对外开放"),
                          "tip": "如实告诉用户当前不可用即可；不要报价、不要让用户打包或上传。"})
        if mode == "docx" and ch.get("typeset_docx_ready") is False:
            return _dump({"error": "typeset_docx_disabled",
                          "message": "Word 按模板排版这条通路暂未开放，目前只支持 LaTeX 工程包"})
    except Exception:  # noqa: BLE001 — 网关读不到状态时不阻断，交给后面的真实调用暴露问题
        pass

    if not file_id:
        if not file_path:
            return _dump({"error": "bad_params",
                          "message": "请给 file_path（本机文件）或 file_id（已上传）"})
        file_id = (await _upload_local(file_path))["file_id"]
        if mode == "docx" and not hanzi:
            hanzi = _docx_hanzi(file_path)
    if mode == "docx" and not template_file_id:
        if not template_path:
            return _dump({"error": "bad_params",
                          "message": "Word 模式需要学校模板：请给 template_path，"
                                     "或先用 owl_upload 传模板拿 template_file_id"})
        template_file_id = (await _upload_local(template_path))["file_id"]

    # 先报价（免费）：把价格明确回给 Agent，由它转告用户
    qparams = {"mode": mode}
    if pages:
        qparams["pages"] = int(pages)
    if hanzi:
        qparams["hanzi"] = int(hanzi)
    try:
        quote = await _call("POST", "/v1/quote", {"action": "typeset", "params": qparams})
    except ToolError as exc:
        # 保留服务端原始错误码（不洗白成 quote_failed），只附加可操作的 tip
        try:
            payload = json.loads(str(exc))
        except Exception:  # noqa: BLE001
            payload = {"error": "quote_failed", "message": str(exc)[:300]}
        if isinstance(payload, dict):
            payload.setdefault("tip", "latex 模式必须带 pages（正文页数）；"
                                      "docx 模式请确认文件是 .docx 且没加密。")
            raise ToolError(json.dumps(payload, ensure_ascii=False))
        raise
    body = {"file_id": file_id, "mode": mode, "quote_id": (quote or {}).get("quote_id", "")}
    if pages:
        body["pages"] = int(pages)
    if hanzi:
        body["hanzi"] = int(hanzi)
    if template_file_id:
        body["template_file_id"] = template_file_id
    if entry:
        body["entry"] = entry
    if title:
        body["title"] = title
    # 封面字段（仅 docx）：学位论文封面是格式审查第一关，问一次比让用户事后补划算
    for k, v in (("author", author), ("student_id", student_id), ("college", college),
                 ("major", major), ("advisor", advisor), ("date", date)):
        if v:
            body[k] = v
    # 盲审版 / 参考文献标准（仅 docx）：口径校验在网关入口，这里只透传；
    # latex 模式传了会被 422 拒，所以按模式决定是否携带，不让 Agent 踩坑
    if mode == "docx":
        if blind:
            body["blind"] = True
        if refs_std and refs_std != "2015":
            body["refs_std"] = refs_std

    # 排版要真跑 LaTeX，实测 4–15 秒、大稿可到 1–2 分钟：超时必须放宽，不能沿用 120s
    # 只对传输层异常（超时/连不上）给人话；服务端业务错误（如余额不足/参数错）
    # 由 _call 抛 ToolError 原样透传，不得误报成「超时、未扣费」诱导重试
    try:
        r = await _call("POST", "/v1/typeset", body, timeout=httpx.Timeout(330.0, connect=10.0))
    except httpx.TimeoutException:
        return _dump({"error": "timeout",
                      "message": "这次排版没有在预期时间内完成，可能是一次性的引擎卡住（不代表你的稿有问题）。"
                                 "扣费状态未知：重试前先用 owl_wallet 查余额核对，避免重复扣费。",
                      "detail": "typeset 超过 330 秒未返回"})
    except httpx.HTTPError as exc:
        return _dump({"error": "network_error",
                      "message": "连不上服务端，请检查网络后重试；若持续出现请反馈。",
                      "detail": str(exc)[:200]})
    out = dict(r or {})
    for k, src in (("pdf_url", "pdf_path"), ("docx_url", "docx_path")):
        p = out.pop(src, None)
        out[k] = (PUBLIC_BASE + p) if p else None
    out["est_points"] = (quote or {}).get("est_points")
    out["points_charged"] = r.get("points_charged")
    out["checklist_tip"] = ("逐项「期望 vs 实测」讲给用户；⚠ 项说清是哪一项不一致、"
                            "要不要改。状态为「—」的是本稿测不了的项，不要念成不合格。"
                            "只讲返回里出现的项，没有的项不要编。")
    gaps = out.get("content_gaps") or []
    out["content_gaps_tip"] = ("这条非空就必须原样转告用户（公式/脚注/图/表列数没搬过去），"
                               "不要说成「已全部排好」。用户据此决定要不要先补稿。"
                               if gaps else None)
    if out.get("font_notice"):
        out["font_notice_tip"] = ("这条必须原样转告用户：PDF 与 Word 用的不是同一套字体。"
                                  "用 font_notice.text（长版）或 .short（短版）的原文讲，"
                                  "不要改写口径，也不要说「PDF 里就是宋体」。")
    if out.get("blind"):
        out["blind_tip"] = ("本次是盲审版：封面作者/学号/导师已脱敏为 ***、致谢整节已隐藏。"
                            "交付时必须说清这两点，并提醒用户：正式提交版要关掉 blind 重排一次"
                            "（72 小时内同一篇稿只收 1 积分工本）。")
    out["files_tip"] = ("pdf_url / docx_url 自带 7 天签名，可直接下载；"
                        "建议存到用户论文目录 07-交付/ 下，文件名用「题目-排版-v1.pdf」")
    return _dump(out)


@mcp.tool()
async def owl_wallet() -> str:
    """查询当前账号积分余额（balance_total / balance_avail，1 积分 = 0.01 元）。

    余额不足以执行下一步时，提示用户去充值，不要重试。
    """
    return _dump(await _call("GET", "/v1/me/wallet"))


@mcp.tool()
async def owl_ledger(limit: int = 50, offset: int = 0) -> str:
    """查询逐笔积分流水（充值/消耗/赠送/退款/过期），含每笔后的余额轨迹。

    用户质疑某笔扣费、要求对账时调用；按 created_at 倒序，limit 上限 500。
    """
    return _dump(await _call("GET", "/v1/me/ledger",
                             params={"limit": max(1, min(int(limit or 50), 500)),
                                     "offset": max(0, int(offset or 0))}))


@mcp.tool()
async def owl_recharge(amount_cny: int, channel: str = "wechat") -> str:
    """创建充值订单，返回支付二维码链接（15 分钟有效）。仅余额不足且用户同意充值时调用。

    amount_cny 仅支持 10 / 30 / 50 / 100 / 500；channel 为 wechat（默认）或 alipay。
    返回的 qr_url 交给用户在浏览器打开即可扫码支付；支付到账约 1 分钟内自动入账，
    之后可用 owl_wallet 确认余额。用户未明确同意前不要调用本工具。
    """
    if amount_cny not in (10, 30, 50, 100, 500):
        return _dump({"error": "bad_amount", "message": "充值档位仅支持 10/30/50/100/500 元"})
    r = await _call("POST", "/v1/pay/recharge",
                    {"points": amount_cny * 100, "channel": channel})
    if isinstance(r, dict) and r.get("qr_path"):
        # qr_path 自带 15 分钟签名（recharge.qr_signed_path），这里只需正确的前缀
        r["qr_url"] = PUBLIC_BASE + r.pop("qr_path")
        r["notice"] = ("请把 qr_url 发给用户在浏览器打开并扫码支付；到账约 1 分钟，"
                       "支付后可用 owl_recharge_status 或 owl_wallet 确认。"
                       "不要重复调用本工具——重复创建会产生多笔未支付订单。")
    return _dump(r)


@mcp.tool()
async def owl_recharge_status(order_no: str) -> str:
    """查询充值订单状态（created/paid/credited/failed/closed）。用户说"我付好了"后调用核实；
    可向渠道主动收敛一次（15s 节流）。credited 即已入账，可用 owl_wallet 查余额。"""
    return _dump(await _call("GET", f"/v1/pay/recharge/{order_no}", params={"refresh": "1"}))


@mcp.tool()
async def owl_fulltext(identifier: str) -> str:
    """取中文期刊全文 PDF 直链（约 1 小时内有效，请立即下载）。

    Args:
        identifier: 检索结果里的 Identifier 字段（纯中文库文献；全球库无全文下载）。

    计费以实时报价为准（owl_products 可查）；72 小时内同一 identifier 重取只收 1 积分；单账号每日上限 100 篇。
    拿到 url 后用 HTTP GET 直接下载（返回 PDF 字节流），建议存到项目目录 02-文献/fulltexts/，
    文件名用「一作-年份-题名前20字.pdf」。404 fulltext_unavailable 表示该文献没有授权全文，
    如实告诉用户，不要换参数重试。
    """
    return _dump(await _call("POST", "/v1/fulltext", {"identifier": identifier}))


@mcp.tool()
async def owl_article(identifier: str, lang: str = "zh") -> str:
    """查单篇文献的完整详情（题名/作者/期刊/年份/DOI/卷期页码）。

    Args:
        identifier: 检索结果里的 Identifier 字段。
        lang: zh=中文库（默认）/ en=全球库。

    计费以实时报价为准（owl_products 可查）；72 小时内查过同一篇按缓存价 1 积分。用于：用户要某篇的 DOI、
    要核对某篇的年卷期页码、或检索结果摘要不够需要完整元数据时。
    404 article_not_found 表示库里没有该文献详情，如实告诉用户。
    """
    return _dump(await _call("GET", "/v1/article",
                             params={"identifier": identifier, "lang": lang}))

@mcp.tool()
async def owl_oa(doi: str = "", title: str = "") -> str:
    """取外文（开放获取）文献的免费全文 PDF 直链。**0 积分，完全免费**。

    Args:
        doi: 文献 DOI（优先，命中率最高）。可用 owl_search 结果的 doi 或 owl_article 取。
        title: 英文题名（没有 DOI 时用；匹配精度低于 DOI）。

    返回 oa_status：gold / hybrid / green / bronze / oa = 有免费版本；closed = 付费墙内；
    unknown = 没探测到（可能缺 DOI）。
      - 有 pdf_url → 直接 HTTP GET 下载，存 02-文献/fulltexts/
      - 只有 landing_page → 把链接给用户，页面里点下载（也算免费）
      - closed → 如实说「这篇在付费墙内，没有合法免费全文」，不要暗示能弄到
    中文文献不要用本工具，用 owl_fulltext（授权全文，价格以实时报价为准）。
    """
    body = {}
    if doi and doi.strip():
        body["doi"] = doi.strip()
    if title and title.strip():
        body["title"] = title.strip()
    if not body:
        return _dump({"error": "bad_params", "message": "doi 或 title 至少给一个"})
    return _dump(await _call("POST", "/v1/oa", body))


@mcp.tool()
async def owl_citations(doi: str, direction: str = "refs", limit: int = 20) -> str:
    """引文追溯：从一篇文献滚雪球找文献（比反复换关键词精准）。

    Args:
        doi: 起点文献的 DOI（先用 owl_search 或 owl_article 拿到）。
        direction: refs=它引用了谁（找源头/经典）；cited=谁引用了它（找后续进展/最新研究）。
        limit: 返回条数，1-50，默认 20。

    计费以实时报价为准（owl_products 可查）；72 小时内同篇同方向缓存 1 积分。
    返回 items 里带 cited_by（被引次数，判断影响力）与 is_oa（可直接免费用 owl_oa 取全文）。
    """
    return _dump(await _call("GET", "/v1/citations",
                             params={"doi": doi, "direction": direction, "limit": limit}))


@mcp.tool()
async def owl_campaign(code: str = "") -> str:
    """查活动 / 兑换活动券码（免费）。

    - 不传 code：返回我的可参与活动、我的邀请码与邀请战绩（用户问「有没有优惠 / 怎么便宜点」
      或余额不足时再调，**不要主动推销**）。
    - 传 code：兑换券码，到账积分有效期 90 天（先到期先扣）。

    邀请规则：好友用你的邀请码注册后，**好友首次付费成功**时双方各得奖励；
    好友只注册不付费不发。奖励自动到账，不需要用户做任何操作。
    """
    if code and code.strip():
        return _dump(await _call("POST", "/v1/campaign/redeem", {"code": code.strip()}))
    return _dump(await _call("GET", "/v1/campaigns"))


@mcp.tool()
async def owl_claim_favorite(image_path: str) -> str:
    """提交 SkillHub 收藏截图，领取「收藏赠积分」活动的积分（免费，每人限 1 次）。

    什么时候用：用户自己提起「我收藏了 / 截图给你 / 收藏活动怎么领」，或 owl_campaign
    返回 favorite.campaign_active=true 且 participated=false 时。**不要主动推销活动**。

    截图三要求（缺一即不通过，先跟用户讲清再提交）：
      ① 能看到技能 id（形如 @user_xxx/owlwrite-paper，网址栏或页面信息都行）；
      ② 必须是已收藏状态（亮星 + 按钮显示「取消收藏」）；
      ③ 不要用官方样例图（带水印会被拒）。

    拒单不占参与次数，按提示换新截图重交即可；每人限 1 次；到账积分 90 天有效。

    Args:
        image_path: 截图在本机的绝对路径（png / jpg / webp，≤5MB）。
    """
    import base64
    p = os.path.expanduser((image_path or "").strip().strip('"').strip("'"))
    if not p or not os.path.isfile(p):
        raise ToolError(json.dumps({"error": "file_not_found",
                                    "message": f"截图文件不存在：{p or '(空路径)'}"},
                                   ensure_ascii=False))
    with open(p, "rb") as f:
        raw = f.read()
    if len(raw) > 5 * 1024 * 1024:
        raise ToolError(json.dumps({"error": "image_too_large",
                                    "message": "截图超过 5MB，请压缩后重试"},
                                   ensure_ascii=False))
    if len(raw) < 1024:
        raise ToolError(json.dumps({"error": "bad_image",
                                    "message": "截图太小（不足 1KB），请上传完整页面截图"},
                                   ensure_ascii=False))
    data = await _call("POST", "/v1/campaign/favorite-claim",
                       {"image_base64": base64.b64encode(raw).decode()}, timeout=180)
    return _dump({**data, "next": "把 points 与「90 天有效」如实告诉用户；若 ok 为 false，"
                                  "按 error 说明让用户换新截图重交（不占参与次数）"})


if __name__ == "__main__":
    mcp.run(transport="stdio")
