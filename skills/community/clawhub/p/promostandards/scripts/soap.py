"""SOAP transport for PromoStandards services.

**Design choice: envelopes are hand-built, not generated from WSDL.**

PromoStandards services are overwhelmingly .NET-generated and historically
fragile against WSDL client libraries — several publish WSDLs that import
schemas over dead links, disagree with what the service actually accepts,
or are served as malformed archives (the Inventory 1.2.1 package is a zip
`unzip` refuses to open). A WSDL client also means fetching and parsing a
remote document at call time, which turns a supplier's slow web server
into our latency and their broken import into our outage.

Building the envelope by hand costs a few lines per operation and buys
predictability: the bytes on the wire are exactly what the adapter says,
they are diffable in a fixture, and a supplier's broken WSDL cannot break
a call that never reads it. This mirrors the approach already proven in
BaconCo's `utils/sanmar.py`.

The complementary rule, and the reason parsing is separate from building:
**requests are strict, responses are lenient.** Requests are built with the
exact namespaces each version's schema declares. Responses are searched by
*local name*, ignoring namespace URIs entirely, because suppliers routinely
return subtly wrong namespaces and a strict parse would reject data that is
otherwise perfectly readable.
"""

from __future__ import annotations

import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET

from errors import SoapFaultError, TransportError  # noqa: E402

SOAP_ENV = "http://schemas.xmlsoap.org/soap/envelope/"

DEFAULT_TIMEOUT = 60
DEFAULT_RETRIES = 3
RETRY_BACKOFF = 2.0


# ---------------------------------------------------------------------------
# minimal transport, injectable for tests
# ---------------------------------------------------------------------------

class _Response:
    __slots__ = ("text", "status_code")

    def __init__(self, text: str, status_code: int) -> None:
        self.text = text
        self.status_code = status_code

    @property
    def ok(self) -> bool:
        return 200 <= self.status_code < 300


class UrllibSession:
    """Stdlib-backed stand-in for a `requests` session.

    Keeping the `.post(url, data=, headers=, timeout=)` signature means the
    offline tests can swap in a fake session that returns canned XML, the
    same idiom the neighbouring skills use.
    """

    def post(self, url: str, data: bytes | str, headers: dict,
             timeout: int = DEFAULT_TIMEOUT) -> _Response:
        payload = data.encode("utf-8") if isinstance(data, str) else data
        req = urllib.request.Request(url, data=payload, headers=headers,
                                     method="POST")
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body = resp.read().decode("utf-8", errors="replace")
                return _Response(body, resp.status)
        except urllib.error.HTTPError as exc:
            # SOAP faults arrive as HTTP 500 with a body worth parsing.
            body = exc.read().decode("utf-8", errors="replace")
            return _Response(body, exc.code)


# ---------------------------------------------------------------------------
# envelope construction
# ---------------------------------------------------------------------------

def build_envelope(body_xml: str, *, namespaces: dict[str, str]) -> str:
    """Wrap `body_xml` in a SOAP 1.1 envelope declaring `namespaces`.

    `body_xml` is expected to already use the prefixes declared here; the
    adapters own both, so they stay in step.
    """
    decls = " ".join(f'xmlns:{prefix}="{uri}"'
                     for prefix, uri in namespaces.items())
    return (
        '<?xml version="1.0" encoding="utf-8"?>'
        f'<soapenv:Envelope xmlns:soapenv="{SOAP_ENV}" {decls}>'
        "<soapenv:Header/>"
        f"<soapenv:Body>{body_xml}</soapenv:Body>"
        "</soapenv:Envelope>"
    )


def element(tag: str, text: object = None) -> str:
    """Render one element, or the empty string when `text` is absent.

    Omitting rather than emitting an empty element is deliberate: for a
    `minOccurs="0"` field, `<password/>` and no `password` element are
    different requests, and some suppliers reject the former.
    """
    if text is None or text == "":
        return ""
    escaped = (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
    return f"<{tag}>{escaped}</{tag}>"


# ---------------------------------------------------------------------------
# response navigation (namespace-agnostic)
# ---------------------------------------------------------------------------

def local(tag: str) -> str:
    """Strip any `{namespace}` prefix from an ElementTree tag."""
    return tag.rsplit("}", 1)[-1] if "}" in tag else tag


def find(node: ET.Element | None, *names: str) -> ET.Element | None:
    """Depth-first search for the first descendant with any of `names`.

    Matching is on local name only — see the module docstring.
    """
    if node is None:
        return None
    wanted = {n.lower() for n in names}
    if local(node.tag).lower() in wanted:
        return node
    for child in node.iter():
        if local(child.tag).lower() in wanted:
            return child
    return None


def find_all(node: ET.Element | None, *names: str) -> list[ET.Element]:
    if node is None:
        return []
    wanted = {n.lower() for n in names}
    return [c for c in node.iter() if local(c.tag).lower() in wanted]


def children(node: ET.Element | None, *names: str) -> list[ET.Element]:
    """All *direct* children matching a local name.

    Necessary wherever a name repeats at more than one level: `description`
    appears both on a Product and on each of its Parts, so a descendant
    search would fold the parts' descriptions into the product's.
    """
    if node is None:
        return []
    wanted = {n.lower() for n in names}
    return [c for c in node if local(c.tag).lower() in wanted]


def child(node: ET.Element | None, *names: str) -> ET.Element | None:
    """Find a *direct* child by local name.

    Preferred over `find` when a name repeats at several depths — e.g.
    `partId` appears both on a part and inside nested arrays.
    """
    if node is None:
        return None
    wanted = {n.lower() for n in names}
    for c in node:
        if local(c.tag).lower() in wanted:
            return c
    return None


def text(node: ET.Element | None, *names: str) -> str | None:
    """Text of the first matching descendant, or None when absent/blank."""
    found = child(node, *names) or find(node, *names)
    if found is None or found.text is None:
        return None
    stripped = found.text.strip()
    return stripped or None


def number(node: ET.Element | None, *names: str) -> float | None:
    """Parse a numeric field, returning None rather than guessing.

    A value that will not parse is treated as absent: it is never coerced
    to 0, which for inventory would turn "unreadable" into "out of stock".
    """
    raw = text(node, *names)
    if raw is None:
        return None
    try:
        return float(raw.replace(",", ""))
    except ValueError:
        return None


def integer(node: ET.Element | None, *names: str) -> int | None:
    value = number(node, *names)
    return int(value) if value is not None else None


def boolean(node: ET.Element | None, *names: str) -> bool | None:
    raw = text(node, *names)
    if raw is None:
        return None
    lowered = raw.strip().lower()
    if lowered in ("true", "1", "yes", "y"):
        return True
    if lowered in ("false", "0", "no", "n"):
        return False
    return None


# ---------------------------------------------------------------------------
# client
# ---------------------------------------------------------------------------

class SoapClient:
    """Posts SOAP envelopes and returns parsed roots.

    Retries are opt-in per call via `idempotent`. Read operations retry on
    transport failure; `sendPO` does not, because a retried write can place
    a duplicate order — a request that timed out may still have been
    received.
    """

    def __init__(self, session: object | None = None, *,
                 timeout: int = DEFAULT_TIMEOUT,
                 retries: int = DEFAULT_RETRIES) -> None:
        self.session = session or UrllibSession()
        self.timeout = timeout
        self.retries = retries

    def call(self, url: str, soap_action: str, envelope: str, *,
             idempotent: bool = True) -> ET.Element:
        headers = {
            "Content-Type": "text/xml; charset=utf-8",
            "SOAPAction": soap_action,
            "Accept": "text/xml, application/soap+xml",
        }
        attempts = self.retries if idempotent else 1
        last: Exception | None = None

        for attempt in range(attempts):
            try:
                resp = self.session.post(url, data=envelope, headers=headers,
                                         timeout=self.timeout)
            except Exception as exc:  # noqa: BLE001 - transport is broad
                last = exc
                if attempt < attempts - 1:
                    time.sleep(RETRY_BACKOFF * (2**attempt))
                    continue
                raise TransportError(
                    f"request to {url} failed: {exc}", url=url
                ) from exc

            body = getattr(resp, "text", "") or ""
            status = getattr(resp, "status_code", 0)

            try:
                root = ET.fromstring(body)
            except ET.ParseError as exc:
                # A non-XML body on a bad status is an endpoint problem; on
                # a good status it is a broken service. Both are transport
                # level, and the snippet is truncated to keep any echoed
                # credentials out of logs.
                if status >= 500 and attempt < attempts - 1:
                    last = exc
                    time.sleep(RETRY_BACKOFF * (2**attempt))
                    continue
                raise TransportError(
                    f"non-XML response (HTTP {status}) from {url}: "
                    f"{body[:200]!r}",
                    status=status, url=url,
                ) from exc

            fault = find(root, "Fault")
            if fault is not None:
                raise SoapFaultError(
                    text(fault, "faultstring", "Reason", "Text")
                    or f"SOAP fault from {url}",
                    code=text(fault, "faultcode", "Code", "Value"),
                    detail=text(fault, "detail", "Detail"),
                )

            if status >= 400:
                raise TransportError(
                    f"HTTP {status} from {url}", status=status, url=url
                )
            return root

        raise TransportError(f"request to {url} failed: {last}", url=url)
