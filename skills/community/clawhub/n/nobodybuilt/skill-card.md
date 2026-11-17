## Description:

nobodybuilt helps agents find validated, underexplored tool or project ideas from text or images, then produce scored concepts, complete project files, and launch strategy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kewang0622](https://clawhub.ai/user/kewang0622)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and builders use this skill to research product gaps, validate demand, rank ideas, generate publishable project artifacts, and prepare launch materials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security verdict is suspicious because the skill can guide agents into publishing, repository, and package-install actions with weak approval and supply-chain controls.

Mitigation: Review before installing, prefer a reviewed local file or pinned commit, and require explicit confirmation before npm install, npx execution, git push, repository creation, marketplace submission, or authenticated publishing.

Risk: The skill can analyze screenshots, photos, and social posts, which may contain private account data or sensitive context.

Mitigation: Avoid sharing private screenshots, credentials, account data, or confidential product information unless the agent environment is approved for that data.

Risk: The skill asks agents to validate product gaps using web searches, so incomplete or stale searches could lead to misleading opportunity claims.

Mitigation: Require cited, current search evidence for gap, demand, name-collision, and traction claims before acting on recommendations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kewang0622/skills/nobodybuilt)
- [Skill Marketplace Publishing Guide](references/MARKETPLACES.md)
- [README Template for Generated Projects](references/README-TEMPLATE.md)
- [Scoring Calibration Reference](references/SCORING.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with code blocks, file contents, ranked score tables, and launch copy]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands for package installation, repository creation, marketplace publishing, and authenticated submission workflows.]

## Skill Version(s):

1.1.0 (source: ClawHub server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
