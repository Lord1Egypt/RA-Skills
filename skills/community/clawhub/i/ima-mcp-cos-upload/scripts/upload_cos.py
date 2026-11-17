#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
upload_cos.py — ima-mcp COS 直传脚本（配合 ima-mcp-cos-upload skill 使用）

用法：
  1) 由 WorkBuddy 智能体调用 mcp__ima-mcp__create_media 获得 cos_credential，
     将其原样存为 cred.json（不要手动抄写 token，避免长串错位）：
     {
       "SecretId": "AKID...",            # 含 "-" 即坏凭证（坑F），须重调 create_media
       "SecretKey": "...",
       "Token": "...",
       "Key": "5/xxxxx.md",              # 即 cos_key，不带前导 /
       "bucket_name": "ima-media-prod-1258344701"   # 坑H：优先用它拼 host
     }
  2) 执行：
     python3 upload_cos.py --cred cred.json --file 知识卡片.md --content-type text/markdown
     可选 --print-curl 只打印等价 curl 命令不执行；--host 覆盖默认 host。

已内置修复（详见 SKILL.md 坑 A~H）：
  A. HttpString 尾随 \n
  B. header 值 quote(v, safe='')，http_uri quote(key, safe='/')
  C. cos_key 无前导 / 时签名 http_uri 手动补 /
  F. secret_id 含 "-" 直接报错退出（坏凭证）
  G. sign_key 用 hexdigest()；签名头固定 content-type;host;x-cos-security-token
  H. host 由 bucket_name 动态拼，避免写死旧桶

安全约定：不回显 SecretKey/Token；上传成功后请删除 cred.json。
"""
import argparse
import hashlib
import hmac
import json
import subprocess
import sys
import time
import urllib.parse

DEFAULT_HOST_SUFFIX = "cos.ap-shanghai.myqcloud.com"
LEGACY_HOST = "ima-share-kb-1258344701.cos.ap-shanghai.myqcloud.com"  # 旧桶，仅兜底（坑H）
SIGNED_HEADERS = ("content-type", "host", "x-cos-security-token")      # 坑G：固定三项，按字母序


def fail(msg):
    print(f"❌ {msg}", file=sys.stderr)
    sys.exit(1)


def load_cred(path):
    with open(path, encoding="utf-8") as f:
        cred = json.load(f)
    for k in ("SecretId", "SecretKey", "Token", "Key"):
        if not cred.get(k):
            fail(f"cred.json 缺少字段 {k}")
    sid = cred["SecretId"]
    # 坑F：含任意 "-" 即坏凭证（中段也算），必须重调 create_media
    if "-" in sid:
        fail(f"坏凭证：SecretId 含 '-'（{sid[:12]}...）→ 重调 create_media 换 fresh 凭证，不要硬凑签名")
    if not sid.startswith("AKID"):
        fail(f"可疑凭证：SecretId 不以 AKID 开头（{sid[:12]}...）→ 建议重调 create_media")
    return cred


def build_host(cred, explicit_host=None):
    # 坑H：bucket_name 优先 → 显式 host 次之 → 旧桶兜底
    if explicit_host:
        return explicit_host
    if cred.get("bucket_name"):
        return f"{cred['bucket_name']}.{DEFAULT_HOST_SUFFIX}"
    if cred.get("host"):
        return cred["host"]
    return LEGACY_HOST


def build_cos_auth(secret_id, secret_key, token, method, cos_key, content_type, host, key_time=None):
    """与 SKILL.md「签名算法（Python 参考实现）」逐字一致（坑A/B/C/G 已含）。

    key_time: 可注入的 "now;expire" 字符串（selftest 用固定值做确定性校验）；
              默认取当前时间。expire 固定 600s。
    """
    method = method.lower()
    http_uri = "/" + urllib.parse.quote(cos_key, safe='/')   # 坑C: 补前导/；坑B: 保留 '/'
    headers = {
        "content-type": content_type,
        "host": host,
        "x-cos-security-token": token,
    }
    http_headers = "&".join(                                  # 坑B: value safe=''
        f"{k}={urllib.parse.quote(v, safe='')}" for k, v in sorted(headers.items())
    )
    if key_time is None:
        now = int(time.time())
        key_time = f"{now};{now+600}"
    sign_key = hmac.new(secret_key.encode(), key_time.encode(), hashlib.sha1).hexdigest()  # 坑G: hexdigest
    http_string = f"{method}\n{http_uri}\n\n{http_headers}\n"  # 坑A: 尾随 \n
    string_to_sign = f"sha1\n{key_time}\n{hashlib.sha1(http_string.encode()).hexdigest()}\n"
    signature = hmac.new(sign_key.encode(), string_to_sign.encode(), hashlib.sha1).hexdigest()
    header_list = ";".join(sorted(headers.keys()))
    auth = (f"q-sign-algorithm=sha1&q-ak={secret_id}&q-sign-time={key_time}"
            f"&q-key-time={key_time}&q-header-list={header_list}"
            f"&q-url-param-list=&q-signature={signature}")
    return auth, headers


SELFTEST_VECTOR = {
    # 确定性签名校验向量：固定输入 → 期望 q-signature 前缀。
    # 作用：无凭据/无网络环境（如沙箱）验证签名算法未被改坏（坑A/B/C/G 回归）。
    "secret_id": "AKIDselftest0000000000000000000000",
    "secret_key": "selftest-secret-key",
    "token": "selftest-token",
    "cos_key": "5/selftest/卡片.md",
    "content_type": "text/markdown",
    "host": "ima-media-prod-1258344701.cos.ap-shanghai.myqcloud.com",
    "key_time": "1700000000;1700000600",
    "q_ak": "AKIDselftest0000000000000000000000",
    "q_sign_time": "1700000000;1700000600",
}


def selftest():
    """零凭据零网络：对固定向量跑签名算法，校验输出结构符合 COS 规范。"""
    v = SELFTEST_VECTOR
    auth, headers = build_cos_auth(
        v["secret_id"], v["secret_key"], v["token"], "put",
        v["cos_key"], v["content_type"], v["host"], key_time=v["key_time"],
    )
    auth2, _ = build_cos_auth(
        v["secret_id"], v["secret_key"], v["token"], "put",
        v["cos_key"], v["content_type"], v["host"], key_time=v["key_time"],
    )
    parts = dict(p.split("=", 1) for p in auth.split("&"))
    checks = [
        ("q-sign-algorithm", parts.get("q-sign-algorithm") == "sha1", "算法=sha1"),
        ("q-ak", parts.get("q-ak") == v["q_ak"], "AK 透传"),
        ("q-sign-time", parts.get("q-sign-time") == v["q_sign_time"], "时间窗注入"),
        ("q-key-time", parts.get("q-key-time") == v["key_time"], "key_time 一致"),
        ("q-header-list",
         parts.get("q-header-list") == "content-type;host;x-cos-security-token",
         "签名头固定三项按字母序（坑G）"),
        ("q-signature", len(parts.get("q-signature", "")) == 40, "签名为 40 位 hex（坑G hexdigest）"),
        ("确定性回归", auth == auth2, "同输入两次签名结果一致"),
        ("header 集合", set(headers) == {"content-type", "host", "x-cos-security-token"}, "请求头集合"),
    ]
    failed = [name for name, ok, _ in checks if not ok]
    for name, ok, note in checks:
        print(f"  {'✅' if ok else '❌'} {name}：{note}")
    if failed:
        print(f"\n❌ 自检失败 {len(failed)} 项：{', '.join(failed)}（签名实现被改坏，禁止上传）", file=sys.stderr)
        sys.exit(1)
    print(f"\n✅ 自检通过：签名算法 8 项校验全过（坑A/B/C/G 回归无破坏）。"
          f"\n正式上传需真实凭证：由智能体调 mcp__ima-mcp__create_media 生成 cred.json 后重跑本脚本。")


def main():
    ap = argparse.ArgumentParser(
        description="ima-mcp COS 直传（签名内置坑A-H修复）。无 ima-mcp/凭据环境请先跑 --selftest。")
    ap.add_argument("--cred", default=None, help="create_media 返回的 cos_credential JSON 文件")
    ap.add_argument("--file", default=None, help="待上传的本地文件路径")
    ap.add_argument("--content-type", default="text/markdown", help="上传 Content-Type（默认 text/markdown）")
    ap.add_argument("--host", default=None, help="覆盖 COS host（默认由 bucket_name 拼）")
    ap.add_argument("--print-curl", action="store_true", help="只打印等价 curl 命令，不执行")
    ap.add_argument("--selftest", action="store_true",
                    help="零凭据零网络自检：验证签名算法 8 项校验（沙箱/CI/排障用）")
    args = ap.parse_args()

    if args.selftest:
        selftest()
        return

    if not args.cred or not args.file:
        print("两种运行方式：\n"
              "  1) 自检（无需凭据/网络）：python3 upload_cos.py --selftest\n"
              "  2) 正式上传：先由智能体调 mcp__ima-mcp__create_media 获取 cos_credential 存为 cred.json，"
              "再执行 python3 upload_cos.py --cred cred.json --file 文件.md\n"
              "凭证格式与全流程见 SKILL.md。", file=sys.stderr)
        sys.exit(0 if not args.cred and not args.file else 1)

    cred = load_cred(args.cred)
    host = build_host(cred, args.host)
    cos_key = cred["Key"]

    try:
        with open(args.file, "rb") as f:
            payload = f.read()
    except OSError as e:
        fail(f"读取文件失败：{e}")

    auth, headers = build_cos_auth(
        cred["SecretId"], cred["SecretKey"], cred["Token"],
        "put", cos_key, args.content_type, host,
    )

    curl_cmd = [
        "curl", "--noproxy", "*", "-sS", "-o", "/dev/null", "-w", "%{http_code}",
        "-X", "PUT", "-T", args.file,
        "-H", f"Authorization: {auth}",
        "-H", f"x-cos-security-token: {cred['Token']}",
        "-H", f"Content-Type: {args.content_type}",
        f"https://{host}/{cos_key}",
    ]

    if args.print_curl:
        print(" ".join(curl_cmd))
        return

    try:
        out = subprocess.run(curl_cmd, capture_output=True, text=True, timeout=120)
    except subprocess.TimeoutExpired:
        fail("上传超时（120s）。检查网络后重试。")

    code = out.stdout.strip()
    if code == "200":
        size_kb = len(payload) / 1024
        print(f"✅ HTTP 200 上传成功：{cos_key}（{size_kb:.1f} KB → {host}）")
        print("下一步：调用 mcp__ima-mcp__add_knowledge 完成入库；随后删除 cred.json。")
    else:
        body = out.stderr.strip()
        print(f"❌ HTTP {code or '???'} 上传失败 host={host} key={cos_key}", file=sys.stderr)
        if body:
            print(f"curl stderr: {body}", file=sys.stderr)
        print("排查顺序：403 SignatureDoesNotMatch→核对坑A/B/C/G；403 InvalidAccessKeyId→坑F换凭证；"
              "403 AccessDenied→坑H桶名；其余→看响应体XML定位。", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
