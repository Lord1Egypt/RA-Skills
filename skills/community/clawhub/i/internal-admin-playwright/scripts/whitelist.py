from urllib.parse import urlparse


def host_allowed(host: str, allowed_hosts: list[str], allowed_suffixes: list[str]) -> bool:
    host = (host or "").lower()
    if host in {h.lower() for h in allowed_hosts}:
        return True
    for s in allowed_suffixes:
        s = s.lower()
        if host.endswith(s):
            return True
    return False


def enforce_route(route, allowed_hosts: list[str], allowed_suffixes: list[str]):
    url = route.request.url
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        return route.abort()

    # 只拦截页面导航请求（document），静态资源全部放行
    # 避免拦截 JS/CSS/字体等外部资源导致页面功能异常
    resource_type = route.request.resource_type
    if resource_type != "document":
        return route.continue_()

    if host_allowed(parsed.hostname or "", allowed_hosts, allowed_suffixes):
        return route.continue_()

    return route.abort()
