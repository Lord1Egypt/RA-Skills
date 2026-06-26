"""
Nextcloud contacts (CardDAV) operations.
Supports CRUD + search via CardDAV protocol using vCard format.
"""

from __future__ import annotations

import argparse
import io
import json
import os
import re
import sys
import urllib.parse
from defusedxml import ElementTree as ET
from typing import Any, Dict, List, Optional, Tuple

try:
    import requests
    from requests.auth import HTTPBasicAuth
    from requests.exceptions import RequestException
except ImportError as exc:
    raise ImportError(
        "'requests' library required. Install with: pip install requests"
    ) from exc


# ── Config / helpers ─────────────────────────────────────────────

DEFAULT_TIMEOUT = 30
CARDDAV_SUCCESS_CODES = {200, 201, 204, 207}


def _confirm_or_die(action_desc: str, auto_approved: bool = False) -> None:
    """Prompt for confirmation before a destructive operation.

    Bypassed when auto_approved is True (e.g., via per-command --yes).
    There is no session-wide or environment bypass.
    Exits with code 2 on non-confirmation.
    """
    if auto_approved:
        return

    if not sys.stdin.isatty():
        print(
            json.dumps({
                "ok": False,
                "error": (
                    f"Confirmation required: {action_desc}. "
                    "Re-run with --yes to confirm this single operation."
                ),
            }),
            file=sys.stderr,
        )
        sys.exit(2)

    try:
        answer = input(f"⚠️  {action_desc} [y/N]: ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        print("", file=sys.stderr)
        sys.exit(2)

    if answer not in ("y", "yes"):
        print("Aborted.", file=sys.stderr)
        sys.exit(2)


def _get_env_config() -> tuple[str, str, str]:
    """Get Nextcloud config from environment variables."""
    url = os.environ.get("NEXTCLOUD_URL", "")
    user = os.environ.get("NEXTCLOUD_USERNAME", "")
    token = os.environ.get("NEXTCLOUD_APP_PASSWORD", "")

    if not url or not user or not token:
        print(
            json.dumps({
                "ok": False,
                "error": "Nextcloud not configured. Set NEXTCLOUD_URL, NEXTCLOUD_USERNAME, NEXTCLOUD_APP_PASSWORD.",
            }),
            file=sys.stderr,
        )
        sys.exit(3)

    return url.rstrip("/"), user, token


def _auth() -> HTTPBasicAuth:
    """Create HTTP Basic Auth for Nextcloud."""
    _, user, token = _get_env_config()
    return HTTPBasicAuth(user, token)


# Module-level cache for DAV principal (avoids PROPFIND per request)
_DAV_PRINCIPAL_CACHE: Optional[str] = None


def _dav_base_path(user: str) -> str:
    """Build the CardDAV base path for the user."""
    return f"remote.php/dav/addressbooks/users/{urllib.parse.quote(user)}"


def _resolve_principal(base_url: str) -> Optional[str]:
    """Discover the DAV principal name from the server.

    Nextcloud may use a different identifier (e.g. a GUID) than the login
    username, so we PROPFIND the root to get current-user-principal.
    Result is cached in _DAV_PRINCIPAL_CACHE.
    """
    global _DAV_PRINCIPAL_CACHE

    if _DAV_PRINCIPAL_CACHE is not None:
        return _DAV_PRINCIPAL_CACHE

    ns = {"d": "DAV:"}
    body = """<?xml version="1.0" encoding="utf-8"?>
<d:propfind xmlns:d="DAV:">
    <d:prop>
        <d:current-user-principal/>
    </d:prop>
</d:propfind>"""
    try:
        resp = requests.request(
            "PROPFIND",
            f"{base_url}/remote.php/dav/",
            auth=_auth(),
            headers={"Depth": "0"},
            data=body,
            timeout=DEFAULT_TIMEOUT,
        )
        if resp.status_code not in CARDDAV_SUCCESS_CODES:
            return None
        root = ET.fromstring(resp.content)
        href = root.find(".//d:current-user-principal/d:href", ns)
        if href is not None and href.text:
            principal = href.text.strip("/").split("/")[-1]
            _DAV_PRINCIPAL_CACHE = principal
            return principal
        return None
    except (RequestException, ET.ParseError):
        return None


def _dav_base() -> str:
    """Get the CardDAV base path using auto-discovered principal."""
    base_url, user, _ = _get_env_config()
    principal = _resolve_principal(base_url)
    if not principal:
        principal = user
    return _dav_base_path(principal)


def _list_addressbooks_raw(base_url: str, dav_path: str) -> Optional[ET.Element]:
    """PROPFIND to list addressbooks (CardDAV collections)."""
    url = f"{base_url}/{dav_path}/"
    headers = {"Depth": "1"}
    body = """<?xml version="1.0" encoding="utf-8"?>
<d:propfind xmlns:d="DAV:" xmlns:card="urn:ietf:params:xml:ns:carddav">
    <d:prop>
        <d:displayname/>
        <d:resourcetype/>
        <card:addressbook-description/>
    </d:prop>
</d:propfind>"""
    try:
        resp = requests.request(
            "PROPFIND",
            url,
            auth=_auth(),
            headers=headers,
            data=body,
            timeout=DEFAULT_TIMEOUT,
        )
        if resp.status_code in CARDDAV_SUCCESS_CODES:
            return ET.fromstring(resp.content)
        return None
    except (RequestException, ET.ParseError):
        return None


def list_addressbooks() -> List[Dict[str, str]]:
    """List available CardDAV addressbooks."""
    base_url, user, _ = _get_env_config()
    dav_base = _dav_base()
    ns = {
        "d": "DAV:",
        "card": "urn:ietf:params:xml:ns:carddav",
    }

    root = _list_addressbooks_raw(base_url, dav_base)
    if root is None:
        return []

    books = []
    for response in root.findall(".//d:response", ns):
        href_el = response.find("d:href", ns)
        props = response.find("d:propstat/d:prop", ns)
        if props is None:
            continue

        # Only include addressbook collections
        rtype = props.find("d:resourcetype", ns)
        if rtype is None or rtype.find("card:addressbook", ns) is None:
            continue

        display = props.find("d:displayname", ns)
        desc = props.find("card:addressbook-description", ns)
        books.append({
            "href": href_el.text if href_el is not None else "",
            "displayname": display.text if display is not None else "",
            "description": desc.text if desc is not None else "",
        })

    return books


def _resolve_default_addressbook(base_url: str, dav_base: str) -> Optional[str]:
    """Return the href of the first addressbook, or None."""
    books = list_addressbooks()
    if not books:
        return None
    return books[0]["href"]


def _vcards_from_multiget(base_url: str, hrefs: List[str]) -> List[Dict[str, Any]]:
    """Bulk fetch vCards via REPORT (addressbook-multiget)."""
    if not hrefs:
        return []

    ns = {
        "d": "DAV:",
        "card": "urn:ietf:params:xml:ns:carddav",
    }

    href_xml = "".join(f"<d:href>{urllib.parse.quote(h, safe='/:@')}</d:href>" for h in hrefs)
    body = f"""<?xml version="1.0" encoding="utf-8"?>
<card:addressbook-multiget xmlns:d="DAV:" xmlns:card="urn:ietf:params:xml:ns:carddav">
    <d:prop>
        <d:getetag/>
        <card:address-data/>
    </d:prop>
    {href_xml}
</card:addressbook-multiget>"""

    url = f"{base_url}/{_dav_base_path('').lstrip('/')}"
    # Find a good base: take the first href and derive
    first_href = hrefs[0]
    parts = first_href.split("/remote.php/")
    if len(parts) > 1:
        url = f"{base_url}/remote.php/{parts[1].split('/')[0]}"

    try:
        resp = requests.request(
            "REPORT",
            url,
            auth=_auth(),
            data=body,
            timeout=DEFAULT_TIMEOUT,
        )
        if resp.status_code not in CARDDAV_SUCCESS_CODES:
            return []

        root = ET.fromstring(resp.content)
        results = []
        for response in root.findall(".//d:response", ns):
            href_el = response.find("d:href", ns)
            data_el = response.find(".//card:address-data", ns)
            if data_el is not None and data_el.text:
                parsed = _vcard_to_dict(data_el.text, href_el.text if href_el is not None else None)
                results.append(parsed)
        return results
    except (RequestException, ET.ParseError):
        return []


def _list_vcards_in_book(base_url: str, book_href: str) -> List[Dict[str, Any]]:
    """List all vCard contacts in an addressbook via PROPFIND."""
    full_url = f"{base_url}/{book_href.lstrip('/')}"
    headers = {"Depth": "1"}
    body = """<?xml version="1.0" encoding="utf-8"?>
<d:propfind xmlns:d="DAV:" xmlns:card="urn:ietf:params:xml:ns:carddav">
    <d:prop>
        <d:getetag/>
        <d:resourcetype/>
        <card:address-data/>
    </d:prop>
</d:propfind>"""

    ns = {
        "d": "DAV:",
        "card": "urn:ietf:params:xml:ns:carddav",
    }

    try:
        resp = requests.request(
            "PROPFIND",
            full_url,
            auth=_auth(),
            headers=headers,
            data=body,
            timeout=DEFAULT_TIMEOUT,
        )
        if resp.status_code not in CARDDAV_SUCCESS_CODES:
            return []

        root = ET.fromstring(resp.content)
        contacts = []
        for response in root.findall(".//d:response", ns):
            href_el = response.find("d:href", ns)
            rtype = response.find(".//d:resourcetype", ns)
            # Skip non-vCard (collections, etc.)
            if rtype is not None and rtype.find("d:collection", ns) is not None:
                continue
            data_el = response.find(".//card:address-data", ns)
            if data_el is not None and data_el.text:
                parsed = _vcard_to_dict(data_el.text, href_el.text if href_el is not None else None)
                contacts.append(parsed)
        return contacts
    except (RequestException, ET.ParseError):
        return []


def _vcard_to_dict(vcard_text: str, href: Optional[str] = None) -> Dict[str, Any]:
    """Parse vCard 3.0/4.0 text into a structured dict."""
    result: Dict[str, Any] = {
        "uid": "",
        "href": href or "",
        "name": "",
        "given_name": "",
        "surname": "",
        "email": "",
        "phone": "",
        "mobile": "",
        "org": "",
        "title": "",
        "note": "",
    }

    # Normalize line continuations (space-started continuation lines)
    vcard_text = re.sub(r"\r?\n ", "", vcard_text)

    # UID
    uid_m = re.search(r"^UID[^:]*:(.+)$", vcard_text, re.MULTILINE)
    if uid_m:
        result["uid"] = uid_m.group(1).strip()

    # FN (full name)
    fn_m = re.search(r"^FN[^:]*:(.+)$", vcard_text, re.MULTILINE)
    if fn_m:
        result["name"] = fn_m.group(1).strip()

    # N (structured name)
    n_m = re.search(r"^N[^:]*:(.+)$", vcard_text, re.MULTILINE)
    if n_m:
        parts = n_m.group(1).split(";")
        if len(parts) > 0:
            result["surname"] = parts[0].strip()
        if len(parts) > 1:
            result["given_name"] = parts[1].strip()

    # EMAIL
    email_m = re.search(r"^EMAIL[^:]*:(.+)$", vcard_text, re.MULTILINE)
    if email_m:
        result["email"] = email_m.group(1).strip()

    # TEL (phone / mobile)
    for tel_m in re.finditer(r"^TEL(;[^:]*)?:(.+)$", vcard_text, re.MULTILINE):
        params = tel_m.group(1) or ""
        number = tel_m.group(2).strip()
        if "TYPE=CELL" in params or "type=cell" in params:
            result["mobile"] = number
        else:
            result["phone"] = number

    # ORG
    org_m = re.search(r"^ORG[^:]*:(.+)$", vcard_text, re.MULTILINE)
    if org_m:
        result["org"] = org_m.group(1).strip().replace(";", ", ")

    # TITLE
    title_m = re.search(r"^TITLE[^:]*:(.+)$", vcard_text, re.MULTILINE)
    if title_m:
        result["title"] = title_m.group(1).strip()

    # NOTE
    note_m = re.search(r"^NOTE[^:]*:(.+)$", vcard_text, re.MULTILINE)
    if note_m:
        result["note"] = note_m.group(1).strip()

    return result


def _dict_to_vcard(data: Dict[str, str], include_uid: bool = False) -> str:
    """Build a vCard 3.0 string from a contact dict."""
    lines = ["BEGIN:VCARD", "VERSION:3.0"]

    given = data.get("given_name", "")
    surname = data.get("surname", "")
    full_name = data.get("name", f"{given} {surname}".strip())

    if not full_name:
        full_name = "Unknown"

    lines.append(f"FN:{full_name}")
    lines.append(f"N:{surname};{given};;;")

    if include_uid and data.get("uid"):
        lines.append(f"UID:{data['uid']}")

    if data.get("email"):
        lines.append(f"EMAIL:{data['email']}")

    if data.get("phone"):
        lines.append(f"TEL;TYPE=VOICE:{data['phone']}")

    if data.get("mobile"):
        lines.append(f"TEL;TYPE=CELL:{data['mobile']}")

    if data.get("org"):
        lines.append(f"ORG:{data['org']}")

    if data.get("title"):
        lines.append(f"TITLE:{data['title']}")

    if data.get("note"):
        lines.append(f"NOTE:{data['note']}")

    lines.append("END:VCARD")
    return "\r\n".join(lines) + "\r\n"


# ── CLI handlers ─────────────────────────────────────────────────


def cmd_list(args: argparse.Namespace) -> None:
    """List contacts from a CardDAV addressbook."""
    base_url, user, _ = _get_env_config()
    dav_base = _dav_base()

    book_href = args.addressbook
    if not book_href:
        book_href = _resolve_default_addressbook(base_url, dav_base)
    if not book_href:
        out({"ok": False, "error": "No addressbooks found"})
        return

    contacts = _list_vcards_in_book(base_url, book_href)
    out({
        "ok": True,
        "addressbook": book_href,
        "count": len(contacts),
        "contacts": contacts,
    })


def cmd_get(args: argparse.Namespace) -> None:
    """Get a single contact by UID."""
    base_url, user, _ = _get_env_config()
    dav_base = _dav_base()

    book_href = args.addressbook
    if not book_href:
        book_href = _resolve_default_addressbook(base_url, dav_base)
    if not book_href:
        out({"ok": False, "error": "No addressbooks found"})
        return

    contacts = _list_vcards_in_book(base_url, book_href)
    for c in contacts:
        if c.get("uid") == args.uid:
            out({"ok": True, "contact": c})
            return

    out({"ok": False, "error": f"Contact not found: {args.uid}"})


def cmd_create(args: argparse.Namespace) -> None:
    """Create a new contact in CardDAV."""
    _confirm_or_die(f"Create Nextcloud contact \"{getattr(args, 'name', '?')}\"")

    base_url, user, _ = _get_env_config()
    dav_base = _dav_base()

    book_href = args.addressbook
    if not book_href:
        book_href = _resolve_default_addressbook(base_url, dav_base)
    if not book_href:
        out({"ok": False, "error": "No addressbooks found"})
        return

    # Generate UID
    import uuid
    uid = str(uuid.uuid4())

    contact_data = {
        "name": args.name,
        "email": args.email or "",
        "phone": args.phone or "",
        "mobile": args.mobile or "",
        "org": args.org or "",
        "title": args.title or "",
        "note": args.note or "",
        "uid": uid,
    }

    # Parse given/surname from full name
    parts = args.name.split(" ", 1) if args.name else ["", ""]
    contact_data["given_name"] = parts[0]
    contact_data["surname"] = parts[1] if len(parts) > 1 else ""

    vcard = _dict_to_vcard(contact_data, include_uid=True)

    # PUT the vCard at the addressbook
    filename = f"{uid}.vcf"
    put_url = f"{base_url}/{book_href.lstrip('/')}{filename}"

    try:
        resp = requests.put(
            put_url,
            auth=_auth(),
            data=vcard,
            headers={"Content-Type": "text/vcard; charset=utf-8"},
            timeout=DEFAULT_TIMEOUT,
        )
        if resp.status_code in {201, 204}:
            out({
                "ok": True,
                "message": f"Contact '{args.name}' created",
                "contact": contact_data,
                "href": f"{book_href}{filename}",
            })
        else:
            out({
                "ok": False,
                "error": f"Failed to create contact: HTTP {resp.status_code}",
                "detail": resp.text[:500],
            })
    except RequestException as e:
        out({"ok": False, "error": f"Request failed: {e}"})


def cmd_update(args: argparse.Namespace) -> None:
    """Update an existing contact via CardDAV."""
    _confirm_or_die(f"Update Nextcloud contact {args.uid}")

    base_url, user, _ = _get_env_config()
    dav_base = _dav_base()

    book_href = args.addressbook
    if not book_href:
        book_href = _resolve_default_addressbook(base_url, dav_base)
    if not book_href:
        out({"ok": False, "error": "No addressbooks found"})
        return

    # Find the contact
    contacts = _list_vcards_in_book(base_url, book_href)
    target = None
    target_href = None
    for c in contacts:
        if c.get("uid") == args.uid:
            target = c
            target_href = c.get("href", "")
            break

    if not target:
        out({"ok": False, "error": f"Contact not found: {args.uid}"})
        return

    # Merge updates
    if args.name:
        target["name"] = args.name
        parts = args.name.split(" ", 1)
        target["given_name"] = parts[0]
        target["surname"] = parts[1] if len(parts) > 1 else ""
    if args.email is not None:
        target["email"] = args.email
    if args.phone is not None:
        target["phone"] = args.phone
    if args.mobile is not None:
        target["mobile"] = args.mobile
    if args.org is not None:
        target["org"] = args.org
    if args.title is not None:
        target["title"] = args.title
    if args.note is not None:
        target["note"] = args.note

    vcard = _dict_to_vcard(target, include_uid=True)

    put_url = f"{base_url}/{target_href.lstrip('/')}" if target_href else ""
    if not put_url:
        # Construct from book_href + uid
        put_url = f"{base_url}/{book_href.lstrip('/')}{args.uid}.vcf"

    try:
        resp = requests.put(
            put_url,
            auth=_auth(),
            data=vcard,
            headers={"Content-Type": "text/vcard; charset=utf-8"},
            timeout=DEFAULT_TIMEOUT,
        )
        if resp.status_code in {204, 200, 201}:
            out({
                "ok": True,
                "message": f"Contact '{target['name']}' updated",
                "contact": target,
            })
        else:
            out({
                "ok": False,
                "error": f"Failed to update contact: HTTP {resp.status_code}",
                "detail": resp.text[:500],
            })
    except RequestException as e:
        out({"ok": False, "error": f"Request failed: {e}"})


def cmd_delete(args: argparse.Namespace) -> None:
    """Delete a contact from CardDAV."""
    _confirm_or_die(f"Delete Nextcloud contact {args.uid}")

    base_url, user, _ = _get_env_config()
    dav_base = _dav_base()

    book_href = args.addressbook
    if not book_href:
        book_href = _resolve_default_addressbook(base_url, dav_base)
    if not book_href:
        out({"ok": False, "error": "No addressbooks found"})
        return

    contacts = _list_vcards_in_book(base_url, book_href)
    target_href = None
    target_name = args.uid
    for c in contacts:
        if c.get("uid") == args.uid:
            target_href = c.get("href", "")
            target_name = c.get("name", args.uid)
            break

    if not target_href:
        out({"ok": False, "error": f"Contact not found: {args.uid}"})
        return

    delete_url = f"{base_url}/{target_href.lstrip('/')}"

    try:
        resp = requests.delete(
            delete_url,
            auth=_auth(),
            timeout=DEFAULT_TIMEOUT,
        )
        if resp.status_code in {204, 200, 404}:
            out({"ok": True, "message": f"Contact '{target_name}' deleted"})
        else:
            out({
                "ok": False,
                "error": f"Failed to delete contact: HTTP {resp.status_code}",
            })
    except RequestException as e:
        out({"ok": False, "error": f"Request failed: {e}"})


def cmd_search(args: argparse.Namespace) -> None:
    """Search contacts by query string."""
    base_url, user, _ = _get_env_config()
    dav_base = _dav_base()

    book_href = args.addressbook
    if not book_href:
        book_href = _resolve_default_addressbook(base_url, dav_base)
    if not book_href:
        out({"ok": False, "error": "No addressbooks found"})
        return

    q = args.query.lower()
    contacts = _list_vcards_in_book(base_url, book_href)

    matches = []
    for c in contacts:
        name = c.get("name", "").lower()
        email = c.get("email", "").lower()
        org = c.get("org", "").lower()
        phone = c.get("phone", "").lower()
        mobile = c.get("mobile", "").lower()
        note = c.get("note", "").lower()

        if q in name or q in email or q in org or q in phone or q in mobile or q in note:
            matches.append(c)

    out({
        "ok": True,
        "query": args.query,
        "count": len(matches),
        "contacts": matches[: args.limit],
    })


def add_parser(subparser) -> None:
    """Add contacts subcommands to the Nextcloud CLI parser."""
    # We'll wire through the argparse setup in __main__

    def _wire(name: str, fn, **kwargs):
        p = subparser.add_parser(name, **kwargs)
        p.set_defaults(func=fn)
        return p

    p = _wire("list", cmd_list, help="List contacts from CardDAV addressbook")
    p.add_argument("--addressbook", help="Addressbook href (default: first found)")
    p.add_argument("--limit", type=int, default=100, help="Max contacts")

    p = _wire("get", cmd_get, help="Get a contact by UID")
    p.add_argument("--uid", required=True, help="Contact UID")
    p.add_argument("--addressbook", help="Addressbook href")

    p = _wire("create", cmd_create, help="Create a new contact")
    p.add_argument("--name", required=True, help="Full name")
    p.add_argument("--email", help="Email address")
    p.add_argument("--phone", help="Phone number")
    p.add_argument("--mobile", help="Mobile phone number")
    p.add_argument("--org", help="Organization")
    p.add_argument("--title", help="Job title")
    p.add_argument("--note", help="Notes")
    p.add_argument("--addressbook", help="Target addressbook href")

    p = _wire("update", cmd_update, help="Update a contact")
    p.add_argument("--uid", required=True, help="Contact UID")
    p.add_argument("--name", help="Full name")
    p.add_argument("--email", help="Email address")
    p.add_argument("--phone", help="Phone number")
    p.add_argument("--mobile", help="Mobile phone number")
    p.add_argument("--org", help="Organization")
    p.add_argument("--title", help="Job title")
    p.add_argument("--note", help="Notes")
    p.add_argument("--addressbook", help="Addressbook href")

    p = _wire("delete", cmd_delete, help="Delete a contact")
    p.add_argument("--uid", required=True, help="Contact UID")
    p.add_argument("--addressbook", help="Addressbook href")

    p = _wire("search", cmd_search, help="Search contacts")
    p.add_argument("--query", required=True, help="Search query")
    p.add_argument("--addressbook", help="Addressbook href")
    p.add_argument("--limit", type=int, default=50, help="Max results")


# Re-export out() and die() for consistency with Exchange module
def out(data: Dict[str, Any]) -> None:
    """Print JSON output."""
    print(json.dumps(data, ensure_ascii=False, default=str))


def die(message: str) -> None:
    """Print error and exit."""
    out({"ok": False, "error": message})
    sys.exit(1)
