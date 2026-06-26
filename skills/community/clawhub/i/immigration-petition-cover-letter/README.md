# USCIS Petition Cover Letter Drafter

**Platforms:** Claude · Openclaw · Codex
**Domain:** U.S. Immigration Law — USCIS Petitions & Applications

## Purpose

A petition-cover-letter drafting partner for immigration attorneys, accredited representatives (BIA-recognized organizations under 8 CFR § 1292.11–.20), in-house immigration counsel, and supervising paralegals. Turns a single USCIS petition or application — and the assembled evidence — into a structured DRAFT cover letter and tabbed exhibit list that walks every named statutory and regulatory eligibility criterion, maps each piece of evidence to the criterion it supports, computes filing fees, and routes to the correct USCIS filing office or Lockbox / e-filing channel for **attorney-of-record review and signature** before filing.

## When to Use

- Drafting a cover letter for I-129 H-1B / H-1B1 / E-3 / TN / L-1A / L-1B / O-1A / O-1B / P / R petitions
- Drafting a cover letter for I-140 EB-1A Extraordinary Ability, EB-1B Outstanding Researcher, EB-1C Multinational Manager, EB-2 / EB-3, EB-2 NIW (National Interest Waiver), EB-5 I-526E
- Drafting a cover letter for I-130 family-based petitions and I-130A spouse beneficiary supplement
- Drafting a cover letter for I-485 Adjustment of Status, I-589 Asylum, I-918 / I-914 / I-360 (VAWA, SIJS, Religious Worker), N-400 Naturalization
- Standardizing exhibit indexing, criterion-to-evidence mapping, and filing-fee computation across a firm's case docket
- Building the cover-letter spine before declarations, expert opinion letters, and the petition forms are finalized
- Re-using the same workflow to draft a Premium Processing I-907 add-on or to convert the cover letter into an RFE-response shell when an RFE arrives

## What It Does

**Phase 1: Attorney, petition, and parties**
1. Captures attorney / accredited-rep name, G-28 / G-28I status, firm, A-number / EOIR ID (where applicable)
2. Captures petition type, USCIS form number(s), edition date, eligibility basis (statute and regulation), and filing posture (new petition / amendment / extension / change of employer / change of status / consular notification / Premium Processing)
3. Captures petitioner (employer, family member, self) and beneficiary identifiers (handled with confidentiality discipline)

**Phase 2: Eligibility criteria walk**
4. Routes the petition to the correct statutory / regulatory criteria spine (e.g., EB-1A — 8 CFR § 204.5(h)(3) ten criteria + final-merits determination per *Kazarian v. USCIS*; EB-2 NIW — *Matter of Dhanasar* three prongs; O-1A — 8 CFR § 214.2(o)(3)(iii); H-1B specialty-occupation — 8 CFR § 214.2(h)(4)(iii)(A); I-130 — INA § 201(b)/203(a) qualifying relationship; I-589 — INA § 208 nexus to a protected ground; N-400 — INA §§ 316/319 residence, physical presence, GMC, English / civics)
5. Walks each criterion one at a time, asking the user which criteria the case relies on and what evidence has been gathered for each

**Phase 3: Evidence-to-criterion mapping**
6. Builds a per-criterion evidence table — every exhibit gets a tab letter / number, a description, a date, a source, and the criterion(s) it supports; orphan exhibits (no criterion mapped) are flagged for removal or re-purposing
7. Flags missing critical evidence per criterion (e.g., EB-1A "original contributions of major significance" without independent expert letters; H-1B specialty occupation without a degree-requirement employer attestation; I-130 marriage-based without bona-fide-marriage evidence)
8. Notes any beneficiary admissibility / waiver issues identified by the user (INA § 212(a) grounds; § 212(h)/(i) / § 245(i) / VAWA / TPS / DACA history) for attorney review — does not assess admissibility itself

**Phase 4: Filing logistics**
9. Computes base filing fee + biometric fee (where applicable) + Asylum Program Fee (where applicable) + Premium Processing I-907 fee (where elected), and verifies the user's stated edition dates of every form
10. Routes to the correct Lockbox or Service Center / Field Office / online filing under current USCIS direct-filing addresses
11. Captures concurrent filings (I-907, I-765, I-131, I-485, I-130 family member) and confirms cross-references in the cover letter

**Phase 5: Cover letter drafting**
12. Drafts a single-issue cover letter with: caption block, RE-line block (petition, petitioner, beneficiary, A-numbers, receipt numbers where applicable), table of contents of exhibits, plain-English statement of relief sought, criterion-by-criterion analysis with exhibit citations, request for approval and (where applicable) consular notification / change of status, premium-processing election, and an unsigned attorney-of-record signature block
13. Caps the cover letter at the firm-appropriate length and recommends sections to move to a stand-alone brief if they exceed a single-issue cover letter's scope (e.g., a freestanding *Dhanasar* brief, a freestanding NIW national-importance memo)
14. Produces a numbered exhibit list / tab index with each tab carrying one document type, the criterion it supports, and the page count

**Phase 6: Quality self-check**
15. Runs an explicit self-check (every criterion mapped to evidence, no orphan exhibits, fees correct, form edition dates verified, no admissibility opinion offered, no UPL exposure, attorney signature block unsigned, identifier handling correct)
16. Produces a DRAFT marked for the attorney of record — agent never files, never signs G-28, never holds itself out as counsel, and never gives the petitioner or beneficiary legal advice directly

## Output

A DRAFT cover-letter packet with:

- Cover letter (caption, RE-line block, table of contents, requested relief, criterion-by-criterion analysis with inline exhibit citations, premium-processing election if any, concurrent-filings cross-reference, signature block — unsigned)
- Tabbed exhibit list (Tab A / B / C … or 1 / 2 / 3 …, document description, source, date, page count, criterion(s) supported)
- Filing-fee computation worksheet (base fee, biometric, Asylum Program Fee, I-907, total) and check / e-filing instructions
- Filing-channel routing (Lockbox address / Service Center / online USCIS-account)
- Concurrent-filing checklist
- Self-check rubric output
- Unresolved-information list (missing evidence by criterion; admissibility / waiver issues flagged to counsel)

## Safety

This skill drafts a cover letter, **not** legal advice and **not** a filing. Every output is labeled **DRAFT — ATTORNEY OF RECORD MUST REVIEW AND SIGN BEFORE FILING**. The agent never (i) files with USCIS, USCIS online account, or Lockbox; (ii) signs the G-28 / Form / cover letter / declaration; (iii) issues legal advice to the petitioner, beneficiary, or third party; (iv) opines on admissibility, deportability, criminal-immigration consequences, the "extreme hardship" standard, or asylum-claim credibility; (v) drafts client declarations as if from the declarant; (vi) speaks to USCIS / ICE / EOIR / consular officers; (vii) recommends a filing strategy that would constitute the Unauthorized Practice of Law if executed without a licensed attorney or accredited representative. The agent treats the beneficiary's A-number, receipt number, passport number, SSN, date of birth, and home address as confidential — recorded in the structured fields only and never pasted into narrative blocks. Where the user is not a licensed attorney or BIA-accredited representative, the agent works only on document-preparation tasks and never explains rights, eligibility, or filing strategy to the petitioner or beneficiary directly.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.
