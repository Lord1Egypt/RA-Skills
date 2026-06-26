# OPC Product Manager

**Product spec generation for solo entrepreneurs** — turn a one-sentence idea into a build-ready spec that Claude Code (or any AI coding agent) can execute directly.

> **Important**: This is a spec generator, not a project management tool. It outputs structured specifications, not gantt charts or sprint plans.

---

## What It Does

### Idea → Spec
- **Minimum Viable Idea gate** — infers missing context, states assumptions instead of interrogating
- **Product type classification** — auto-detects: web app, API, CLI tool, browser extension, mobile app, static site, automation, AI agent
- **Full build-ready spec** — product brief, user stories, scope fence, tech stack, data model, API sketch, UI/UX flow, build instructions

### Scope Management
- **Complexity scoring** — 1-10 scale based on entities, auth, integrations, real-time, payments
- **MVP enforcement** — actively cuts scope, challenges assumptions, defers non-essential features
- **Scope creep detection** — flags patterns that signal over-building
- **"What NOT to build"** — anti-patterns specific to your product type

### Tech Stack
- **Opinionated defaults** by product type — not a comparison, a decision
- **Solo-friendly** — optimized for fast to build, cheap to run, easy to deploy
- **Cost estimates** — rough monthly cost at launch
- **"Don't do this"** — no microservices, no self-hosted DBs, no custom auth

### Agent Handoff
- **AGENTS.md-style spec** — pure structured instructions for Claude Code
- **Copy-paste commands** — exact setup, test, and deploy commands
- **Acceptance criteria as checkboxes** — agent can verify each requirement

### Review Mode
- **Agent-buildability score** — 7-point checklist: stories, stack, data model, API, commands, scope, clarity
- **Gap analysis** — what's missing for an agent to start building
- **Upgrade offer** — fills gaps and generates complete spec

---

## Installation

### Option 1: Clone the full repo

```bash
git clone https://github.com/LeonFJR/opc-skills.git
```

### Option 2: Copy just this skill

Copy the `opc-product-manager/` directory into your project.

### Option 3: Add to Claude Code settings

In your project's `.claude/settings.json`:

```json
{
  "permissions": {
    "allow": [
      "Read(opc-product-manager/**)"
    ]
  }
}
```

---

## Usage Examples

### Generate a full spec from an idea

```
/opc-product-manager

I want to build a tool that helps freelancers track time and generate invoices
```

### Quick 1-page spec

```
/opc-product-manager

Quick spec: browser extension that blocks distracting websites during focus time
```

### Check if your idea is too complex

```
/opc-product-manager

Scope check: a marketplace for local food producers with real-time delivery tracking,
payment processing, and a review system
```

### Get a tech stack recommendation

```
/opc-product-manager

Tech stack for an AI-powered writing assistant
```

### Generate Claude Code handoff

```
/opc-product-manager

Generate handoff for my task tracker spec
```

### Review an existing spec

```
/opc-product-manager

Review this spec: [paste your PRD]
```

### Check product status

```
/opc-product-manager

What am I building?
```

---

## Archive Structure

```
products/
├── INDEX.json
├── my-task-tracker/
│   ├── spec.md                    # Full build-ready spec
│   ├── handoff.md                 # Claude Code handoff (if generated)
│   └── metadata.json              # Structured metadata
└── focus-blocker-extension/
    ├── spec.md
    └── metadata.json
```

---

## Skill Architecture

```
opc-product-manager/
├── SKILL.md                                    # Core workflow (~380 lines)
├── README.md                                   # This file
├── LICENSE                                     # MIT
├── references/
│   ├── tech-stack-guide.md                     # Stack recommendations by product type
│   ├── user-story-patterns.md                  # Story writing + acceptance criteria patterns
│   └── scope-assessment.md                     # Complexity scoring, MVP cutting rules
├── templates/
│   ├── product-spec.md                         # Full build-ready spec template
│   ├── quick-spec.md                           # 1-page streamlined spec template
│   ├── handoff-spec.md                         # Claude Code AGENTS.md-style handoff template
│   └── product-metadata-schema.json            # Metadata schema
└── scripts/
    └── product_tracker.py                      # Product index, status, complexity tracking
```

**Progressive disclosure**: SKILL.md loads references on-demand during specific phases — the model only reads what it needs for the current task.

---

## Requirements

- Claude Code CLI (or any Claude-based coding agent)
- Python 3.8+ (for `product_tracker.py` — stdlib only, no pip install needed)

---

## What This Skill Is NOT

- **Not a project management tool** — no sprints, no gantt charts, no velocity tracking
- **Not a design tool** — no wireframes, no Figma files, no UI kits
- **Not a code generator** — it generates specs, not code. The agent builds from the spec.
- **Not a market research tool** — no TAM analysis, no competitive matrices
- **Not for enterprise** — no JIRA integration, no stakeholder management, no committee reviews

## When to Involve a Human Expert

📋 **EXPERT RECOMMENDED** scenarios (flagged automatically):
- Regulated data handling (HIPAA, PCI, COPPA)
- Payment processing compliance
- User-generated content at scale
- Enterprise security requirements (SOC 2)
- Infrastructure > $500/month
- Native mobile app development
- Complex multi-tenant permissions
- AI model training/fine-tuning

---

## License

MIT — see [LICENSE](LICENSE).
