## Description: <br>
通过 AISA 调用 Perplexity Sonar 模型生成带引用的深度研究答案。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bibaofeng](https://clawhub.ai/user/bibaofeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and research users use this skill to generate citation-backed Chinese research answers through AISA-hosted Perplexity Sonar models when synthesis, comparison, or long-form cited responses are more useful than raw search links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The included client can perform broader remote search and URL extraction than the Perplexity Sonar description suggests. <br>
Mitigation: Review the client behavior before installation and prefer a narrower Sonar-only skill if that is the intended capability. <br>
Risk: Research prompts, URLs, and retrieved result data are sent to AISA endpoints. <br>
Mitigation: Avoid private or internal URLs and sensitive content, and use the skill only when sending this data to AISA is acceptable. <br>
Risk: The skill requires the sensitive AISA_API_KEY credential. <br>
Mitigation: Provide the key only in the intended runtime environment and rotate or revoke it if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bibaofeng/perplexity-research-zh) <br>
- [AISA API endpoint](https://api.aisa.one/apis/v1) <br>
- [AISA](https://aisa.one) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown and terminal output with citations or inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY and sends prompts, URLs, and retrieved result data to AISA endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
