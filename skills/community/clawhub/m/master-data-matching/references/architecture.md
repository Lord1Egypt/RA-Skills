# Master Data Intelligent Matching System — Architecture

## System Overview

The Master Data Intelligent Matching System (MDM) is a production-ready skill for entity resolution across four business domains: Procurement, Finance, Sales, and HR. It processes OCR-extracted entity records and matches them against a master database using a dual-path retrieval strategy, with mandatory human-in-the-loop verification and continuous active learning.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           MATCHING PIPELINE                                 │
│                                                                              │
│  ┌─────────────┐    ┌──────────────────┐    ┌─────────────────────────────┐  │
│  │  OCR Entity │───▶│  Domain Schema   │───▶│  OCR → Schema Line Mapping  │  │
│  │  (raw)      │    │  Validation      │    │  + Confidence Colors        │  │
│  └─────────────┘    └──────────────────┘    └──────────────┬──────────────┘  │
│                                                            │                  │
│                                                            ▼                  │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                     DUAL-PATH ENTITY RETRIEVAL                         │  │
│  │                                                                        │  │
│  │   PATH 1: Exact Match          PATH 2: Vector Semantic Search          │  │
│  │   Threshold: 0.92             Threshold: 0.70                          │  │
│  │   All critical fields =      Weighted field similarity               │  │
│  │                                                                        │  │
│  └──────────────────────────┬────────────────────────────────────────────┘  │
│                              │                                               │
│                              ▼                                               │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                   MATCH RESULT AGGREGATOR                             │  │
│  │   - exact matches first (overrides semantic)                          │  │
│  │   - overall confidence = max(path1, path2)                            │  │
│  │   - needsHumanReview = confidence < 0.92 or no match                 │  │
│  └────────────────────────────────┬────────────────────────────────────────┘  │
│                                   │                                          │
│                                   ▼                                          │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                   FIELD VALUE VERIFICATION                            │  │
│  │   Per-field 4-state check: MATCH / MISMATCH / NEW_INFO / DB_ONLY     │  │
│  │   Color coding: green / red / yellow / blue                          │  │
│  └────────────────────────────────┬────────────────────────────────────────┘  │
│                                   │                                          │
│                                   ▼                                          │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                   HUMAN-IN-THE-LOOP (HITL)                            │  │
│  │   If needsHumanReview: generate review request with actions:         │  │
│  │   - confirm_match   - reject_match   - create_new   - update_fields  │  │
│  │                                                                        │  │
│  │   Human submits decision → processHumanDecision()                    │  │
│  └────────────────────────────────┬────────────────────────────────────────┘  │
│                                   │                                          │
│                                   ▼                                          │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                   ACTIVE LEARNING                                     │  │
│  │   Collect learning payloads from human decisions                     │  │
│  │   Track per-field error rates, per-domain stats                      │  │
│  │   Auto-adjust thresholds when field error rate > 30%                │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Business Domain Isolation

Each domain has its own schema with:
- **Critical fields** (weight 0.20–0.30): Used for exact matching. ALL must match for exact-match path.
- **Non-critical fields** (weight 0.05): Used for semantic similarity but not exact matching.

### Domain Schemas

#### Procurement
| Field           | Type   | Weight | Critical |
|-----------------|--------|--------|----------|
| vendor_name     | string | 0.30   | ✅       |
| vendor_code     | string | 0.25   | ✅       |
| tax_id          | string | 0.20   | ✅       |
| contact_person  | string | 0.05   | ❌       |
| email           | string | 0.05   | ❌       |
| phone           | string | 0.05   | ❌       |
| address         | string | 0.05   | ❌       |
| bank_account    | string | 0.05   | ❌       |

#### Finance
| Field               | Type   | Weight | Critical |
|---------------------|--------|--------|----------|
| company_name        | string | 0.30   | ✅       |
| registration_number | string | 0.25   | ✅       |
| tax_id              | string | 0.20   | ✅       |
| fiscal_year_end     | date   | 0.05   | ❌       |
| registered_capital  | number | 0.05   | ❌       |
| legal_representative| string | 0.05   | ❌       |
| address             | string | 0.05   | ❌       |
| bank_account        | string | 0.05   | ❌       |

#### Sales
| Field           | Type   | Weight | Critical |
|-----------------|--------|--------|----------|
| customer_name   | string | 0.30   | ✅       |
| customer_code   | string | 0.25   | ✅       |
| industry        | string | 0.10   | ❌       |
| contact_person  | string | 0.10   | ❌       |
| email           | string | 0.10   | ❌       |
| phone           | string | 0.05   | ❌       |
| address         | string | 0.05   | ❌       |
| credit_limit    | number | 0.05   | ❌       |

#### HR
| Field           | Type   | Weight | Critical |
|-----------------|--------|--------|----------|
| employee_name   | string | 0.30   | ✅       |
| employee_id     | string | 0.25   | ✅       |
| id_number       | string | 0.20   | ✅       |
| department      | string | 0.05   | ❌       |
| position        | string | 0.05   | ❌       |
| email           | string | 0.05   | ❌       |
| phone           | string | 0.05   | ❌       |
| hire_date       | date   | 0.05   | ❌       |

## Dual-Path Retrieval Strategy

### Path 1: Exact Match (Threshold 0.92)
- Only considers **critical fields**
- ALL critical fields must match exactly (normalized string equality)
- Returns score = 1.0 if all match, 0 otherwise
- Exact matches **override** semantic matches (higher priority)

### Path 2: Vector Semantic Search (Threshold 0.70)
- Considers **all fields**
- Each field contributes: `similarity × field_weight`
- Normalized by total weight: `Σ(similarity × weight) / Σ(weight)`
- Uses character bigram Jaccard for string similarity
- Number fields use relative difference: `1 - |a-b| / max(|a|,|b|)`
- Date fields use string similarity

### Aggregation
```
if exactMatches.length > 0:
    bestMatch = exactMatches[0]
    overallConfidence = exactMatches[0].score
    path = 'exact'
else if semanticMatches.length > 0:
    bestMatch = semanticMatches[0]
    overallConfidence = semanticMatches[0].score
    path = 'semantic'
else:
    bestMatch = null
    overallConfidence = 0
    path = null

needsHumanReview = overallConfidence < 0.92 OR bestMatch is null
```

## OCR Field to Schema Visual Line Mapping

### Mapping Algorithm
1. Normalize OCR field name and schema field name (trim, lowercase, collapse whitespace)
2. For each OCR field, find best schema field match by character bigram Jaccard
3. If similarity > 0.5, accept mapping; otherwise mark as unmapped
4. Return mapping with per-field confidence and color

### Confidence Color System

| Color | Label  | Confidence   | Hex       | Condition                     |
|-------|--------|--------------|-----------|-------------------------------|
| 🟢   | green  | ≥ 0.92       | #22c55e   | Exact match or very high sim  |
| 🟡   | yellow | 0.70–0.92    | #eab308   | Good similarity               |
| 🔴   | red    | < 0.70       | #ef4444   | Low similarity or unmapped    |
| 🔵   | blue   | db-only      | #3b82f6   | Database field, no OCR data   |

## Field Value Verification

### 4 States

```
┌─────────────────────────────────────────────────────────────────┐
│                        VERIFICATION STATES                       │
│                                                                  │
│  MATCH ──────▶ OCR = DB (within threshold)                      │
│    │                                                           │
│    │  (both non-empty)                                         │
│    ▼                                                           │
│  MISMATCH ────▶ OCR ≠ DB (below threshold)                     │
│                                                                  │
│  NEW_INFO ────▶ OCR has value, DB empty                        │
│                                                                  │
│  DB_ONLY ─────▶ DB has value, OCR empty                        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Verification Logic
```javascript
if (ocrEmpty && dbEmpty) → MATCH
else if (ocrEmpty)       → DB_ONLY
else if (dbEmpty)        → NEW_INFO
else if (similarity ≥ 0.92) → MATCH
else                     → MISMATCH
```

## Human-in-the-Loop Flow

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  OCR Entity  │────▶│   Pipeline   │────▶│  Review?     │
│              │     │              │     │              │
└──────────────┘     └──────────────┘     └──────┬───────┘
                                                 │
                            ┌────────────────────┤
                            │                    │
                           YES                   NO
                            │                    │
                            ▼                    ▼
                    ┌──────────────┐     ┌──────────────┐
                    │ Generate     │     │ Auto-apply   │
                    │ HITL Request │     │ (if skipHitl)│
                    │              │     │              │
                    │ Actions:     │     └──────────────┘
                    │ - confirm    │
                    │ - reject     │
                    │ - create_new │
                    │ - update     │
                    └──────┬───────┘
                           │
                           ▼ Human Decision
                    ┌──────────────┐
                    │ processHuman │
                    │ Decision()   │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │ Learning     │
                    │ Payload      │
                    └──────────────┘
```

### HITL Request Payload
```javascript
{
  domain,
  timestamp,
  needsReview,
  overallConfidence,
  matchPath,
  ocrEntity,
  suggestedMatch,
  fieldVerification,
  schemaFields,
  mismatchedFields,
  newInfoFields,
  reviewActions: [
    { action: 'confirm_match', label: 'Confirm Match', enabled: ... },
    { action: 'reject_match', label: 'Reject Match', enabled: ... },
    { action: 'create_new', label: 'Create New Record', enabled: ... },
    { action: 'update_fields', label: 'Update & Confirm', enabled: ... },
  ]
}
```

## Active Learning

### Learning Payload
```javascript
{
  event: 'match_confirmed' | 'match_rejected' | 'new_record_created' | 'fields_updated',
  domain,
  ocrEntity,
  matchedRecord,
  correctedData,
  confidence,
  reason
}
```

### Learning Statistics
```javascript
{
  totalDecisions: number,
  domainStats: {
    [domain]: { confirmed: number, rejected: number, newRecords: number }
  },
  fieldErrorRates: {
    [fieldName]: { errors: number, total: number }
  },
  adjustedThresholds: {
    exactMatch: number,
    vectorSemantic: number
  }
}
```

### Threshold Adjustment Rule
When a field has ≥5 observations and error rate > 30%:
```
exactMatch = min(1.0, exactMatch + 0.02)
vectorSemantic = min(exactMatch - 0.01, vectorSemantic + 0.02)
```

This tightens requirements for problematic fields, reducing false positives.

## Similarity Functions

### String Similarity (Jaccard of Character Bigrams)
```
bigrams(s) = { s[i:i+2] for i in 0..len(s)-2 }
similarity(a, b) = |bigrams(a) ∩ bigrams(b)| / |bigrams(a) ∪ bigrams(b)|
```

### Field-Type-Aware Similarity
| Type   | Method                                                  |
|--------|--------------------------------------------------------|
| string | Character bigram Jaccard (normalized, case-insensitive) |
| number | 1 - \|a-b\| / max(\|a\|, \|b\|), clamped to [0,1]    |
| date   | String similarity (YYYY-MM-DD format)                  |

## File Structure
```
master-data-matching/
├── SKILL.md              # This file
├── index.js              # Main module
├── package.json
├── references/
│   └── architecture.md    # This file
└── assets/
    ├── domain-schemas.json    # Domain schema configs
    └── matching-config.json   # Matching thresholds config
```

## Configuration

### Default Thresholds
```javascript
MATCHING_THRESHOLDS = {
  exactMatch: 0.92,
  vectorSemantic: 0.70,
}
```

### Color Palette
```javascript
COLORS = {
  high:   { hex: '#22c55e', label: 'green' },
  medium: { hex: '#eab308', label: 'yellow' },
  low:    { hex: '#ef4444', label: 'red' },
  dbOnly: { hex: '#3b82f6', label: 'blue' },
}
```
