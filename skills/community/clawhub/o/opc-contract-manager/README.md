# OPC Contract Manager

A Contract Review + Contract Ops Copilot for solo entrepreneurs and one-person company CEOs.

This skill helps you **review contracts, prepare for negotiations, track deadlines, and manage your contract archive** — all from Claude Code. It produces actionable output: not just "here's what's wrong," but "here's what to say, what to ask for, and when to walk away."

> **Important:** This is a practical risk review tool, not legal advice. Always consult a qualified attorney before making binding decisions.

## What It Does

### Pre-Signing
- **Full contract review** with clause-by-clause analysis using a 14-item checklist
- **Risk assessment** with dual-dimension scoring (severity + negotiation priority)
- **Contract-type-aware prioritization** — NDAs, MSAs, SaaS agreements, contractor agreements, partnerships, and SOWs each get tailored focus areas
- **Redline suggestions** with exact modifications or suggested additional language
- **Negotiation strategy** — must-haves, nice-to-haves, fallback positions, concession candidates
- **Email draft** ready to copy-paste to the counterparty
- **Lawyer escalation triggers** — automatically flags when you need professional legal review

### Post-Signing
- **Contract archive** with structured JSON metadata and markdown reports
- **Deadline tracking** — expirations, renewals, cancellation notice windows, payment deadlines
- **Urgent deadline alerts** — auto-checks for 7-day deadlines when you invoke the skill
- **Portfolio search** by counterparty, type, risk level, dates, or structural flags

### Portfolio Intelligence (5+ contracts)
- **Cross-contract insights** — payment term trends, counterparty concentration risk, liability exposure, termination risk score
- **Confidence metadata** on every insight — you know exactly how reliable each finding is

## Installation

### Option 1: Clone to skills directory

```bash
git clone https://github.com/LeonFJR/opc-skills.git ~/.claude/skills/opc-skills
```

### Option 2: Copy just this skill

```bash
cp -r opc-contract-manager ~/.claude/skills/opc-contract-manager
```

### Option 3: Project-level skill

Add to your project's `.claude/settings.json`:

```json
{
  "skills": ["path/to/opc-contract-manager"]
}
```

## Usage

### Review a contract

```
/opc-contract-manager

[paste contract text or provide file path]
```

The skill auto-detects the contract type and counterparty. No need to answer a questionnaire — it infers what it needs and asks only when something is genuinely ambiguous.

### Quick clause check

```
/opc-contract-manager

Is this non-compete clause reasonable? "Contractor shall not engage in any
competing business within the United States for a period of 24 months..."
```

### Archive a signed contract

```
/opc-contract-manager

Archive this contract: [paste or file path]
Counterparty: Acme Corp
Signed on: 2026-01-15
```

### Check deadlines

```
/opc-contract-manager

Show me my contract dashboard
```

### Search contracts

```
/opc-contract-manager

Find all contracts with Acme Corp
Which contracts have uncapped liability?
What's expiring in the next 60 days?
```

## Archive Structure

When you archive contracts, the skill creates a structured directory:

```
contracts/
├── INDEX.json                                    # Master index (auto-generated)
├── INSIGHTS.json                                 # Portfolio insights (auto at 5+ contracts)
├── INSIGHTS.md                                   # Human-readable insights
├── 2026-03-01_acme-corp_msa/
│   ├── metadata.json                             # Structured metadata
│   ├── review-report.md                          # Full review report
│   ├── summary.md                                # One-page summary
│   └── original-contract.pdf                     # Original document
├── 2026-02-15_beta-inc_nda/
│   ├── metadata.json
│   ├── review-report.md
│   ├── summary.md
│   └── original-contract.pdf
└── ...
```

## Skill Architecture

```
opc-contract-manager/
├── SKILL.md                                      # Core workflow (~250 lines)
├── README.md                                     # This file
├── LICENSE                                       # MIT
├── references/
│   ├── red-flags-checklist.md                    # 30+ red flags across 10 categories
│   ├── standard-clauses.md                       # Balanced clause examples + 6 type-specific checklists
│   ├── solo-entrepreneur-concerns.md             # 12 risk factors specific to one-person companies
│   └── termination-for-convenience.md            # Deep-dive: 11 analysis dimensions + counter-proposals
├── templates/
│   ├── review-report.md                          # 11-section report (decision snapshot → email draft)
│   ├── contract-metadata-schema.json             # 40+ field JSON schema
│   ├── risk-matrix.md                            # Dual-dimension scoring framework
│   ├── key-dates-tracker.md                      # Event + owner + consequence tracking
│   └── contract-summary.md                       # One-page contract summary
└── scripts/
    ├── deadline_checker.py                       # Deadline scanner (--json, --human, --quiet)
    └── index_builder.py                          # Index builder + cross-contract insights
```

**Progressive disclosure**: Only `SKILL.md` is loaded initially. Reference files are loaded on-demand during the specific phase that needs them, keeping context lean.

## Requirements

- Claude Code CLI
- Python 3.8+ (for archive scripts — stdlib only, no pip install needed)

## What This Skill Is NOT

This skill is designed for routine commercial contracts. It is **not** a substitute for professional legal advice. Specifically, it will flag and recommend a lawyer for:

- Equity, financing, or investment documents
- Employment classification issues
- Complex regulatory compliance (HIPAA, biometric data, etc.)
- Litigation or dispute-related documents
- International arbitration complexity
- High-value contracts that warrant professional review

## License

MIT
