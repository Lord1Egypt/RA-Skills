import socket
import warnings
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

TARGET_PORTS = [18789, 18790, 18792]

def check_port(ip, port, timeout_s):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout_s)
            result = sock.connect_ex((ip, port))
            return port if result == 0 else None
    except Exception:
        return None

def scan_ports(ip, ports, timeout_s=0.5, max_workers=64):
    open_ports = []
    max_workers = min(max_workers, len(ports), 64) if ports else 1
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(check_port, ip, port, timeout_s) for port in ports]
        for future in as_completed(futures):
            port = future.result()
            if port:
                open_ports.append(port)
    return sorted(open_ports)

def _extract_version_from_headers(headers):
    v = headers.get("X-OpenClaw-Version")
    return v

def _extract_version_from_status_json(data):
    if isinstance(data, dict):
        v = data.get("version")
        if isinstance(v, str) and v.strip():
            return v.strip()
    return None

def _looks_like_openclaw_text(text):
    if not text:
        return False
    t = text.lower()
    return "openclaw" in t

def _probe_http(session, base_url, timeout_s, verify):
    try:
        r = session.get(base_url + "/", timeout=timeout_s, verify=verify, allow_redirects=False)
        version = _extract_version_from_headers(r.headers)
        if version:
            return {"version": version, "evidence": "header"}
        if _looks_like_openclaw_text(r.text):
            return {"version": "unknown", "evidence": "body"}
    except requests.RequestException:
        pass

    for p in ("/api/status", "/api/v1/status", "/status"):
        try:
            r = session.get(base_url + p, timeout=timeout_s, verify=verify, allow_redirects=False)
            if not r.ok:
                continue
            version = _extract_version_from_headers(r.headers)
            if version:
                return {"version": version, "evidence": f"header:{p}"}
            try:
                data = r.json()
                v = _extract_version_from_status_json(data)
                if v:
                    return {"version": v, "evidence": f"json:{p}"}
            except ValueError:
                if _looks_like_openclaw_text(r.text):
                    return {"version": "unknown", "evidence": f"text:{p}"}
        except requests.RequestException:
            continue

    return None

def identify_service(ip, port, http_timeout_s=2, insecure=False):
    if insecure:
        warnings.simplefilter("ignore", InsecureRequestWarning)

    with requests.Session() as session:
        session.trust_env = False
        http_url = f"http://{ip}:{port}"
        hit = _probe_http(session, http_url, timeout_s=http_timeout_s, verify=True)
        if hit:
            return {"service": "OpenClaw", "version": hit["version"], "url": http_url, "port": port, "scheme": "http", "evidence": hit["evidence"]}

        https_url = f"https://{ip}:{port}"
        try:
            hit = _probe_http(session, https_url, timeout_s=http_timeout_s, verify=True)
            if hit:
                return {"service": "OpenClaw", "version": hit["version"], "url": https_url, "port": port, "scheme": "https", "evidence": hit["evidence"], "tls_verify": True}
        except requests.exceptions.SSLError:
            hit = None

        if insecure:
            hit = _probe_http(session, https_url, timeout_s=http_timeout_s, verify=False)
            if hit:
                return {"service": "OpenClaw", "version": hit["version"], "url": https_url, "port": port, "scheme": "https", "evidence": hit["evidence"], "tls_verify": False}

    return None

def run_scan(target_ip, ports=None, port_timeout_s=0.5, http_timeout_s=2, max_workers=64, insecure=False):
    ports = ports or TARGET_PORTS
    print(f"[*] Starting scan on {target_ip}...")
    open_ports = scan_ports(target_ip, ports, timeout_s=port_timeout_s, max_workers=max_workers)

    if not open_ports:
        print(f"[-] No open ports found on {target_ip}")
        return {"target": target_ip, "open_ports": [], "services": []}

    print(f"[+] Open ports: {open_ports}")
    services = []
    for port in open_ports:
        service_info = identify_service(target_ip, port, http_timeout_s=http_timeout_s, insecure=insecure)
        if service_info:
            print(f"[+] Service Identified: {service_info['service']} (v{service_info['version']}) on port {port}")
            services.append(service_info)
        else:
            print(f"[-] Unknown service on port {port}")

    return {"target": target_ip, "open_ports": open_ports, "services": services}
