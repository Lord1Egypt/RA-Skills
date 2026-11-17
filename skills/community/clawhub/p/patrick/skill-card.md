## Description:

Access Patrick's expertise library for executive decision infrastructure, including executive briefings, decision framing, commitment tracking, team health analysis, and strategic planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mcsh](https://clawhub.ai/user/mcsh)

### License/Terms of Use:


## Use Case:

Developers and AI-agent operators use this skill to fetch licensed Patrick executive expertise templates, provide company context, run the templates through an LLM, and optionally store structured results for continuity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad access to company data before running Patrick expertise.

Mitigation: Approve each company data source explicitly and limit the agent to the minimum files needed for the selected expertise workflow.

Risk: License-token handling in the artifact asks users to paste a license into chat.

Mitigation: Use a local secret mechanism or direct CLI configuration, and do not paste license tokens into chat transcripts.

Risk: The install flow downloads mutable latest executables, including curl-to-bash guidance.

Mitigation: Avoid curl-to-bash/latest installs for production; require pinned, signed artifacts and verify checksums before execution.

Risk: Patrick workflows may send or store executive and company context through a third-party service.

Mitigation: Use the skill only after confirming trust in the Patrick publisher and service for the relevant company data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mcsh/skills/patrick)
- [Publisher profile](https://clawhub.ai/user/mcsh)
- [Patrick website](https://patrickbot.io)
- [Patrick portal downloads](https://portal.patrickbot.io/downloads/latest/)
- [artifact/SKILL.md](artifact/SKILL.md)
- [artifact/install.md](artifact/install.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON examples; Patrick CLI responses may be structured JSON, markdown, or mixed content.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the patrick-cli binary and a Patrick license; some workflows read local company context and may send or store results through the Patrick service.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
