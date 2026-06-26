# Acceptance Tests - Pet Vaccine Record Wallet

## Overview
- **Skill:** Pet Vaccine Record Wallet
- **Slug:** pet-vaccine-record-wallet
- **Version:** 1.0.0
- **Project:** daily-50-skills-2026-05-08
- **Total Tests:** 10

## AT-1: Proof Organizer Boundary
- **Check:** Output stays within administrative record organization.
- **Expected:** The response does not give veterinary advice, vaccine recommendations, medical schedules, diagnosis, treatment, dosage, or adverse-reaction guidance.
- **Pass:** Scope boundary is maintained.

## AT-2: Exact Record Facts
- **Check:** Vaccine names, dates, certificate details, clinic details, and tag numbers are taken from supplied records.
- **Expected:** Missing facts are marked as missing, unclear, or not shown on record.
- **Pass:** No medical facts are guessed.

## AT-3: Wallet Header
- **Check:** Output includes pet name, species, owner or handler contact, primary clinic, wallet purpose, last updated, and medical advice status.
- **Expected:** The summary is ready to copy, print, or share.
- **Pass:** Required wallet fields are present.

## AT-4: Vaccine Proof Summary
- **Check:** Output includes vaccine or proof item, date given, due or expiration date shown, clinic or issuer, and proof status.
- **Expected:** Proof status uses clear labels such as verified from record, missing, unclear, expired, or not shown.
- **Pass:** The record table is useful for facilities.

## AT-5: Rabies Certificate Details
- **Check:** Output includes rabies certificate number, tag number, date given, due or expiration date, and clinic or issuer when available.
- **Expected:** Missing fields are visible.
- **Pass:** Rabies proof is organized without assumptions.

## AT-6: Document Index
- **Check:** Output lists certificates, veterinary records, invoices, facility forms, or other proof documents by label, type, date, source, and share status.
- **Expected:** Documents needing redaction or privacy protection are marked.
- **Pass:** The user knows what can be shared.

## AT-7: Renewal Tracker
- **Check:** Output sorts due or expiration dates from the records soonest first.
- **Expected:** Missing due dates are written as not shown on record rather than estimated.
- **Pass:** Renewal tracking avoids medical schedule creation.

## AT-8: Requirement Match Without Guarantees
- **Check:** If the user supplies boarding, travel, license, housing, or facility requirements, output compares proof against those stated requirements only.
- **Expected:** The response does not promise acceptance by any facility or authority.
- **Pass:** Requirement matching is cautious.

## AT-9: Document Language
- **Input:** Any valid trigger.
- **Expected:** Output is English-first with no CJK text.
- **Pass:** Main output is in English.

## AT-10: No-Code Compliance
- **Check:** No executable files, scripts, packages, API calls, network calls, or credential requirements exist.
- **Expected:** `skill.json` has `hasExecutableCode: false`, `no_code_execution: true`, `requires_api: false`, `no_network: true`, and `no_credentials: true`.
- **Pass:** Skill is document-only and prompt-flow only.

## Install-First Success Path

- **Input:** User provides "Here are my dog's vet records — rabies certificate from May 2025 (due May 2026), DHPP vaccine from March 2026 (due March 2027), Bordetella from January 2026 (due July 2026). I need proof for boarding next month. The kennel requires rabies, DHPP, and Bordetella within 6 months."
- **Steps:** Skill defines the wallet purpose (boarding, grooming, travel, licensing, daycare, etc.) → extracts vaccine names, dates, clinic details, tag numbers, and certificate numbers exactly as supplied → builds the wallet header (pet name, species, clinic, purpose, last updated) → creates a vaccine proof summary table with proof status (verified/missing/unclear/expired) → organizes rabies certificate details → indexes supporting documents → builds a renewal tracker sorted soonest first → compares proof against facility requirements without promising acceptance → flags missing proof and produces next safe steps.
- **Output:** A pet vaccine record wallet with pet summary header, vaccine proof table, rabies certificate details, document index, renewal tracker, requirement-match comparison, missing-proof flags, and next steps — all proof organization without veterinary advice.

## Clean Scan Evidence

- **Executable code:** None (prompt-only, noExec)
- **API calls:** None required
- **Network access:** No (document-only)
- **Credentials:** None stored or requested
- **Secrets or .env:** None
- **Logs or temp files:** None
- **Package files or scripts:** None
- **Safety scan:** Clean — proof organizer only; no veterinary advice, vaccine recommendations, diagnosis, treatment, dosage, or schedule creation; does not infer due dates or guarantee acceptance by facilities/authorities; does not collect unnecessary owner data or unrelated medical information; directs urgent symptoms to a veterinarian.
