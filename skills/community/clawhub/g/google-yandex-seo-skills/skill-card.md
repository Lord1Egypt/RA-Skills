## Description:

Use this skill when the user wants an SEO audit, technical SEO review, page-level Google or Yandex analysis, robots.txt or sitemap validation, canonical/indexability checks, or a client-ready SEO report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[horosheff](https://clawhub.ai/user/horosheff)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, SEO specialists, and site owners use this skill to run local page-level SEO audits for Google and Yandex, then turn the generated findings into prioritized remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The crawler can fetch arbitrary user-provided URLs, which may expose internal network services or cloud metadata endpoints when run from sensitive networks.

Mitigation: Audit only trusted URLs, or run the skill in an isolated network with URL allowlists, private-IP blocking, same-origin sitemap limits, timeouts, body-size limits, and dependency updates.

Risk: SEO and GEO findings are heuristic and limited to local HTML parsing, so they can miss browser-rendered behavior, Core Web Vitals, backlinks, SERP signals, competitor data, and live LLM citation behavior.

Mitigation: Treat findings as triage guidance and validate high-impact recommendations with authoritative search, browser-rendering, analytics, and performance tooling before making production decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/horosheff/skills/google-yandex-seo-skills)
- [Install Guide](references/install.md)
- [Check Inventory](references/checks.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown report and JSON findings, with concise text summaries and shell commands for local execution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes audit artifacts to a configured output directory; default mode is single-page, with internal crawl mode only when explicitly requested.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
