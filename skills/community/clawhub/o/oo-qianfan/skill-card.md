## Description: <br>
Operates Baidu Qianfan through OOMOL's qianfan connector for reading, creating, updating, and deleting Qianfan resources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent call Baidu Qianfan chat, completion, embedding, reranking, file, batch, OCR, image generation, and video generation workflows through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to an OOMOL-connected Baidu Qianfan account. <br>
Mitigation: Install it only for agents that should use that account, and keep account connection and billing state under the user's control. <br>
Risk: Write actions can create jobs, upload files, generate content, or otherwise change Qianfan resources. <br>
Mitigation: Inspect the live action schema and confirm the exact payload and expected effect with the user before running write actions. <br>
Risk: Destructive actions can delete stored Qianfan responses. <br>
Mitigation: Require explicit user approval for the target resource before running destructive actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-qianfan) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [Baidu Qianfan homepage](https://qianfan.cloud.baidu.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schema inspection before constructing action payloads.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
