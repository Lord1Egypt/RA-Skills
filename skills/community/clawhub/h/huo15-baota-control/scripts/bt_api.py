#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
宝塔面板 HTTP API 封装（供龙虾/自动化调用）。
鉴权：request_token = md5( str(request_time) + md5(api_key) )，POST 表单。
注意：必须带浏览器 User-Agent，否则宝塔反扫描会返回伪装 404。
零依赖（仅标准库）。
"""
from __future__ import annotations
import sys, os, json, time, hashlib, ssl, argparse
import urllib.request, urllib.parse

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")


def md5(s: str) -> str:
    return hashlib.md5(s.encode("utf-8")).hexdigest()


class BtPanel:
    def __init__(self, url: str, key: str):
        self.url = url.rstrip("/")
        self.key = key

    def _auth(self):
        t = int(time.time())
        return {"request_time": t,
                "request_token": md5(str(t) + md5(self.key))}

    def call(self, endpoint: str, params: dict | None = None, timeout: int = 20):
        data = self._auth()
        if params:
            data.update(params)
        body = urllib.parse.urlencode(data).encode()
        req = urllib.request.Request(
            self.url + endpoint, data=body,
            headers={"User-Agent": UA,
                     "Content-Type": "application/x-www-form-urlencoded",
                     "Accept": "application/json, text/javascript, */*"})
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        try:
            with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
                raw = r.read().decode("utf-8", "replace")
                status = r.status
        except urllib.error.HTTPError as e:
            raw = e.read().decode("utf-8", "replace")
            status = e.code
        try:
            return json.loads(raw)
        except Exception:
            return {"_status": status, "_raw": raw[:400]}

    # ---- 高层封装（只读为主，写操作需显式调用） ----
    def sysinfo(self):
        return self.call("/system?action=GetSystemTotal")
    def network(self):
        return self.call("/system?action=GetNetWork")
    def disk(self):
        return self.call("/system?action=GetDiskInfo")
    def sites(self, limit=100):
        return self.call("/data?action=getData",
                         {"table": "sites", "limit": limit, "p": 1})
    def databases(self, limit=100):
        return self.call("/data?action=getData",
                         {"table": "databases", "limit": limit, "p": 1})
    def site_stop(self, site_id, name):
        return self.call("/site?action=SiteStop", {"id": site_id, "name": name})
    def site_start(self, site_id, name):
        return self.call("/site?action=SiteStart", {"id": site_id, "name": name})


def load_panel(name=None, cfg_path=None):
    cfg_path = cfg_path or os.path.expanduser("~/.huo15/baota.json")
    with open(cfg_path) as f:
        cfg = json.load(f)
    panels = cfg["panels"]
    if name:
        p = next(x for x in panels if x["name"] == name)
    else:
        p = panels[0]
    return BtPanel(p["url"], p.get("token") or p["key"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", help="sysinfo|network|disk|sites|databases|site_stop|site_start|raw")
    ap.add_argument("--panel", help="面板名(默认第一个)")
    ap.add_argument("--url"); ap.add_argument("--key")
    ap.add_argument("--endpoint"); ap.add_argument("--params", default="{}")
    ap.add_argument("--id"); ap.add_argument("--name")
    a = ap.parse_args()
    bt = BtPanel(a.url, a.key) if a.url and a.key else load_panel(a.panel)
    if a.cmd == "raw":
        out = bt.call(a.endpoint, json.loads(a.params))
    elif a.cmd in ("site_stop", "site_start"):
        out = getattr(bt, a.cmd)(a.id, a.name)
    else:
        out = getattr(bt, a.cmd)()
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
