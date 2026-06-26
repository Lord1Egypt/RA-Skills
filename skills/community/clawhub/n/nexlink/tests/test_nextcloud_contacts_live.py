"""
Live integration tests for Nextcloud contacts (CardDAV).
Requires NEXTCLOUD_URL, NEXTCLOUD_USERNAME, NEXTCLOUD_APP_PASSWORD.

Run:
    NEXTCLOUD_URL=... NEXTCLOUD_USERNAME=... NEXTCLOUD_APP_PASSWORD=... \\
      python3 -m pytest tests/test_nextcloud_contacts_live.py -v

Skips automatically when env vars missing.
"""

import os
import sys
import uuid
from unittest.mock import patch

import pytest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

# ── Skip conditions ────────────────────────────────────────────

HAS_ENV = all(
    os.environ.get(k)
    for k in ("NEXTCLOUD_URL", "NEXTCLOUD_USERNAME", "NEXTCLOUD_APP_PASSWORD")
)

skip_reason = None
if not HAS_ENV:
    skip_reason = "NEXTCLOUD_* environment variables not set"

live_test = pytest.mark.skipif(skip_reason is not None, reason=skip_reason or "")


# ── Helpers ────────────────────────────────────────────────────

TEST_PREFIX = "NEXLINK_TEST_"


def _make_test_name(base: str) -> str:
    """Generate a unique test contact name."""
    return f"{TEST_PREFIX}{base}_{uuid.uuid4().hex[:8]}"


def _nc_create_contact(name: str, **fields) -> str:
    """Create a contact directly via CardDAV PUT and return the UID.

    Uses the nexlink module internally so this also tests the code path.
    Uses cmd_create-like logic but returns UID for test tracking.
    """
    import uuid as _uuid
    from modules.nextcloud.contacts import (
        _dav_base,
        _get_env_config,
        _dict_to_vcard,
        die as _die,
    )

    base_url, _, _ = _get_env_config()
    dav_base = _dav_base()
    book_href = fields.get("addressbook") or None

    # If no explicit book, use the module's resolve
    if not book_href:
        from modules.nextcloud.contacts import _resolve_default_addressbook
        book_href = _resolve_default_addressbook(base_url, dav_base)

    if not book_href:
        raise RuntimeError("No addressbooks found on Nextcloud")

    uid = str(_uuid.uuid4())
    parts = name.split(" ", 1) if name else ["", ""]
    contact_data = {
        "name": name,
        "uid": uid,
        "given_name": parts[0],
        "surname": parts[1] if len(parts) > 1 else "",
        "email": fields.get("email", ""),
        "phone": fields.get("phone", ""),
        "mobile": fields.get("mobile", ""),
        "org": fields.get("org", ""),
        "title": fields.get("title", ""),
        "note": fields.get("note", ""),
    }

    vcard = _dict_to_vcard(contact_data, include_uid=True)
    filename = f"{uid}.vcf"
    put_url = f"{base_url}/{book_href.lstrip('/')}{filename}"

    import requests
    from modules.nextcloud.contacts import _auth
    resp = requests.put(
        put_url,
        auth=_auth(),
        data=vcard,
        headers={"Content-Type": "text/vcard; charset=utf-8"},
        timeout=30,
    )
    if resp.status_code not in (201, 204):
        raise RuntimeError(f"Failed to create contact: HTTP {resp.status_code} - {resp.text[:200]}")

    return uid


def _nc_delete_contact(uid: str) -> None:
    """Delete a contact by UID (find href first, then DELETE)."""
    from modules.nextcloud.contacts import _dav_base, _get_env_config, _auth, _resolve_default_addressbook, _list_vcards_in_book
    import requests

    base_url, _, _ = _get_env_config()
    dav_base = _dav_base()
    book_href = _resolve_default_addressbook(base_url, dav_base)
    if not book_href:
        return

    contacts = _list_vcards_in_book(base_url, book_href)
    for c in contacts:
        if c.get("uid") == uid:
            href = c.get("href", "")
            if href:
                del_url = f"{base_url}/{href.lstrip('/')}"
                try:
                    requests.delete(del_url, auth=_auth(), timeout=30)
                except Exception:
                    pass
            return


def _nc_list_uids() -> set:
    """Return set of all UIDs in default addressbook."""
    from modules.nextcloud.contacts import _dav_base, _get_env_config, _resolve_default_addressbook, _list_vcards_in_book
    base_url, _, _ = _get_env_config()
    dav_base = _dav_base()
    book_href = _resolve_default_addressbook(base_url, dav_base)
    if not book_href:
        return set()
    contacts = _list_vcards_in_book(base_url, book_href)
    return {c.get("uid", "") for c in contacts}


# ── Fixture: book href ────────────────────────────────────────

@pytest.fixture(scope="module")
def nc_book_href():
    """Return the default addressbook href."""
    from modules.nextcloud.contacts import _dav_base, _get_env_config, _resolve_default_addressbook
    base_url, _, _ = _get_env_config()
    dav_base = _dav_base()
    book_href = _resolve_default_addressbook(base_url, dav_base)
    if not book_href:
        pytest.skip("No addressbooks found on Nextcloud")
    return book_href


# ── Tests ─────────────────────────────────────────────────────

class TestNextcloudContactsLive:
    """Live integration tests for Nextcloud contacts."""

    # ── Addressbooks ───────────────────────────────────────

    @live_test
    def test_list_addressbooks(self):
        """List addressbooks returns valid structure with contacts book."""
        from modules.nextcloud.contacts import list_addressbooks

        books = list_addressbooks()
        assert len(books) >= 1

        # At least one should be the real Contacts addressbook
        names = [b["displayname"] for b in books]
        assert "Contacts" in names

        for b in books:
            assert "href" in b
            assert "displayname" in b
            assert b["href"].startswith("/")

    # ── Create + cleanup ───────────────────────────────────

    @live_test
    def test_create_and_cleanup(self):
        """Create a contact, verify it appears in listing, delete, confirm gone."""
        name = _make_test_name("CreateCleanup")
        email = f"{name}@nc-test.local"

        uid = _nc_create_contact(name, email=email)

        try:
            # Verify it appears in listing
            from modules.nextcloud.contacts import _dav_base, _get_env_config, _resolve_default_addressbook, _list_vcards_in_book
            base_url, _, _ = _get_env_config()
            dav_base = _dav_base()
            book_href = _resolve_default_addressbook(base_url, dav_base)

            contacts = _list_vcards_in_book(base_url, book_href)
            uids = {c.get("uid", "") for c in contacts}
            assert uid in uids, f"Contact {uid} not found in listing"

            # Find it and verify name/email
            for c in contacts:
                if c.get("uid") == uid:
                    assert name in c.get("name", "")
                    assert email == c.get("email", "")
                    break
            else:
                pytest.fail(f"Contact {uid} found in UIDs but not in detail search")
        finally:
            _nc_delete_contact(uid)

        # Confirm gone
        remaining = _nc_list_uids()
        assert uid not in remaining

    @live_test
    def test_create_full(self):
        """Create a contact with all fields populated and verify roundtrip."""
        name = _make_test_name("FullFields")
        email = f"{name}@full.nc-test"
        phone = "+40-711-111-111"
        mobile = "+40-722-222-222"
        org = "TestOrg Inc"
        title = "Integration Tester"
        note = "Created by NextLink live test"

        uid = _nc_create_contact(name, email=email, phone=phone, mobile=mobile, org=org, title=title, note=note)

        try:
            from modules.nextcloud.contacts import _dav_base, _get_env_config, _resolve_default_addressbook, _list_vcards_in_book
            base_url, _, _ = _get_env_config()
            dav_base = _dav_base()
            book_href = _resolve_default_addressbook(base_url, dav_base)

            contacts = _list_vcards_in_book(base_url, book_href)
            for c in contacts:
                if c.get("uid") == uid:
                    assert c["name"] == name, f"name: {c['name']} != {name}"
                    assert c["email"] == email
                    assert c["phone"] == phone, f"phone: {c['phone']} != {phone}"
                    assert c["mobile"] == mobile, f"mobile: {c['mobile']} != {mobile}"
                    assert c["org"] == org
                    assert c["title"] == title
                    assert c["note"] == note
                    break
            else:
                pytest.fail(f"Contact {uid} not found after create")
        finally:
            _nc_delete_contact(uid)

    # ── List ───────────────────────────────────────────────

    @live_test
    def test_list_contacts(self, nc_book_href):
        """List contacts returns valid dict structure."""
        from modules.nextcloud.contacts import _dav_base, _get_env_config, _list_vcards_in_book
        base_url, _, _ = _get_env_config()

        contacts = _list_vcards_in_book(base_url, nc_book_href)
        assert isinstance(contacts, list)

        for c in contacts:
            assert "uid" in c
            assert "name" in c
            assert "href" in c

    # ── Get ────────────────────────────────────────────────

    @live_test
    def test_get_by_uid(self):
        """Create a contact and retrieve it by UID via cmd_get."""
        from modules.nextcloud.contacts import cmd_get

        name = _make_test_name("GetByUID")
        email = f"{name}@get.nc-test"
        uid = _nc_create_contact(name, email=email)

        try:
            captured = {}
            with patch("modules.nextcloud.contacts.out", lambda d: captured.update(d)):
                import argparse
                args = argparse.Namespace(uid=uid, addressbook=None)
                cmd_get(args)

            assert captured.get("ok"), f"cmd_get failed: {captured}"
            contact = captured.get("contact", {})
            assert contact.get("uid") == uid
            assert name in contact.get("name", "")
            assert email == contact.get("email", "")
        finally:
            _nc_delete_contact(uid)

    @live_test
    def test_get_nonexistent_uid(self):
        """Get with non-existent UID returns error."""
        from modules.nextcloud.contacts import cmd_get

        captured = {}
        with patch("modules.nextcloud.contacts.out", lambda d: captured.update(d)):
            import argparse
            args = argparse.Namespace(uid="nonexistent-uid-xxx", addressbook=None)
            cmd_get(args)

        assert not captured.get("ok", True), f"Expected error, got: {captured}"

    # ── Search ─────────────────────────────────────────────

    @live_test
    def test_search_by_name(self):
        """Create a contact, search by name substring."""
        from modules.nextcloud.contacts import cmd_search

        name = _make_test_name("SearchByName")
        email = f"{name}@search.nc-test"
        uid = _nc_create_contact(name, email=email)

        try:
            captured = {}
            with patch("modules.nextcloud.contacts.out", lambda d: captured.update(d)):
                import argparse
                args = argparse.Namespace(query=name.split("_")[0], addressbook=None, limit=50)
                cmd_search(args)

            assert captured.get("ok")
            assert captured.get("count", 0) >= 1
            names = [c["name"] for c in captured.get("contacts", [])]
            assert name in names
        finally:
            _nc_delete_contact(uid)

    @live_test
    def test_search_by_email(self):
        """Create a contact, search by email domain."""
        from modules.nextcloud.contacts import cmd_search

        name = _make_test_name("SearchEmail")
        email = f"{name}@search-email.nc-test"
        uid = _nc_create_contact(name, email=email)

        try:
            captured = {}
            with patch("modules.nextcloud.contacts.out", lambda d: captured.update(d)):
                import argparse
                args = argparse.Namespace(query="search-email.nc-test", addressbook=None, limit=50)
                cmd_search(args)

            assert captured.get("ok")
            emails = [c.get("email", "") for c in captured.get("contacts", [])]
            assert email in emails
        finally:
            _nc_delete_contact(uid)

    @live_test
    def test_search_by_org(self):
        """Create a contact, search by org."""
        from modules.nextcloud.contacts import cmd_search

        name = _make_test_name("SearchOrg")
        org = "UniqueOrgNameForTesting"
        uid = _nc_create_contact(name, org=org)

        try:
            captured = {}
            with patch("modules.nextcloud.contacts.out", lambda d: captured.update(d)):
                import argparse
                args = argparse.Namespace(query=org, addressbook=None, limit=50)
                cmd_search(args)

            assert captured.get("ok")
            assert captured.get("count", 0) >= 1
        finally:
            _nc_delete_contact(uid)

    @live_test
    def test_search_nonexistent(self):
        """Search for something that doesn't exist returns count=0."""
        from modules.nextcloud.contacts import cmd_search

        captured = {}
        with patch("modules.nextcloud.contacts.out", lambda d: captured.update(d)):
            import argparse
            args = argparse.Namespace(query="ZZZZ_NONEXISTENT_QUERY_XXXX", addressbook=None, limit=50)
            cmd_search(args)

        assert captured.get("ok")
        assert captured.get("count", -1) == 0

    # ── Update ─────────────────────────────────────────────

    @live_test
    def test_update_contact(self):
        """Create a contact, update name and org, verify roundtrip."""
        from modules.nextcloud.contacts import cmd_update

        name = _make_test_name("UpdateOrig")
        updated_name = name.replace("UpdateOrig", "UpdateMod")
        uid = _nc_create_contact(name, email=f"{name}@update.nc-test")

        try:
            captured = {}
            with patch("modules.nextcloud.contacts.out", lambda d: captured.update(d)):
                import argparse
                args = argparse.Namespace(uid=uid, name=updated_name, email=None,
                                          phone=None, mobile=None, org="UpdatedOrg",
                                          title=None, note=None, addressbook=None)
                cmd_update(args)

            assert captured.get("ok"), f"Update failed: {captured}"

            # Verify by getting the contact
            from modules.nextcloud.contacts import _dav_base, _get_env_config, _resolve_default_addressbook, _list_vcards_in_book
            base_url, _, _ = _get_env_config()
            dav_base = _dav_base()
            book_href = _resolve_default_addressbook(base_url, dav_base)

            contacts = _list_vcards_in_book(base_url, book_href)
            for c in contacts:
                if c.get("uid") == uid:
                    assert updated_name in c.get("name", "")
                    assert c.get("org") == "UpdatedOrg"
                    break
            else:
                pytest.fail(f"Contact {uid} not found after update")
        finally:
            _nc_delete_contact(uid)

    # ── Delete ─────────────────────────────────────────────

    @live_test
    def test_delete_nonexistent(self):
        """Delete with non-existent UID returns error."""
        from modules.nextcloud.contacts import cmd_delete

        captured = {}
        with patch("modules.nextcloud.contacts.out", lambda d: captured.update(d)):
            import argparse
            args = argparse.Namespace(uid="nonexistent-uid-yyy", addressbook=None)
            cmd_delete(args)

        assert not captured.get("ok", True), f"Expected error, got: {captured}"
