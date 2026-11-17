"""Submit public site URLs to the official IndexNow endpoint."""

import argparse
import ipaddress
import json
from pathlib import Path
import re
import secrets
import socket
import subprocess
import sys
import tempfile
from urllib.parse import urlencode, urlsplit, urlunsplit
from xml.etree import ElementTree


INDEXNOW_API = "https://api.indexnow.org/indexnow"
KEY_FILE = Path(".indexnow-key")
PUBLIC_DIR = Path("public")
DEFAULT_SITEMAP = PUBLIC_DIR / "sitemap.xml"
SITEMAP_NAMESPACE = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
MAX_SITEMAP_BYTES = 50 * 1024 * 1024
MAX_BATCH_SIZE = 10_000
HOSTNAME = re.compile(
    r"(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z](?:[a-z0-9-]{0,61}[a-z0-9])?"
)
PRIVATE_SUFFIXES = (".localhost", ".local", ".internal", ".test", ".invalid")
KEY = re.compile(r"[A-Za-z0-9-]{8,128}")
PUBLIC_IPV6 = ipaddress.ip_network("2000::/3")
# Azure routes this public-looking address to a platform service inside the virtual network.
AZURE_PLATFORM_IP = ipaddress.ip_address("168.63.129.16")
TRANSITION_IPV6 = (ipaddress.ip_network("2001::/32"), ipaddress.ip_network("2002::/16"))
CURL = (
    "curl", "--disable", "--globoff", "--noproxy", "*", "--proto", "=https",
    "--connect-timeout", "5", "--max-time", "30", "--silent", "--show-error",
)


def verification_file(key):
    directory = PUBLIC_DIR if PUBLIC_DIR.is_dir() else Path(".")
    return directory / f"{key}.txt"


def read_key():
    if not KEY_FILE.is_file():
        raise ValueError("No IndexNow key found. Run generate-key to set one up.")
    key = KEY_FILE.read_text(encoding="utf-8").strip()
    if not KEY.fullmatch(key):
        raise ValueError("The IndexNow key file must contain 8 to 128 letters, digits, or hyphens.")
    return key


def generate_key():
    if KEY_FILE.exists() and input("Replace the current IndexNow key? [y/N] ").lower() not in ("y", "yes"):
        print("Kept the current IndexNow key.")
        return

    key = secrets.token_hex(16)
    path = verification_file(key)
    with path.open("x", encoding="utf-8") as file:
        file.write(key + "\n")
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=".", delete=False) as file:
            staged_key = Path(file.name)
        try:
            staged_key.write_text(key + "\n", encoding="utf-8")
            staged_key.replace(KEY_FILE)
        finally:
            staged_key.unlink(missing_ok=True)
    except OSError:
        path.unlink()
        raise
    print(f"Created {KEY_FILE} and {path}. Serve the verification file at the site root before submitting.")


def parse_url(url, *, sitemap=False):
    if re.search(r"[\x00-\x20\x7f\\]", url):
        raise ValueError("URLs must not contain whitespace, control characters, or backslashes.")
    parsed = urlsplit(url)
    schemes = ("https",) if sitemap else ("http", "https")
    if parsed.scheme not in schemes or not parsed.hostname or parsed.username is not None or parsed.fragment:
        raise ValueError("Use an absolute public URL without credentials or a fragment. Remote sitemaps require HTTPS.")
    host = parsed.hostname.encode("idna").decode("ascii")
    if not HOSTNAME.fullmatch(host) or len(host) > 253 or host.endswith(PRIVATE_SUFFIXES):
        raise ValueError("Use a public DNS hostname.")
    port = 443 if parsed.scheme == "https" else 80
    if parsed.port not in (None, port):
        raise ValueError("Use the standard port for the URL scheme.")
    normalized = urlunsplit((parsed.scheme, host, parsed.path or "/", parsed.query, ""))
    return host, normalized


def resolve_public_addresses(host):
    addresses = dict.fromkeys(
        ipaddress.ip_address(record[4][0])
        for record in socket.getaddrinfo(f"{host}.", 443, type=socket.SOCK_STREAM)
    )
    if not addresses:
        raise ValueError("The sitemap hostname has no usable DNS addresses.")
    for address in addresses:
        if not address.is_global or address.is_multicast or address.is_reserved or address == AZURE_PLATFORM_IP:
            raise ValueError("The sitemap hostname resolves to a non-public address.")
        if address.version == 6 and (
            address not in PUBLIC_IPV6 or any(address in network for network in TRANSITION_IPV6)
        ):
            raise ValueError("The sitemap hostname resolves to an unsupported IPv6 address.")
    return ",".join(f"[{address}]" if address.version == 6 else str(address) for address in addresses)


def fetch_sitemap(host, url):
    addresses = resolve_public_addresses(host)
    # Pin the connection to the checked results while preserving the TLS hostname.
    # Curl starts without user configuration, proxies, or redirect following.
    command = [
        *CURL, "--resolve", f"{host}:443:{addresses}", "--max-redirs", "0",
        "--max-filesize", str(MAX_SITEMAP_BYTES), "--write-out", "\n%{http_code}",
        "--", url,
    ]
    with subprocess.Popen(command, stdout=subprocess.PIPE) as process:
        response = process.stdout.read(MAX_SITEMAP_BYTES + 5)
        if len(response) > MAX_SITEMAP_BYTES + 4:
            process.kill()
            raise ValueError("The sitemap exceeds the 50 MiB size limit.")
        if process.wait():
            raise ValueError("Could not download the sitemap within the connection and size limits.")

    data, _, status = response.rpartition(b"\n")
    if status != b"200":
        raise ValueError("The sitemap must return HTTP 200 directly. Use its final public HTTPS URL.")
    return data


class SitemapTreeBuilder(ElementTree.TreeBuilder):
    def doctype(self, name, public_id, system_id):
        raise ValueError("Sitemap XML must not contain a document type declaration.")


def sitemap_urls(data):
    if len(data) > MAX_SITEMAP_BYTES:
        raise ValueError("The sitemap exceeds the 50 MiB size limit.")
    parser = ElementTree.XMLParser(target=SitemapTreeBuilder())
    root = ElementTree.fromstring(data, parser=parser)
    if root.tag not in ("urlset", SITEMAP_NAMESPACE + "urlset"):
        raise ValueError("Provide a URL sitemap (urlset). For a sitemap index, select a child sitemap.")
    namespace = SITEMAP_NAMESPACE if root.tag.startswith("{") else ""
    return [node.text.strip() if node.text else "" for node in root.findall(f"{namespace}url/{namespace}loc")]


def prepare_submission(urls, expected_host=None):
    if not urls:
        raise ValueError("Provide at least one page URL.")
    parsed = [parse_url(url) for url in urls]
    host = expected_host or parsed[0][0]
    if any(url_host != host for url_host, _ in parsed):
        raise ValueError("All page URLs must match the submission hostname.")
    return host, [url for _, url in parsed]


def submit_request(key, host, urls, *, single=False):
    args = [*CURL, "--output", "/dev/null", "--write-out", "%{http_code}"]
    if single:
        query = urlencode({"url": urls[0], "key": key})
        args.extend(["--", f"{INDEXNOW_API}?{query}"])
        body = b""
    else:
        body = json.dumps({
            "host": host,
            "key": key,
            "keyLocation": f"https://{host}/{key}.txt",
            "urlList": urls,
        }).encode("utf-8")
        args.extend([
            "--header", "Content-Type: application/json; charset=utf-8",
            "--data-binary", "@-", "--", INDEXNOW_API,
        ])

    result = subprocess.run(args, input=body, capture_output=True, check=True)
    status = result.stdout.decode("ascii")
    if status not in ("200", "202"):
        raise ValueError(f"IndexNow returned HTTP {status} for the current batch.")
    message = "received" if status == "200" else "received and pending key verification"
    print(f"HTTP {status} ({message}): {len(urls)} URL(s) for {host}")


def submit(args):
    key = read_key()
    expected_host = None
    if args.command == "submit":
        urls = args.urls
    elif args.command == "submit-sitemap":
        with Path(args.path).open("rb") as file:
            urls = sitemap_urls(file.read(MAX_SITEMAP_BYTES + 1))
    else:
        expected_host, url = parse_url(args.url, sitemap=True)
        urls = sitemap_urls(fetch_sitemap(expected_host, url))

    host, urls = prepare_submission(urls, expected_host)
    single = args.command == "submit" and len(urls) == 1
    for offset in range(0, len(urls), MAX_BATCH_SIZE):
        submit_request(key, host, urls[offset:offset + MAX_BATCH_SIZE], single=single)


def status():
    if KEY_FILE.is_file():
        key = read_key()
        path = verification_file(key)
        verified = path.is_file() and path.read_text(encoding="utf-8").strip() == key
        print("IndexNow key configured.")
        print("Local verification file matches the key." if verified else "Local verification file is missing or does not match.")
    else:
        print("No IndexNow key configured. Run generate-key to set one up.")
    print("Default sitemap found." if DEFAULT_SITEMAP.is_file() else "No public/sitemap.xml found.")


def main():
    parser = argparse.ArgumentParser(prog="indexnow.sh", description=__doc__)
    commands = parser.add_subparsers(dest="command", metavar="command")
    commands.add_parser("generate-key", help="Create an IndexNow key and a local verification file.")
    commands.add_parser("status", help="Show the local key, verification file, and sitemap status.")
    commands.add_parser("submit", help="Submit one or more public URLs.").add_argument("urls", nargs="+")
    local = commands.add_parser("submit-sitemap", help="Submit URLs from a local sitemap.")
    local.add_argument("path", nargs="?", default=DEFAULT_SITEMAP)
    remote = commands.add_parser("submit-sitemap-url", help="Submit URLs from a public HTTPS sitemap.")
    remote.add_argument("url")

    args = parser.parse_args()
    try:
        if args.command is None:
            parser.print_help()
        elif args.command == "generate-key":
            generate_key()
        elif args.command == "status":
            status()
        else:
            submit(args)
    except subprocess.CalledProcessError:
        print("Error: could not reach the IndexNow endpoint.", file=sys.stderr)
        return 1
    except (OSError, ValueError, EOFError, ElementTree.ParseError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
