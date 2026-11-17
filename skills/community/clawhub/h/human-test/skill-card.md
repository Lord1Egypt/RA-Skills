## Description:

Call real humans to test your product (URL or app). Get structured usability feedback with screen recordings, NPS scores, and AI-aggregated findings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[avivahe326](https://clawhub.ai/user/avivahe326)

### License/Terms of Use:


## Use Case:

Developers, product teams, and agents use this skill to request human usability testing for a product URL or app and receive structured feedback, NPS scores, screen-recording analysis, and prioritized recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hosted testing may expose product workflows, staging systems, or user data to third-party testers.

Mitigation: Use hosted testing only for products and workflows appropriate for third-party review, and avoid sensitive user data or private staging systems unless a data-handling agreement is in place.

Risk: Self-hosting asks users to install and run an unpinned package and expose AI API keys.

Mitigation: Run self-hosted deployments in an isolated environment, review and pin the package source/version first, and expose only one low-privilege API key.

Risk: Repo-aware code fix features may require granting repository access to an external GitHub account.

Mitigation: Prefer a disposable mirror or read-only repository access, revoke access after use, and manually review every generated diff or PR before merging.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/avivahe326/skills/human-test)
- [Human Test web platform](https://human-test.work)
- [Server-resolved publisher profile](https://clawhub.ai/user/avivahe326)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown usability reports, JSON API responses and webhook payloads, curl commands, and optional code-fix diffs or PR links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include metadata, severity-ranked issues, evidence, impact, recommendations, NPS analysis, and prioritized next steps.]

## Skill Version(s):

1.6.1 (source: server release metadata; artifact frontmatter reports 1.6.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
