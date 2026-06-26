## Description: <br>
Provides OpenAI-compatible access to Claude models through SkillBoss using one API key and pay-as-you-go pricing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[godferylindsay](https://clawhub.ai/user/godferylindsay) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to configure agents, curl calls, or OpenAI SDK clients for Claude model access through the SkillBoss third-party gateway without managing separate provider accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review marks the release suspicious because it presents as a Claude API helper while steering agents toward a broad paid SkillBoss gateway and remote setup instructions. <br>
Mitigation: Use it only when the user intends to trust SkillBoss as the API gateway, and inspect the remote setup page before following it. <br>
Risk: The skill requires a sensitive SkillBoss API key and can incur pay-as-you-go API charges. <br>
Mitigation: Store SKILLBOSS_API_KEY only in an approved secret or environment mechanism, monitor billing, and require explicit user approval before making paid calls. <br>
Risk: The gateway advertises access beyond Claude models, including scraping, social, email, and other non-chat services. <br>
Mitigation: Restrict usage to the requested Claude models unless the user explicitly approves routing prompts or requests to other models or service categories. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/godferylindsay/godfery-claude-api) <br>
- [SkillBoss setup guide](https://skillboss.co/skill.md) <br>
- [SkillBoss console](https://skillboss.co/console) <br>
- [SkillBoss chat completions endpoint](https://api.skillboss.co/v1/chat/completions) <br>
- [SkillBoss products](https://skillboss.co/products) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown setup guidance with shell commands, curl examples, Python SDK code, endpoint details, and model-selection guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and routes API calls through SkillBoss endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
