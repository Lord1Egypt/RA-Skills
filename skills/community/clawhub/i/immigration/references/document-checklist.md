# Document Checklist Generator

## Purpose
Generate comprehensive, personalized document checklists for specific visa applications with requirements and tracking.

## When to Use
- "What documents do I need for [visa]?"
- "Help me prepare my application"
- "Generate checklist for [country] [visa type]"

## Document Categories

### 1. Identity Documents
| Document | Requirements | Common Issues |
|----------|-------------|---------------|
| Passport | Valid 6+ months beyond travel | Insufficient validity, damaged pages |
| Photos | Specific size, recent, plain background | Wrong dimensions, glasses, smiling |
| Birth Certificate | Original or certified copy | Not translated, missing apostille |

### 2. Financial Documents
| Document | Shows | Typical Requirements |
|----------|-------|---------------------|
| Bank Statements | Financial stability | 3-6 months, sufficient balance |
| Tax Returns | Income history | Last 2-3 years, all pages |
| Pay Stubs | Current employment | Last 3-6 months |
| Employment Letter | Job confirmation | On letterhead, specific details |

### 3. Civil Documents
| Document | Purpose | Special Requirements |
|----------|---------|---------------------|
| Birth Certificate | Identity, age | Certified, translated, apostilled |
| Marriage Certificate | Spousal relationship | Certified copy, translation |
| Divorce Decree | Previous marriage ended | Certified, final decree only |
| Police Clearance | Good character | From all countries lived 6+ months |

### 4. Education Documents
| Document | Purpose | Requirements |
|----------|---------|--------------|
| Diplomas | Degree verification | Original or certified copy |
| Transcripts | Coursework details | Sealed, official copy |
| Credential Evaluation | Foreign degree equivalent | NACES member evaluation |

### 5. Employment Documents
| Document | Purpose | Requirements |
|----------|---------|--------------|
| Offer Letter | Job confirmation | Signed, detailed terms |
| Contract | Employment terms | All pages, signed |
| Employer Support Letter | Company sponsorship | On letterhead, specific language |

## Data Structure

```json
{
  "checklists": [
    {
      "id": "uuid",
      "visa_type": "H-1B",
      "country": "USA",
      "created_at": "2024-03-01",
      "documents": [
        {
          "category": "Identity",
          "name": "Valid Passport",
          "required": true,
          "requirements": "Valid 6 months beyond employment start date",
          "how_to_obtain": "Renew at passport agency if needed",
          "translation_needed": false,
          "notarization_needed": false,
          "status": "collected",
          "collected_date": "2024-03-01",
          "expiry_date": "2028-03-01",
          "notes": "Valid until 2028"
        }
      ],
      "completion_percentage": 45
    }
  ]
}
```

## Script Usage

```bash
# Generate H-1B checklist
python scripts/generate_checklist.py \
  --visa "H-1B" \
  --country "USA" \
  --applicant-type "individual"

# Generate family-based checklist
python scripts/generate_checklist.py \
  --visa "CR-1" \
  --country "USA" \
  --applicant-type "spouse" \
  --petitioner "US citizen"

# Check document status
python scripts/document_inventory.py --checklist-id "uuid"
```

## Output Format

```
DOCUMENT CHECKLIST: H-1B Specialty Occupation
Generated: March 1, 2024
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

IDENTITY DOCUMENTS [2/2 collected]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
☑ Valid Passport
  Required: Valid 6 months beyond employment start
  Status: ✅ Collected (expires 2028-03-01)
  Notes: Current passport sufficient

☐ Visa Photos (2)
  Required: 2x2 inches, white background, taken within 30 days
  Status: ⏳ Needed
  Action: Schedule at CVS/photo center
  Notes: Cannot wear glasses; neutral expression

FINANCIAL DOCUMENTS [1/3 collected]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
☐ Bank Statements (3 months)
  Required: Show sufficient funds or salary deposits
  Status: ⏳ Needed
  Action: Request from bank or download statements

☑ Employment Verification Letter
  Required: On company letterhead, signed by authorized person
  Status: ✅ Collected
  Collected: 2024-02-28

☐ Pay Stubs (last 3 months)
  Required: Show current employment and salary
  Status: ⏳ Needed

EMPLOYMENT DOCUMENTS [2/2 collected]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
☑ Form I-129 (Petition)
  Status: ✅ Employer will file

☑ Labor Condition Application (LCA)
  Status: ✅ Certified by DOL

...

OVERALL PROGRESS: 7/12 documents collected (58%)

⚠️  URGENT: Visa photos needed within 7 days
📅 Passport expires in 4 years - no action needed

Next Steps:
1. Get visa photos taken
2. Collect last 3 months bank statements
3. Request official transcripts from university
```

## Document Status Tracking

### Status Options
- `needed` - Not yet collected
- `in-progress` - Working on obtaining
- `collected` - Have in possession
- `submitted` - Sent to immigration authority
- `expired` - No longer valid (needs renewal)

### Critical Flags
- **Urgent** - Needed within 7 days
- **Expiring Soon** - Document expires within 60 days
- **Complex** - Requires multiple steps (translation, apostille, etc.)

## Common Document Pitfalls

### Translations
- Must be certified translations (not self-translated)
- Translator must certify accuracy and competency
- Original + translation both required

### Apostille/Authentication
- Hague Convention countries: Apostille
- Non-Hague countries: Embassy authentication
- Process takes 2-8 weeks typically

### Validity Periods
- Police clearances: Usually 6-12 months
- Medical exams: Usually 6 months
- Financial documents: Usually 3-6 months
- Passport photos: Usually 6 months

## Tracking Commands

```bash
# Mark document as collected
python scripts/document_inventory.py \
  --checklist-id "uuid" \
  --document "Passport" \
  --status collected \
  --expiry "2028-03-01"

# List all pending documents
python scripts/document_inventory.py \
  --status needed \
  --sort-by urgency

# Check for expiring documents
python scripts/document_inventory.py \
  --expiring-within 90
```
