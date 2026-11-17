## Description:

LogicArt Code Review analyzes code with LogicArt to identify bugs, security issues, complexity, suggestions, and logic flow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpaulgrayson](https://clawhub.ai/user/jpaulgrayson)

### License/Terms of Use:


## Use Case:

Developers and engineering agents use this skill to submit selected code or local files for LogicArt analysis and present prioritized review findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected code or entire local files may be sent to LogicArt for analysis.

Mitigation: Use the skill only for code you are authorized to share with LogicArt, and avoid confidential repositories, secrets, .env files, private keys, customer data, or regulated code unless approved.

Risk: The artifact supports file-based analysis through --file, which can broaden the amount of local content submitted.

Mitigation: Review the target file path before running analysis and prefer the smallest relevant code snippet when sensitive content may be nearby.

## Reference(s):

- [LogicArt](https://logic.art)
- [LogicArt Analyze API](https://logic.art/api/agent/analyze)
- [Validate Repo](https://validate-repo.replit.app)
- [ClawHub Release Page](https://clawhub.ai/jpaulgrayson/skills/logicart-review)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [JSON from the analyzer, typically summarized by the agent as Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include bugs, security issues, complexity score, suggestions, and logic flow when returned by LogicArt.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
