## Description:

Queries the public M5Burner/M5Stack firmware repository by keyword, device, category, functional intent, ID, version, developer, UIFlow2 release, recommendation, ranking, or comment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuyun2000](https://clawhub.ai/user/yuyun2000)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and agents use this skill to answer public M5Stack firmware discovery questions and retrieve current M5Burner catalog metadata. It supports read-only searches, detail lookups, version history, device and category lookup, developer firmware listings, UIFlow2 releases, rankings, comments, and recommendation-style candidate generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Firmware search terms and lookup details are sent to the public M5Burner service.

Mitigation: Use the skill only for public firmware discovery questions and avoid submitting sensitive project, device, or account information in queries.

Risk: The API base URL is configurable, which could send queries to an untrusted compatible deployment.

Mitigation: Keep the default HTTPS M5Burner endpoint unless intentionally testing against a deployment you control and trust.

Risk: Firmware descriptions, comments, and source URLs are public third-party content and may be incomplete or misleading.

Mitigation: Treat returned metadata as discovery information, verify important claims manually, and avoid presenting popularity or heuristic scores as quality or compatibility guarantees.

Risk: Account credentials or bearer tokens could expose private capabilities that are outside the skill scope.

Mitigation: Do not provide, request, print, or persist bearer tokens or account credentials; use only documented public catalog routes.

## Reference(s):

- [M5Burner Public Query API](references/api.md)
- [M5Burner Public Firmware Service](https://burner.m5stack.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and JSON or table command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses live public M5Burner data and should include retrieval dates when values may change.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
