## Description:

Investigate public online footprints using open-source intelligence techniques across usernames, emails, people, companies, domains, IPs, phone numbers, locations, images, and other public targets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elyasuuuuu](https://clawhub.ai/user/elyasuuuuu)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and security teams use this skill for authorized public-footprint investigations, defensive exposure checks, account-correlation review, domain or IP enrichment, and structured OSINT reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The domain helper can execute shell commands from unsanitized domain input.

Mitigation: Do not run the domain helper until domain validation is added and whois/dig are invoked without bash.

Risk: Profile, IP, domain, and HIBP checks can disclose target identifiers to third-party services.

Mitigation: Use the skill only for authorized public defensive investigations and avoid checks that are not necessary for the user-approved purpose.

Risk: Exported reports may aggregate personal data from public sources.

Mitigation: Store and share reports with appropriate access controls and keep raw evidence separate from summary judgments.

## Reference(s):

- [Investigator Skill Page](https://clawhub.ai/elyasuuuuu/skills/investigator)
- [elyasuuuuu Publisher Profile](https://clawhub.ai/user/elyasuuuuu)
- [Aggregation](references/aggregation.md)
- [API Integrations](references/apis.md)
- [Breach Checks](references/breach-checks.md)
- [Configuration](references/configuration.md)
- [Modules](references/modules.md)
- [OSINT Sources](references/osint-sources.md)
- [Output](references/output.md)
- [Platform Validation](references/platform-validation.md)
- [Platforms](references/platforms.md)
- [Profile Media](references/profile-media.md)
- [Report Format](references/report-format.md)
- [Safety](references/safety.md)
- [Scoring](references/scoring.md)
- [Target Types](references/target-types.md)
- [Tooling](references/tooling.md)
- [Username Variants](references/variants.md)
- [Workflow](references/workflow.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Concise Markdown summaries, optional extended reports, structured JSON exports, and shell commands for helper scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should distinguish confirmed, likely, weak, not-verifiable, and no-evidence findings and should keep raw evidence separate from summary judgments.]

## Skill Version(s):

2.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
