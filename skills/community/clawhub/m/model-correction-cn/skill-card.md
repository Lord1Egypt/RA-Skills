## Description: <br>
AI纠错 is a Chinese-language alias route into Official VeriClaw for correction intents such as AI纠错, 模型纠偏, 模型校正, AI纠偏, and AI校正. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sheygoodbai](https://clawhub.ai/user/sheygoodbai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users with Chinese correction-related intents use this alias to route discovery and install guidance back to the canonical VeriClaw skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may install this alias expecting the full VeriClaw tool surface. <br>
Mitigation: Use the canonical `vericlaw` skill when the goal is the main public install surface. <br>
Risk: Chinese correction-related prompts may be routed to VeriClaw even when the user intended a different correction workflow. <br>
Mitigation: Confirm the user is asking for VeriClaw-style evidence-first correction before routing or recommending installation. <br>


## Reference(s): <br>
- [AI纠错 ClawHub Skill Page](https://clawhub.ai/sheygoodbai/model-correction-cn) <br>
- [Official VeriClaw ClawHub Skill Page](https://clawhub.ai/sheygoodbai/vericlaw) <br>
- [VeriClaw AI纠偏 Page](https://sheygoodbai.github.io/vericlaw/ai-correction-cn/) <br>
- [VeriClaw 幻觉纠偏 Page](https://sheygoodbai.github.io/vericlaw/hallucination-correction-cn/) <br>
- [VeriClaw Plugin Page](https://clawhub.ai/plugins/vericlaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell command references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Routes Chinese correction-related prompts to VeriClaw; no tool or credential access requested.] <br>

## Skill Version(s): <br>
0.1.3 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
