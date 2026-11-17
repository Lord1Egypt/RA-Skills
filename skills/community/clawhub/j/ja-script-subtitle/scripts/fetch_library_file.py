#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Step 0 —— 从 WorkBuddy 资料库下载真实文件

背景: 附件在本地 /root/uploads 下常常只是 10KB 的「资料库占位 HTML」，
      不是真文件（用 `file` 一看是 HTML 就知道）。必须走资料库 API 取真的。

用法:
    python fetch_library_file.py <out_dir> <nodeId>:<filename> [<nodeId>:<filename> ...]

示例:
    python fetch_library_file.py ./in \
        GJ71l3SeKQ6sugg6sMoH1B:A2.txt \
        NFu6v52cano3vBrLjQHmGg:A2.mp3

nodeId 就是资料库链接 https://www.workbuddy.cn/space/d/<nodeId> 里 d/ 后面那串。
"""
import json, os, subprocess, sys, urllib.request

SK = "/opt/sandbox-prefetched/blobs/skill/library/latest"
GEN = f"{SK}/drive/get_download_link.py"

if len(sys.argv) < 3:
    sys.exit(__doc__)
outdir = sys.argv[1]
os.makedirs(outdir, exist_ok=True)


def get_url(node_id):
    r = subprocess.run([sys.executable, GEN, "--node-id", node_id],
                       capture_output=True, text=True)
    for line in r.stdout.splitlines():
        if line.startswith("KS_DRIVE_DOWNLOAD"):
            return json.loads(line.split(" ", 1)[1])["download_url"]
    raise SystemExit(f"拿不到下载链接: {node_id}\n{r.stdout}\n{r.stderr}")


for spec in sys.argv[2:]:
    node_id, name = spec.split(":", 1)
    url = get_url(node_id)                       # 预签名 URL，短期有效，需立刻下载
    dst = os.path.join(outdir, name)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=300) as resp, open(dst, "wb") as f:
        f.write(resp.read())
    print(f"{name:32s} -> {os.path.getsize(dst):>12,d} bytes")
