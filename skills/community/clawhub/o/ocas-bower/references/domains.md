# Domain-Specific Organization Logic

Bower recognizes common life and work domains and applies domain-native organization rules within them. This file defines: how to detect each domain, whether to apply prescriptive or descriptive logic, and what the canonical structure looks like.

---

## Detection and mode selection

**Prescriptive mode** applies when a domain is "clearly started": a top-level or second-level folder exists whose name matches the domain's detection vocabulary, AND it contains at least 5 files or 2 subfolders. In prescriptive mode, Bower proposes moves toward the canonical structure for that domain, including creating missing structural folders.

**Descriptive mode** applies to all other folders: Bower infers your existing variant of organization and extends it without restructuring.

A file may belong to a domain even if it lives outside the domain's root folder. When content classification identifies a file as belonging to a known domain and a domain root exists, that is a location outlier with destination = the domain root (or its appropriate subfolder per canonical structure).

---

## Domain: Taxes

**Detection vocabulary:** "tax", "taxes", "irs", "tax return", "w2", "w-2", "1099", "schedule k", "hmrc", "vat"

**Canonical structure:**
```
Taxes/
  {YYYY}/
    Returns/
    Supporting Documents/
    Correspondence/
  {YYYY}/
    ...
```

**Prescriptive rules:**
- Group by tax year first, always. The year is the primary organizing axis.
- Within a year: Returns (filed documents), Supporting Documents (W-2s, 1099s, receipts, statements), Correspondence (IRS/HMRC letters, notices, refund confirmations).
- A file with a year in its name or content belongs in that year's folder.
- If a tax year folder exists but subfolders do not: propose creating Returns, Supporting Documents, Correspondence.
- Files named or containing "W-2", "1099", "K-1" → Supporting Documents.
- Files named or containing "return", "filing", "form 1040", "form 1120" → Returns.
- Files named or containing "notice", "letter", "correspondence", "CP" + number → Correspondence.

**Naming convention:** year folders use 4-digit year only (e.g. `2024`), not `Tax Year 2024` unless the existing convention already uses that form.

---

## Domain: Projects

**Detection vocabulary:** "projects", "project", "clients", "client work", "engagements", "work"

**Canonical structure:**
```
Projects/
  {Project Name}/
    Brief/
    Assets/
    Deliverables/
    Archive/
  Active/      (optional -- if user has created this)
  Archive/     (optional -- if user has created this)
```

**Prescriptive rules:**
- The primary organizing axis is project name, not date or client.
- Each project gets its own named folder. Files mentioning a project name consistently belong in that project's folder.
- If the user has created Active/ and Archive/ subdirectories, respect that pattern: in-progress projects under Active/, completed ones under Archive/.
- Do not create subfolders (Brief, Assets, Deliverables) unless the project folder already has 10+ files and no existing subfolder structure -- at that point they are worth proposing.
- Files at the root of the Projects folder with a clear project name in their content → propose moving into the named project subfolder.

**Date handling:** dates belong in filenames within a project folder, not in the project folder name itself (unless the project is inherently date-scoped, e.g. "Q1 2026 Campaign").

---

## Domain: Home

**Detection vocabulary:** "home", "house", "apartment", "property", "household", "real estate"

**Canonical structure:**
```
Home/
  {System or Room}/    (e.g. HVAC, Roof, Kitchen, Plumbing, Electrical)
  {Year}/              (if user uses year-based organization)
  Insurance/
  Mortgage/
  Warranties/
  Improvements/
```

**Prescriptive rules:**
- Home organization splits into two valid patterns: system-based (HVAC, Roof, Plumbing) and year-based (2022, 2023). Detect which the user has started and prescribe within that pattern. If both patterns exist, classify files into whichever axis is stronger per-file.
- System-based: files mentioning a specific home system or room → that system's folder.
- Year-based: files with a clear date → that year's folder.
- Warranties, manuals, insurance policies, and mortgage documents are cross-cutting -- always belong in their named folder regardless of which axis dominates.
- Appliance manuals and warranty documents that mention a specific product: propose into Warranties/ with the product name preserved in the filename.

---

## Domain: Finance / Banking

**Detection vocabulary:** "finance", "financial", "banking", "bank", "investments", "brokerage", "accounts", "statements"

**Canonical structure:**
```
Finance/
  {Institution Name}/
    {YYYY}/
      Statements/
      Confirmations/
  Tax Documents/    (overlap with Taxes domain -- defer to Taxes root if it exists)
  Insurance/
```

**Prescriptive rules:**
- Primary axis: institution (Chase, Fidelity, Schwab, etc.). Secondary axis: year.
- Institution name is detected from file content or filename. Files from multiple institutions belong in separate institution subfolders.
- Bank statements, brokerage statements → Statements/.
- Trade confirmations, 1099-B, 1099-DIV → Confirmations/ or defer to Taxes if a Taxes root exists.
- If institution subfolders do not exist but 5+ files from the same institution are present: propose creating the institution folder.
- Do not create year folders within an institution until 3+ years of documents are present.

---

## Domain: Legal

**Detection vocabulary:** "legal", "contracts", "agreements", "law", "attorney", "nda", "lease", "deed"

**Canonical structure:**
```
Legal/
  Contracts/
    Active/
    Expired/
  Personal/      (wills, trusts, estate documents)
  Property/      (deeds, title, survey)
  Employment/
  NDAs/
```

**Prescriptive rules:**
- Classify by document type first, counterparty second.
- Active contracts: expiry date in the future or unknown. Expired: expiry date in the past or "terminated" in content.
- NDAs get their own folder due to volume and sensitivity.
- Wills, trusts, power of attorney → Personal/.
- Deeds, titles, closing documents, HOA agreements → Property/.
- Offer letters, severance, employment agreements → Employment/.

---

## Domain: Medical / Health

**Detection vocabulary:** "medical", "health", "insurance", "eob", "explanation of benefits", "records", "rx", "prescription", "lab", "doctor", "hospital"

**Canonical structure:**
```
Medical/
  {Person Name}/       (if household has multiple people)
  Insurance/
    EOBs/
    Policies/
  Records/
    Labs/
    Imaging/
    Visit Notes/
  Prescriptions/
```

**Prescriptive rules:**
- If multiple household members' records exist, the first axis is person name.
- EOBs (Explanation of Benefits): date-named, into Insurance/EOBs/.
- Lab results, imaging reports, visit notes: into Records/ with appropriate subfolder.
- Insurance policy documents: into Insurance/Policies/.
- Prescriptions or medication records: into Prescriptions/.
- Privacy note: medical files are high sensitivity. Bower never includes medical content in the apply digest highlights. Apply digest lists only the count and destination folder, not filenames or content.

---

## Domain: Archive / Reference

**Detection vocabulary:** "archive", "archived", "reference", "old", "historical", "backup"

**Canonical structure:**
```
Archive/
  {YYYY}/
  {Original Domain}/    (e.g. Archive/Projects/, Archive/Finance/)
```

**Prescriptive rules:**
- Archive folders are low-intervention: Bower avoids moving files out of Archive unless confidence is high and the file clearly belongs to an active domain root.
- Files placed into Archive by the user are intentional. Treat Archive subfolders as sacred folders unless they contain clear mis-files (e.g., a current-year tax document in Archive/2019/).
- Within Archive, the organizing axis is year or original domain depending on which the user has started.

---

## Domain: Education / Learning

**Detection vocabulary:** "school", "university", "college", "course", "class", "lecture", "education", "study", "degree", "certificate"

**Canonical structure:**
```
Education/
  {Institution or Program}/
    {Course or Subject}/
      Notes/
      Assignments/
      Resources/
  Certificates/
```

**Prescriptive rules:**
- Primary axis: institution or program name.
- Secondary axis: course or subject within that program.
- Certificates, diplomas, transcripts → Certificates/ at the top level of Education/.

---

## Multi-domain files

A file may match signals from two domains (e.g., a tax document from a home sale matches both Taxes and Home). Resolution order:

1. Prefer the domain whose root folder is the more specific destination (deeper in the tree).
2. If equal depth, prefer the domain whose keywords appear more frequently in the file's content summary.
3. If still tied, generate proposals for both destinations at `med` confidence and let the user decide.

---

## Adding new domains

When Bower detects a consistent folder pattern that doesn't match any known domain (e.g., a "Photography" or "Music" root with 20+ files and emerging substructure), it logs a `domain_candidate` entry in `analysis_events.jsonl`. Bower does not invent domain logic for unknown domains -- it falls back to generic descriptive rules. Domain candidates are surfaced in `bower.status` for the user to acknowledge.

---

## Domain interaction with generic rules

Domain logic runs before generic outlier logic. If a file is resolved by domain rules, it is not also evaluated by generic rules. If domain logic produces no proposal (file already in correct position), generic rules evaluate the file normally for other outlier classes (name inconsistency, stale staging, etc.).

Permission safety, staleness gate, proposal cap, and feedback suppression all apply to domain proposals identically to generic proposals.
