"""
Business Info Scraper - Extract business details from a website URL.
Uses only stdlib (urllib) + html.parser - no beautifulsoup required.

Usage:
    python scrape_business.py <website_url>

Security:
  - Scheme validation (http/https only)
  - DNS resolution + private-IP blocking (blocks localhost, private,
    loopback, link-local, multicast, and reserved ranges)
  - No redirects followed to untrusted hosts
  - No internal/private network addresses accepted
"""

import urllib.request
import urllib.parse
import socket
import ssl
import re
import sys
import html.parser
import ipaddress

class BusinessInfoParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.meta_description = ""
        self.h1_tags = []
        self.current_tag = None
        self.current_text = ""
        self.all_text = []
        self.in_title = False
        self.in_meta_desc = False
        self.in_h1 = False
        self.in_head = False

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "title":
            self.in_title = True
        elif tag == "meta":
            name = attrs_dict.get("name", "").lower()
            if name == "description":
                self.in_meta_desc = True
                self.meta_description = attrs_dict.get("content", "")
        elif tag == "h1":
            self.in_h1 = True
            self.current_text = ""
        elif tag in ("p", "span", "div", "header", "section"):
            self.current_text = ""

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        elif tag == "h1":
            if self.current_text.strip():
                self.h1_tags.append(self.current_text.strip())
            self.in_h1 = False
        elif tag in ("p", "span", "div", "header", "section"):
            if self.current_text.strip():
                self.all_text.append(self.current_text.strip())
            self.current_text = ""

    def handle_data(self, data):
        data = data.strip()
        if not data:
            return
        if self.in_title:
            self.title = data
        elif self.in_h1:
            self.current_text += " " + data
        elif self.in_meta_desc:
            pass  # already captured in attribute

def _is_public_host(hostname):
    """
    Resolve hostname via DNS and verify ALL returned IPs are public.
    Returns False if any IP falls in private/loopback/link-local/reserved/multicast range.
    """
    try:
        infos = socket.getaddrinfo(hostname, None)
        for info in infos:
            ip_str = info[4][0]
            ip = ipaddress.ip_address(ip_str)
            if (ip.is_private or ip.is_loopback or ip.is_link_local
                    or ip.is_reserved or ip.is_multicast):
                return False
        return True
    except Exception:
        return False


def scrape_business_info(url):
    """
    Scrape a website and extract business-relevant information.
    Returns a dict with: name, tagline, description, services, contact
    """
    # Normalize URL
    url = url.strip()
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    # --- SSRF protection ---
    parsed = urllib.parse.urlparse(url)

    # 1. Scheme block
    if parsed.scheme not in ("http", "https"):
        return {"error": "Only http and https URLs are allowed.", "url": url}

    hostname = parsed.hostname
    if not hostname:
        return {"error": "Could not determine hostname.", "url": url}

    # 2. Block obvious localhost / internal hostnames
    blocked_names = ("localhost", "127.0.0.1", "0.0.0.0", "::1", "[::1]",
                     "internal", "intranet", "private", "local", "home",
                     "router", "gateway", "bind")
    if hostname.lower() in blocked_names or any(hostname.lower().endswith(p) for p in blocked_names):
        return {"error": f"Internal or reserved hostname blocked ({hostname}).", "url": url}

    # 3. DNS resolution — block if ANY resolved IP is non-public
    if not _is_public_host(hostname):
        return {"error": f"Hostname resolves to a private/internal IP ({hostname}).", "url": url}

class _NoRedirect(urllib.request.HTTPRedirectHandler):
    """Strict redirect blocker — prevents following any redirect to any host."""
    def redirect_request(self, req, fp, code, msg, hdrs, newurl):
        return None  # Block all redirects

    def http_response(self, request, response):
        return response

    https_response = http_response


def scrape_business_info(url):
    """
    Scrape a website and extract business-relevant information.
    Returns a dict with: name, tagline, description, services, contact
    """
    # Normalize URL
    url = url.strip()
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    # --- SSRF protection ---
    parsed = urllib.parse.urlparse(url)

    # 1. Scheme block
    if parsed.scheme not in ("http", "https"):
        return {"error": "Only http and https URLs are allowed.", "url": url}

    hostname = parsed.hostname
    if not hostname:
        return {"error": "Could not determine hostname.", "url": url}

    # 2. Block obvious localhost / internal hostnames
    blocked_names = ("localhost", "127.0.0.1", "0.0.0.0", "::1", "[::1]",
                     "internal", "intranet", "private", "local", "home",
                     "router", "gateway", "bind")
    if hostname.lower() in blocked_names or any(hostname.lower().endswith(p) for p in blocked_names):
        return {"error": f"Internal or reserved hostname blocked ({hostname}).", "url": url}

    # 3. DNS resolution — block if ANY resolved IP is non-public
    if not _is_public_host(hostname):
        return {"error": f"Hostname resolves to a private/internal IP ({hostname}).", "url": url}

    # 4. HTTPS + SSL + NO REDIRECTS
    ctx = ssl.create_default_context()
    ctx.check_hostname = True
    ctx.verify_mode = ssl.CERT_REQUIRED

    opener = urllib.request.build_opener(_NoRedirect)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        response = opener.open(req, timeout=15, context=ctx)
        status = response.getcode()
        if 300 <= status < 400:
            return {"error": f"Redirect blocked — server responded with HTTP {status}. "
                               "Only direct HTTP responses are allowed.", "url": url}
        html_content = response.read().decode("utf-8", errors="ignore")
    except urllib.error.HTTPError as e:
        if 300 <= e.code < 400:
            loc = e.headers.get("Location", "")
            return {"error": f"Redirect blocked to {loc!r}. Only direct responses allowed.", "url": url}
        return {"error": f"HTTP error {e.code}: {e.reason}", "url": url}
    except ssl.SSLCertVerificationError as e:
        return {"error": f"SSL certificate error for {hostname} — {e}", "url": url}
    except Exception as e:
        return {"error": str(e), "url": url}

    # Parse HTML
    parser = BusinessInfoParser()
    try:
        parser.feed(html_content)
    except Exception:
        pass

    # Extract title as business name
    name = parser.title.split("|")[0].split("-")[0].split("—")[0].strip()

    # Meta description
    description = parser.meta_description.strip()

    # H1 tags as tagline or services
    h1_text = " | ".join(parser.h1_tags[:3])

    # Find service-like text from paragraphs
    service_keywords = ["services", "we offer", "our courses", "what we do", "solutions", "products"]
    services = []
    for para in parser.all_text:
        para_lower = para.lower()
        if any(kw in para_lower for kw in service_keywords):
            services.append(para[:200])
            if len(services) >= 4:
                break

    # Contact info (simple regex patterns)
    email_match = re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", html_content)
    phone_match = re.search(r"(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", html_content)

    result = {
        "url": url,
        "name": name[:100] if name else None,
        "tagline": h1_text[:200] if h1_text else None,
        "description": description[:300] if description else None,
        "services": services,
        "email": email_match.group(0) if email_match else None,
        "phone": phone_match.group(0) if phone_match else None,
    }

    return result

def print_report(data):
    print("\n=== BUSINESS INFO EXTRACTED ===")
    print(f"URL: {data.get('url')}")
    print(f"Name: {data.get('name', 'N/A')}")
    print(f"Tagline: {data.get('tagline', 'N/A')}")
    print(f"Description: {data.get('description', 'N/A')}")
    print(f"Services found: {len(data.get('services', []))}")
    for i, s in enumerate(data.get('services', []), 1):
        print(f"  {i}. {s[:100]}...")
    print(f"Email: {data.get('email', 'N/A')}")
    print(f"Phone: {data.get('phone', 'N/A')}")
    if "error" in data:
        print(f"ERROR: {data['error']}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scrape_business.py <website_url>")
        print("Example: python scrape_business.py https://www.caddeskcentre.com")
        sys.exit(1)

    url = sys.argv[1]
    data = scrape_business_info(url)
    print_report(data)
