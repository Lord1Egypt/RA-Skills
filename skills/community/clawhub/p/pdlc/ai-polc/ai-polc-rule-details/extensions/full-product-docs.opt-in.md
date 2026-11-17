<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Extension: Full Product Docs (Opt-In Prompt)

**Trigger:** User mentions "PRD", "feature brief", "product wiki", "product documentation templates"
**Stage:** 12 (Product Documentation)

---

## Detection

If any of the following are true, present this prompt:
- User explicitly requests PRD or feature brief templates
- Stakeholder Density = High and Market = B2B or Enterprise
- Depth = Comprehensive

## Activation Prompt

```
I detect you'd benefit from the Full Product Docs extension.

This upgrades Stage 12 from release notes governance to:
• PRD template (problem → solution → scope → metrics → timeline)
• Feature brief template (for pre-build stakeholder communication)
• Product wiki governance (structure, ownership, update cadence)
• API change communication template (for developer-facing products)

This is useful for enterprise products, B2B with contractual documentation,
or teams with heavy stakeholder communication needs.

Activate Full Product Docs? (yes/no)
```

If yes → load `full-product-docs.md`
