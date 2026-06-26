---
name: master-data-matching
description: >
  Production-ready Master Data Intelligent Matching System.
  Use when: matching vendor/customer/employee records, deduplicating master data,
  resolving OCR-extracted entities against database records, or any entity resolution
  task across procurement/finance/sales/HR domains.
  Activates on: master data, entity matching, record deduplication, vendor matching,
  customer matching, OCR reconciliation, master data quality.
version: 1.0.0
triggers:
  - master data matching
  - entity matching
  - record deduplication
  - vendor matching
  - customer matching
  - OCR reconciliation
  - master data quality
  - procurement matching
  - finance matching
  - HR matching
  - human in the loop
  - active learning
---

# Master Data Intelligent Matching System

## Overview

A production-ready skill for intelligent entity resolution across business domains. It combines exact-match and vector-semantic retrieval, OCR field mapping with confidence coloring, and human-in-the-loop verification with active learning.

## Usage

```javascript
import mdm from './index.js';

// 1. Get supported domains
mdm.getSupportedDomains(); // ['procurement', 'finance', 'sales', 'hr']

// 2. Build OCR-to-schema mapping with confidence colors
const mapping = mdm.buildOcrSchemaMapping(ocrFields, 'procurement');

// 3. Run full matching pipeline
const result = mdm.runMatchingPipeline(ocrEntity, 'procurement', dbRecords);

// 4. Format result as summary
console.log(mdm.formatMatchingSummary(result));
```

## Key Features

### Business Domain Isolation
Four isolated schemas:
- **procurement** — vendor records (vendor_name, vendor_code, tax_id, contact, etc.)
- **finance** — company records (company_name, registration_number, fiscal_year_end, etc.)
- **sales** — customer records (customer_name, customer_code, industry, credit_limit, etc.)
- **hr** — employee records (employee_name, employee_id, id_number, department, etc.)

### OCR Field to Schema Visual Line Mapping
`buildOcrSchemaMapping(ocrFields, domain)` maps raw OCR field names to schema fields with confidence colors:

| Color   | Score       | Meaning                          |
|---------|-------------|----------------------------------|
| 🟢 green | ≥ 0.92      | High confidence mapping          |
| 🟡 yellow | 0.70–0.92   | Medium confidence mapping        |
| 🔴 red   | < 0.70      | Low confidence / unmapped        |
| 🔵 blue  | db-only     | Database field, no OCR data     |

### Dual-Path Entity Retrieval
`dualPathEntityRetrieval(entity, domain, dbRecords)` runs two parallel paths:

1. **Exact Match** (threshold 0.92) — ALL critical fields must match exactly
2. **Vector Semantic** (threshold 0.70) — weighted similarity across all fields

Results include `needsHumanReview: true` if confidence < 0.92 or no match found.

### Field Value Verification
`verifyFieldValues(ocrEntity, dbRecord, domain)` returns 4-state verification per field:

| State       | Meaning                                           |
|-------------|---------------------------------------------------|
| `match`     | OCR and DB values agree                          |
| `mismatch`  | Values differ (requires human resolution)         |
| `new_info`  | Field only in OCR (new information)              |
| `db_only`   | Field only in DB (not in OCR document)           |

### Human-in-the-Loop
Every pipeline result generates a `hitlRequest` with:
- Mismatched fields highlighted
- New info fields listed
- Available review actions: confirm_match, reject_match, create_new, update_fields

Use `processHumanDecision(decision, state)` to process human feedback and generate learning payloads.

### Active Learning
`updateActiveLearning(payloads, stats)` tracks:
- Per-domain confirmation/rejection/new-record rates
- Per-field error rates
- Auto-adjusts thresholds when field error rate > 30%

## Example

```javascript
import mdm from './index.js';

// Sample OCR entity from a vendor invoice
const ocrVendor = {
  vendor_name: 'Acme Corporation Ltd',
  vendor_code: 'V-5001',
  tax_id: '91110000123456789X',
  contact_person: 'John Smith',
  email: 'john.smith@acme.com',
};

// Existing database records
const dbRecords = [
  {
    id: 'rec_001',
    vendor_name: 'Acme Corporation Ltd',
    vendor_code: 'V-5001',
    tax_id: '91110000123456789X',
    contact_person: 'John Smith',
    email: 'j.smith@acme.com',  // slight email mismatch
    phone: '+86-10-12345678',
    address: 'Beijing Chaoyang District',
    bank_account: '6222021234567890',
  },
];

// Run pipeline
const result = mdm.runMatchingPipeline(ocrVendor, 'procurement', dbRecords);
console.log(mdm.formatMatchingSummary(result));

// Process human decision
const decision = { action: 'confirm_match', notes: 'Email mismatch acceptable' };
const { status, learningPayload } = mdm.processHumanDecision(decision, {
  domain: 'procurement',
  ocrEntity: ocrVendor,
  matchResult: result.matchResult,
});

// Update active learning
const newStats = mdm.updateActiveLearning([learningPayload], {});
```

## API Reference

| Function                          | Description                                    |
|-----------------------------------|------------------------------------------------|
| `getSupportedDomains()`           | List all supported business domains            |
| `getDomainSchema(domain)`         | Get field schema for a domain                  |
| `buildOcrSchemaMapping(ocr, dom)` | Map OCR fields to schema with confidence       |
| `dualPathEntityRetrieval(...)`    | Run exact + semantic matching                  |
| `verifyFieldValues(...)`          | 4-state field verification                     |
| `runMatchingPipeline(...)`        | Full orchestration pipeline                     |
| `generateHitlReviewRequest(...)`  | Build human review request payload             |
| `processHumanDecision(...)`       | Handle human feedback                          |
| `updateActiveLearning(...)`       | Update learning stats from decisions           |
| `formatMatchingSummary(...)`      | Human-readable result summary                  |
