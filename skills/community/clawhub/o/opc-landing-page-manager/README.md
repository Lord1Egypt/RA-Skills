# OPC Landing Page Manager — Claude Code Skill

A landing page strategist, copywriter, and builder for solo entrepreneurs and one-person company CEOs.

Give it a product idea, and it takes you from **strategic positioning to a complete, self-contained HTML landing page** — covering copywriting frameworks, conversion optimization, responsive design, and accessibility.

## What It Does

### Strategy
- **Minimum Viable Brief (MVB) gate** — infers missing context, states assumptions instead of interrogating
- **Evidence tier assessment** — classifies projects as Tier 1 (outcome proof), Tier 2 (mechanism proof), or Tier 3 (preview) based on available evidence
- **Page type selection** — forces one of 4 page types (waitlist, demo booking, direct purchase, service lead-gen) with locked section orders
- **Target audience analysis** — who, what they want, what frustrates them
- **Value proposition crafting** — specific, benefit-led positioning
- **Competitive positioning** — what makes your product different
- **Conversion goal definition** — matching CTA to product stage
- **Framework selection** — PAS, AIDA, BAB, 4Ps, StoryBrand — chosen for your product type
- **Strategy canvas** — one-page strategic foundation document

### Copywriting
- **Section-by-section copy** — hero, problem, solution, features, how-it-works, FAQ, CTA
- **Proven frameworks** — not generic filler, every sentence relates to your product
- **Headline formulas** — specific, benefit-led, under 12 words
- **CTA optimization** — action + benefit, risk reversal, no "Submit" buttons
- **SEO + social meta** — page title, description, Open Graph tags
- **Copy brief** — structured document for review before building

### Design
- **Pre-built color palettes** — SaaS/Tech, Creative, Business, Bold, Minimal, Dark Mode
- **Typography system** — system fonts by default, Google Fonts on request
- **Layout patterns** — split hero, centered, full-width, responsive grids
- **Spacing system** — consistent vertical rhythm and section spacing
- **Component styles** — buttons, cards, sections with hover effects

### Code Generation
- **Self-contained HTML** — single file, inline CSS, no external dependencies
- **Responsive** — mobile-first, works on 320px to 1280px+
- **Accessible** — semantic HTML, WCAG AA contrast, skip navigation, keyboard-navigable
- **Print-ready** — clean print styles included
- **Image placeholders** — CSS gradient placeholders with replacement instructions

### Iteration & Variants
- **Section-level editing** — "Change the headline", "Rewrite the FAQ"
- **Tone adjustment** — professional, casual, bold
- **A/B variants** — 3 headline options, CTA alternatives, layout variations
- **Design pivots** — switch color palettes, hero layouts, section order

### Review Mode
- **7-category rubric** — Clarity, Offer, Proof, Friction, Mobile, Accessibility, SEO/Social
- **Fixed scoring** — each category 1-5 with automatic-fail conditions, overall grade bands
- **Specific improvements** — top 3 prioritized recommendations, not generic advice

### Readiness Tracking
- **Publish-readiness score** — 0-100 score based on CTA targets, privacy/terms, analytics, assets, blockers
- **Compliance checks** — hard rules for privacy policy (data collection), terms of service (payments), cookie consent (EU)
- **Missing assets tracking** — what's still needed before launch
- **Publish blockers** — issues that must be resolved before going live

### Cross-Skill Integration
- **Contract linkage** — pull client info, pricing, and legal entity from opc-contract-manager
- **Invoice linkage** — track related invoices from opc-invoice-manager

## Installation

### Option 1: Clone to skills directory

```bash
git clone https://github.com/LeonFJR/opc-skills.git ~/.claude/skills/opc-skills
```

### Option 2: Copy just this skill

```bash
cp -r opc-landing-page-manager ~/.claude/skills/opc-landing-page-manager
```

### Option 3: Project-level skill

Add to your project's `.claude/settings.json`:

```json
{
  "skills": ["path/to/opc-landing-page-manager"]
}
```

## Usage

### Build a landing page from a product idea

```
/opc-landing-page-manager

I'm building a time-tracking tool for freelance designers.
It auto-detects which project you're working on from your Figma files.
$15/month. Launching next month.
```

The skill walks through Strategy → Copy → Design → Build, generating a complete landing page.

### Quick build (skip strategy)

```
/opc-landing-page-manager

Build me a landing page for InvoiceBot — an invoicing tool for solo founders.
Headline: "Get paid 2x faster"
CTA: "Start your free trial"
Features: auto-invoicing, payment reminders, cash flow dashboard
```

### Strategy only

```
/opc-landing-page-manager

Help me think through the positioning for my new
developer productivity tool. I'm not sure who to target.
```

### Iterate on an existing page

```
/opc-landing-page-manager

Change the hero to a centered layout and make the
headline more urgent. Keep everything else the same.
```

### Generate copy variants

```
/opc-landing-page-manager

Give me 3 headline options for my landing page.
Current: "The fastest way to manage your contracts"
```

### Review an existing page

```
/opc-landing-page-manager

Review this landing page and tell me how to improve conversions:
[paste HTML or provide file path]
```

### Review with rubric scoring

```
/opc-landing-page-manager

Review this landing page and score it:
[paste HTML or provide file path]
```

### Check project status

```
/opc-landing-page-manager

Show me my landing page projects
```

### Audit HTML quality

```bash
python3 scripts/page_audit.py my-page.html
python3 scripts/page_audit.py my-page.html --compliance
python3 scripts/page_audit.py --dir ./landing-pages --json
```

### Check readiness

```bash
python3 scripts/project_tracker.py --readiness ./landing-pages
```

### Cross-skill integration

```
/opc-landing-page-manager

Build a landing page for the product in contract 2026-01-15_acme_service-agreement
```

## Project Structure

```
landing-pages/
├── INDEX.json                                    # Master index (auto-generated)
├── my-product/
│   ├── index.html                                # Generated landing page
│   ├── metadata.json                             # Project metadata
│   ├── strategy-canvas.md                        # Strategy document
│   └── copy-brief.md                             # Copy document
├── my-product/v2/                                # Version 2 (after iteration)
│   ├── index.html
│   └── metadata.json
└── ...
```

## Skill Architecture

```
opc-landing-page-manager/
├── SKILL.md                                      # Core workflow (~370 lines)
├── README.md                                     # This file
├── LICENSE                                       # MIT
├── references/
│   ├── copywriting-frameworks.md                 # PAS, AIDA, BAB, 4Ps, StoryBrand + headline formulas
│   ├── landing-page-anatomy.md                   # Section order, page type templates, product-type recs
│   ├── conversion-optimization.md                # Conversion principles, evidence tiers, compliance rules
│   ├── design-system.md                          # Color palettes, typography, spacing, layout, components
│   └── review-rubric.md                          # 7-category fixed scoring rubric for Review mode
├── templates/
│   ├── landing-page.html                         # HTML template — general purpose (structural reference)
│   ├── waitlist-page.html                        # HTML template — waitlist/pre-launch pages
│   ├── service-page.html                         # HTML template — service/consulting lead-gen pages
│   ├── project-metadata-schema.json              # Full project metadata schema
│   ├── strategy-canvas.md                        # Strategy canvas template
│   └── copy-brief.md                             # Copy brief template
└── scripts/
    ├── project_tracker.py                        # Project index, status, readiness, version tracking
    └── page_audit.py                             # HTML structural quality and compliance auditor
```

**Progressive disclosure**: Only `SKILL.md` is loaded initially. Reference files are loaded on-demand during the specific phase that needs them.

## Requirements

- Claude Code CLI
- Python 3.8+ (for project tracker — stdlib only, no pip install needed)

## What This Skill Is NOT

This skill generates landing pages as self-contained HTML files. It is **not**:

- A full website builder (multi-page sites, routing, backend)
- A graphic design tool (custom illustrations, logo creation, photo editing)
- An SEO audit tool (keyword research, backlink analysis)
- A hosting or deployment service
- An A/B testing platform (it generates variants; you test them)
- A CMS (it generates static files; no database, no admin panel)

## License

MIT
