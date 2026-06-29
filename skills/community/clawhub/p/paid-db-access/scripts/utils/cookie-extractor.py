#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cookie 提取器：从浏览器 Cookie 列表中自动提取所需项

使用方式：
  方法1：从浏览器 F12 手动复制
    1. F12 → Application → Cookies → 目标网站
    2. 全选表格 → 复制 → 粘贴到文本文件
    3. 运行：python cookie-extractor.py --input cookies.txt --db ieee

  方法2：交互式输入
    直接运行：python cookie-extractor.py --interactive

输出：精简的 Cookie 字符串，只包含 config.yaml 中 required + optional 项
"""

import argparse
import json
import sys
from pathlib import Path

# 从 config.yaml 中定义的数据库 Cookie 需求
DB_CONFIG = {
    "ieee": {
        "required": ["WLSESSION", "PF", "TSPD_101"],
        "optional": ["TS0143c1eb", "TS016349ac", "TS01e11c15", "TS01f293bb",
                      "TS45dadd5e077", "TS8b476361027", "TS8ecf3524027",
                      "osano_consentmanager", "usbls"]
    },
    "wos": {
        "required": ["SID", "JSESSIONID"],
        "optional": []
    },
    "scopus": {
        "required": ["SESSION_ID", "INST_TOKEN"],
        "optional": []
    },
    "acm": {
        "required": ["JSESSIONID"],
        "optional": []
    },
    "cnki": {
        "required": ["Ecp_ClientId", "Ecp_session"],
        "optional": []
    },
}


def parse_cookie_text(text):
    """从浏览器复制的 Cookie 表格文本中解析出 name=value 对。
    支持格式：
      - 制表符分隔（浏览器直接复制的高保真格式）
      - 分号分隔（Cookie 头格式）
    """
    cookies = {}

    # 逐行解析
    for line in text.strip().split('\n'):
        line = line.strip()
        if not line:
            continue

        # 制表符分隔格式（名称\t值\t域名\t路径\t过期...）
        if '\t' in line:
            parts = line.split('\t')
            if len(parts) >= 2:
                name = parts[0].strip()
                value = parts[1].strip()
                if name and not name.startswith('#'):
                    cookies[name] = value
            continue

        # 分号分隔格式（name=value; name2=value2...）
        if ';' in line or '=' in line:
            for part in line.split(';'):
                part = part.strip()
                if '=' in part:
                    name, value = part.split('=', 1)
                    name = name.strip()
                    value = value.strip()
                    if name:
                        cookies[name] = value
            continue

    return cookies


def extract_for_db(cookies, db_name):
    """从已解析的 cookies 中提取指定数据库所需的项。"""
    if db_name not in DB_CONFIG:
        print(f"[MISS] 未知数据库: {db_name}")
        print(f"   可用选项: {', '.join(DB_CONFIG.keys())}")
        return None

    config = DB_CONFIG[db_name]
    extracted = {}
    missing_required = []

    for name in config["required"]:
        if name in cookies:
            extracted[name] = cookies[name]
        else:
            missing_required.append(name)

    for name in config["optional"]:
        if name in cookies:
            extracted[name] = cookies[name]

    if missing_required:
        print(f"\n[MISS] 缺少 {len(missing_required)} 个必需 Cookie，访问 {db_name.upper()} 将无法通过认证：")
        for name in missing_required:
            print(f"     - {name}")
        print(f"\n   原因诊断：")
        print(f"     ① 是否已在浏览器中登录 {db_name.upper()}？")
        print(f"     ② 登录后是否刷新了页面？")
        print(f"     ③ F12 是否选择了正确的域名？（如 ieeexplore.ieee.org 而非 www.ieee.org）")
        print(f"\n   解决步骤：")
        print(f"     1. 浏览器打开 {db_name.upper()} 首页")
        print(f"     2. 用学校 SSO 完成登录")
        print(f"     3. 确认页面显示已登录状态（如右上角显示用户名或机构名）")
        print(f"     4. F12 → Application → Cookies → 选择主域名")
        print(f"     5. 全选表格 → Ctrl+C 复制 → 重新运行本工具")
        return None

    return extracted


def format_cookie_string(cookies):
    """格式化为 HTTP Cookie 头字符串。"""
    return "; ".join(f"{k}={v}" for k, v in cookies.items())


def main():
    parser = argparse.ArgumentParser(
        description="从浏览器 Cookie 列表中提取付费数据库所需的精简 Cookie")
    parser.add_argument("--db", choices=list(DB_CONFIG.keys()),
                        help="目标数据库")
    parser.add_argument("--input", help="Cookie 文本文件路径")
    parser.add_argument("--interactive", action="store_true",
                        help="交互模式")
    parser.add_argument("--format", choices=["string", "json"], default="string",
                        help="输出格式 (默认: string)")
    args = parser.parse_args()

    if not any([args.db, args.interactive]):
        parser.print_help()
        sys.exit(1)

    # 选择数据库
    db_name = args.db
    if not db_name:
        print("可用数据库:")
        for i, name in enumerate(DB_CONFIG.keys(), 1):
            print(f"  {i}. {name}")
        choice = input("\n选择数据库 (序号): ").strip()
        try:
            db_name = list(DB_CONFIG.keys())[int(choice) - 1]
        except (ValueError, IndexError):
            print("[MISS] 无效选择")
            sys.exit(1)

    # 读取输入
    if args.input:
        if args.input == '-':
            text = sys.stdin.read()
        else:
            try:
                text = Path(args.input).read_text(encoding='utf-8')
            except FileNotFoundError:
                print(f"[MISS] 找不到文件: {args.input}")
                print(f"   请确认文件路径正确。如从浏览器粘贴，请使用 --interactive 模式。")
                sys.exit(1)
    else:
        print(f"\n[INPUT] 请粘贴从浏览器复制的 Cookie 数据")
        print("   (F12 → Application → Cookies → 全选 → 复制 → 粘贴到此处)")
        print("   粘贴完成后，在新行输入 END 然后按回车：\n")
        lines = []
        while True:
            line = input()
            if line.strip().upper() == 'END':
                break
            lines.append(line)
        text = '\n'.join(lines)

    if not text or not text.strip():
        print("[MISS] 输入为空。请粘贴 Cookie 数据后重试。")
        print("   提示：浏览器 F12 → Application → Cookies → 选择网站 → 全选表格 → Ctrl+C 复制")
        sys.exit(1)

    # 解析
    all_cookies = parse_cookie_text(text)
    if not all_cookies:
        print("[MISS] 未能解析任何 Cookie。请检查输入格式。")
        sys.exit(1)

    print(f"\n[OK] 共解析到 {len(all_cookies)} 个 Cookie")

    # 展示找到了哪些目标 cookie
    config = DB_CONFIG[db_name]
    found_req = [n for n in config["required"] if n in all_cookies]
    found_opt = [n for n in config["optional"] if n in all_cookies]
    print(f"\n   目标数据库: {db_name.upper()}")
    print(f"   必需 Cookie ({len(config['required'])} 项): {'[OK] 全部找到' if len(found_req) == len(config['required']) else f'[WARN] 找到 {len(found_req)}/{len(config['required'])}'}")
    for n in config["required"]:
        mark = " [OK]" if n in all_cookies else " [MISS]"
        print(f"     {mark}  {n}")
    if config["optional"]:
        print(f"   可选 Cookie ({len(found_opt)}/{len(config['optional'])} 项):")
        for n in config["optional"][:5]:
            if n in all_cookies:
                print(f"     [OK]  {n}")
        if len(config["optional"]) > 5:
            print(f"     ... (还有 {len(config['optional'])-5} 项)")

    # 提取
    extracted = extract_for_db(all_cookies, db_name)
    if not extracted:
        sys.exit(1)

    print(f"[OK] 提取到 {len(extracted)} 个 {db_name.upper()} 相关 Cookie")
    print(f"   必需: {len(DB_CONFIG[db_name]['required'])} 个 (全部找到)")
    print(f"   可选: {len([k for k in extracted if k in DB_CONFIG[db_name]['optional']])} 个\n")

    if args.format == "json":
        output = json.dumps(extracted, indent=2, ensure_ascii=False)
    else:
        output = format_cookie_string(extracted)

    print("━" * 50)
    print(output)
    print("━" * 50)
    print(f"\n[TIP] 将此 Cookie 字符串填入 config.yaml 对应数据库的 cookies.value 字段。")


if __name__ == "__main__":
    main()
