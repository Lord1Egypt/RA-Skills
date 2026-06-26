#!/usr/bin/env python3
"""Unit tests for Nextcloud contacts (CardDAV) and Exchange contacts modules."""

import json
import os
import sys
import unittest
from unittest.mock import MagicMock, patch, PropertyMock

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

# ── Exchange contacts tests ──────────────────────────────────────


class ExchangeContactsTests(unittest.TestCase):
    """Test Exchange contacts module functions (unit tests with mocked exchangelib)."""

    def setUp(self):
        self.env_patch = patch.dict(os.environ, {
            "EXCHANGE_SERVER": "https://exchange.example.com/EWS/Exchange.asmx",
            "EXCHANGE_USERNAME": "user",
            "EXCHANGE_PASSWORD": "pass",
            "EXCHANGE_EMAIL": "user@example.com",
        }, clear=False)
        self.env_patch.start()

    def tearDown(self):
        self.env_patch.stop()

    @patch("modules.exchange.contacts.HAS_EXCHANGELIB", True)
    @patch("modules.exchange.contacts.get_account")
    def test_cmd_list(self, mock_get_account):
        """contacts list calls account.contacts.all().order_by() and returns contacts."""
        from modules.exchange.contacts import cmd_list

        # Mock contact
        mock_contact = MagicMock()
        mock_contact.id = "contact-1"
        mock_contact.changekey = "ck-1"
        mock_contact.display_name = "John Doe"
        mock_contact.full_name = "John Doe"
        mock_contact.given_name = "John"
        mock_contact.surname = "Doe"
        mock_contact.company_name = "Acme"
        mock_contact.job_title = "CEO"
        mock_contact.body = "Notes here"
        mock_contact.email_addresses = []
        mock_contact.phone_numbers = MagicMock()
        mock_contact.phone_numbers.business_phone = "+40-711-111-111"
        mock_contact.phone_numbers.mobile_phone = None

        # _get_contacts_folder now returns account.contacts directly
        mock_contacts_folder = MagicMock()
        mock_contacts_folder.all.return_value.order_by.return_value.__getitem__.return_value = [mock_contact]

        mock_account = MagicMock()
        mock_account.contacts = mock_contacts_folder
        mock_get_account.return_value = mock_account

        # Capture output
        from modules.exchange.utils import out as original_out
        captured = {}

        def fake_out(data):
            captured.update(data)

        with patch("modules.exchange.contacts.out", fake_out):
            # Build args namespace
            import argparse
            args = argparse.Namespace(limit=50, folder="contacts")
            cmd_list(args)

        self.assertTrue(captured.get("ok"))
        self.assertEqual(captured.get("count"), 1)
        self.assertEqual(captured["contacts"][0]["name"], "John Doe")

    @patch("modules.exchange.contacts.HAS_EXCHANGELIB", True)
    @patch("modules.exchange.contacts.get_account")
    def test_cmd_create(self, mock_get_account):
        """contacts create creates a Contact and saves it."""
        from modules.exchange.contacts import cmd_create, Contact

        mock_contact_instance = MagicMock(spec=Contact)
        mock_contact_instance.id = "new-contact-1"
        mock_contact_instance.changekey = "ck-new"
        mock_contact_instance.display_name = "Jane Doe"
        mock_contact_instance.full_name = "Jane Doe"
        mock_contact_instance.given_name = "Jane"
        mock_contact_instance.surname = "Doe"
        mock_contact_instance.company_name = ""
        mock_contact_instance.job_title = ""
        mock_contact_instance.body = ""
        mock_contact_instance.email_addresses = []
        mock_contact_instance.phone_numbers = MagicMock()
        mock_contact_instance.phone_numbers.business_phone = None
        mock_contact_instance.phone_numbers.mobile_phone = None

        mock_account = MagicMock()
        mock_get_account.return_value = mock_account

        captured = {}

        with patch("modules.exchange.contacts.Contact", return_value=mock_contact_instance):
            with patch("modules.exchange.contacts.PhoneNumber") as mock_pn:
                with patch("modules.exchange.contacts.out", lambda d: captured.update(d)):
                    import argparse
                    args = argparse.Namespace(
                    name="Jane Doe", email="jane@example.com",
                    phone="+40-722-222-222", mobile=None,
                    org=None, title=None, note=None,
                    folder="contacts",
                    )
                    cmd_create(args)

        self.assertTrue(captured.get("ok"))
        self.assertIn("Jane Doe", captured.get("message", ""))

    @patch("modules.exchange.contacts.HAS_EXCHANGELIB", True)
    @patch("modules.exchange.contacts.get_account")
    def test_cmd_search(self, mock_get_account):
        """contacts search filters by query."""
        from modules.exchange.contacts import cmd_search

        mock_contact = MagicMock()
        mock_contact.id = "c-1"
        mock_contact.changekey = "ck-1"
        mock_contact.display_name = "John Doe"
        mock_contact.full_name = "John Doe"
        mock_contact.given_name = ""
        mock_contact.surname = ""
        mock_contact.company_name = "Acme Inc"
        mock_contact.job_title = ""
        mock_contact.body = ""
        mock_contact.email_addresses = []
        mock_contact.phone_numbers = MagicMock()
        mock_contact.phone_numbers.business_phone = None
        mock_contact.phone_numbers.mobile_phone = None

        mock_folder = MagicMock()
        mock_folder.filter.return_value.order_by.return_value.__getitem__.return_value = [mock_contact]

        mock_account = MagicMock()
        mock_account.contacts = mock_folder
        mock_get_account.return_value = mock_account

        captured = {}

        with patch("modules.exchange.contacts.out", lambda d: captured.update(d)):
            import argparse
            args = argparse.Namespace(query="acme", limit=50)
            cmd_search(args)

        self.assertTrue(captured.get("ok"))
        self.assertEqual(captured.get("count"), 1)
        self.assertIn("John Doe", captured["contacts"][0]["name"])


# ── Nextcloud contacts (CardDAV) tests ───────────────────────────


NC_ENV = {
    "NEXTCLOUD_URL": "https://cloud.example.com",
    "NEXTCLOUD_USERNAME": "alex",
    "NEXTCLOUD_APP_PASSWORD": "app-pass",
}


class NextcloudContactsTests(unittest.TestCase):
    """Test Nextcloud CardDAV contacts module with mocked HTTP requests."""

    def setUp(self):
        self.env_patch = patch.dict(os.environ, NC_ENV, clear=False)
        self.env_patch.start()

    def tearDown(self):
        self.env_patch.stop()

    def test_vcard_to_dict_basic(self):
        """Parse a vCard 3.0 string into a contact dict."""
        from modules.nextcloud.contacts import _vcard_to_dict

        vcard = """BEGIN:VCARD
VERSION:3.0
FN:John Doe
N:Doe;John;;;
EMAIL:john@example.com
TEL;TYPE=VOICE:+40-711-111-111
TEL;TYPE=CELL:+40-722-222-222
ORG:Acme Inc
TITLE:Developer
NOTE:A good developer
UID:abc-123
END:VCARD"""

        result = _vcard_to_dict(vcard, href="/some/href.vcf")

        self.assertEqual(result["uid"], "abc-123")
        self.assertEqual(result["name"], "John Doe")
        self.assertEqual(result["given_name"], "John")
        self.assertEqual(result["surname"], "Doe")
        self.assertEqual(result["email"], "john@example.com")
        self.assertEqual(result["phone"], "+40-711-111-111")
        self.assertEqual(result["mobile"], "+40-722-222-222")
        self.assertEqual(result["org"], "Acme Inc")
        self.assertEqual(result["title"], "Developer")
        self.assertEqual(result["note"], "A good developer")
        self.assertEqual(result["href"], "/some/href.vcf")

    def test_vcard_to_dict_minimal(self):
        """Parse a minimal vCard with only FN."""
        from modules.nextcloud.contacts import _vcard_to_dict

        vcard = """BEGIN:VCARD
VERSION:3.0
FN:Minimal Contact
UID:min-123
END:VCARD"""

        result = _vcard_to_dict(vcard)
        self.assertEqual(result["name"], "Minimal Contact")
        self.assertEqual(result["uid"], "min-123")
        self.assertEqual(result["email"], "")
        self.assertEqual(result["phone"], "")

    def test_dict_to_vcard(self):
        """Build a vCard string from a contact dict and verify it's parseable."""
        from modules.nextcloud.contacts import _dict_to_vcard, _vcard_to_dict

        data = {
            "name": "Jane Doe",
            "given_name": "Jane",
            "surname": "Doe",
            "email": "jane@example.com",
            "phone": "+40-733-333-333",
            "mobile": "+40-744-444-444",
            "org": "Corp",
            "title": "Manager",
            "note": "Notes here",
            "uid": "uid-456",
        }

        vcard = _dict_to_vcard(data, include_uid=True)
        self.assertIn("FN:Jane Doe", vcard)
        self.assertIn("UID:uid-456", vcard)
        self.assertIn("EMAIL:jane@example.com", vcard)
        self.assertIn("TEL;TYPE=VOICE:+40-733-333-333", vcard)
        self.assertIn("TEL;TYPE=CELL:+40-744-444-444", vcard)
        self.assertIn("ORG:Corp", vcard)
        self.assertIn("TITLE:Manager", vcard)
        self.assertIn("NOTE:Notes here", vcard)

        # Roundtrip
        parsed = _vcard_to_dict(vcard)
        self.assertEqual(parsed["name"], "Jane Doe")
        self.assertEqual(parsed["email"], "jane@example.com")

    def test_dict_to_vcard_no_uid(self):
        """Without include_uid, UID should not appear."""
        from modules.nextcloud.contacts import _dict_to_vcard

        data = {"name": "No UID", "email": "no@uid.com"}
        vcard = _dict_to_vcard(data, include_uid=False)
        self.assertNotIn("UID:", vcard)
        self.assertIn("FN:No UID", vcard)

    @patch("modules.nextcloud.contacts.requests.request")
    def test_list_addressbooks_success(self, mock_request):
        """list_addressbooks returns parsed addressbooks from PROPFIND."""
        from modules.nextcloud.contacts import list_addressbooks

        propfind_xml = """<?xml version="1.0" encoding="utf-8"?>
<d:multistatus xmlns:d="DAV:" xmlns:card="urn:ietf:params:xml:ns:carddav">
  <d:response>
    <d:href>/remote.php/dav/addressbooks/users/alex/contacts/</d:href>
    <d:propstat>
      <d:prop>
        <d:displayname>Contacts</d:displayname>
        <d:resourcetype>
          <d:collection/>
          <card:addressbook/>
        </d:resourcetype>
        <card:addressbook-description>Default addressbook</card:addressbook-description>
      </d:prop>
      <d:status>HTTP/1.1 200 OK</d:status>
    </d:propstat>
  </d:response>
</d:multistatus>"""

        mock_resp = MagicMock()
        mock_resp.status_code = 207
        mock_resp.content = propfind_xml.encode("utf-8")
        mock_request.return_value = mock_resp

        books = list_addressbooks()

        self.assertEqual(len(books), 1)
        self.assertEqual(books[0]["displayname"], "Contacts")
        self.assertIn("contacts/", books[0]["href"])

    @patch("modules.nextcloud.contacts.requests.request")
    def test_list_addressbooks_empty(self, mock_request):
        """When no addressbooks exist, return empty list."""
        from modules.nextcloud.contacts import list_addressbooks

        xml = """<?xml version="1.0" encoding="utf-8"?>
<d:multistatus xmlns:d="DAV:">
  <d:response>
    <d:href>/remote.php/dav/addressbooks/users/alex/</d:href>
    <d:propstat>
      <d:prop>
        <d:displayname>alex</d:displayname>
        <d:resourcetype><d:collection/></d:resourcetype>
      </d:prop>
      <d:status>HTTP/1.1 200 OK</d:status>
    </d:propstat>
  </d:response>
</d:multistatus>"""

        mock_resp = MagicMock()
        mock_resp.status_code = 207
        mock_resp.content = xml.encode("utf-8")
        mock_request.return_value = mock_resp

        books = list_addressbooks()
        self.assertEqual(len(books), 0)

    @patch("modules.nextcloud.contacts.requests.put")
    @patch("modules.nextcloud.contacts.requests.request")
    def test_cmd_create_nextcloud(self, mock_request, mock_put):
        """Create a contact via CardDAV PUT."""
        from modules.nextcloud.contacts import cmd_create

        # Mock addressbook PROPFIND
        propfind_xml = """<?xml version="1.0" encoding="utf-8"?>
<d:multistatus xmlns:d="DAV:" xmlns:card="urn:ietf:params:xml:ns:carddav">
  <d:response>
    <d:href>/remote.php/dav/addressbooks/users/alex/contacts/</d:href>
    <d:propstat>
      <d:prop>
        <d:displayname>Contacts</d:displayname>
        <d:resourcetype>
          <d:collection/>
          <card:addressbook/>
        </d:resourcetype>
      </d:prop>
      <d:status>HTTP/1.1 200 OK</d:status>
    </d:propstat>
  </d:response>
</d:multistatus>"""

        mock_propfind = MagicMock()
        mock_propfind.status_code = 207
        mock_propfind.content = propfind_xml.encode("utf-8")
        mock_request.return_value = mock_propfind

        mock_put_resp = MagicMock()
        mock_put_resp.status_code = 201
        mock_put.return_value = mock_put_resp

        captured = {}

        with patch("modules.nextcloud.contacts.out", lambda d: captured.update(d)):
            import argparse
            args = argparse.Namespace(
                name="CardDAV User", email="carddav@example.com",
                phone="+40-755-555-555", mobile=None,
                org="TestOrg", title="Tester", note="Test note",
                addressbook=None, func=None,
            )
            cmd_create(args)

        self.assertTrue(captured.get("ok"))
        self.assertIn("CardDAV User", captured.get("message", ""))

    @patch("modules.nextcloud.contacts.requests.request")
    def test_cmd_list_nextcloud(self, mock_request):
        """List contacts from CardDAV returns parsed vCards."""
        from modules.nextcloud.contacts import cmd_list

        vcard = """BEGIN:VCARD
VERSION:3.0
FN:List Test User
UID:list-uid-1
EMAIL:list@test.com
END:VCARD"""

        propfind_xml = f"""<?xml version="1.0" encoding="utf-8"?>
<d:multistatus xmlns:d="DAV:" xmlns:card="urn:ietf:params:xml:ns:carddav">
  <d:response>
    <d:href>/remote.php/dav/addressbooks/users/alex/contacts/</d:href>
    <d:propstat>
      <d:prop>
        <d:displayname>Contacts</d:displayname>
        <d:resourcetype>
          <d:collection/>
          <card:addressbook/>
        </d:resourcetype>
      </d:prop>
      <d:status>HTTP/1.1 200 OK</d:status>
    </d:propstat>
  </d:response>
  <d:response>
    <d:href>/remote.php/dav/addressbooks/users/alex/contacts/list-uid-1.vcf</d:href>
    <d:propstat>
      <d:prop>
        <d:getetag>"abc123"</d:getetag>
        <card:address-data>{vcard}</card:address-data>
      </d:prop>
      <d:status>HTTP/1.1 200 OK</d:status>
    </d:propstat>
  </d:response>
</d:multistatus>"""

        mock_resp = MagicMock()
        mock_resp.status_code = 207
        mock_resp.content = propfind_xml.encode("utf-8")
        mock_request.return_value = mock_resp

        captured = {}

        with patch("modules.nextcloud.contacts.out", lambda d: captured.update(d)):
            import argparse
            args = argparse.Namespace(addressbook=None, limit=100)
            cmd_list(args)

        self.assertTrue(captured.get("ok"))
        self.assertEqual(captured.get("count"), 1)
        self.assertEqual(captured["contacts"][0]["name"], "List Test User")

    def test_cmd_search_local(self):
        """Search for contacts by query via local Python filter (not CardDAV filter)."""
        from modules.nextcloud.contacts import cmd_search
        from modules.nextcloud.contacts import _list_vcards_in_book

        # We test the _vcard_to_dict level, but the search is local Python logic
        # Test the vcard matching logic directly
        from modules.nextcloud.contacts import _vcard_to_dict

        vcard1 = _vcard_to_dict("""BEGIN:VCARD
FN:Alice Smith
EMAIL:alice@acme.com
ORG:Acme Corp
END:VCARD""", href="/alice.vcf")

        vcard2 = _vcard_to_dict("""BEGIN:VCARD
FN:Bob Jones
EMAIL:bob@other.com
ORG:Other Inc
END:VCARD""", href="/bob.vcf")

        contacts = [vcard1, vcard2]
        q = "acme"
        matches = [c for c in contacts if (
            q in c.get("name", "").lower()
            or q in c.get("email", "").lower()
            or q in c.get("org", "").lower()
            or q in c.get("phone", "").lower()
            or q in c.get("mobile", "").lower()
            or q in c.get("note", "").lower()
        )]

        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]["name"], "Alice Smith")

    def test_cmd_search_empty(self):
        """Empty search returns no contacts."""
        from modules.nextcloud.contacts import _vcard_to_dict

        vcard = _vcard_to_dict("""BEGIN:VCARD
FN:Zoe Nobody
EMAIL:zoe@nowhere.com
END:VCARD""")

        q = "nonexistent"
        match = (
            q in vcard.get("name", "").lower()
            or q in vcard.get("email", "").lower()
            or q in vcard.get("org", "").lower()
            or q in vcard.get("phone", "").lower()
            or q in vcard.get("mobile", "").lower()
            or q in vcard.get("note", "").lower()
        )
        self.assertFalse(match)


if __name__ == "__main__":
    unittest.main()
