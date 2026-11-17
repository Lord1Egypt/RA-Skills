## Description:

Build complete local lead generation websites with SEO optimization, conversion tracking, and RGPD compliance for service businesses targeting local markets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucasgulino](https://clawhub.ai/user/lucasgulino)

### License/Terms of Use:


## Use Case:

Developers and website-building agents use this skill to plan and generate local lead-generation websites with service pages, SEO metadata, structured data, contact flows, cookie consent, and legal pages. It is aimed at local service businesses such as trades, repairs, and professional services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Page generation can write files based on user-provided JSON and templates.

Mitigation: Use only trusted templates and data, then add filename containment checks and schema validation before production use.

Risk: The bundled contact form logs lead data and shows success without confirmed backend delivery.

Mitigation: Remove lead-data console logging, submit over HTTPS to a real backend or CRM, and show success only after delivery is confirmed.

Risk: Lead-generation websites can become misleading or spam-like if they use cloned location pages, fake proof, or unclear marketplace disclosure.

Mitigation: Apply the bundled anti-spam guardrails, use original local content and real proof, and disclose lead-generation or intermediary status on key pages.

Risk: The RGPD materials are templates and may not satisfy every legal or jurisdiction-specific requirement.

Mitigation: Have legal and privacy reviewers adapt the cookie, privacy, legal notice, consent, and data-retention language before launch.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lucasgulino/skills/lead-gen-website)
- [SEO Checklist for Lead Generation Websites](references/seo-checklist.md)
- [Conversion Best Practices for Lead Generation Websites](references/conversion-best-practices.md)
- [RGPD Compliance Guide for Lead Generation Websites](references/rgpd-compliance.md)
- [Garde-fous anti-spam](references/google-spam-guardrails-2024.md)
- [GBP Playbook](references/gbp-local-seo-playbook.md)
- [Micro-budget Ads Playbook](references/ads-micro-budget-4eur-playbook.md)
- [Schema.org](https://schema.org)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with TypeScript/React templates, JSON examples, generated files, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces website plans, React components and pages, SEO files, structured-data guidance, conversion tracking patterns, and compliance checklists.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
