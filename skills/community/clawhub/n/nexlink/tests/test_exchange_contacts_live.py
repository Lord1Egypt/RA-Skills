"""
Live integration tests for Exchange contacts (EWS).
Requires exchangelib and EXCHANGE_* environment variables.

Run:
    EXCHANGE_SERVER=... EXCHANGE_USERNAME=... EXCHANGE_PASSWORD=... EXCHANGE_EMAIL=... \
      python3 -m pytest tests/test_exchange_contacts_live.py -v

Or:
    pytest -m exchange_live tests/ -v

Skips automatically when exchangelib is not available or env vars missing.
"""

import os
import sys
import uuid
from unittest.mock import patch

import pytest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

# ── Skip conditions ────────────────────────────────────────────

HAS_EXCHANGELIB = False
try:
    import exchangelib  # noqa: F401
    HAS_EXCHANGELIB = True
except ImportError:
    pass

HAS_ENV = all(
    os.environ.get(k)
    for k in ("EXCHANGE_SERVER", "EXCHANGE_USERNAME", "EXCHANGE_PASSWORD", "EXCHANGE_EMAIL")
)

skip_reason = None
if not HAS_EXCHANGELIB:
    skip_reason = "exchangelib not installed"
elif not HAS_ENV:
    skip_reason = "EXCHANGE_* environment variables not set"

live_test = pytest.mark.skipif(skip_reason is not None, reason=skip_reason or "")
requires_exchange = pytest.mark.exchange_live


# ── Helpers ────────────────────────────────────────────────────

TEST_PREFIX = "NEXLINK_TEST_"


def _make_test_name(base: str) -> str:
    """Generate a unique test contact name."""
    return f"{TEST_PREFIX}{base}_{uuid.uuid4().hex[:8]}"


def _cleanup_contact(account, contact_id: str) -> None:
    """Safely move a contact to trash by ID."""
    try:
        contact = account.contacts.get(id=contact_id)
        if contact:
            contact.move_to_trash()
    except Exception:
        pass


def _ensure_contact(account, name: str, **fields) -> object:
    """Create a contact and return it. Caller must clean up.

    Imports Contact/PhoneNumber directly from exchangelib
    rather than the NextLink module (which may have try/except None).
    """
    from exchangelib import Contact
    from exchangelib.indexed_properties import PhoneNumber, EmailAddress

    contact = Contact(
        folder=account.contacts,
        display_name=name,
        given_name=fields.get("given_name", name.split(" ")[0]),
        surname=fields.get("surname", name.split(" ")[1] if " " in name else ""),
        company_name=fields.get("org"),
        job_title=fields.get("title"),
        body=fields.get("note"),
    )

    if fields.get("email"):
        contact.email_addresses = [EmailAddress(email=fields["email"], label="EmailAddress1")]

    if fields.get("phone"):
        contact.phone_numbers = [PhoneNumber(label="BusinessPhone", phone_number=fields["phone"])]

    if fields.get("mobile"):
        phones = list(contact.phone_numbers or [])
        phones.append(PhoneNumber(label="MobilePhone", phone_number=fields["mobile"]))
        contact.phone_numbers = phones

    contact.save()
    return contact


# ── Fixture: account ───────────────────────────────────────────

@pytest.fixture(scope="module")
def exchange_account():
    """Provide a live Exchange account connection."""
    from modules.exchange.connection import get_account

    account = get_account()
    return account


# ── Tests ──────────────────────────────────────────────────────

class TestExchangeContactsLive:
    """Live integration tests for Exchange contacts."""

    # ── Connection ─────────────────────────────────────────

    @live_test
    def test_connect(self, exchange_account):
        """Can connect to Exchange and inspect the account."""
        assert exchange_account is not None
        assert exchange_account.primary_smtp_address
        assert "@" in exchange_account.primary_smtp_address

    # ── List ───────────────────────────────────────────────

    @live_test
    def test_list(self, exchange_account):
        """List contacts returns valid structure."""
        from modules.exchange.contacts import _get_contacts_folder, _contact_to_dict

        folder = _get_contacts_folder(exchange_account)
        contacts = list(folder.all().order_by("display_name")[:3])

        assert len(contacts) >= 0  # might have zero contacts
        for c in contacts:
            d = _contact_to_dict(c)
            assert "id" in d
            assert "changekey" in d
            assert "name" in d
            assert d["id"] is not None

    @live_test
    def test_list_limit(self, exchange_account):
        """--limit 1 returns at most 1 contact."""
        from modules.exchange.contacts import _get_contacts_folder

        folder = _get_contacts_folder(exchange_account)
        contacts = list(folder.all().order_by("display_name")[:1])

        assert len(contacts) <= 1

    # ── Create + cleanup ───────────────────────────────────

    @live_test
    def test_create_and_cleanup(self, exchange_account):
        """Create a contact then delete it, verifying both steps."""
        from modules.exchange.contacts import _get_contacts_folder, _contact_to_dict

        name = _make_test_name("CreateCleanup")

        contact = _ensure_contact(exchange_account, name, email=f"{name}@test.local")
        created_id = contact.id

        try:
            d = _contact_to_dict(contact)
            assert d["name"] == name
            assert f"{name}@test.local" in d["email"]

            # Verify we can find it
            folder = _get_contacts_folder(exchange_account)
            found = folder.get(id=created_id)
            assert found is not None
            assert found.display_name == name
        finally:
            contact.move_to_trash()

        # Confirm it's gone — use try/except since get raises on trashed items
        from exchangelib.errors import ErrorItemNotFound
        folder = _get_contacts_folder(exchange_account)
        gone = None
        try:
            gone = folder.get(id=created_id)
        except ErrorItemNotFound:
            pass
        except Exception:
            # contact.move_to_trash() may have set changekey, causing other errors
            pass
        assert gone is None

    @live_test
    def test_create_full(self, exchange_account):
        """Create a contact with all fields populated and verify roundtrip."""
        from modules.exchange.contacts import _contact_to_dict

        name = _make_test_name("FullFields")
        email = f"{name}@full.test"
        phone = "+40-711-111-111"
        mobile = "+40-722-222-222"
        org = "TestOrg Inc"
        title = "Integration Tester"

        contact = _ensure_contact(
            exchange_account,
            name,
            email=email,
            phone=phone,
            mobile=mobile,
            org=org,
            title=title,
            note="Created by NextLink live test",
        )

        try:
            d = _contact_to_dict(contact)
            assert d["name"] == name
            assert d["email"] == email
            assert d["phone"] == phone
            assert d["mobile"] == mobile
            assert d["org"] == org
            assert d["title"] == title
            assert d["note"] == "Created by NextLink live test"
        finally:
            contact.move_to_trash()

    # ── Update ─────────────────────────────────────────────

    @live_test
    def test_update(self, exchange_account):
        """Create a contact, update name and phone, verify."""
        from modules.exchange.contacts import _get_contacts_folder, _contact_to_dict

        original_name = _make_test_name("UpdateOrig")
        updated_name = original_name.replace("UpdateOrig", "UpdateMod")

        contact = _ensure_contact(exchange_account, original_name, email=f"{original_name}@update.test")
        contact_id = contact.id

        try:
            # Update
            contact.display_name = updated_name
            contact.given_name = updated_name.split(" ")[0]
            contact.surname = updated_name.split(" ")[1] if " " in updated_name else ""
            from exchangelib import Contact
            from exchangelib.indexed_properties import PhoneNumber, EmailAddress
            if not contact.phone_numbers:
                contact.phone_numbers = [PhoneNumber(label="BusinessPhone")]
            contact.phone_numbers[0].phone_number = "+40-733-333-333"
            contact.save()

            # Verify
            folder = _get_contacts_folder(exchange_account)
            refreshed = folder.get(id=contact_id)
            d = _contact_to_dict(refreshed)
            assert d["name"] == updated_name
            assert "+40-733-333-333" in d["phone"]
        finally:
            contact.move_to_trash()

    # ── Search ─────────────────────────────────────────────

    @live_test
    def test_search_by_name(self, exchange_account):
        """Create a contact with a unique name, search for it by name."""
        from modules.exchange.contacts import cmd_search

        name = _make_test_name("SearchByName")
        contact = _ensure_contact(exchange_account, name, email=f"{name}@search.test")

        try:
            captured = {}
            with patch("modules.exchange.contacts.out", lambda d: captured.update(d)):
                import argparse
                args = argparse.Namespace(query=name.split("_")[0], limit=50)
                cmd_search(args)

            assert captured.get("ok")
            assert captured.get("count", 0) >= 1
            names = [c["name"] for c in captured.get("contacts", [])]
            assert name in names
        finally:
            contact.move_to_trash()

    @live_test
    def test_search_by_email(self, exchange_account):
        """Create a contact, search by email domain."""
        from modules.exchange.contacts import cmd_search

        name = _make_test_name("SearchEmail")
        email = f"{name}@search-email-test.local"
        contact = _ensure_contact(exchange_account, name, email=email)

        try:
            captured = {}
            with patch("modules.exchange.contacts.out", lambda d: captured.update(d)):
                import argparse
                args = argparse.Namespace(query="search-email-test.local", limit=50)
                cmd_search(args)

            assert captured.get("ok")
            emails = [c.get("email", "") for c in captured.get("contacts", [])]
            assert email in emails
        finally:
            contact.move_to_trash()

    # ── Error cases ────────────────────────────────────────

    @live_test
    def test_get_nonexistent(self, exchange_account):
        """Get a non-existent contact ID returns error."""
        from modules.exchange.contacts import cmd_get

        captured = {}

        def fake_die(msg):
            captured["error"] = msg
            raise SystemExit(1)

        with pytest.raises(SystemExit):
            with patch("modules.exchange.contacts.die", fake_die):
                import argparse
                args = argparse.Namespace(id="nonexistent-this-does-not-exist-xxx")
                cmd_get(args)

        err = captured.get("error", "").lower()
        assert "not found" in err or "malformed" in err

    @live_test
    def test_delete_nonexistent(self, exchange_account):
        """Delete a non-existent contact returns error."""
        from modules.exchange.contacts import cmd_delete

        captured = {}

        def fake_die(msg):
            captured["error"] = msg
            raise SystemExit(1)

        with pytest.raises(SystemExit):
            with patch("modules.exchange.contacts.die", fake_die):
                import argparse
                args = argparse.Namespace(id="nonexistent-this-does-not-exist-xxx")
                cmd_delete(args)

        err = captured.get("error", "").lower()
        assert "not found" in err or "malformed" in err

    # ── _contact_to_dict unit (on a real object) ───────────

    @live_test
    def test_contact_to_dict_real(self, exchange_account):
        """_contact_to_dict produces expected fields from a real Contact object."""
        from modules.exchange.contacts import _contact_to_dict

        name = _make_test_name("ToDictReal")
        contact = _ensure_contact(
            exchange_account,
            name,
            email=f"{name}@todict.test",
            phone="+40-744-444-444",
        )

        try:
            d = _contact_to_dict(contact)
            assert isinstance(d, dict)
            assert d["id"] == contact.id
            assert d["changekey"] == contact.changekey
            assert d["name"] == name
            assert d["email"] == f"{name}@todict.test"
            assert d["phone"] == "+40-744-444-444"
        finally:
            contact.move_to_trash()
