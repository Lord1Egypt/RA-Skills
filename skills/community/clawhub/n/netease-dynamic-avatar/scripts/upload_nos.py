#!/usr/bin/env python3
"""把动图直传网易云 NOS（跳过 /upload/img/op 裁切）。

用法:
    python upload_nos.py <token> <objectKey> <file> [content-type]

参数从浏览器 /api/nos/token/alloc 的返回里取：
    token      -> result.token
    objectKey  -> result.objectKey
    docId      -> result.docId （本脚本会从 objectKey 里再推一遍）

成功后回浏览器设头像：
    POST /api/user/avatar/upload/v1  imgid=<docId>&checkToken=<WM.getToken 结果>
"""

import json
import sys
import urllib.error
import urllib.request

DEFAULT_HOST = "https://nosup-hz1.127.net"
BUCKET = "yyimgs"


def discover_host(bucket=BUCKET):
    try:
        with urllib.request.urlopen(
            "https://wanproxy.127.net/lbs?version=1.0&bucketname=" + bucket, timeout=15
        ) as r:
            j = json.loads(r.read().decode("utf-8", "replace"))
        ups = j.get("upload") or []
        if ups:
            host = ups[0]
            if not host.startswith("http"):
                host = "https://" + host
            print("lbs 选择上传节点:", host)
            return host
    except Exception as e:  # noqa: BLE001
        print("lbs 查询失败(%s)，用默认节点" % e)
    return DEFAULT_HOST


def main():
    if len(sys.argv) < 4:
        sys.stderr.write(__doc__)
        return 1

    token, object_key, path = sys.argv[1], sys.argv[2], sys.argv[3]
    ctype = sys.argv[4] if len(sys.argv) > 4 else "image/webp"

    with open(path, "rb") as f:
        data = f.read()

    head = data[:12]
    if head[:4] == b"RIFF" and head[8:12] == b"WEBP":
        kind = "webp"
    elif head[:3] == b"GIF":
        kind = "gif"
    elif head[:2] == b"\xff\xd8":
        kind = "jpeg"
    else:
        kind = "unknown"

    print("本地文件: %s  大小=%d  识别类型=%s  魔数=%r" % (path, len(data), kind, head))
    if len(data) > 5 * 1024 * 1024:
        sys.stderr.write("超过 5MB 硬限制，先压缩\n")
        return 1

    host = discover_host()
    url = "%s/%s/%s?offset=0&complete=true&version=1.0" % (host, BUCKET, object_key)
    print("POST", url)

    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("x-nos-token", token)
    req.add_header("Content-Type", ctype)
    req.add_header("Content-Length", str(len(data)))

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            body = resp.read().decode("utf-8", "replace")
            print("HTTP", resp.status)
            print("响应:", body[:800])
            print("")
            print("下一步: 用下面的 docId 调 /api/user/avatar/upload/v1")
            print("docId =", object_key.split("/")[-1])
            return 0
    except urllib.error.HTTPError as e:
        print("HTTPError", e.code)
        print(e.read().decode("utf-8", "replace")[:800])
        return 2
    except Exception as e:  # noqa: BLE001
        print("ERR", type(e).__name__, e)
        return 3


if __name__ == "__main__":
    sys.exit(main())
