#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""OpenList/AList 直链助手：登录 OpenList，取某个文件的 raw_url，并修正为对外可达的端口。

用法:
  python openlist_url.py --base https://openlist-router1.youguess.site:8443 \
      --username test --password '***' --path '/00.我的文件/电子书/xxx.pdf'

输出：一行可直接给 `mineru_pdf2md.py --pdf-url` 用的 URL。
说明：AList 返回的 raw_url 常用站点默认端口(443)，若你的 OpenList 实际走 :8443，
本脚本会把 host:port 改成 --base 里的，避免 443 不通。
"""
import argparse
import time
from urllib.parse import urlsplit, urlunsplit

import requests

requests.packages.urllib3.disable_warnings()


def login(base, user, pwd, retries=8):
    for _ in range(retries):
        try:
            r = requests.post(base + "/api/auth/login",
                              json={"username": user, "password": pwd},
                              timeout=25, verify=False)
            j = r.json()
            if j.get("code") == 200:
                return j["data"]["token"]
            raise SystemExit(f"登录失败: {j}")
        except requests.RequestException:
            time.sleep(2)
    raise SystemExit("登录请求失败（网络不可达）")


def get_url(base, token, path, retries=8):
    for _ in range(retries):
        try:
            r = requests.post(base + "/api/fs/get", headers={"Authorization": token},
                              json={"path": path, "password": ""}, timeout=30, verify=False)
            j = r.json()
            if j.get("code") != 200:
                raise SystemExit(f"取直链失败: {j}")
            raw = j["data"]["raw_url"]
            b = urlsplit(base)
            u = urlsplit(raw)
            return urlunsplit((u.scheme, b.netloc, u.path, u.query, u.fragment))
        except requests.RequestException:
            time.sleep(2)
    raise SystemExit("取直链请求失败（网络不可达）")


def main():
    ap = argparse.ArgumentParser(description="OpenList 文件直链获取（修正端口）")
    ap.add_argument("--base", required=True, help="OpenList 站点，如 https://host:8443")
    ap.add_argument("--username", required=True)
    ap.add_argument("--password", required=True)
    ap.add_argument("--path", required=True, help="文件在 OpenList 中的绝对路径，如 /dir/a.pdf")
    args = ap.parse_args()
    tok = login(args.base.rstrip("/"), args.username, args.password)
    print(get_url(args.base.rstrip("/"), tok, args.path))


if __name__ == "__main__":
    main()
