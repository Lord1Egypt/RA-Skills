## Description: <br>
Generate Upwork/freelance bid materials from a job description, including English proposal draft, bid-worthiness score, pricing suggestion, milestone split, and follow-up messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeterWang](https://clawhub.ai/user/jeterWang) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Freelancers and proposal writers use this skill to turn job descriptions into bid-readiness scores, proposal drafts, pricing suggestions, milestone plans, and follow-up copy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: External billing code includes a hardcoded API key and unclear charge controls. <br>
Mitigation: Remove the hardcoded API key, use a platform-managed billing mechanism, and require explicit user confirmation before any charge. <br>
Risk: Users may not understand what data is sent to SkillPay during paid operations. <br>
Mitigation: Clearly disclose the data sent to SkillPay before enabling billing-backed features. <br>
Risk: Broken command or runtime logic may prevent intended billing and proposal workflows from executing reliably. <br>
Mitigation: Repair and test the command/runtime logic before installation or release. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jeterWang/proposal-copilot) <br>
- [Publisher Profile](https://clawhub.ai/user/jeterWang) <br>
- [SkillPay Billing Service](https://skillpay.me) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Copy-paste-ready text or JSON containing score, decision, reasons, proposal, pricing, milestones, and follow-up messages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Paid generation, pricing, and follow-up paths are described as using SkillPay billing at 0.001 USDT per call.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
