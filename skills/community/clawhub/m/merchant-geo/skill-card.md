## Description:

商家GEO推手 helps small merchants collect store materials, generate GEO-optimized promotional content for eight Chinese media platforms, and prepare drafts or browser automation commands for publication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hitjcl](https://clawhub.ai/user/hitjcl)

### License/Terms of Use:

MIT-0

## Use Case:

External small-business merchants use this skill to turn storefront photos, product photos, business-license details, and customer examples into platform-specific promotional articles, short-video scripts, tags, posting guides, and exportable drafts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive merchant identity, contact, license, storefront, product, and personal-photo data.

Mitigation: Use the data only for draft generation, avoid uploading unnecessary personal or license images, and delete local JSON or Markdown outputs after review.

Risk: Browser automation may interact with logged-in publishing accounts and could post or prepare content under the merchant's account.

Mitigation: Require explicit merchant confirmation before publication, avoid saving platform passwords for this workflow, and review the target account and platform page before every final publish action.

Risk: Generated statistics, testimonials, claims, or case-study details may be inaccurate or unsupported.

Mitigation: Verify every factual claim, number, customer quote, and compliance-sensitive statement against merchant-provided evidence before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hitjcl/skills/merchant-geo)
- [Browser Automation Guide](references/browser_automation_guide.md)
- [Client Onboarding Guide](references/client_onboarding_guide.md)
- [GEO Content Templates](references/content_templates.md)
- [GEO Keyword Strategy Guide](references/geo_keywords.md)
- [Platform GEO Guide](references/platform_guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, JSON records, plain-text draft packages, and shell command snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include merchant profiles, generated promotional copy, platform-specific tags, draft files, posting guides, and browser automation steps.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
