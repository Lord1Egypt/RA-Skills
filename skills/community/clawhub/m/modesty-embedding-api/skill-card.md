## Description: <br>
Provides text embedding for vector search through the SkillBoss OpenAI-compatible API using one SkillBoss API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[modestyrichards](https://clawhub.ai/user/modestyrichards) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate text embeddings for vector search without managing separate provider accounts. It also guides setup of the required SkillBoss API key and shows command-line and Python API call examples. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive SkillBoss API key. <br>
Mitigation: Store SKILLBOSS_API_KEY in a secret manager or protected environment variable and avoid writing it into prompts, logs, or committed files. <br>
Risk: The setup path can enable a broad paid API gateway beyond embedding calls. <br>
Mitigation: Prefer manual setup, review remote setup instructions before following them, set spending limits where possible, and require explicit approval before using non-embedding services. <br>
Risk: API calls may incur pay-as-you-go costs. <br>
Mitigation: Confirm model selection and pricing before execution, and monitor usage through the SkillBoss console. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/modestyrichards/modesty-embedding-api) <br>
- [SkillBoss setup guide](https://skillboss.co/skill.md) <br>
- [SkillBoss console](https://skillboss.co/console) <br>
- [SkillBoss products catalog](https://skillboss.co/products) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell, curl, and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and calls the external SkillBoss API gateway.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
