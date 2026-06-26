# Immigration Pathway Finder

## Purpose
Help users understand available immigration pathways based on their destination, purpose, and personal situation.

## When to Use
- "I want to move to [country]"
- "What are my options for immigrating to [country]?"
- "How can I work in [country]?"
- "What visas are available for students?"

## Data Structure

```json
{
  "pathways": [
    {
      "id": "uuid",
      "country": "Canada",
      "visa_type": "Express Entry - Federal Skilled Worker",
      "category": "work",
      "description": "Permanent residence for skilled workers",
      "basic_requirements": [
        "1 year continuous skilled work experience",
        "Language proficiency (CLB 7)",
        "Educational credential assessment"
      ],
      "processing_time": "6-12 months",
      "government_fees": "$CAD 1,365+",
      "pros": ["Permanent residence", "No job offer required"],
      "cons": ["Competitive points system", "Requires high language scores"],
      "first_steps": [
        "Get language test results",
        "Complete educational credential assessment",
        "Create Express Entry profile"
      ],
      "notes": "Points-based system; higher scores get invited faster"
    }
  ]
}
```

## Common Pathway Categories

### Work-Based Immigration
| Pathway | Typical Requirements | Timeline |
|---------|---------------------|----------|
| Employer-Sponsored | Job offer, labor certification | 1-3 years |
| Skilled Worker (Points) | Work experience, language, education | 6-18 months |
| Intra-Company Transfer | Employed 1+ year, executive/managerial | 2-6 months |
| Startup/Entrepreneur | Business plan, investment, experience | 6-18 months |

### Family-Based Immigration
| Relationship | Typical Requirements | Timeline |
|--------------|---------------------|----------|
| Spouse/Partner | Marriage/cohabitation proof, financial sponsor | 12-24 months |
| Parent/Child | Proof of relationship, financial requirements | 1-10 years |
| Sibling | Proof of relationship, limited quotas | 10-20 years |

### Study-Based Pathways
| Pathway | Requirements | Timeline |
|---------|--------------|----------|
| Student Visa | School acceptance, financial proof, intent to return | 1-6 months |
| Post-Graduation Work | Graduate from eligible institution | 1-3 years |
| Student to PR | Work experience after graduation | Varies |

## Script Usage

```bash
# Find pathways for work in Canada
python scripts/pathway_finder.py \
  --country "Canada" \
  --purpose "work" \
  --occupation "software engineer"

# Find family sponsorship options
python scripts/pathway_finder.py \
  --country "USA" \
  --purpose "family" \
  --relationship "spouse"

# Find study options
python scripts/pathway_finder.py \
  --country "UK" \
  --purpose "study" \
  --level "masters"
```

## Output Format

```
IMMIGRATION PATHWAYS: Canada (Work)

Option 1: Express Entry - Federal Skilled Worker
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Type: Permanent Residence
Processing: 6-12 months | Fees: $CAD 1,365+

Requirements:
  ✓ 1 year continuous skilled work experience
  ✓ Language proficiency CLB 7 (IELTS/CELPIP)
  ✓ Educational Credential Assessment
  ✓ Proof of funds ($13,000+ for single applicant)

Pros:
  • Permanent residence from day one
  • No job offer required
  • Can include spouse and children

Cons:
  • Competitive points-based system
  • Requires high language scores
  • CRS score determines invitation speed

First Steps:
  1. Take language test (IELTS General or CELPIP)
  2. Get Educational Credential Assessment (ECA)
  3. Create Express Entry profile
  4. Wait for Invitation to Apply (ITA)

⚠️  Note: Minimum CRS score varies by draw; check current trends

---

Option 2: Provincial Nominee Program (PNP)
...

IMPORTANT: Requirements change frequently. Verify current criteria
on official government websites before making decisions.
```

## Research Guidelines

When user asks about pathways:
1. **Outline categories** available (work, family, study, investment)
2. **Highlight key requirements** without guaranteeing eligibility
3. **Provide timelines** as estimates (actual varies)
4. **Include fees** as approximate (subject to change)
5. **Link to official sources** for most current information
6. **Add disclaimer** about legal advice

## Common Countries Quick Reference

### USA
- H-1B: Specialty occupation, lottery system
- L-1: Intra-company transfer
- EB-2/EB-3: Employment-based permanent residence
- F-1: Student visa
- Family-sponsored: Immediate relatives vs preference categories

### Canada
- Express Entry: FSW, CEC, FST (points-based)
- PNP: Province-specific pathways
- Study Permit → PGWP → PR
- Family Sponsorship

### UK
- Skilled Worker Visa (points-based)
- Global Talent Visa
- Student Route
- Family Visa

### Australia
- General Skilled Migration (points-based)
- Employer Sponsored
- Student to PR pathways

## Safety Note

Always emphasize:
- Immigration rules change frequently
- Eligibility requirements vary by individual circumstances
- Official government sources are the authority
- Consult immigration attorney for personalized advice
