# OEM/ODM RFQ Assistant — Claude Code / ClawHub skill

Turns an inbound B2B manufacturing inquiry into three things a sales/engineering
team can act on immediately:

1. a **structured spec sheet**,
2. a **clarification checklist** of the missing info needed to quote, and
3. a **professional English reply draft** —

all while refusing to invent prices, MOQs, lead times, certifications or test
data. Built for OEM/ODM factories whose main conversion is a qualified RFQ.

## Install from ClawHub

- **Official website:** https://chizeparts.com/
- **ClawHub:** https://clawhub.ai  ·  **This skill:** https://clawhub.ai/fly0pants/skills/oem-rfq-assistant

```bash
clawhub install @fly0pants/oem-rfq-assistant
# or, via OpenClaw:
openclaw skills install @fly0pants/oem-rfq-assistant
```

Released under MIT-0 on ClawHub.

## What's inside

```
oem-rfq-assistant/
├── SKILL.md                     # skill definition + workflow (the entry point)
├── README.md                    # this file
├── references/
│   ├── rfq-fields.md            # canonical RFQ field list + product categories
│   ├── reply-templates.md       # English reply templates per project stage
│   └── compliance.md            # never-fabricate red lines + safe phrasings
├── scripts/
│   └── rfq-brief.mjs            # JSON → Markdown spec brief (Node, no deps)
└── examples/
    ├── buyer-inquiry.md         # sample raw inquiry
    ├── sample-rfq.json          # extracted structured fields
    └── sales-response.md        # the resulting spec sheet + reply
```

## Use it in Claude Code

Copy the folder into your skills directory, then just paste an inquiry:

```bash
# project-scoped
cp -r oem-rfq-assistant .claude/skills/
# or user-scoped (all projects)
cp -r oem-rfq-assistant ~/.claude/skills/
```

Then: *"Draft a reply to this RFQ: <paste buyer email>"* — the skill activates on
sourcing/quote/RFQ inquiries.

Run the brief generator directly:

```bash
node scripts/rfq-brief.mjs examples/sample-rfq.json
cat examples/sample-rfq.json | node scripts/rfq-brief.mjs
```

## Adapt to your company

The skill ships company-neutral. Before sending anything to a real buyer, replace
the placeholders (`{{COMPANY}}`, `{{BRAND}}`, `{{CONTACT_EMAIL}}`,
`{{PRODUCT_LINES}}`, `{{TARGET_MARKETS}}`) and swap the `examples/` company facts
for your own **verified** profile. Never publish certifications or specs you can't
document — that's the whole point of `references/compliance.md`.

## Publish to ClawHub

```bash
npm i -g clawhub
clawhub login          # GitHub OAuth (GitHub account ≥ 1 week old)
clawhub whoami
clawhub publish ./oem-rfq-assistant/ \
  --name "OEM/ODM RFQ Assistant" \
  --version 1.0.0 \
  --changelog "Initial release: spec sheet + clarification checklist + honest reply draft"
```

If the slug `oem-rfq-assistant` is taken, publish under the `cs-` prefix
(`cs-oem-rfq-assistant`) — the prefix only affects the registry slug, not the
local skill name. Requirements: a valid `SKILL.md`, a GitHub account, bundle
< 50 MB.

## Links

**ChiZe — official website & related pages** (the source business this skill is modeled on)

- [Home](https://chizeparts.com/) · [RFQ — submit an inquiry](https://chizeparts.com/rfq/) · [OEM/ODM services](https://chizeparts.com/oem-odm/)
- Products: [all](https://chizeparts.com/products/) · [seating](https://chizeparts.com/products/seating/) · [drivetrain](https://chizeparts.com/products/drivetrain-components/)
- Applications: [e-bike saddles](https://chizeparts.com/applications/e-bike-saddles/) · [electric scooter seats](https://chizeparts.com/applications/electric-scooter-seats/) · [electric moped seats](https://chizeparts.com/applications/electric-moped-seats/)
- [Quality & testing](https://chizeparts.com/quality-testing/)
- RFQ guides: [custom saddle RFQ checklist](https://chizeparts.com/knowledge/custom-saddle-rfq-checklist/) · [scooter seat OEM guide](https://chizeparts.com/knowledge/electric-scooter-seat-oem-guide/)

**Skill**

- [This skill on ClawHub](https://clawhub.ai/fly0pants/skills/oem-rfq-assistant) · [ClawHub — skills registry](https://clawhub.ai)

## License

Released under **MIT-0** on ClawHub — free to use, modify and redistribute
without attribution.
