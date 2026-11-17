## Description:

Generate a 90-day social media calendar in HighLevel Social Planner CSV format by using a client's sitemap for link-back URLs and post topics, then creating AI-written posts and optional AI-generated images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eddieflux](https://clawhub.ai/user/eddieflux)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing operators, agency teams, and developers use this skill to generate a client-specific social calendar CSV for HighLevel Social Planner, with posts based on the client's sitemap and business details. The skill can optionally create matching images and upload them to public hosting so the CSV contains usable image URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Client details, CRM data, sitemap-derived topics, and post prompts may be sent to third-party AI providers.

Mitigation: Confirm client consent, review the generated prompts, and use only approved providers and least-privilege API keys.

Risk: Command-line secrets and hosting credentials may be exposed through shell history, process listings, or unsafe storage.

Mitigation: Avoid passing long-lived secrets on shared systems, rotate credentials after testing, and use dedicated keys or accounts with the minimum required access.

Risk: FTP and public image uploads can expose generated assets or credentials if used on untrusted networks or overly broad hosting accounts.

Mitigation: Prefer SSH with known host verification and an unprivileged account; use FTP only on trusted networks and only when uploads are required.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/eddieflux/skills/highlevel-90d-social-media-generator)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Files, CSV, JSON, Images, Shell commands]

**Output Format:** [HighLevel Social Planner CSV with companion posts JSON, optional image files, and command-line progress output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default output is 45 scheduled posts over 90 days; image generation and public image URLs depend on optional provider and hosting credentials.]

## Skill Version(s):

1.0.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
