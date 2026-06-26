import sys
import json
import re
import socket
from urllib.parse import urlparse, urljoin
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

# Blocked IP patterns (SSRF protection)
BLOCKED_IP_PATTERNS = [
    re.compile(r"^10\."),                           # 10.0.0.0/8
    re.compile(r"^172\.(1[6-9]|2[0-9]|3[0-1])\."), # 172.16.0.0/12
    re.compile(r"^192\.168\."),                     # 192.168.0.0/16
    re.compile(r"^169\.254\."),                     # 169.254.0.0/16 (link-local)
    re.compile(r"^127\."),                          # 127.0.0.0/8 (loopback)
    re.compile(r"^localhost$", re.IGNORECASE),    # localhost
]

# Blocked hostnames
BLOCKED_HOSTNAMES = {"localhost", "0.0.0.0", "::1"}


def is_internal_host(host: str) -> bool:
    """Check if host is an internal/reserved address."""
    if host.lower() in BLOCKED_HOSTNAMES:
        return True
    for pattern in BLOCKED_IP_PATTERNS:
        if pattern.match(host):
            return True
    # Try reverse DNS to detect internal IPs
    try:
        resolved = socket.gethostbyname(host)
        for pattern in BLOCKED_IP_PATTERNS:
            if pattern.match(resolved):
                return True
    except (socket.gaierror, socket.herror):
        pass
    return False


def sniff_llms_txt(url):
    parsed = urlparse(url)
    domain = f"{parsed.scheme}://{parsed.netloc}"
    host = parsed.netloc

    # SSRF check
    if is_internal_host(host):
        return {"target_url": url, "found_index": None, "type": None, "error": "Internal hosts blocked (SSRF protection)"}

    # 1. Infer common doc root paths
    url_with_slash = url if url.endswith('/') else url + '/'
    paths_to_try = [url_with_slash]
    path_parts = parsed.path.strip('/').split('/')
    for i in range(len(path_parts)):
        sub_path = '/' + '/'.join(path_parts[:i+1]) + '/'
        paths_to_try.append(urljoin(domain, sub_path))
        paths_to_try.append(domain + '/')

    roots = list(dict.fromkeys(paths_to_try))
    results = {"target_url": url, "found_index": None, "type": None, "content_preview": ""}

    # 2. Probe for llms.txt
    for root in roots:
        for filename in ["llms.txt", "llms-full.txt"]:
            probe_url = urljoin(root, filename)
            try:
                response = urlopen(probe_url, timeout=5)
                if response.status == 200:
                    content = response.read().decode('utf-8', errors='ignore')
                    if "# " in content or "- [" in content:
                        results["found_index"] = probe_url
                        results["type"] = "llms.txt"
                        results["content_preview"] = content[:2000]
                        return results
            except (URLError, HTTPError):
                continue

    # 3. Fallback to Sitemap
    for root in roots:
        sitemap_url = urljoin(root, "sitemap.xml")
        try:
            response = urlopen(sitemap_url, timeout=5)
            if response.status == 200:
                results["found_index"] = sitemap_url
                results["type"] = "sitemap.xml"
                results["content_preview"] = "Sitemap found."
                return results
        except (URLError, HTTPError):
            continue

    return results


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No URL provided"}))
        sys.exit(1)
    target_url = sys.argv[1]
    print(json.dumps(sniff_llms_txt(target_url), indent=2, ensure_ascii=False))
