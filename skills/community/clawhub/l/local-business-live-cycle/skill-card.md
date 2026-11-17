## Description:

AI operations advisor for local business owners that helps diagnose stores, draft short-video scripts, prepare livestream frameworks, write livestream scripts, review performance data, and answer operations questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1027399464-tech](https://clawhub.ai/user/1027399464-tech)

### License/Terms of Use:

MIT-0

## Use Case:

External local business owners and operators use this skill to diagnose store readiness, plan Douyin-oriented short video and livestream workflows, generate customer-acquisition scripts, and turn performance data into next actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary flags under-disclosed commercial handoffs and external data-sharing prompts.

Mitigation: Disclose any Notion or WeChat handoff before use and do not share merchant reports, screenshots, or metrics externally unless the merchant consents and sensitive details are redacted.

Risk: The security guidance notes that generated HTML reports may load remote scripts.

Mitigation: Review generated HTML before distribution and pin or bundle remote dependencies locally where possible.

Risk: The security summary flags local file and process side effects.

Mitigation: Review expected local writes and process actions before installation, especially when handling merchant data.

## Reference(s):

- [Server-resolved GitHub import](https://github.com/1027399464-tech/local-business-live-skills/tree/main/local-business-live-cycle)
- [ClawHub skill page](https://clawhub.ai/1027399464-tech/skills/local-business-live-cycle)
- [diagnosis-questions.md](references/diagnosis-questions.md)
- [tongcheng-live-pattern.md](references/tongcheng-live-pattern.md)
- [standalone-html-tool.md](references/standalone-html-tool.md)
- [trace-evaluation-20260720.md](references/trace-evaluation-20260720.md)
- [darwin-evaluation-20260720.md](references/darwin-evaluation-20260720.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, plain text, code snippets, shell commands, configuration instructions, and generated HTML report templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce merchant-facing reports, video scripts, livestream scripts, diagnostic recommendations, and operational checklists.]

## Skill Version(s):

0.1.0 (source: server release metadata; SKILL.md frontmatter reports 2.4.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
