## Description:

Helps advertising agencies and brand marketers plan AI-assisted image, short-video, and content marketing workflows with audience strategy, content calendars, prompts, platform rewrites, AI-HIVE task records, and review gates for factual accuracy, authorization, and commercial claims.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers, agency teams, creators, and content partners use this skill to produce reviewable Chinese advertising-agency marketing plans, image and video prompts, AI-HIVE generation commands, and post-campaign review structures. It is intended for workflows where facts, rights to media, budget, routing, and platform requirements are checked before paid generation or publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials can be sent to a user-configurable API host.

Mitigation: Use only the official AI-HIVE endpoint unless the alternate host is fully trusted, and keep API keys limited, rotatable, and out of files, screenshots, logs, and version control.

Risk: The skill can automatically download unvalidated remote generation results.

Mitigation: Use --no-download or a dedicated output directory for untrusted tasks, then review downloaded media before opening, publishing, or reusing it.

Risk: Marketing outputs can include inaccurate facts, unauthorized media use, or unsupported commercial-performance claims.

Mitigation: Verify product facts, prices, qualifications, source media rights, and platform requirements before generation or publication; label AI-generated or illustrative material and avoid promises about virality, ranking, approvals, sales, or return on investment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wubin1836/skills/industry-advertising-agency-marketing-ai-hive)
- [Publisher Profile](https://clawhub.ai/user/wubin1836)
- [AI-HIVE](https://ai-hive.iclip.cn/chat)
- [Advertising Agency Image and Video Marketing Playbook](references/industry-playbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON files and inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include AI-HIVE task records, prompt sets, platform-specific rewrites, and review checklists.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
