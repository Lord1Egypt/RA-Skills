## Description:

Routes ambiguous local skill requests to the most appropriate downstream skill before the agent reads and follows that skill's instructions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chaoyang78](https://clawhub.ai/user/chaoyang78)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill when a request could match multiple locally installed skills and the agent needs to choose the right downstream skill first. It is especially focused on high-overlap clusters such as ACP/ACPX harness workflows, Lark, WeChat/Official Accounts, Xiaohongshu, and OpenCLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may route an agent toward downstream skills that perform account actions, publishing, posting, or harness delegation.

Mitigation: Review downstream skills separately before allowing account actions, publishing workflows, posting workflows, or harness delegation.

Risk: Chinese-language routing guidance may be misunderstood by reviewers or operators who cannot read the source language.

Mitigation: Have a qualified reviewer confirm the routing table and overlap rules before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chaoyang78/skills/local-skills-router)
- [ClawHub Publisher Profile](https://clawhub.ai/user/chaoyang78)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown routing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill itself provides routing guidance and does not bundle executable code, persistence, credentials, or hidden execution behavior.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
