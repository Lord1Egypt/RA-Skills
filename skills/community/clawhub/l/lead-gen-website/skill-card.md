## Description: <br>
Build complete local lead generation websites with SEO optimization, conversion tracking, and RGPD compliance. Use for creating service-based websites targeting local markets (plumbers, electricians, home services, etc.) with 10-20 pages, structured data, analytics, and legal compliance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LucasGulino](https://clawhub.ai/user/LucasGulino) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and site-building agents use this skill to plan, build, optimize, and validate local service lead generation websites with SEO, conversion tracking, RGPD-oriented legal pages, cookie consent, and local marketing deliverables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled contact form handles personal lead data and currently logs submitted form data in the browser console. <br>
Mitigation: Replace the placeholder submission handler with a secured backend or CRM flow, remove console logging, and avoid exposing personal lead data in client-side logs. <br>
Risk: The skill claims RGPD/GDPR compliance, but privacy notice, lawful basis, consent handling, and recipient disclosure must be implemented for each generated site. <br>
Mitigation: Add visible privacy information near forms, disclose analytics, UTM, CRM, and WhatsApp recipients, and ensure non-essential tracking loads only after valid consent. <br>
Risk: Lead records and WhatsApp conversation logs can create retention and access-control obligations. <br>
Mitigation: Define retention, deletion, access-control, and anonymization rules before production use, and document how users can exercise data rights. <br>
Risk: Local lead-generation SEO can drift into doorway pages, scaled generic content, fake addresses, or misleading service claims. <br>
Mitigation: Apply the bundled anti-spam guardrails: keep pages original and intent-focused, avoid cloned city pages, use real NAP/business details, and disclose intermediary lead-generation models on key pages. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/LucasGulino/lead-gen-website) <br>
- [Publisher profile](https://clawhub.ai/user/LucasGulino) <br>
- [SEO Checklist for Lead Generation Websites](references/seo-checklist.md) <br>
- [Conversion Best Practices for Lead Generation Websites](references/conversion-best-practices.md) <br>
- [RGPD Compliance Guide for Lead Generation Websites](references/rgpd-compliance.md) <br>
- [Garde-fous anti-spam (Google Spam Policies + March 2024)](references/google-spam-guardrails-2024.md) <br>
- [GBP Playbook (Local SEO) - Relevance / Distance / Prominence](references/gbp-local-seo-playbook.md) <br>
- [Micro-budget Ads (4 EUR/jour) - Playbook](references/ads-micro-budget-4eur-playbook.md) <br>
- [WhatsApp Ops - Qualification & Log](references/whatsapp-ops-qualification.md) <br>
- [Design Philosophy Examples for Lead Generation Websites](references/design-philosophies.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline code, shell commands, JSON examples, generated project files, React templates, and SEO/legal configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce content structures, design ideas, React components/pages, robots.txt, sitemap.xml, JSON-LD snippets, GBP and ads checklists, validation notes, and delivery summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
