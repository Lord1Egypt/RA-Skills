## Description: <br>
Prospector Lite is a B2B outreach framework for OpenClaw agents that structures prospect research, email verification, bounce handling, pipeline tracking, duplicate prevention, domain reputation protection, and lessons learned. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nicuahmadi](https://clawhub.ai/user/nicuahmadi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, revenue teams, and agent operators use this skill to run reputation-aware B2B prospecting workflows, including prospect qualification, verified work-email outreach, follow-up handling, and pipeline tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can support recurring B2B cold outreach and mailbox review without clear approval boundaries. <br>
Mitigation: Use a dedicated sending account or labeled mailbox, review recipients and drafts before live sends, and disable or tightly control any prospecting cron. <br>
Risk: Cold outreach can create anti-spam, privacy, opt-out, and sender-reputation exposure. <br>
Mitigation: Confirm legal and policy compliance before use, enforce verified work-email rules, respect opt-outs, process bounces, and keep daily send limits low. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nicuahmadi/prospector-lite) <br>
- [Publisher profile](https://clawhub.ai/user/nicuahmadi) <br>
- [Sora Labs](https://sora-labs.net) <br>
- [Sora Labs tools](https://sora-labs.net/tools/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with email templates, tracking-file templates, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides the agent to create and update prospects/pipeline.md, prospects/lessons-learned.md, and PRODUCTS.md; live email sending depends on separately configured mail tooling.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and OpenClaw frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
