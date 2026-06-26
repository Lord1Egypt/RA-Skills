## Description: <br>
Generates Chinese tech-news digests from configured news feeds and saves text, Markdown, and JSON summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ppop0uuiu](https://clawhub.ai/user/ppop0uuiu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators can use this skill to fetch configured technology-news feeds, translate or summarize items into Chinese, and produce digest artifacts for review or publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The server release identity is local-model-router, but the reviewed artifacts implement tech-news digest behavior. <br>
Mitigation: Install only when the tech-news digest behavior is intended, and confirm updated publisher documentation before relying on local model routing behavior. <br>
Risk: Configured feeds may be sent to a third-party translation service. <br>
Mitigation: Avoid adding private or internal RSS sources unless third-party translation is acceptable. <br>
Risk: Broad API tokens are documented without clearly implemented integrations in the reviewed artifacts. <br>
Mitigation: Provide only narrow credentials needed for the intended workflow and review publisher updates before enabling additional integrations. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ppop0uuiu/local-model-router) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Default RSS sources](artifact/config/defaults/sources.json) <br>
- [Default topics](artifact/config/defaults/topics.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Plain text, Markdown, and JSON files with optional shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces feed-derived summaries and saved workspace artifacts.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
