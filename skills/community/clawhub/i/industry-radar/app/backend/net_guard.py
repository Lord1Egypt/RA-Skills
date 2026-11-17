"""
出站抓取的统一安全出口（SSRF 防护）。

背景
----
本服务的正文页 URL 来自 RSS 条目、也就是**外部可控内容**。若直接
`requests.get(article_url)`，攻击者只要在源里塞一条指向
`http://169.254.169.254/...`（云元数据）或 `http://10.0.0.5:8080/`
（内网服务）的链接，就能借服务端身份去访问内网。

策略（默认拒绝）
----
1. 只允许 http / https，其余协议（file://、gopher://、ftp://…）一律拒绝。
2. 拒绝携带 userinfo 的 URL（`http://a:b@host`），避免解析歧义。
2b. 端口白名单（默认 80/443，`IR_ALLOWED_PORTS` 可配），杜绝借高位端口探测内网服务；
    IP 字面量仅当落在公网地址段时才放行。
3. 主机名先按字面判断，再做 DNS 解析，**所有**解析结果必须落在公网地址段，
   否则拒绝——命中回环、私网、链路本地（含 169.254.169.254 元数据）、
   CGNAT、保留段、组播、IPv6 ULA / link-local 都要拦。
4. 不自动跟随重定向：手动逐跳跟随（最多 MAX_REDIRECTS 次），
   每一跳都重新走第 1~3 步，防止「公网 302 到内网」绕过。
5. 响应体限量读取（默认 3MB），避免被超大响应拖垮。
6. **连接固定到已校验 IP**：校验通过后不再让 requests/urllib3 重新解析域名，
   而是用自定义 HTTPAdapter 把 TCP 目标改写成该 IP，同时保留原始 Host 头与
   TLS SNI / 证书校验。这样「校验时公网、连接时内网」的 DNS 重绑定（TOCTOU）
   无法生效；会话同时设置 trust_env=False，避免环境代理重新解析域名。

残余风险与生产建议
----
本模块已消除应用层 DNS 重绑定窗口，但仍建议在网络层做纵深防御：云上部署时在
VPC 侧配置 Security Group + NAT 白名单，禁止访问 169.254.169.254 与内网网段。
注意：为保持 IP 固定有效，本模块**故意忽略** HTTP_PROXY / HTTPS_PROXY 环境变量；
如需经代理出网，请使用 TUN / fake-IP 模式（并显式设置 IR_ALLOW_PROXY_FAKEIP=1）。
"""
from __future__ import annotations

import ipaddress
import logging
import os
import socket
from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple
from urllib.parse import urljoin, urlparse, urlunparse

import requests
from requests.adapters import HTTPAdapter

from config import ALLOWED_PORTS

log = logging.getLogger("industryradar.netguard")

ALLOWED_SCHEMES = ("http", "https")
MAX_REDIRECTS = 3
DEFAULT_MAX_BYTES = 3 * 1024 * 1024


class UnsafeUrlError(ValueError):
    """URL 未通过出站安全校验。"""


# 明确禁止的地址段（含云元数据、回环、私网、保留、组播）
_BLOCKED_NETWORKS = tuple(ipaddress.ip_network(n) for n in (
    "0.0.0.0/8",          # 本网络
    "10.0.0.0/8",         # 私网 A
    "100.64.0.0/10",      # CGNAT（云厂商内部常用）
    "127.0.0.0/8",        # 回环
    "169.254.0.0/16",     # 链路本地：169.254.169.254 云元数据
    "172.16.0.0/12",      # 私网 B
    "192.0.0.0/24",       # IETF 协议分配
    "192.0.2.0/24",       # TEST-NET-1
    "192.168.0.0/16",     # 私网 C
    "198.51.100.0/24",    # TEST-NET-2
    "203.0.113.0/24",     # TEST-NET-3
    "224.0.0.0/4",        # 组播
    "240.0.0.0/4",        # 保留 + 广播
    "::/128", "::1/128",  # 未指定 / 回环
    "fc00::/7",           # IPv6 ULA
    "fe80::/10",          # IPv6 链路本地
    "ff00::/8",           # IPv6 组播
    "64:ff9b::/96",       # NAT64（可映射到内网 v4）
))

# 本地代理（如 Clash fake-IP 模式）会把所有域名解析到 198.18.0.0/15。
# 该段是「基准测试保留段」（RFC 2544），不属于公网地址，也不对应任何真实站点；
# 放行它等于把「域名最终连到哪里」的解释权交给本机代理与路由，与「仅公网、
# 默认拒绝」的承诺冲突，因此**默认拒绝**。确需在 fake-IP 代理后演示时，
# 显式设置 IR_ALLOW_PROXY_FAKEIP=1（兼容旧开关 IR_BLOCK_PROXY_FAKEIP=0）。
_PROXY_FAKEIP_NET = ipaddress.ip_network("198.18.0.0/15")


def _proxy_fakeip_allowed() -> bool:
    """fake-IP 段是否放行；每次调用读取环境变量，便于测试与运行时切换。"""
    if os.getenv("IR_ALLOW_PROXY_FAKEIP", "0") == "1":
        return True
    # 兼容旧版语义：显式置 IR_BLOCK_PROXY_FAKEIP=0 表示放行
    return os.getenv("IR_BLOCK_PROXY_FAKEIP", "1") == "0"

# IPv6 里包裹的 IPv4（NAT64 / IPv4-translated），必须拆开再判段，
# 否则 ::ffff:127.0.0.1 之类的写法能绕过检查。
_NAT64_NETS = (
    ipaddress.ip_network("64:ff9b::/96"),
    ipaddress.ip_network("::ffff:0:0:0/96"),
)

_BLOCKED_HOSTNAMES = {
    "localhost", "localhost.localdomain", "ip6-localhost", "ip6-loopback",
    "metadata", "metadata.google.internal", "instance-data",
}
_BLOCKED_SUFFIXES = (".localhost", ".local", ".internal", ".home.arpa")


def _strip_zone(addr: str) -> str:
    """去掉 IPv6 的 scope id（fe80::1%eth0 → fe80::1）。"""
    return addr.split("%", 1)[0]


def _unwrap_v4(ip):
    """把 IPv6 里包裹的 IPv4 拆出来（::ffff:a.b.c.d / NAT64 / v4-translated）。"""
    if not isinstance(ip, ipaddress.IPv6Address):
        return ip
    if ip.ipv4_mapped is not None:
        return ip.ipv4_mapped
    for net in _NAT64_NETS:
        if ip in net:
            return ipaddress.IPv4Address(int(ip) & 0xFFFFFFFF)
    return ip


def is_public_ip(addr: str) -> bool:
    """判断单个 IP 字面量是否为可访问的公网地址。"""
    try:
        ip = _unwrap_v4(ipaddress.ip_address(_strip_zone(addr)))
    except ValueError:
        return False

    # fake-IP 代理段：默认拒绝，需显式 IR_ALLOW_PROXY_FAKEIP=1（详见上方说明）
    if isinstance(ip, ipaddress.IPv4Address) and ip in _PROXY_FAKEIP_NET \
            and _proxy_fakeip_allowed():
        return True

    if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved \
            or ip.is_multicast or ip.is_unspecified:
        return False
    return not any(ip in net for net in _BLOCKED_NETWORKS if net.version == ip.version)


def _resolve(host: str) -> Set[str]:
    """解析主机名，返回全部 A/AAAA 地址；解析失败返回空集。"""
    try:
        infos = socket.getaddrinfo(host, None, type=socket.SOCK_STREAM)
    except socket.gaierror as exc:
        log.debug("dns resolve failed: %s (%s)", host, exc)
        return set()
    return {_strip_zone(info[4][0]) for info in infos}


@dataclass(frozen=True)
class ValidatedUrl:
    """通过校验的目标：连接必须使用这里的 IP，不得再次解析域名。"""

    url: str
    scheme: str
    host: str
    port: int
    ips: Tuple[str, ...]


def _validate(url: str) -> ValidatedUrl:
    """校验 URL 并返回「已校验 IP 列表」，供连接层固定使用。"""
    raw = (url or "").strip()
    if not raw:
        raise UnsafeUrlError("空 URL")

    try:
        p = urlparse(raw)
    except ValueError as exc:
        raise UnsafeUrlError(f"URL 无法解析: {raw!r}") from exc

    scheme = p.scheme.lower()
    if scheme not in ALLOWED_SCHEMES:
        raise UnsafeUrlError(f"不允许的协议: {p.scheme or '(none)'}")
    if p.username or p.password:
        raise UnsafeUrlError("URL 不允许携带用户凭证")

    # 端口白名单：自定义源与正文页只走标准 Web 端口，避免被用来探测内网高位端口服务。
    # p.port 在端口非法（如 :99999、:abc）时抛 ValueError，这里一并按拒绝处理。
    try:
        port = p.port
    except ValueError as exc:
        raise UnsafeUrlError(f"端口不合法: {raw!r}") from exc
    if port is not None and port not in ALLOWED_PORTS:
        raise UnsafeUrlError(f"不允许的端口: {port}")
    port = port if port is not None else (443 if scheme == "https" else 80)

    host = (p.hostname or "").strip().lower().rstrip(".")
    if not host:
        raise UnsafeUrlError("URL 缺少主机名")
    if host in _BLOCKED_HOSTNAMES or host.endswith(_BLOCKED_SUFFIXES):
        raise UnsafeUrlError(f"禁止访问的主机: {host}")

    # 字面量 IP：直接判段
    try:
        literal = ipaddress.ip_address(_strip_zone(host))
    except ValueError:
        literal = None

    if literal is not None:
        if not is_public_ip(str(literal)):
            raise UnsafeUrlError(f"禁止访问的地址: {host}")
        return ValidatedUrl(raw, scheme, host, port, (str(literal),))

    # 域名：解析后所有地址都必须是公网地址（有任一内网结果即拒绝）
    addrs = _resolve(host)
    if not addrs:
        raise UnsafeUrlError(f"域名无法解析: {host}")
    for addr in addrs:
        if not is_public_ip(addr):
            raise UnsafeUrlError(f"域名解析到内网地址: {host} -> {addr}")
    # 排序保证行为可复现；调用方按顺序逐个尝试连接
    return ValidatedUrl(raw, scheme, host, port, tuple(sorted(addrs)))


def check_url(url: str) -> str:
    """校验 URL 是否允许出站；通过返回原 URL，否则抛 UnsafeUrlError。"""
    return _validate(url).url


def is_fetchable(url: str) -> bool:
    """check_url 的布尔版，便于调用方提前短路。"""
    try:
        check_url(url)
        return True
    except UnsafeUrlError as exc:
        log.warning("blocked outbound url: %s (%s)", url, exc)
        return False


class SafeResponse:
    """受限响应对象，接口与 requests.Response 的最小子集兼容。"""

    __slots__ = ("status_code", "headers", "content", "url", "_encoding")

    def __init__(self, status_code: int, headers: Dict[str, str], content: bytes, url: str) -> None:
        self.status_code = status_code
        self.headers = headers
        self.content = content
        self.url = url
        self._encoding = None
        ctype = (headers.get("content-type") or "").lower()
        for part in ctype.split(";"):
            part = part.strip()
            if part.startswith("charset="):
                self._encoding = part.split("=", 1)[1].strip("\"'")

    @property
    def text(self) -> str:
        if self._encoding:
            try:
                return self.content.decode(self._encoding, errors="replace")
            except LookupError:
                pass
        return self.content.decode("utf-8", errors="replace")

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise requests.HTTPError(f"{self.status_code} for url: {self.url}")


class _PeerCheckMixin:
    """连接建立后复核对端 IP，确保真正连上的就是刚校验过的那个地址。

    URL 主机已改写成 IP，理论上不会再解析域名；这里再加一道兜底：若连接层
    （代理、自定义 socket、NAT64 等）把目标改到了别的地址，立即中止请求。
    """

    _expected_ip: str

    def get_connection(self, url: str, proxies: object = None):  # type: ignore[override]
        pool = super().get_connection(url, proxies)  # type: ignore[misc]
        expected = self._expected_ip
        original_new_conn = pool._new_conn

        def new_conn_checked(*args: object, **kwargs: object):
            conn = original_new_conn(*args, **kwargs)
            original_connect = conn.connect

            def connect_checked() -> None:
                original_connect()
                sock = getattr(conn, "sock", None)
                if sock is None:
                    return
                try:
                    peer = sock.getpeername()[0]
                except OSError:
                    return
                if peer != expected:
                    raise requests.ConnectionError(
                        f"连接对端 {peer} 与已校验 IP {expected} 不一致，已中止"
                    )

            conn.connect = connect_checked  # type: ignore[method-assign]
            return conn

        pool._new_conn = new_conn_checked  # type: ignore[method-assign]
        return pool


class _PinnedHTTPSAdapter(_PeerCheckMixin, HTTPAdapter):
    """把 TCP 目标固定到已校验 IP，但 TLS 的 SNI 与证书校验仍针对原始域名。

    requests 默认会根据 URL 再次解析域名，这中间存在「校验时返回公网 IP、
    连接时返回内网 IP」的 DNS 重绑定窗口（TOCTOU）。这里把 URL 主机改写为
    已校验 IP，并让 urllib3 用 server_hostname / assert_hostname 指回原域名，
    既消除二次解析，又保持证书校验强度。
    """

    def __init__(self, server_hostname: str, expected_ip: str, **kwargs: object) -> None:
        self._server_hostname = server_hostname
        self._expected_ip = expected_ip
        super().__init__(**kwargs)

    def init_poolmanager(self, *args: object, **kwargs: object) -> None:
        kwargs["server_hostname"] = self._server_hostname
        kwargs["assert_hostname"] = self._server_hostname
        super().init_poolmanager(*args, **kwargs)  # type: ignore[arg-type]


class _PinnedHTTPAdapter(_PeerCheckMixin, HTTPAdapter):
    """明文 http 版：URL 主机已改写为 IP，其余行为与默认适配器一致。"""

    def __init__(self, expected_ip: str, **kwargs: object) -> None:
        self._expected_ip = expected_ip
        super().__init__(**kwargs)


def _netloc_for_ip(ip: str, port: int, default_port: bool) -> str:
    host = f"[{ip}]" if ":" in ip else ip
    return host if default_port else f"{host}:{port}"


def _fetch_once(
    target: ValidatedUrl,
    ip: str,
    *,
    headers: Optional[Dict[str, str]],
    timeout: int,
    max_bytes: int,
) -> SafeResponse:
    """连到指定 IP 取一次响应；不跟随重定向，响应体截断到 max_bytes。"""
    parsed = urlparse(target.url)
    default_port = (target.scheme == "http" and target.port == 80) or (
        target.scheme == "https" and target.port == 443
    )
    connect_url = urlunparse(
        (
            target.scheme,
            _netloc_for_ip(ip, target.port, default_port),
            parsed.path or "/",
            parsed.params,
            parsed.query,
            "",
        )
    )

    # 连接目标已改成 IP，Host 头必须还原成原始主机名，否则虚拟主机站点会 404。
    host_header = target.host if default_port else f"{target.host}:{target.port}"
    send_headers: Dict[str, str] = {"Host": host_header}
    for key, value in (headers or {}).items():
        if key.lower() != "host":
            send_headers[key] = value

    session = requests.Session()
    # 环境代理会重新解析域名，使 IP 固定失效，因此显式忽略代理配置。
    session.trust_env = False
    adapter: HTTPAdapter = (
        _PinnedHTTPSAdapter(server_hostname=target.host, expected_ip=ip, max_retries=0)
        if target.scheme == "https"
        else _PinnedHTTPAdapter(expected_ip=ip, max_retries=0)
    )
    session.mount(target.scheme + "://", adapter)
    try:
        resp = session.get(
            connect_url, headers=send_headers, timeout=timeout,
            allow_redirects=False, stream=True,
        )
        try:
            chunks: List[bytes] = []
            total = 0
            for chunk in resp.iter_content(8192):
                if not chunk:
                    continue
                chunks.append(chunk)
                total += len(chunk)
                if total >= max_bytes:
                    log.warning("response truncated at %d bytes: %s", total, target.url)
                    break
            return SafeResponse(resp.status_code, dict(resp.headers), b"".join(chunks)[:max_bytes], target.url)
        finally:
            resp.close()
    finally:
        session.close()


def safe_get(
    url: str,
    *,
    headers: Optional[Dict[str, str]] = None,
    timeout: int = 15,
    max_bytes: int = DEFAULT_MAX_BYTES,
    max_redirects: int = MAX_REDIRECTS,
) -> SafeResponse:
    """带 SSRF 校验的 GET。每一跳都校验；连接固定到已校验 IP；超限截断。"""
    target = _validate(url)

    for _ in range(max_redirects + 1):
        resp: Optional[SafeResponse] = None
        last_exc: Optional[Exception] = None
        # 逐 IP 尝试：所有候选都来自本次校验结果，不再触发新的 DNS 查询。
        for ip in target.ips:
            try:
                resp = _fetch_once(
                    target, ip, headers=headers, timeout=timeout, max_bytes=max_bytes,
                )
                break
            except requests.RequestException as exc:
                last_exc = exc
                log.warning("connect failed via %s for %s: %s", ip, target.host, exc)

        if resp is None:
            raise last_exc if last_exc is not None else UnsafeUrlError(f"无法连接: {target.url}")

        location = resp.headers.get("Location") or resp.headers.get("location")
        if resp.status_code in (301, 302, 303, 307, 308) and location:
            target = _validate(urljoin(target.url, location))  # 跳转目标重新校验
            continue
        return resp

    raise UnsafeUrlError(f"重定向次数超过上限 ({max_redirects}): {url}")
