#!/usr/bin/env python3
"""Tests for the bundled PDF reader (scripts/pdftext.py) and its use by the audit.

Every fixture PDF is assembled here, byte by byte, so the suite carries no sample documents
and cannot drift from what the reader actually handles.
"""

from __future__ import annotations

import sys
import tempfile
import unittest
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import packet_audit as pa  # noqa: E402
import pdftext  # noqa: E402

DECISION = "2027-06-01"


# ---------------------------------------------------------------------------
# fixture builders
# ---------------------------------------------------------------------------

def assemble(objects: list[bytes], trailer: bytes = b"/Root 1 0 R") -> bytes:
    out = bytearray(b"%PDF-1.4\n")
    for number, body in enumerate(objects, 1):
        out += b"%d 0 obj\n" % number + body + b"\nendobj\n"
    out += b"trailer\n<< " + trailer + b" >>\n%%EOF\n"
    return bytes(out)


def stream(body: bytes, compress: bool = True) -> bytes:
    data = zlib.compress(body) if compress else body
    filt = b"/Filter /FlateDecode " if compress else b""
    return b"<< /Length %d " % len(data) + filt + b" >>\nstream\n" + data + b"\nendstream"


def single_page(content: bytes, font: bytes | None = None,
                extra_objects: list[bytes] | None = None) -> bytes:
    font = font or b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
        b"/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
        font,
        stream(content),
    ] + list(extra_objects or [])
    return assemble(objects)


CMAP = b"""begincmap
1 begincodespacerange <0000> <FFFF> endcodespacerange
1 beginbfrange <0001> <0005> <0041> endbfrange
2 beginbfchar <0006> <006E> <0007> <0061> <0008> <006D> endbfchar
endcmap"""


def write(tmp: str, name: str, data: bytes) -> Path:
    path = Path(tmp) / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return path


# ---------------------------------------------------------------------------
# reader
# ---------------------------------------------------------------------------

class ReadsText(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def test_simple_text_layer(self):
        path = write(self.tmp.name, "a.pdf", single_page(
            b"BT /F1 12 Tf 72 700 Td (Name: Jordan Alvarez) Tj ET\n"
            b"BT /F1 12 Tf 72 680 Td (Date of expiry: 11/02/2030) Tj ET"))
        text = "\n".join(pdftext.extract_pages(path))
        self.assertIn("Jordan Alvarez", text)
        self.assertIn("11/02/2030", text)

    def test_glyph_by_glyph_positioning_keeps_words_together(self):
        # The pattern that breaks naive readers: one Td + Tj per glyph. Deltas are the real
        # advances for a Courier glyph (600/1000 em at 50 pt = 30 units), as a writer would emit.
        word = "TD Canada Trust"
        body = b"BT /F1 50 Tf 100 700 Td "
        for char in word:
            body += b"(" + char.encode() + b") Tj 30 0 Td "
        body += b"ET"
        font = (b"<< /Type /Font /Subtype /Type1 /BaseFont /Courier /FirstChar 32 "
                b"/LastChar 126 /Widths [" + b" ".join(b"600" for _ in range(95)) + b"] >>")
        path = write(self.tmp.name, "b.pdf", single_page(body, font=font))
        text = "\n".join(pdftext.extract_pages(path))
        self.assertIn("TD Canada Trust", text)
        self.assertNotIn("T D C", text)

    def test_imprecise_advances_do_not_split_words(self):
        # Real writers round advances; a 1-point slop on a 12 pt font must not become a space.
        font = (b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /FirstChar 32 "
                b"/LastChar 126 /Widths [" + b" ".join(b"500" for _ in range(95)) + b"] >>")
        body = b"BT /F1 12 Tf 72 700 Td (Hello) Tj 31 0 Td (World) Tj ET"
        path = write(self.tmp.name, "b2.pdf", single_page(body, font=font))
        self.assertIn("HelloWorld", "\n".join(pdftext.extract_pages(path)).replace("\n", ""))

    def test_two_byte_codes_follow_tounicode(self):
        font = (b"<< /Type /Font /Subtype /Type0 /BaseFont /X /Encoding /Identity-H "
                b"/ToUnicode 6 0 R >>")
        path = write(self.tmp.name, "c.pdf", single_page(
            b"BT /F1 12 Tf 72 700 Td <00010002000300040005> Tj ET",
            font=font,
            extra_objects=[b"<< /Length %d >>\nstream\n" % len(CMAP) + CMAP + b"\nendstream"]))
        text = "\n".join(pdftext.extract_pages(path))
        self.assertIn("ABCDE", text)

    def test_page_order_follows_the_page_tree(self):
        objects = [
            b"<< /Type /Catalog /Pages 2 0 R >>",
            b"<< /Type /Pages /Kids [5 0 R 3 0 R 4 0 R] /Count 3 >>",
            b"<< /Type /Page /Parent 2 0 R /Resources << /Font << /F1 6 0 R >> >> /Contents 7 0 R >>",
            b"<< /Type /Page /Parent 2 0 R /Resources << /Font << /F1 6 0 R >> >> /Contents 7 0 R >>",
            b"<< /Type /Page /Parent 2 0 R /Resources << /Font << /F1 6 0 R >> >> /Contents 7 0 R >>",
            b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
            stream(b"BT /F1 12 Tf 72 700 Td (PAGE-THREE) Tj ET"),
        ]
        # give each page its own content object so the marker identifies it
        for index, marker in ((6, b"PAGE-THREE"), (7, b"PAGE-FOUR"), (8, b"PAGE-FIVE")):
            objects.append(stream(b"BT /F1 12 Tf 72 700 Td (" + marker + b") Tj ET"))
        objects[2] = objects[2].replace(b"7 0 R", b"8 0 R")
        objects[3] = objects[3].replace(b"7 0 R", b"9 0 R")
        objects[4] = objects[4].replace(b"7 0 R", b"10 0 R")
        path = write(self.tmp.name, "d.pdf", assemble(objects))
        text = pdftext.extract_pages(path)
        self.assertEqual([t.strip() for t in text], ["PAGE-FIVE", "PAGE-THREE", "PAGE-FOUR"])

    def test_pages_inside_an_object_stream_are_found(self):
        inner = [
            (10, b"<< /Type /Catalog /Pages 11 0 R >>"),
            (11, b"<< /Type /Pages /Kids [12 0 R] /Count 1 >>"),
            (12, b"<< /Type /Page /Parent 11 0 R /Resources << /Font << /F1 1 0 R >> >> "
                 b"/Contents 2 0 R >>"),
        ]
        header, packed = [], b""
        for number, body in inner:
            header.append(b"%d %d" % (number, len(packed)))
            packed += body + b"\n"
        head = b" ".join(header) + b"\n"
        packed_all = zlib.compress(head + packed)
        objstm = (b"<< /Type /ObjStm /N 3 /First %d /Length %d /Filter /FlateDecode >>\nstream\n"
                  % (len(head), len(packed_all)) + packed_all + b"\nendstream")
        objects = [
            b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
            stream(b"BT /F1 12 Tf 72 700 Td (FROM OBJECT STREAM) Tj ET"),
            objstm,
        ]
        path = write(self.tmp.name, "e.pdf", assemble(objects, trailer=b"/Root 10 0 R"))
        self.assertEqual(pdftext.extract_pages(path)[0].strip(), "FROM OBJECT STREAM")


class RefusesToGuess(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def test_encrypted_pdf_names_the_reason(self):
        path = write(self.tmp.name, "enc.pdf", assemble(
            [b"<< /Type /Catalog /Pages 2 0 R >>",
             b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
             b"<< /Type /Page /Parent 2 0 R /Contents 4 0 R >>",
             stream(b"BT (secret) Tj ET")],
            trailer=b"/Root 1 0 R /Encrypt 9 0 R"))
        with self.assertRaises(pdftext.PDFError) as caught:
            pdftext.extract_pages(path)
        self.assertIn("encrypted", str(caught.exception))

    def test_image_only_pdf_is_not_invented(self):
        path = write(self.tmp.name, "scan.pdf", single_page(b"0 0 100 100 re f"))
        with self.assertRaises(pdftext.PDFError) as caught:
            pdftext.extract_pages(path)
        self.assertIn("text layer", str(caught.exception))

    def test_file_with_pdf_extension_but_no_header(self):
        path = write(self.tmp.name, "fake.pdf", b"this is really a text file")
        with self.assertRaises(pdftext.PDFError) as caught:
            pdftext.extract_pages(path)
        self.assertIn("not a PDF", str(caught.exception))

    def test_missing_file_is_reported_not_crashed(self):
        with self.assertRaises(pdftext.PDFError) as caught:
            pdftext.extract_pages(Path(self.tmp.name) / "nope.pdf")
        self.assertIn("cannot read", str(caught.exception))


class NoThirdPartyImports(unittest.TestCase):
    def test_reader_imports_only_the_standard_library(self):
        source = (ROOT / "scripts" / "pdftext.py").read_text(encoding="utf-8")
        allowed = {"__future__", "base64", "re", "zlib", "pathlib"}
        imported = set()
        for line in source.splitlines():
            line = line.strip()
            if line.startswith("import "):
                imported.add(line.split()[1].split(".")[0])
            elif line.startswith("from "):
                imported.add(line.split()[1].split(".")[0])
        self.assertEqual(imported - allowed, set())


class AuditReadsPdfs(unittest.TestCase):
    TEXT_FILES = {
        "payslip.txt": ("PAYSLIP\nName: Jordan Alvarez\nEmployer: Northwind Logistics LLC\n"
                        "Gross pay: 4,200.00\nPay period: May 2027\n"),
        "employment.txt": ("EMPLOYMENT VERIFICATION LETTER\nFull name: Jordan Alvarez\n"
                           "Employer: Northwind Logistics LLC\nMonthly income: 4,200.00\n"),
        "application.txt": ("RENTAL APPLICATION FORM\nApplicant name: Jordan Alvarez\n"
                            "Address: 448 Cedar Street Apt 3B, Denver CO 80211\n"
                            "Employer: Northwind Logistics LLC\n"),
        "bank.txt": ("ACCOUNT STATEMENT\nName: Jordan Alvarez\n"
                     "Address: 448 Cedar St Apt 3B, Denver CO 80211\n"
                     "Opening balance: 5,000.00\nClosing balance: 6,200.00\n"
                     "Statement period: May 2027\n"),
    }

    def packet(self, expiry: bytes) -> Path:
        folder = Path(self.tmp.name) / "packet"
        folder.mkdir()
        for name, body in self.TEXT_FILES.items():
            (folder / name).write_text(body, encoding="utf-8")
        (folder / "id.pdf").write_bytes(single_page(
            b"BT /F1 12 Tf 72 720 Td (GOVERNMENT PHOTO ID) Tj ET\n"
            b"BT /F1 12 Tf 72 700 Td (Name: Jordan Alvarez) Tj ET\n"
            b"BT /F1 12 Tf 72 680 Td (Date of birth: 03/14/1989) Tj ET\n"
            b"BT /F1 12 Tf 72 660 Td (Date of expiry: " + expiry + b") Tj ET"))
        return folder

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def test_pdf_replaces_a_text_document_in_a_packet(self):
        folder = self.packet(b"11/02/2030")
        report = pa.audit(folder, pa.load_profile(ROOT / "profiles" / "rental-us.json"),
                          pa.parse_iso(DECISION), "2027-05-01T00:00:00")
        found = {f["code"] for f in report["findings"]}
        self.assertNotIn("PA-R01", found, [f["detail"] for f in report["findings"]])
        self.assertEqual(report["verdict"], "READY", [f["detail"] for f in report["findings"]])

    def test_expiry_inside_a_pdf_is_still_caught(self):
        folder = self.packet(b"12/01/2026")
        report = pa.audit(folder, pa.load_profile(ROOT / "profiles" / "rental-us.json"),
                          pa.parse_iso(DECISION), "2027-05-01T00:00:00")
        expiring = [f for f in report["findings"] if f["code"] == "PA-X01"]
        self.assertTrue(expiring, [f["detail"] for f in report["findings"]])
        self.assertIn("id.pdf", expiring[0]["docs"])

    def test_unreadable_pdf_is_a_cited_warning(self):
        folder = self.packet(b"11/02/2030")
        (folder / "id.pdf").write_bytes(assemble(
            [b"<< /Type /Catalog /Pages 2 0 R >>",
             b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
             b"<< /Type /Page /Parent 2 0 R /Contents 4 0 R >>",
             stream(b"BT (secret) Tj ET")],
            trailer=b"/Root 1 0 R /Encrypt 9 0 R"))
        report = pa.audit(folder, pa.load_profile(ROOT / "profiles" / "rental-us.json"),
                          pa.parse_iso(DECISION), "2027-05-01T00:00:00")
        unreadable = [f for f in report["findings"] if f["code"] == "PA-R01"]
        self.assertTrue(unreadable)
        self.assertIn("id.pdf", unreadable[0]["docs"])
        self.assertIn("encrypted", unreadable[0]["detail"])


if __name__ == "__main__":
    unittest.main()
