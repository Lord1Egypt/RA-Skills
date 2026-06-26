## Description: <br>
Capture successful OpenClaw interactions and convert them into reusable skills with an optimized execution path summary, then publish to ClawHub and distribute bilingual sharing posts to Moltbook, Zhihu, Xiaohongshu, or other configured channels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JimmyWangJimmy](https://clawhub.ai/user/JimmyWangJimmy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to turn a completed, successful workflow into reusable skill artifacts, an optimal execution path summary, a ClawHub publish payload, and bilingual distribution copy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish generated content externally when real publish or sharing flags and credentials are supplied. <br>
Mitigation: Use dry-run first, inspect the generated skill bundle and share_payloads, remove private workflow details, and provide only scoped ClawHub tokens or webhook URLs for intended destinations. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/JimmyWangJimmy/openclaw-success-skill-publisher) <br>
- [Publish Contract](references/publish_contract.md) <br>
- [ClawHub Publish Copy](docs_clawhub_publish_bilingual.md) <br>
- [ClawHub API Base](https://api.clawhub.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown, JSON, generated skill files, shell command examples, and configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces summary.md, optimal_path.md, generated_skill/, share_payloads/, and publish_report.json; dry-run mode keeps publish and sharing payloads local.] <br>

## Skill Version(s): <br>
1.0.3 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
