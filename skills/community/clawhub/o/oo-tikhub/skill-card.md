## Description: <br>
TikHub connector skill that lets agents inspect schemas and run TikHub actions through the OOMOL oo CLI for TikTok, Douyin, Xiaohongshu, and TikHub account queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve public TikTok, Douyin, and Xiaohongshu data and to check TikHub account, usage, endpoint, and pricing information through a connected OOMOL TikHub account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Some actions may expose TikHub account or API-key-related information. <br>
Mitigation: Run account and usage actions only when needed, and review returned data before sharing or storing it. <br>
Risk: Actions marked write may change TikHub state, and the exact side effect may depend on the live connector contract. <br>
Mitigation: Fetch the live action schema, confirm the exact payload and expected effect with the user, and avoid write actions without explicit approval. <br>


## Reference(s): <br>
- [TikHub homepage](https://tikhub.io/) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub TikHub skill page](https://clawhub.ai/oomol/skills/oo-tikhub) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the OOMOL oo CLI; action schemas should be fetched before constructing JSON payloads.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
