---
name: Automate HR Onboarding with Zapier Integrations & Google Drive Storage
description: "Automate HR workflows including benefits enrollment, onboarding, and payroll integration. Use when the user needs to streamline employee processes, reduce manual HR tasks, or personalize employee experiences across HRIS systems."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {"openclaw":{"requires":{"env":["HRIS_API_KEY","PAYROLL_API_KEY","SLACK_WEBHOOK_URL"],"bins":["curl","jq"]},"os":["macos","linux","win32"],"files":["SKILL.md"],"emoji":"🚀"}}
---

## Overview

HRFlow is an AI-driven HR process automation skill that intelligently orchestrates complex employee workflows across your entire HR ecosystem. Whether you're managing benefits enrollment, automating onboarding sequences, or syncing payroll data, HRFlow eliminates manual work and creates frictionless experiences for your team.

**Why HRFlow Matters:**
- **Reduce administrative burden** by 70-80% on repetitive HR tasks
- **Improve accuracy** in payroll, benefits, and compliance workflows
- **Personalize employee experiences** with AI-powered process recommendations
- **Real-time integration** with Workday, BambooHR, Gusto, ADP, and custom HRIS systems
- **Audit-ready compliance** with full workflow logging and approval chains

**Key Integrations:**
- HRIS: Workday, BambooHR, Namely, TriNet
- Payroll: Gusto, ADP, Paychex, Square Payroll
- Communication: Slack, Microsoft Teams, Email
- Document Management: DocuSign, HelloSign
- Analytics: Tableau, Power BI

---

## Quick Start

### Example 1: Automate Benefits Enrollment for New Hires
```
"Set up an automated benefits enrollment workflow for our new hire cohort. 
Trigger personalized emails with plan comparisons based on employee lifecycle 
stage, include DocuSign integration for enrollment forms, and sync completed 
enrollments back to Workday within 24 hours. Send daily Slack summaries to HR."
```

### Example 2: Create Intelligent Onboarding Sequences
```
"Build a 30-day AI-driven onboarding workflow that personalizes tasks based on 
department and role. Include hardware provisioning (auto-order laptop and phone), 
system access requests (GitHub, Slack, Google Workspace), manager 1-on-1 
scheduling, and culture documentation. Notify managers of pending tasks via Teams."
```

### Example 3: Sync Payroll Changes Across Systems
```
"Automate our payroll processing: pull updated employee data from BambooHR 
salary changes, map to Gusto payroll system, validate against tax withholding 
rules, and if any discrepancies occur, flag for HR review and escalate to 
slack #payroll-alerts. Generate a compliance report for finance."
```

### Example 4: Benefits Renewal Campaign with AI Personalization
```
"Launch our annual benefits renewal: segment employees by tenure and benefits 
tier, generate personalized communication highlighting plan changes relevant to 
each segment, track engagement metrics in real-time, and auto-escalate inactive 
employees to HR for phone outreach."
```

---

## Capabilities

### 1. **Intelligent Workflow Orchestration**
- Design complex multi-step HR processes with conditional logic
- Trigger workflows on events: new hire date, anniversary, role change, performance review
- Support approval chains and deadline-driven escalations
- Run parallel tasks (e.g., background check + equipment ordering simultaneously)

**Usage Example:**
```
Workflow: New Hire Activation
├── Day 1: Send welcome email + equipment order
├── Day 3: System access provisioning + manager sync
├── Day 7: Benefits enrollment (personalized by role)
├── Day 14: Culture onboarding & direct report mapping
└── Day 30: 30-day check-in survey
```

### 2. **Bi-directional HRIS & Payroll Integration**
- Real-time data sync between Workday, BambooHR, Gusto, ADP
- Automatic field mapping and data transformation
- Validation rules to catch errors before they propagate
- Audit logs for compliance and troubleshooting
- Support for custom HRIS via REST/SOAP APIs

**Supported Data Points:**
- Employee demographics (name, address, tax ID)
- Salary, benefits elections, deductions
- Department, manager, cost center assignments
- Time off accruals and usage
- Performance ratings and promotion flags

### 3. **AI-Powered Personalization Engine**
- Analyze employee lifecycle stage, role, department, tenure
- Generate customized communication and benefits recommendations
- Predict opt-out risk and auto-trigger engagement campaigns
- Segment audiences for targeted communications
- A/B test message variants for maximum engagement

### 4. **Multi-Channel Notifications**
- Email (with rich HTML templates and merge fields)
- Slack (interactive buttons, real-time alerts)
- Microsoft Teams (workflow cards, approvals)
- SMS (for urgent time-off or paycheck notifications)
- In-app notifications (if integrated with employee portal)

### 5. **Document Automation & E-Signature**
- Auto-generate offer letters, employment agreements, policy acknowledgments
- DocuSign/HelloSign integration for e-signatures
- Automatic filing and compliance tracking
- Template library with pre-built HR documents

### 6. **Compliance & Audit Reporting**
- Maintain immutable workflow logs for all HR processes
- Generate compliance reports for SOC2, GDPR, FCRA
- Track approval chains and reviewer signatures
- Export audit trails in standardized formats
- Real-time compliance violation alerts

---

## Configuration

### Required Environment Variables

```bash
# HRIS System Authentication
export HRIS_API_KEY="your-workday-or-bamboohr-api-key"
export HRIS_SYSTEM="workday"  # Options: workday, bamboohr, namely, custom
export HRIS_TENANT_ID="your-tenant-id"

# Payroll System Authentication
export PAYROLL_API_KEY="your-gusto-or-adp-api-key"
export PAYROLL_SYSTEM="gusto"  # Options: gusto, adp, paychex, square

# Communication Channels
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
export SLACK_DEFAULT_CHANNEL="#hr-alerts"
export SENDGRID_API_KEY="your-sendgrid-key"  # For email

# Document Signing
export DOCUSIGN_API_KEY="your-docusign-integration-key"
export DOCUSIGN_ACCOUNT_ID="your-account-id"

# Security & Compliance
export ENCRYPTION_KEY="your-256-bit-encryption-key"
export AUDIT_LOG_RETENTION_DAYS="2555"  # 7 years
export DATA_RESIDENCY="us-east-1"  # GDPR/compliance region
```

### Optional Configuration

```bash
# Workflow Settings
export WORKFLOW_TIMEOUT_MINUTES="1440"  # Max runtime before auto-fail
export APPROVAL_REMINDER_HOURS="24"  # Escalate pending approvals
export BATCH_PROCESS_SIZE="100"  # For bulk operations

# AI Personalization
export PERSONALIZATION_MODEL="openai-gpt4"
export SENTIMENT_ANALYSIS_ENABLED="true"
export ENGAGEMENT_SCORE_THRESHOLD="0.6"

# Custom HRIS Endpoint (if using custom system)
export CUSTOM_HRIS_BASE_URL="https://your-hris.company.com/api/v2"
export CUSTOM_HRIS_AUTH_TYPE="oauth2"  # or basic, bearer
```

### Initial Setup

1. **Authenticate with HRIS:**
   - Generate API key in Workday/BambooHR admin console
   - Test connection: `hrf test-hris-connection`

2. **Configure Payroll Integration:**
   - Link Gusto/ADP account via OAuth
   - Map employee fields between HRIS and payroll
   - Validate data sync with test batch

3. **Set Up Communication Channels:**
   - Create Slack app and generate webhook
   - Configure SendGrid for transactional email
   - Test notifications: `hrf test-notification slack`

4. **Document Signing (Optional):**
   - Register with DocuSign or HelloSign
   - Upload HR document templates
   - Assign signer roles and routing

---

## Example Outputs

### Output 1: New Hire Workflow Status Report
```
HRFlow Workflow Report - New Hire Activation
Generated: 2024-01-15 10:30 AM

Hire: Sarah Chen | Start Date: 2024-01-15 | Department: Engineering

✅ COMPLETED (Day 1):
  ✓ Welcome email sent (2024-01-15 09:00)
  ✓ Laptop order placed: MacBook Pro 16" (Order #WH-445829)
  ✓ Manager notification sent to James Rodriguez

⏳ IN PROGRESS (Day 3):
  ⏱ System access provisioning (80% complete)
    - GitHub: pending manager approval
    - Slack workspace: activated
    - Google Workspace: active
  ⏱ Security training assignment: due 2024-01-18

📋 PENDING (Day 7):
  ⏰ Benefits enrollment: due 2024-01-22
    - Medical: 3 plan options + personalized comparison
    - 401(k): auto-enrollment at 3% (adjustable)
    - FSA election: recommended based on dependent status
  ⏰ I-9 verification: scheduled for 2024-01-20

RISK FLAGS: None
APPROVAL CHAIN: All completed on-time
```

### Output 2: Payroll Sync Validation Report
```
HRFlow Payroll Integration Report
Sync Date: 2024-01-15 | Cycle: Bi-weekly

SOURCE: BambooHR → DESTINATION: Gusto Payroll
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PROCESSED: 487 employee records
✅ MATCHED: 483 (99.2%)
⚠️  WARNINGS: 3
❌ ERRORS: 1

WARNINGS (Requires Review):
1. Marcus Johnson - Salary change +8% detected
   Action: Waiting HR approval in #payroll-alerts
2. Priya Patel - Tax withholding mismatch (-$12/paycheck)
   Recommendation: Verify W-4 on file
3. New hire - Michael Torres - Missing direct deposit info
   Action: Auto-sent banking form request

ERRORS (Blocked):
1. Jennifer Lee - Duplicate employee ID in Gusto
   Status: HR contacted, awaiting resolution

DATA CONSISTENCY CHECKS:
✓ Tax IDs match across systems
✓ Deduction codes valid
✓ Department mappings correct
✓ Benefit plan elections aligned
```

### Output 3: Benefits Enrollment Campaign Summary
```
HRFlow Benefits Renewal Campaign - 2024
Campaign Dates: Jan 8-22 | Target: 250 employees

OVERALL ENGAGEMENT: 92% (230/250)
├── Opened email: 98% (245/250)
├── Clicked enrollment link: 94% (235/250)
└── Completed enrollment: 92% (230/250)

BY SEGMENT:
Tenure < 1 year:  88% completion (12 pending → escalate to phone)
Tenure 1-5 years: 95% completion (5 pending)
Tenure 5+ years:  93% completion (9 pending)

BY DEPARTMENT:
Engineering:  96% ✓ (highest engagement)
Sales:        89% (send reminder to Sales Ops)
Finance:      94% ✓
HR:           100% ✓ (all staff completed)

PLAN ELECTIONS TRENDS:
Medical plans: No change (69% HMO, 31% PPO)
401(k): +3% avg contribution increase (from 5.2% to 5.5%)
FSA: 42% enrollment (stable year-over-year)
Wellness: +12% uptake in gym benefits

NEXT STEPS:
→ Phone outreach for 26 pending employees (Jan 23-24)
→ Generate finalized census for plan administrators
→ Sync all elections to payroll system (Jan 25)
→ Send confirmation statements (Jan 26)
```

---

## Tips & Best Practices

### 1. **Start with High-ROI Processes**
- **First automation:** New hire onboarding (saves 8-12 hours per hire)
- **Second:** Benefits enrollment (eliminates manual data entry, reduces errors)
- **Third:** Payroll sync validation (prevents costly mistakes)

### 2. **Segment Your Audience Strategically**
```
Create workflows by employee lifecycle stage:
├── New hires (0-30 days): intensive onboarding
├── Established (30-365 days): integration + development
├── Tenured (1+ years): career pathing, benefits optimization
└── Offboarding: exit workflows, knowledge transfer
```

### 3. **Leverage Personalization for Engagement**
- Use employee role and seniority to tailor benefits explanations
- Reference employee's spouse/dependent status in FSA recommendations
- Highlight plan changes most relevant to their demographic
- Include manager context in onboarding (direct report names, team norms)

### 4. **Set Up Approval Chains Correctly**
- Keep approval levels to 2-3 max (faster decisions)
- Auto-escalate after 48 hours of inaction
- Assign backup approvers to prevent bottlenecks
- Use AI to flag "unusual" requests for manual review (e.g., 50% salary increase)

### 5. **Monitor Compliance Continuously**
- Set alerts for gaps in required training or documentation
- Audit audit logs monthly for suspicious patterns
- Validate payroll calculations against external benchmarks
- Track e-signature compliance (ESIGN Act, UETA)

### 6. **Optimize Communication Timing**
- Send benefits communications on Tuesdays-Thursdays (higher open rates)
- Avoid Mondays (inbox overload) and Fridays (weekend mind-set)
- Schedule onboarding tasks before new hire's first day (reduce Day 1 chaos)
- Use timezone-aware scheduling for distributed teams

### 7. **Test Before Rolling Out to All Employees**
- Run workflows on a pilot group (50-100 employees) first
- Collect feedback and refine templates
- Validate all integrations are passing correct data
- Train HR staff on escalation and troubleshooting

---

## Safety & Guardrails

### What HRFlow Will NOT Do

**Employee Termination Automation:**
- Will not auto-terminate employees or deactivate systems
- Requires explicit human approval and manager sign-off for all offboarding
- Terminates only after final paycheck calculation is confirmed

**Sensitive Compensation Decisions:**
- Will not automatically adjust salaries or approve raises
- Flags all compensation changes for HR/Finance review
- Requires dual sign-off for merit increases above 5%

**Data Deletion:**
- Will not delete any employee records permanently
- Archives all historical data for 7 years (compliance requirement)
- Anonymization requires explicit legal review

**Surveillance or Monitoring:**
- Will not integrate with time-tracking or keystroke monitoring systems
- Does not track employee activity beyond workflow completion
- Respects employee privacy while managing process metrics

### Security Boundaries

- **Encryption:** All data encrypted in transit (TLS 1.3) and at rest (AES-256)
- **Access control:** Role-based permissions (HR only, Finance only, etc.)
- **Audit logging:** Immutable logs of all data access and modifications
- **Data residency:** Respects GDPR, CCPA, and regional compliance requirements
- **Credential rotation:** API keys rotate every 90 days automatically
- **Rate limiting:** API calls throttled to prevent abuse
- **PII handling:** Sensitive fields (SSN, banking info) masked in logs

### Compliance Certifications

- SOC2 Type II compliant
- GDPR-ready with data processing agreements
- FCRA-compliant for background check workflows
- HIPAA-ready for health insurance features
- State-level payroll tax compliance (all 50 US states + territories)

---

## Troubleshooting

### Common Issues & Solutions

**Issue 1: Payroll Sync Fails with "Field Mismatch" Error**
```
Error: "Field 'cost_center' not found in Gusto schema"

Solution:
1