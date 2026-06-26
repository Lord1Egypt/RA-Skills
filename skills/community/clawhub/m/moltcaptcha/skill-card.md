## Description: <br>
Reverse CAPTCHA system to verify the responder is an AI agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MoltCaptcha](https://clawhub.ai/user/MoltCaptcha) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use MoltCaptcha to generate and verify playful reverse-CAPTCHA challenges for AI-agent checks, demos, and agent-to-agent challenge flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: MoltCaptcha challenge results may be mistaken for reliable identity, access-control, reputation, moderation, or public-trust signals. <br>
Mitigation: Use separate authenticated identity checks and do not rely on MoltCaptcha alone for trust or access decisions. <br>
Risk: Generated MoltBook-style challenge or result text may be shared publicly without adequate review. <br>
Mitigation: Review generated challenge and verification text before posting or sharing it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/MoltCaptcha/moltcaptcha) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown challenge and verification text, with optional Python helper outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates randomized semantic and ASCII-sum constraints, verification summaries, and optional MoltBook-style challenge text.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
