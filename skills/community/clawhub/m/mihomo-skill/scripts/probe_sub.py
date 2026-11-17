#!/usr/bin/env python3
"""订阅链接可用性探针：判定一个 Clash/Mihomo 订阅地址到底卡在哪一层。

用法:
    python3 probe_sub.py <订阅URL> [--ua UA] [--tries N] [--json]

为什么需要它:
    "订阅拉不下来"有五六种完全不同的原因（DNS 污染 / TCP 阻断 / SNI 阻断 /
    需要代理才能访问 / 服务端拒绝 / 激活未完成），症状都是 mihomo 日志里
    一句 "pull error"。逐层探测才能定位，否则容易误判成"订阅废了"。
    RST 类阻断往往是概率性的，单次失败不代表被墙，因此默认重试。

verdict 取值:
    OK_SNI             正常，mihomo 直连即可拉取
    OK_NO_SNI_ONLY     SNI 被阻断，需走引导节点/代理隧道拉取
    TLS_BLOCKED        带/不带 SNI 都握不上手
    TCP_BLOCKED        TCP 层不通
    DNS_FAIL           解析不出任何地址
    HTTP_ERROR         网络通但服务端拒绝（看 body：激活/欠费/失效）
"""

import argparse
import json
import re
import socket
import ssl
import subprocess
import sys
from urllib.parse import urlparse

RESOLVERS = [
    ("system", None),
    ("8.8.8.8", "8.8.8.8"),
    ("1.1.1.1", "1.1.1.1"),
    ("223.5.5.5", "223.5.5.5"),
    ("119.29.29.29", "119.29.29.29"),
]

KNOWN_POISON = {
    "93.46.8.90", "46.82.174.69", "8.7.198.46", "59.24.3.174",
    "243.185.187.39", "59.24.3.173", "203.98.7.65", "37.61.54.158",
}


def resolve(host, server):
    cmd = ["/usr/bin/dig", "+short", "+time=3", "+tries=1"]
    if server:
        cmd.append("@" + server)
    cmd.append(host)
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=8).stdout
    except Exception:
        return []
    ips = []
    for line in out.splitlines():
        line = line.strip()
        if re.fullmatch(r"\d{1,3}(?:\.\d{1,3}){3}", line) and line not in ips:
            ips.append(line)
    return ips


def resolve_doh(host):
    """DoH 兜底解析：CDN 会轮换 IP，本地解析器给的地址可能正好被墙。
    走 JSON API 拿另一批地址，扩大候选集。"""
    import urllib.request

    urls = [
        "https://dns.alidns.com/resolve?name=%s&type=A" % host,
        "https://cloudflare-dns.com/dns-query?name=%s&type=A" % host,
    ]
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    ips = []
    for u in urls:
        try:
            req = urllib.request.Request(
                u, headers={"Accept": "application/dns-json", "User-Agent": "mihomo-skill/1.0"}
            )
            data = json.loads(opener.open(req, timeout=6).read().decode())
            for ans in data.get("Answer") or []:
                ip = ans.get("data", "")
                if re.fullmatch(r"\d{1,3}(?:\.\d{1,3}){3}", ip) and ip not in ips:
                    ips.append(ip)
        except Exception:
            continue
    return ips


def tcp_ok(ip, port, timeout=5):
    try:
        s = socket.create_connection((ip, port), timeout=timeout)
        s.close()
        return True
    except Exception:
        return False


def http_probe(ip, port, host, path, use_sni, ua, timeout=12):
    """返回 (ok, detail, body)。ok 表示握手成功并拿到响应头。"""
    raw = None
    ssock = None
    try:
        raw = socket.create_connection((ip, port), timeout=timeout)
        if port == 443 or True:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            try:
                ctx.set_ciphers("DEFAULT@SECLEVEL=1")
            except Exception:
                pass
            ssock = ctx.wrap_socket(raw, server_hostname=(host if use_sni else None))
    except ssl.SSLError as e:
        if raw:
            raw.close()
        return False, "SSL error: %s" % e, ""
    except (ConnectionResetError, BrokenPipeError):
        if raw:
            raw.close()
        return False, "握手阶段被 RST（阻断特征）", ""
    except Exception as e:
        if raw:
            raw.close()
        return False, "连接失败: %s" % e, ""

    try:
        req = (
            "GET {path} HTTP/1.1\r\nHost: {host}\r\nUser-Agent: {ua}\r\n"
            "Accept: */*\r\nAccept-Encoding: identity\r\nConnection: close\r\n\r\n"
        ).format(path=path or "/", host=host, ua=ua)
        ssock.settimeout(timeout)
        ssock.sendall(req.encode())
        chunks, total = [], 0
        while total < 4_000_000:
            try:
                b = ssock.recv(65536)
            except socket.timeout:
                break
            if not b:
                break
            chunks.append(b)
            total += len(b)
        data = b"".join(chunks)
    except Exception as e:
        return False, "已握手但读响应失败: %s" % e, ""
    finally:
        try:
            ssock.close()
        except Exception:
            pass

    text = data.decode("utf-8", "replace")
    m = re.match(r"HTTP/\d(?:\.\d)?\s+(\d{3})", text)
    status = int(m.group(1)) if m else 0
    body = text.split("\r\n\r\n", 1)[1] if "\r\n\r\n" in text else ""
    return True, "HTTP %d, body %d 字节" % (status, len(body)), body


def try_both(ip, port, host, path, ua, tries):
    """对一个 IP 反复尝试，返回 (sni_result, nosni_result)。result=(ok, detail, body)"""
    best_sni, best_nosni = (False, "未尝试", ""), (False, "未尝试", "")
    for _ in range(tries):
        r = http_probe(ip, port, host, path, True, ua)
        if r[0] and len(r[2]) > 200:
            best_sni = r
            break
        if r[0]:
            best_sni = r
        else:
            best_sni = r
    for _ in range(tries):
        r = http_probe(ip, port, host, path, False, ua)
        if r[0] and len(r[2]) > 200:
            best_nosni = r
            break
        if r[0]:
            best_nosni = r
        else:
            best_nosni = r
    return best_sni, best_nosni


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--ua", default="clash.meta/1.19.0")
    ap.add_argument("--tries", type=int, default=6)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    u = urlparse(args.url)
    host = u.hostname
    port = u.port or (443 if u.scheme == "https" else 80)
    path = u.path or "/"
    if u.query:
        path += "?" + u.query

    rep = {"url": args.url, "host": host, "port": port, "resolvers": {}, "checks": {}}
    for label, server in RESOLVERS:
        rep["resolvers"][label] = resolve(host, server)

    all_ips = []
    for ips in rep["resolvers"].values():
        for ip in ips:
            if ip not in all_ips:
                all_ips.append(ip)

    poisoned = [l for l, ips in rep["resolvers"].items() if ips and all(i in KNOWN_POISON for i in ips)]
    rep["polluted_resolvers"] = poisoned

    if not all_ips:
        rep["verdict"] = "DNS_FAIL"
        emit(rep, args.json)
        return 0

    clean = [ip for ip in all_ips if ip not in KNOWN_POISON]
    candidates = list(clean or all_ips)

    reachable = [ip for ip in candidates[:4] if tcp_ok(ip, port)]
    if not reachable:
        doh_ips = [ip for ip in resolve_doh(host) if ip not in KNOWN_POISON and ip not in candidates]
        rep["doh_extra"] = doh_ips
        for ip in doh_ips[:4]:
            if tcp_ok(ip, port):
                reachable.append(ip)
        candidates += doh_ips

    rep["candidates"] = candidates
    rep["checks"]["tcp_reachable"] = reachable
    if not reachable:
        rep["verdict"] = "TCP_BLOCKED"
        emit(rep, args.json)
        return 0

    sni = nosni = (False, "未尝试", "")
    used_ip = reachable[0]
    for ip in reachable:
        s, n = try_both(ip, port, host, path, args.ua, args.tries)
        if (s[0] and len(s[2]) > 200) or (n[0] and len(n[2]) > 200):
            sni, nosni, used_ip = s, n, ip
            break
        sni, nosni, used_ip = s, n, ip

    rep["used_ip"] = used_ip
    rep["checks"]["tls_with_sni"] = sni[1]
    rep["checks"]["tls_without_sni"] = nosni[1]

    body = ""
    if sni[0] and len(sni[2]) > 200:
        rep["verdict"] = "OK_SNI"
        body = sni[2]
    elif nosni[0] and len(nosni[2]) > 200:
        rep["verdict"] = "OK_NO_SNI_ONLY"
        body = nosni[2]
    elif sni[0] or nosni[0]:
        rep["verdict"] = "HTTP_ERROR"
        body = sni[2] or nosni[2]
    else:
        rep["verdict"] = "TLS_BLOCKED"

    if body:
        rep["body_size"] = len(body)
        head = body[:400].strip()
        rep["body_head"] = head
        try:
            j = json.loads(body)
            if isinstance(j, dict):
                rep["body_json"] = {k: j[k] for k in ("status", "error_code", "message") if k in j}
        except Exception:
            pass

    emit(rep, args.json)
    return 0


def emit(rep, as_json):
    if as_json:
        print(json.dumps(rep, ensure_ascii=False, indent=2))
        return
    print("URL      : %s" % rep["url"])
    print("目标     : %s:%s" % (rep["host"], rep["port"]))
    for label, ips in rep["resolvers"].items():
        mark = "  [污染]" if ips and all(i in KNOWN_POISON for i in ips) else ""
        print("  解析 %-13s %s%s" % (label, " ".join(ips) or "(空)", mark))
    if rep.get("used_ip"):
        print("实测 IP  : %s" % rep["used_ip"])
    for k, v in rep["checks"].items():
        if isinstance(v, list):
            v = " ".join(v) or "(无)"
        print("  %-16s %s" % (k, v))
    if rep.get("body_json"):
        print("服务端回 : %s" % json.dumps(rep["body_json"], ensure_ascii=False))
    elif rep.get("body_head"):
        print("响应体   : %s" % rep["body_head"][:180].replace("\n", " "))
    print("结论     : %s" % rep["verdict"])
    tips = {
        "OK_SNI": "mihomo 配 proxy: DIRECT 即可正常拉取",
        "OK_NO_SNI_ONLY": "SNI 被阻断 → 用「引导节点」方案：加一条可用静态节点，provider 设 proxy: <该节点>",
        "TLS_BLOCKED": "TLS 完全握不上，考虑换域名/换机场，或全程走隧道拉取",
        "TCP_BLOCKED": "端口不通，先确认订阅地址本身是否还有效",
        "DNS_FAIL": "解析不出地址，域名可能已废弃",
        "HTTP_ERROR": "网络通、服务端拒绝：按 body 里的 error_code 处置（激活/欠费/失效）",
    }
    print("处置     : %s" % tips.get(rep["verdict"], ""))


if __name__ == "__main__":
    sys.exit(main())
