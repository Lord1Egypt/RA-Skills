#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
login.py — 配置并验证家具制造系统登录凭据，保存到个人 tools.md

用法
  交互式（用户自己跑，密码不回显）：
      python3 login.py

  非交互（推荐 AI 用：secret 走 stdin，避免出现在命令行历史 / ps）：
      printf '%s' "$ODOO_PASSWORD" | python3 login.py set \
          --login <账号> --secret-stdin
      # 省略的 url/db 默认 https://test.heysleep.cn / test

  其它：
      python3 login.py show     # 显示当前配置（secret 脱敏）
      python3 login.py test     # 用已保存配置测试连接

安全
  - 凭据写入 ~/.huo15/tools.md（可用 FMFG_TOOLS_MD 改路径），文件权限 600。
  - 配置块与 huo15-huihuo-odoo 技能各自独立标记，互不覆盖。
  - 建议用 Odoo「API Key」而非登录密码（偏好设置 → 账户安全 → 新建 API 密钥），
    --auth-type apikey。API Key 可随时吊销，泄漏风险远低于主密码。
"""

from __future__ import annotations

import argparse
import getpass
import sys

from odoo_client import DEFAULTS, Odoo, OdooError, load_config, mask, save_config


def _read_secret(args) -> str:
    """按优先级取 secret：--secret-stdin > --secret > 交互输入。"""
    if getattr(args, "secret_stdin", False):
        data = sys.stdin.read().strip()
        if not data:
            raise OdooError("--secret-stdin 指定了，但 stdin 没有读到内容。")
        return data
    if getattr(args, "secret", None):
        sys.stderr.write(
            "⚠️  通过 --secret 明文传参会留在 shell 历史/进程列表，建议改用 --secret-stdin。\n"
        )
        return args.secret
    label = "API Key" if getattr(args, "auth_type", "password") == "apikey" else "密码"
    return getpass.getpass(f"请输入 {label}（输入时不显示）：")


def _verify_and_save(cfg: dict) -> int:
    """验证连接成功后才落盘，避免存错凭据。"""
    odoo = Odoo(cfg)
    uid = odoo.authenticate()
    cfg["uid"] = uid
    path = save_config(cfg)
    user = odoo.read("res.users", [uid], ["name", "login"])
    who = f"{user[0]['name']} <{user[0]['login']}>" if user else f"uid={uid}"
    print(f"✅ 登录成功：{who}")
    print(f"   凭据已保存到 {path}（权限 600，请勿提交 git）")
    return uid


def cmd_interactive():
    cfg = load_config()
    print("初始化家具制造系统连接 —— 依次输入 4 项（方括号内为默认值，直接回车采用）\n")
    url = input(f"① 系统地址（如 test.heysleep.cn）[{cfg.get('url') or DEFAULTS['url']}]: ").strip() \
        or cfg.get("url") or DEFAULTS["url"]
    db = input(f"② 数据库（如 test）[{cfg.get('db') or DEFAULTS['db']}]: ").strip() \
        or cfg.get("db") or DEFAULTS["db"]
    login = input(f"③ 账号（邮箱或用户名）[{cfg.get('login') or ''}]: ").strip() \
        or cfg.get("login", "")
    secret = getpass.getpass("④ 密码（或 API Key，输入时不显示）: ")
    if not login or not secret:
        raise OdooError("账号和密码不能为空。")
    cfg.update(url=url, db=db, login=login,
               auth_type=cfg.get("auth_type", "password"),
               transport=cfg.get("transport", "xmlrpc"), secret=secret)
    _verify_and_save(cfg)


def cmd_set(args):
    cfg = load_config()
    cfg["url"] = args.url or cfg.get("url") or DEFAULTS["url"]
    cfg["db"] = args.db or cfg.get("db") or DEFAULTS["db"]
    cfg["auth_type"] = args.auth_type
    cfg["transport"] = args.transport
    if args.login:
        cfg["login"] = args.login
    if not cfg.get("login"):
        raise OdooError("缺少账号：用 --login 指定。")
    cfg["secret"] = _read_secret(args)
    _verify_and_save(cfg)


def cmd_show():
    cfg = load_config()
    print(f"URL       : {cfg.get('url')}")
    print(f"DB        : {cfg.get('db')}")
    print(f"Login     : {cfg.get('login') or '(未配置)'}")
    print(f"Auth type : {cfg.get('auth_type')}")
    print(f"Transport : {cfg.get('transport')}")
    print(f"Secret    : {mask(cfg.get('secret'))}")
    print(f"uid(cache): {cfg.get('uid') or '(未缓存)'}")


def cmd_test():
    odoo = Odoo()
    uid = odoo.authenticate()
    user = odoo.read("res.users", [uid], ["name", "login"])
    who = f"{user[0]['name']} <{user[0]['login']}>" if user else f"uid={uid}"
    print(f"✅ 连接正常：{who}（uid={uid}）")


def build_parser():
    p = argparse.ArgumentParser(description="配置/验证家具制造系统登录凭据")
    sub = p.add_subparsers(dest="cmd")

    s = sub.add_parser("set", help="非交互配置（secret 走 stdin 最安全）")
    s.add_argument("--url")
    s.add_argument("--db")
    s.add_argument("--login")
    s.add_argument("--auth-type", dest="auth_type", default="password",
                   choices=["password", "apikey"])
    s.add_argument("--transport", default="xmlrpc",
                   choices=["xmlrpc", "jsonrpc"])
    s.add_argument("--secret", help="明文 secret（不推荐，会进 shell 历史）")
    s.add_argument("--secret-stdin", dest="secret_stdin", action="store_true",
                   help="从标准输入读 secret（推荐）")

    sub.add_parser("init", help="交互式初始化：依次提示输入 地址/数据库/账号/密码")
    sub.add_parser("show", help="显示当前配置（secret 脱敏）")
    sub.add_parser("test", help="测试已保存的连接")
    return p


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    args = build_parser().parse_args(argv)
    try:
        if args.cmd == "set":
            cmd_set(args)
        elif args.cmd == "show":
            cmd_show()
        elif args.cmd == "test":
            cmd_test()
        else:
            cmd_interactive()
    except OdooError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n已取消。", file=sys.stderr)
        sys.exit(130)


if __name__ == "__main__":
    main()
