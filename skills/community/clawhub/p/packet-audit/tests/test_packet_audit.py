#!/usr/bin/env python3
"""Fixture-driven tests for packet-audit.

Every test builds its own packet in a temporary folder, so the suite carries no
sample documents and cannot drift from what the engine actually reads.
"""

from __future__ import annotations

import hashlib
import io
import json
import shutil
import sys
import tempfile
import unittest
import zipfile
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import packet_audit as pa  # noqa: E402

DECISION = "2027-06-01"

CLEAN = {
    "id.txt": (
        "GOVERNMENT PHOTO ID\n"
        "Name: Jordan Alvarez\n"
        "Date of birth: 03/14/1989\n"
        "Date of expiry: 11/02/2030\n"
    ),
    "payslip.txt": (
        "PAYSLIP\n"
        "Name: Jordan Alvarez\n"
        "Employer: Northwind Logistics LLC\n"
        "Gross pay: 4,200.00\n"
        "Pay period: May 2027\n"
    ),
    "employment.txt": (
        "EMPLOYMENT VERIFICATION LETTER\n"
        "Full name: Jordan Alvarez\n"
        "Employer: Northwind Logistics LLC\n"
        "Monthly income: 4,200.00\n"
    ),
    "application.txt": (
        "RENTAL APPLICATION FORM\n"
        "Applicant name: Jordan Alvarez\n"
        "Address: 448 Cedar Street Apt 3B, Denver CO 80211\n"
        "Employer: Northwind Logistics LLC\n"
    ),
    "bank.txt": (
        "ACCOUNT STATEMENT\n"
        "Name: Jordan Alvarez\n"
        "Address: 448 Cedar St Apt 3B, Denver CO 80211\n"
        "Opening balance: 5,000.00\n"
        "Closing balance: 6,200.00\n"
        "Statement period: May 2027\n"
    ),
}


def write_packet(folder: Path, files: dict[str, str | bytes]) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    for name, body in files.items():
        path = folder / name
        if isinstance(body, bytes):
            path.write_bytes(body)
        else:
            path.write_text(body, encoding="utf-8")


def run(folder: Path, profile: str = "rental-us", extra: list[str] | None = None):
    out = folder / "out"
    argv = ["--folder", str(folder), "--profile", profile, "--decision-date", DECISION,
            "--out", str(out), "--now", "2027-05-01T00:00:00"]
    return pa.main(argv + (extra or []))


def codes(report: dict) -> list[str]:
    return [f["code"] for f in report["findings"]]


class CleanPacket(unittest.TestCase):
    def test_clean_packet_is_ready_with_no_findings(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / "packet"
            write_packet(folder, CLEAN)
            report = pa.audit(folder, pa.load_profile(ROOT / "profiles" / "rental-us.json"),
                              pa.parse_iso(DECISION), "2027-05-01T00:00:00")
            self.assertEqual(report["findings"], [], codes(report))
            self.assertEqual(report["verdict"], "READY")
            self.assertEqual(report["counts"]["error"], 0)

    def test_clean_packet_exits_zero_and_writes_three_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / "packet"
            write_packet(folder, CLEAN)
            self.assertEqual(run(folder), 0)
            out = folder / "out"
            for name in ("packet-report.md", "packet-report.json", "packet-manifest.json"):
                self.assertTrue((out / name).is_file(), name)

    def test_manuscript_matches_recomputed_hashes(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / "packet"
            write_packet(folder, CLEAN)
            run(folder)
            manifest = json.loads((folder / "out" / "packet-manifest.json").read_text())
            self.assertEqual(manifest["schema"], "packet-audit/manifest/1")
            self.assertEqual(len(manifest["files"]), len(CLEAN))
            for entry in manifest["files"]:
                digest = hashlib.sha256((folder / entry["path"]).read_bytes()).hexdigest()
                self.assertEqual(entry["sha256"], digest)

    def test_address_wording_synonyms_are_not_a_finding(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / "packet"
            write_packet(folder, CLEAN)
            report = pa.audit(folder, pa.load_profile(ROOT / "profiles" / "rental-us.json"),
                              pa.parse_iso(DECISION), "2027-05-01T00:00:00")
            self.assertNotIn("PA-C01", codes(report))


class SeededFailures(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.folder = Path(self.tmp.name) / "packet"
        files = dict(CLEAN)
        files["id.txt"] = CLEAN["id.txt"].replace("11/02/2030", "12/01/2026")
        files["payslip.txt"] = CLEAN["payslip.txt"].replace("Jordan Alvarez", "Jordan Alverez") \
                                                  .replace("4,200.00", "4,000.00")
        files["bank.txt"] = CLEAN["bank.txt"].replace("448 Cedar St", "512 Cedar St")
        files["photo.jpg"] = b"\xff\xd8\xff\xe0not-really-a-jpeg"
        files["application copy.txt"] = CLEAN["application.txt"]
        write_packet(self.folder, files)
        self.report = pa.audit(self.folder,
                               pa.load_profile(ROOT / "profiles" / "rental-us.json"),
                               pa.parse_iso(DECISION), "2027-05-01T00:00:00")

    def tearDown(self):
        self.tmp.cleanup()

    def test_expired_id_is_reported(self):
        self.assertIn("PA-X01", codes(self.report))

    def test_name_conflict_is_reported(self):
        conflicts = [f for f in self.report["findings"] if f["code"] == "PA-C01" and f["field"] == "full_name"]
        self.assertTrue(conflicts, codes(self.report))
        docs = set(conflicts[0]["docs"])
        self.assertIn("id.txt", docs)

    def test_address_number_conflict_is_reported(self):
        conflicts = [f for f in self.report["findings"] if f["code"] == "PA-C01" and f["field"] == "address"]
        self.assertTrue(conflicts, codes(self.report))
        self.assertIn("512", conflicts[0]["detail"])

    def test_unreadable_image_is_a_warning_not_a_guess(self):
        unreadable = [f for f in self.report["findings"] if f["code"] == "PA-R01"]
        self.assertTrue(unreadable)
        self.assertIn("photo.jpg", unreadable[0]["docs"])
        self.assertIn("OCR", unreadable[0]["detail"])

    def test_duplicate_is_noted(self):
        self.assertIn("PA-D01", codes(self.report))

    def test_verdict_and_exit_code_block(self):
        self.assertEqual(self.report["verdict"], "NOT READY")
        self.assertEqual(run(self.folder), 2)

    def test_every_finding_cites_a_document(self):
        for item in self.report["findings"]:
            if item["code"] in {"PA-E01"}:
                continue
            self.assertTrue(item["docs"], item["code"])


class AuthoritativeDocument(unittest.TestCase):
    def test_absent_optional_primary_is_silent(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / "packet"
            files = dict(CLEAN)
            del files["employment.txt"]
            write_packet(folder, files)
            report = pa.audit(folder, pa.load_profile(ROOT / "profiles" / "rental-us.json"),
                              pa.parse_iso(DECISION), "2027-05-01T00:00:00")
            self.assertNotIn("PA-C03", codes(report))

    def test_present_primary_without_the_field_is_flagged(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / "packet"
            files = dict(CLEAN)
            files["id.txt"] = ("GOVERNMENT PHOTO ID\nDate of birth: 03/14/1989\n"
                               "Date of expiry: 11/02/2030\n")
            write_packet(folder, files)
            report = pa.audit(folder, pa.load_profile(ROOT / "profiles" / "rental-us.json"),
                              pa.parse_iso(DECISION), "2027-05-01T00:00:00")
            c03 = [f for f in report["findings"] if f["code"] == "PA-C03"]
            self.assertTrue(c03, codes(report))
            self.assertIn("full name", c03[0]["detail"].lower())


class MissingDocuments(unittest.TestCase):
    def test_missing_required_document_blocks(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / "packet"
            write_packet(folder, {"application.txt": CLEAN["application.txt"]})
            report = pa.audit(folder, pa.load_profile(ROOT / "profiles" / "rental-us.json"),
                              pa.parse_iso(DECISION), "2027-05-01T00:00:00")
            missing = [f for f in report["findings"] if f["code"] == "PA-E01"]
            self.assertGreaterEqual(len(missing), 2)
            self.assertTrue(any("photo ID" in f["detail"] for f in missing))
            self.assertEqual(report["verdict"], "NOT READY")

    def test_missing_required_field_is_a_warning(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / "packet"
            files = dict(CLEAN)
            files["payslip.txt"] = "PAYSLIP\nName: Jordan Alvarez\nPay period: May 2027\n"
            write_packet(folder, files)
            report = pa.audit(folder, pa.load_profile(ROOT / "profiles" / "rental-us.json"),
                              pa.parse_iso(DECISION), "2027-05-01T00:00:00")
            self.assertIn("PA-F01", codes(report))


class Extraction(unittest.TestCase):
    def test_docx_text_is_extracted_with_stdlib(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "letter.docx"
            document = (
                '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
                "<w:body><w:p><w:r><w:t>Name: Jordan Alvarez</w:t></w:r></w:p>"
                "<w:p><w:r><w:t>Date of birth: 03/14/1989</w:t></w:r></w:p></w:body></w:document>"
            )
            with zipfile.ZipFile(path, "w") as zf:
                zf.writestr("word/document.xml", document)
            pages, method = pa.extract(path, ".docx")
            self.assertEqual(method, "docx")
            self.assertIn("Jordan Alvarez", pages[0])
            self.assertIn("\n", pages[0])

    def test_sidecar_text_stands_in_for_a_pdf(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / "packet"
            folder.mkdir()
            (folder / "bank.pdf").write_bytes(b"%PDF-1.4 not a real pdf")
            (folder / "bank.pdf.txt").write_text(CLEAN["bank.txt"], encoding="utf-8")
            entry = pa.extract(folder / "bank.pdf", ".pdf")
            self.assertEqual(entry[1], "sidecar")
            self.assertIsNotNone(entry[0])

    def test_date_order_follows_the_profile(self):
        self.assertEqual(pa.normalise_date("12/01/2026", "mdy"), "2026-12-01")
        self.assertEqual(pa.normalise_date("12/01/2026", "dmy"), "2026-01-12")
        self.assertEqual(pa.normalise_date("03/14/1989", "mdy"), "1989-03-14")
        self.assertEqual(pa.normalise_date("14/03/1989", "mdy"), "1989-03-14")
        self.assertIsNone(pa.normalise_date("not a date", "mdy"))

    def test_unknown_binary_is_reported_not_parsed(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "payload.bin"
            path.write_bytes(b"\x00\x01\x02")
            pages, method = pa.extract(path, ".bin")
            self.assertIsNone(pages)
            self.assertIn("unsupported", method)


class Profiles(unittest.TestCase):
    def test_shipped_profiles_validate(self):
        profiles = sorted((ROOT / "profiles").glob("*.json"))
        self.assertGreaterEqual(len(profiles), 3)
        for path in profiles:
            profile = pa.load_profile(path)
            self.assertTrue(profile["id"])

    def test_invalid_profile_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "broken.json"
            path.write_text(json.dumps({"id": "broken"}), encoding="utf-8")
            with self.assertRaises(pa.ProfileError):
                pa.load_profile(path)

    def test_list_profiles_prints_each_id(self):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            code = pa.main(["--list-profiles"])
        self.assertEqual(code, 0)
        for path in (ROOT / "profiles").glob("*.json"):
            self.assertIn(path.stem, buffer.getvalue())


class CommandLine(unittest.TestCase):
    def test_bad_arguments_exit_three(self):
        with tempfile.TemporaryDirectory() as tmp:
            with redirect_stderr(io.StringIO()):
                self.assertEqual(pa.main(["--folder", tmp]), 3)

    def test_missing_folder_exits_three(self):
        with redirect_stderr(io.StringIO()):
            self.assertEqual(pa.main(["--folder", "/nope/nope", "--profile", "rental-us"]), 3)

    def test_json_flag_prints_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / "packet"
            write_packet(folder, CLEAN)
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                pa.main(["--folder", str(folder), "--profile", "rental-us",
                         "--decision-date", DECISION, "--out", str(folder / "out"),
                         "--now", "2027-05-01T00:00:00", "--json"])
            payload = json.loads(buffer.getvalue())
            self.assertEqual(payload["schema"], "packet-audit/report/1")
            self.assertEqual(payload["verdict"], "READY")


class OtherProfile(unittest.TestCase):
    def test_schengen_packet_runs_on_its_own_profile(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / "packet"
            write_packet(folder, {
                "passport.txt": ("PASSPORT\nSurname and forenames: Jordan Alvarez\n"
                                 "Date of birth: 14/03/1989\nDate of expiry: 02/11/2030\n"),
                "insurance.txt": ("TRAVEL INSURANCE POLICY\nFull name: Jordan Alvarez\n"
                                  "Sum insured: 30000\nEnd of cover: 20/12/2027\n"),
                "bank.txt": ("ACCOUNT STATEMENT\nName: Jordan Alvarez\n"
                             "Closing balance: 6,200.00\nStatement period: May 2027\n"),
                "hotel.txt": ("BOOKING CONFIRMATION\nFull name: Jordan Alvarez\n"
                              "Check-in: 01/07/2027\nCheck-out: 08/07/2027\nNights: 7\n"),
                "flights.txt": ("ITINERARY\nFull name: Jordan Alvarez\n"
                                "Departure: 01/07/2027\nArrival: 01/07/2027\n"),
            })
            out = folder / "out"
            code = pa.main(["--folder", str(folder), "--profile", "schengen-visa",
                            "--decision-date", "2027-06-01", "--out", str(out),
                            "--now", "2027-05-01T00:00:00"])
            report = json.loads((out / "packet-report.json").read_text())
            self.assertEqual(report["counts"]["error"], 0,
                             [f["code"] + ": " + f["detail"] for f in report["findings"]])
            self.assertEqual(code, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
