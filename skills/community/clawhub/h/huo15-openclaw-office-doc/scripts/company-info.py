#!/usr/bin/env python3
"""
company-info.py - 本地公司信息读写工具

职责：
1. 读取 ~/.huo15/company-info.json 作为主缓存
2. 若缺失关键字段（company_name / logo_path），可选回落 Odoo（第三优先级）
3. 提供 CLI：--get / --set / --check
   - --check：对 SKILL 工作流友好，返回 JSON + 退出码（0 完整 / 2 缺失）

关键字段：
  company_name  公司全称（必填）
  logo_path     LOGO 图片绝对路径（必填）
  slogan        口号 / 页眉副标题（可选）
  address       注册 / 办公地址（可选）
  phone         联系电话（可选）
  email         联系邮箱（可选）
  website       官网（可选）
"""

import os
import sys
import json
import ssl
import argparse
import urllib.request

HOME = os.path.expanduser("~")
HUO15_DIR = os.path.join(HOME, ".huo15")
ASSETS_DIR = os.path.join(HUO15_DIR, "assets")
CONFIG_PATH = os.path.join(HUO15_DIR, "company-info.json")
DEFAULT_LOGO_PATH = os.path.join(ASSETS_DIR, "logo.png")

REQUIRED_FIELDS = ("company_name", "logo_path")
OPTIONAL_FIELDS = ("slogan", "address", "phone", "email", "website")
ALL_FIELDS = REQUIRED_FIELDS + OPTIONAL_FIELDS


def load_config():
    if not os.path.exists(CONFIG_PATH):
        return {}
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def save_config(data):
    os.makedirs(HUO15_DIR, exist_ok=True)
    clean = {k: v for k, v in data.items() if k in ALL_FIELDS and v}
    with open(CONFIG_PATH, "w", encoding="utf-8") as fh:
        json.dump(clean, fh, ensure_ascii=False, indent=2)
    os.chmod(CONFIG_PATH, 0o600)
    return clean


def logo_is_valid(path):
    return bool(path) and os.path.exists(path) and os.path.getsize(path) > 1000


def try_odoo_fallback(info):
    """第三优先级：尝试从 Odoo 拉取公司名与 LOGO。

    仅当本地 JSON 仍然缺字段时才会跑。任何异常都静默失败。
    """
    import xmlrpc.client

    creds_file = os.path.join(
        HOME, ".openclaw", "agents",
        os.environ.get("OC_AGENT_ID", "main"),
        "odoo_creds.json",
    )
    cfg_file = os.path.join(HOME, ".openclaw", "openclaw.json")
    if not (os.path.exists(creds_file) and os.path.exists(cfg_file)):
        return info

    try:
        with open(creds_file, encoding="utf-8") as fh:
            creds = json.load(fh)
        with open(cfg_file, encoding="utf-8") as fh:
            cfg = json.load(fh)

        odoo_env = cfg.get("skills", {}).get("entries", {}).get("huo15-odoo", {}).get("env", {})
        url = odoo_env.get("ODOO_URL", "https://huihuoyun.huo15.com")
        db = odoo_env.get("ODOO_DB", "huo15_prod")
        user = creds.get("user", "")
        password = creds.get("password", "")
        if not (user and password):
            return info

        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common", context=ctx)
        uid = common.authenticate(db, user, password, {})
        if not uid:
            return info

        models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object", context=ctx)
        data = models.execute_kw(
            db, uid, password, "res.company", "search_read",
            [[("id", "=", 1)]], {"fields": ["name", "logo"], "limit": 1},
        )
        if not data:
            return info

        if not info.get("company_name"):
            info["company_name"] = data[0].get("name") or info.get("company_name")

        logo_id = data[0].get("logo")
        if logo_id and not logo_is_valid(info.get("logo_path")):
            os.makedirs(ASSETS_DIR, exist_ok=True)
            try:
                urllib.request.urlretrieve(
                    f"{url}/web/image/res.company/{logo_id}/logo",
                    DEFAULT_LOGO_PATH,
                )
                if logo_is_valid(DEFAULT_LOGO_PATH):
                    info["logo_path"] = DEFAULT_LOGO_PATH
            except Exception:
                pass
    except Exception:
        pass

    return info


def resolve(use_odoo=True):
    """按优先级返回公司信息字典（未必完整）。"""
    info = load_config()

    if not logo_is_valid(info.get("logo_path")) and logo_is_valid(DEFAULT_LOGO_PATH):
        info["logo_path"] = DEFAULT_LOGO_PATH

    missing = [k for k in REQUIRED_FIELDS if not info.get(k)]
    if missing and use_odoo:
        info = try_odoo_fallback(info)
        if info.get("company_name") or info.get("logo_path"):
            save_config(info)
    return info


def check(use_odoo=True):
    """返回 (info, missing_fields)。"""
    info = resolve(use_odoo=use_odoo)
    missing = [k for k in REQUIRED_FIELDS if not info.get(k)]
    if "logo_path" in info and not logo_is_valid(info.get("logo_path")):
        if "logo_path" not in missing:
            missing.append("logo_path")
    return info, missing


def cmd_get(args):
    info, missing = check(use_odoo=not args.no_odoo)
    print(json.dumps({"info": info, "missing": missing, "path": CONFIG_PATH},
                     ensure_ascii=False, indent=2))
    return 0 if not missing else 2


def cmd_set(args):
    info = load_config()
    for field in ALL_FIELDS:
        value = getattr(args, field.replace("-", "_"), None)
        if value is not None:
            info[field] = value
    if args.clear:
        for field in args.clear:
            info.pop(field, None)
    saved = save_config(info)
    print(json.dumps({"info": saved, "path": CONFIG_PATH},
                     ensure_ascii=False, indent=2))
    return 0


def cmd_check(args):
    info, missing = check(use_odoo=not args.no_odoo)
    result = {
        "info": info,
        "missing": missing,
        "complete": not missing,
        "path": CONFIG_PATH,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not missing else 2


def build_parser():
    parser = argparse.ArgumentParser(description="huo15 公司信息读写工具")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_get = sub.add_parser("get", help="读取当前公司信息")
    p_get.add_argument("--no-odoo", action="store_true", help="跳过 Odoo 回落")
    p_get.set_defaults(func=cmd_get)

    p_set = sub.add_parser("set", help="设置 / 更新字段")
    for field in ALL_FIELDS:
        p_set.add_argument(f"--{field.replace('_', '-')}", default=None)
    p_set.add_argument("--clear", nargs="*", default=[], help="要清空的字段列表")
    p_set.set_defaults(func=cmd_set)

    p_check = sub.add_parser("check", help="检查必填字段，缺失时 exit 2")
    p_check.add_argument("--no-odoo", action="store_true")
    p_check.set_defaults(func=cmd_check)

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
