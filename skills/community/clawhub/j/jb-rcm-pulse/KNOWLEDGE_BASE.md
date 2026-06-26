# RCM Knowledge Base — JB Burkett
*Built by JB's Claw — updated daily as JB learns*
*Last updated: 2026-03-22*

---

## DOMAIN 1: Revenue Cycle Fundamentals

### The 10 Steps (Industry Standard)
1. Patient pre-registration → insurance verification
2. Registration → demographics + insurance captured
3. Charge capture → service rendered → codes assigned
4. Utilization review → medical necessity check
5. Claim submission → EDI to payer
6. Claim processing → payer-adjudicated
7. Payment posting → ERA/EFT or patient pays
8. Denial management → appeal or rework
9. Patient collections → statement, payment plan, collections
10. Revenue reconciliation → audit, integrity

### Key Distinctions
- **Clean claim:** No errors, goes straight to processing
- **Dirty claim:** Errors → rejection → must be corrected and resubmitted
- **Denial vs. Rejection:** Denial = payer processed and refused | Rejection = clearinghouse caught errors before submission
- **Soft denial:** Temporarily denied, can be appealed with additional info
- **Hard denial:** Final refusal, often due to timely filing or lack of authorization

### JB's Notes
- SparkChange sits somewhere in the automation/AI layer of this cycle — understanding where determines what to pitch
- The "dirty claim" problem is where most AI/automation plays are — claim scrubbing before submission

---

## DOMAIN 2: Medical Billing & Coding

### CPT Codes (Current Procedural Terminology)
- **Category I:** Standard medical procedures (most common)
- **Category II:** Performance measurement tracking
- **Category III:** Emerging technology, temporary codes
- **E/M Codes:** Evaluation and Management — 99201-99499 (office visits, consults, hospital care)
  - Level selection based on MDM (Medical Decision Making) or Time
  - 2021 AMA changes: time-based coding expanded, MDM framework updated
- **Modifiers:** 24, 25, 26, 50, 51, 52, 53, 59, 76, 77, 78, 79, 91 — change how codes are interpreted by payers

### ICD-10-CM (Diagnosis Codes)
- 70,000+ codes in US system
- Chapter structure (not sequential)
- Always code to highest specificity — no "unspecified" unless truly unknown
- Laterality: left vs. right vs. bilateral (important for audits)
- "Code also" vs. "code first" rules

### HCPCS Codes
- Level II: Supplies, equipment, drugs (J-codes for injectables)
- Level I: CPT codes (same as above)
- CMS maintains Level II — updated quarterly

### Common JB/SparkChange Coding Issues
- Modifier 25: Significant, separate E/M service same day as procedure — frequently audited
- Modifier 59: Distinct procedural service — payer scrutiny increasing
- Unbundling: Billing separate codes when one comprehensive code applies

---

## DOMAIN 3: Claims Submission & EDI

### Clearinghouse Role
- Scrubs claims for errors before forwarding to payers
- Payer-specific edits: insurance-specific rules applied before submission
- Most clearinghouses: Availity, Waystar, Change Healthcare, TriZetto
- SparkChange likely touches this layer with automation

### Timely Filing Limits (Major Commercial Payers)
- Medicare: Within 1 calendar year of service date
- Medicaid: Varies by state (typically 6-12 months)
- BCBS: Typically 6 months to 1 year
- United: 6 months to 1 year
- Aetna: 6 months to 1 year
- Commercial: Usually 90 days to 1 year

**If denied for timely filing → almost never reversible**

### ERA/EFT (Electronic Remittance + Funds Transfer)
- ERA: Electronic explanation of benefits — replaces paper EOBs
- EFT: Electronic deposit to bank account
- Most practices still manually post — automation opportunity here

---

## DOMAIN 4: Denials Management

### Denial Categories (by原因)
1. **Coding denials:** Incorrect/unbundled codes, missing modifiers
2. **Medical necessity denials:** Service not justified for diagnosis
3. **Authorization denials:** No prior auth obtained
4. **Eligibility denials:** Patient not covered on date of service
5. **Timely filing denials:** Submitted after deadline
6. **Duplicate denials:** Same claim submitted twice
7. **Contractual denials:** Provider not in network for service

### Denial Hierarchy
```
Initial Denial → Appeal Level 1 (1st level payer review)
             → Appeal Level 2 (2nd level review)
             → Appeal Level 3 (Independent Review / IRO)
             → State Insurance Department complaint
             → Final: Litigation
```

### Top 5 Denial Codes (Most Common)
1. **CO-4:** The procedure code is inconsistent with the modifier
2. **CO-16:** Claim lacks information (most common — easiest to fix)
3. **CO-18:** Duplicate claim
4. **CO-22:** Coordination of benefits secondary payer information
5. **CO-45:** Charges exceed fee schedule

### Denial Prevention (Front-End)
- Real-time eligibility verification before visit
- Prior auth automation
- Claim scrubber before submission
- Staff training on modifier usage
- Charge master review annually

---

## DOMAIN 5: Payer Behavior & Reimbursement

### Major Payer Types
- **Medicare Part A:** Hospital inpatient
- **Medicare Part B:** Physician/outpatient
- **Medicare Advantage (MA):** Private plans, growing fast (50%+ of Medicare beneficiaries)
- **Medicaid:** State-based, income-based
- **Commercial:** BCBS, UHC, Aetna, Cigna, Humana, local plans
- **Self-pay:** No insurance

### Reimbursement Models
- **FFS (Fee for Service):** Per service, per code — volume incentivized
- **Value-Based Care (VBC):** Quality + cost metrics — outcome incentivized
- **Capitation:** Fixed per-member-per-month — utilization risk borne by provider
- **Bundled Payment:** Fixed episode payment — all services for a condition

### Key Concept: MPFS vs. Site of Service
- Same CPT code → different payment depending on where performed
- Hospital Outpatient (HO) vs. Physician Office (PO) reimbursement differential
- 3-day payment window for hospitals (pre-admission services bundled into inpatient)

---

## DOMAIN 6: Patient Financial Experience

### Price Transparency Rules
- CMS effective Jan 1, 2021: Hospitals must publish standard charges online (machine-readable file)
- CMS effective July 1, 2024: Shoppable services must show prices in plain language
- No Surprises Act (Jan 2022): Protects patients from surprise bills for out-of-network emergency/ancillary

### Patient Payment Collection
- Point-of-service collections: Collect before/during visit (best success rate)
- Payment plans: 0% interest standard,collections after 90-120 days
- Financial assistance: Charity care policies (required for non-profit hospitals)
- Early-out vs. late-out collections: Difference matters for patient relations

---

## DOMAIN 7: Compliance

### HIPAA (Administrative Simplification)
- Protected Health Information (PHI): Any individually identifiable health info
- Minimum Necessary: Only access/use PHI needed for the task
- BAA: Required when outsourcing any RCM function
- Breach Notification: 60-day deadline to notify HHS + patients
- HIPAA penalties: Tiered $100-$50,000 per violation

### No Surprises Act (NSA) Components
1. **Good Faith Estimates:** Required for uninsured/self-pay patients
2. **Surprise Billing Protection:** Out-of-network emergency + ancillary services
3. **IDR (Independent Dispute Resolution):** Process for providers/payors to contest rates
4. **Advanced Explanation of Benefits:** Required before scheduled services

### CMS Payment Integrity Programs
- **RAC (Recovery Audit Contractors):** Post-payment audit, look for overpayments
- **MAC (Medicare Administrative Contractors):** MACs handle claims processing + medical review
- **UPIN/NPI:** Provider identifiers — must be accurate on every claim

---

## DOMAIN 8: RCM Technology & AI

### Where AI/Automation Hits First
1. **Claims scrubbing** (pre-submission error detection)
2. **Prior authorization** (automation of approval workflows)
3. **Denial prediction** (ML models scoring likelihood of denial before submission)
4. **Payment posting** (ERA auto-post to reduce manual entry)
5. **Patient responsibility estimation** (eligibility + benefits → real-time estimates)

### Key Vendors
- **Waystar:** Clearinghouse + RCM SaaS (Waystar acquired eSolutions, Navicure)
- **Change Healthcare (RCM sold to Optum):** Massive EDI network + analytics
- **Availity:** Payer-provider connectivity platform
- **FinThrive:** Revenue integrity + claims editing
- **athenahealth:** Practice management + RCM for practices
- **Cotiviti:** Payment accuracy + fraud detection
- **Cloudmed / R1 RCM:** End-to-end RCM outsourcing

### SparkChange Angle
- SparkChange likely operates in the **automation/intelligence layer** — between the EHR and the clearinghouse
- Competitive positioning: Where does the AI actually reduce headcount vs. just speeding up existing work?

---

## DOMAIN 9: Revenue Integrity & Charge Master

### Charge Master (CDM)
- Hospital's list of all billable services + standard charges
- Must be updated annually minimum (CMS requirement)
- Chargemaster rates ≠ what Medicare/payers pay
- Audit regularly: undercoded services = revenue leakage

### Revenue Leakage Points
1. Underutilization of services (not billing for everything rendered)
2. Eligibility gaps (not verifying coverage before service)
3. Modifier misuse (leaving money on the table or triggering audits)
4. Provider credentialing gaps (services not covered if provider not credentialed)
5. Missing charges (services rendered but not captured in billing)

### Key Metric: Clean Claim Rate
- Industry benchmark: 85%+ clean claim rate at submission
- Below 85% = significant rework cost and cash delay
- Best-in-class: 95%+

---

## DOMAIN 10: RCM Metrics & KPIs

### Golden Metrics
| Metric | Definition | Benchmark |
|--------|-----------|-----------|
| **Clean Claim Rate** | % submitted without errors | 85%+ |
| **Denial Rate** | % of claims denied | <5% |
| **AR Days (DSO)** | Days in accounts receivable | <40 days |
| **First-Pass Resolution Rate** | % denials resolved without escalation | 70%+ |
| **Net Collection Rate** | % of collectible revenue actually collected | 95%+ |
| **Cost to Collect** | $ spent to collect $100 | <$3 |
| **Credit Balance Rate** | $ in credit balances / total revenue | Track trends |

### AR Aging Buckets
- 0-30 days: Current — monitor only
- 31-60 days: Early — follow up
- 61-90 days: Late — aggressive follow up
- 90+ days: Write-off candidate or referral to collection

---

## DOMAIN 11: Current Regulatory Landscape (2026)

### CMS 2026 Updates
- **April 1, 2026 ICD-10 updates:** 80 new procedure codes effective
- **2026 MPFS:** Medicare Physician Fee Schedule final rule released late 2025
- **No Surprises Act enforcement:** IDR process ongoing, lawsuits active
- **Price transparency:** CMS increasing audit frequency, penalties up to $300/day for small hospitals

### RCM Staffing & Labor Trends
- Remote billing staff becoming standard
- AI tools reducing need for entry-level billing (increasing demand for analysts)
- Outsourcing vs. insourcing: In-house AI-assisted billing vs. full outsource
- HIM/coding staffing: Supply shortage driving coding automation demand

---

## JB's Key Questions (Learning Log)
*Tracking what JB asks to measure learning progression*

- [2026-03-22] JB asked about charge master vs. fee schedule — difference is who sets rates (hospital vs. payer)
- [2026-03-22] JB asked aboutpayer mix and how it affects RCM strategy
- [2026-03-22] JB wants to understand denial root cause taxonomy deeply

---

## JB's "Aha" Moments (For SparkChange)
*Real insights connecting RCM to operational improvement*

- Denials are mostly a front-end problem caught at back-end = expensive rework
- Payer variation is the reason every client's RCM is a "snowflake" — can't build one system for all payers
- Revenue cycle automation's hardest part isn't the tech — it's the payer policy variation

---

*Last updated: 2026-03-22*
*Next review: Weekly — add new JB questions, refine accuracy, add SparkChange angles*
