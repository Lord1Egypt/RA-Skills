## Description:

Infoseek finds and evaluates web sources, analyzes entities and conflicting claims across sources, and produces structured research reports with optional local archiving.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gyint](https://clawhub.ai/user/gyint)

### License/Terms of Use:

MIT

## Use Case:

Researchers, analysts, and developers can use Infoseek to gather and compare sources for industry, trend, competitor, market, and technology research, then save structured reports for later reference.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HTTP hosting or credential-assisted browsing can expose local files or API keys.

Mitigation: Prefer local stdio operation in an isolated environment with only necessary keys. Keep HTTP hosting and credential-assisted browsing disabled until built-in administrator access, unrestricted file access, and credential origin matching are fixed.

Risk: External providers, private inputs, and untrusted datasets can create data exposure risks.

Mitigation: Verify provider destinations, disable tracing for private inputs, and load only trusted NumPy datasets.

## Reference(s):

- [Infoseek source repository](https://github.com/GYINT/infoseek)
- [Infoseek on ClawHub](https://clawhub.ai/gyint/skills/info-seek)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown]

**Output Format:** [Structured Markdown research reports with source summaries and cross-source analysis; optional local archives]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Content varies by research topic and available sources; archiving is optional.]

## Skill Version(s):

2.2.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
