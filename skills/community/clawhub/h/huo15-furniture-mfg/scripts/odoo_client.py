#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
odoo_client.py — 家具制造智能体（huo15-furniture-mfg）统一 Odoo 访问客户端

零第三方依赖（仅 Python 标准库）。同时支持两种 API 通道：
  - XML-RPC （默认，最稳定）  /xmlrpc/2/common + /xmlrpc/2/object
  - JSON-RPC（urllib 实现）   /jsonrpc

职责：
  1. 凭据管理：从个人 tools.md 读取 / 写入连接配置（权限 0600）。
     配置块标记独立于 huo15-huihuo-odoo 技能，两者可共存于同一 tools.md。
  2. 认证：支持「登录密码」与「API Key」两种 secret。
  3. 通用 ORM 调用：search_read / search_count / read / read_group /
     formatted_read_group / fields_get / name_search 等（P0 只读，无 create/write）。

被 order.py / mfg.py / quality.py 等业务脚本复用，也可独立测试连接：
    python3 odoo_client.py test
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.request
import xmlrpc.client
from pathlib import Path

# 默认凭据文件（与 huihuo-odoo 共用 ~/.huo15/tools.md，但各自维护独立标记块）
DEFAULT_TOOLS_MD = os.environ.get(
    "FMFG_TOOLS_MD", str(Path.home() / ".huo15" / "tools.md")
)

# tools.md 中本技能维护的配置块标记（勿与其他技能混用）
BLOCK_START = "<!-- huo15-furniture-mfg:start -->"
BLOCK_END = "<!-- huo15-furniture-mfg:end -->"

# 默认连接：和栖家居测试环境（P0 阶段只允许 test 库，见 CLAUDE.md）
DEFAULTS = {
    "url": "https://test.heysleep.cn",
    "db": "test",
    "login": "",
    "auth_type": "password",  # password | apikey
    "secret": "",
    "transport": "xmlrpc",    # xmlrpc | jsonrpc
}


class OdooError(RuntimeError):
    """对外暴露的友好错误（已翻译 Fault / 网络异常）。"""


# --------------------------------------------------------------------------- #
# 凭据：tools.md 读 / 写
# --------------------------------------------------------------------------- #
def _config_block_template(cfg: dict) -> str:
    return (
        f"{BLOCK_START}\n"
        "## 🛏️ 和栖家居制造系统（huo15-furniture-mfg 技能自动维护，勿改标记行）\n\n"
        "```yaml\n"
        "# huo15-furniture-mfg-config\n"
        f"url: {cfg.get('url', '')}\n"
        f"db: {cfg.get('db', '')}\n"
        f"login: {cfg.get('login', '')}\n"
        f"auth_type: {cfg.get('auth_type', 'password')}   # password | apikey\n"
        f"transport: {cfg.get('transport', 'xmlrpc')}      # xmlrpc | jsonrpc\n"
        f"secret: {json.dumps(cfg.get('secret', ''), ensure_ascii=False)}\n"
        f"uid: {cfg.get('uid', '') if cfg.get('uid') else ''}\n"
        "```\n"
        f"{BLOCK_END}"
    )


def _parse_block(text: str) -> dict:
    m = re.search(
        re.escape(BLOCK_START) + r"(.*?)" + re.escape(BLOCK_END), text, re.S
    )
    if not m:
        return {}
    cfg: dict = {}
    for raw in m.group(1).splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith("```"):
            continue
        if line.startswith("##") or line.startswith("<!--"):
            continue
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.strip()
        if val.startswith('"') or val.startswith("'"):
            try:
                val = json.loads(val) if val.startswith('"') else val.strip("'")
            except Exception:
                val = val.strip("'\"")
        else:
            val = val.split("#", 1)[0].strip()
        if key in ("url", "db", "login", "auth_type", "secret", "transport", "uid"):
            cfg[key] = val
    if cfg.get("uid"):
        try:
            cfg["uid"] = int(cfg["uid"])
        except (TypeError, ValueError):
            cfg.pop("uid", None)
    return cfg


def load_config(tools_md: str | None = None) -> dict:
    """读取配置：tools.md 标记块，再被环境变量覆盖，最后回退 DEFAULTS。"""
    cfg = dict(DEFAULTS)
    path = Path(tools_md or DEFAULT_TOOLS_MD)
    if path.exists():
        cfg.update(_parse_block(path.read_text(encoding="utf-8")))
    env_map = {
        "FMFG_ODOO_URL": "url",
        "FMFG_ODOO_DB": "db",
        "FMFG_ODOO_LOGIN": "login",
        "FMFG_ODOO_AUTH_TYPE": "auth_type",
        "FMFG_ODOO_SECRET": "secret",
        "FMFG_ODOO_TRANSPORT": "transport",
    }
    for env, key in env_map.items():
        if os.environ.get(env):
            cfg[key] = os.environ[env]
    return cfg


def save_config(cfg: dict, tools_md: str | None = None) -> str:
    """把配置写入 tools.md 的本技能标记块（其余内容原样保留），权限 0600。"""
    path = Path(tools_md or DEFAULT_TOOLS_MD)
    path.parent.mkdir(parents=True, exist_ok=True)
    cfg = dict(cfg)
    cfg["url"] = normalize_url(cfg.get("url"))
    block = _config_block_template(cfg)
    if path.exists():
        text = path.read_text(encoding="utf-8")
        if BLOCK_START in text and BLOCK_END in text:
            text = re.sub(
                re.escape(BLOCK_START) + r".*?" + re.escape(BLOCK_END),
                block,
                text,
                flags=re.S,
            )
        else:
            text = text.rstrip() + "\n\n" + block + "\n"
    else:
        text = (
            "# 个人工具凭据登记（tools.md）\n\n"
            "> 本文件由火一五技能维护，含敏感凭据，已设权限 600。请勿提交到 git。\n\n"
            + block
            + "\n"
        )
    path.write_text(text, encoding="utf-8")
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass
    return str(path)


def mask(secret: str) -> str:
    """脱敏显示 secret（日志/终端用，永不打印明文）。"""
    if not secret:
        return "(空)"
    if len(secret) <= 4:
        return "*" * len(secret)
    return secret[:2] + "*" * (len(secret) - 4) + secret[-2:]


def normalize_url(url: str) -> str:
    """规范化系统地址：可只输 test.heysleep.cn，自动补 https:// 并去尾斜杠。"""
    url = (url or "").strip().rstrip("/")
    if url and not url.startswith(("http://", "https://")):
        url = "https://" + url
    return url


# --------------------------------------------------------------------------- #
# 客户端
# --------------------------------------------------------------------------- #
class Odoo:
    """Odoo ORM 调用封装，XML-RPC / JSON-RPC 双通道。"""

    def __init__(self, cfg: dict | None = None, tools_md: str | None = None):
        self.cfg = cfg or load_config(tools_md)
        self.url = normalize_url(self.cfg.get("url"))
        self.db = self.cfg.get("db") or ""
        self.login = self.cfg.get("login") or ""
        self.secret = self.cfg.get("secret") or ""
        self.transport = (self.cfg.get("transport") or "xmlrpc").lower()
        self.uid: int | None = self.cfg.get("uid") or None
        self._object = None

    # -- 认证 -------------------------------------------------------------- #
    def authenticate(self) -> int:
        if not (self.url and self.db and self.login and self.secret):
            raise OdooError(
                "尚未初始化凭据。请先运行：python3 scripts/login.py init"
                "（依次输入 系统地址 / 数据库 / 账号 / 密码）。"
            )
        try:
            if self.transport == "jsonrpc":
                self.uid = self._jsonrpc(
                    "common", "authenticate", [self.db, self.login, self.secret, {}]
                )
            else:
                common = xmlrpc.client.ServerProxy(f"{self.url}/xmlrpc/2/common")
                self.uid = common.authenticate(self.db, self.login, self.secret, {})
        except xmlrpc.client.Fault as e:
            raise OdooError(f"认证失败（XML-RPC Fault）：{e.faultString}") from e
        except Exception as e:
            raise OdooError(f"无法连接 {self.url}：{e}") from e
        if not self.uid:
            raise OdooError("认证被拒绝：账号或密码/API Key 错误，或数据库名 db 不对。")
        return self.uid

    def ensure_uid(self) -> int:
        return self.uid if self.uid else self.authenticate()

    # -- 底层调用 ---------------------------------------------------------- #
    def _jsonrpc(self, service: str, method: str, args: list):
        payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {"service": service, "method": method, "args": args},
            "id": 1,
        }
        req = urllib.request.Request(
            f"{self.url}/jsonrpc",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        if data.get("error"):
            err = data["error"]
            msg = err.get("data", {}).get("message") or err.get("message") or str(err)
            raise OdooError(f"JSON-RPC 错误：{msg}")
        return data.get("result")

    def execute_kw(self, model: str, method: str, args: list, kwargs: dict | None = None):
        uid = self.ensure_uid()
        kwargs = kwargs or {}
        try:
            if self.transport == "jsonrpc":
                return self._jsonrpc(
                    "object",
                    "execute_kw",
                    [self.db, uid, self.secret, model, method, args, kwargs],
                )
            if self._object is None:
                self._object = xmlrpc.client.ServerProxy(f"{self.url}/xmlrpc/2/object")
            return self._object.execute_kw(
                self.db, uid, self.secret, model, method, args, kwargs
            )
        except xmlrpc.client.Fault as e:
            raise OdooError(
                f"调用 {model}.{method} 失败：{e.faultString.strip().splitlines()[-1]}"
            ) from e
        except OdooError:
            raise
        except Exception as e:
            raise OdooError(f"调用 {model}.{method} 网络异常：{e}") from e

    # -- 常用便捷方法 ------------------------------------------------------ #
    def search_read(self, model, domain, fields=None, **kw):
        kwargs = {"fields": fields or []}
        kwargs.update(kw)
        return self.execute_kw(model, "search_read", [domain], kwargs)

    def search(self, model, domain, **kw):
        return self.execute_kw(model, "search", [domain], kw)

    def search_count(self, model, domain):
        return self.execute_kw(model, "search_count", [domain])

    def read(self, model, ids, fields=None):
        return self.execute_kw(model, "read", [ids], {"fields": fields or []})

    def name_search(self, model, name, domain=None, limit=10):
        # Odoo 19 把 name_search 的 args 参数改名为 domain，传 args 会 TypeError
        return self.execute_kw(
            model, "name_search", [],
            {"name": name, "domain": domain or [], "limit": limit},
        )

    def fields_get(self, model, attributes=("string", "type")):
        return self.execute_kw(
            model, "fields_get", [], {"attributes": list(attributes)}
        )

    # -- 写方法（P1 起提供；只允许 actions.py 经确认制调用，查询脚本禁用） --- #
    def create(self, model, vals: dict) -> int:
        return self.execute_kw(model, "create", [vals])

    def write(self, model, ids, vals: dict) -> bool:
        ids = ids if isinstance(ids, list) else [ids]
        return self.execute_kw(model, "write", [ids, vals])

    def unlink(self, model, ids) -> bool:
        ids = ids if isinstance(ids, list) else [ids]
        return self.execute_kw(model, "unlink", [ids])

    def call(self, model, method, ids, **kwargs):
        """记录级方法调用（message_post 等）。"""
        return self.execute_kw(model, method, [ids], kwargs)

    def read_group(self, model, domain, fields, groupby, lazy=False, **kw):
        """分组聚合（多 groupby 默认 lazy=False，避免只展开第一维的坑）。"""
        kw["lazy"] = lazy
        return self.execute_kw(model, "read_group", [domain, fields, groupby], kw)

    def formatted_read_group(self, model, domain, groupby, aggregates, **kw):
        """Odoo 19 推荐的分组聚合。旧版本无此方法时自动回退 read_group。"""
        kwargs = {"groupby": groupby, "aggregates": aggregates}
        kwargs.update(kw)
        try:
            return self.execute_kw(model, "formatted_read_group", [domain], kwargs)
        except OdooError:
            fields = [a for a in aggregates if a != "__count"]
            return self.read_group(model, domain, fields, groupby, lazy=False)


# --------------------------------------------------------------------------- #
# CLI：测试连接
# --------------------------------------------------------------------------- #
def _cmd_test(tools_md: str | None = None):
    cfg = load_config(tools_md)
    print(f"URL       : {cfg.get('url')}")
    print(f"DB        : {cfg.get('db')}")
    print(f"Login     : {cfg.get('login') or '(未配置)'}")
    print(f"Auth      : {cfg.get('auth_type')}  Transport: {cfg.get('transport')}")
    print(f"Secret    : {mask(cfg.get('secret'))}")
    odoo = Odoo(cfg)
    uid = odoo.authenticate()
    print(f"\n✅ 认证成功，uid = {uid}")
    user = odoo.read("res.users", [uid], ["name", "login", "lang"])
    if user:
        print(f"   当前用户：{user[0]['name']} <{user[0]['login']}>  lang={user[0].get('lang')}")


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    cmd = argv[0] if argv else "test"
    try:
        if cmd == "test":
            _cmd_test()
        else:
            print(__doc__)
    except OdooError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
