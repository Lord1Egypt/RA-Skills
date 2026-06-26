## Description: <br>
Helps an agent decide whether, when, and how much a user should learn by tying learning effort to a concrete problem, current confirmed knowledge, knowledge decay, ROI, and explore-versus-apply tradeoffs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[li-evan](https://clawhub.ai/user/li-evan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill when deciding whether to learn a topic, how deeply to study it, or how to allocate limited time across learning and project work. The skill guides the agent to ask for a concrete problem, confirm what the user already knows, and recommend learning, not learning, or learning only the minimal useful subset. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may push conversations toward time, ROI, and minimal-useful-learning decisions even when a user wants broader exploration. <br>
Mitigation: Use it when the user is making a learning investment decision, and switch to a broader planning or exploration skill when the user explicitly wants depth, discovery, or long-term curriculum design. <br>
Risk: It depends on confirmed user knowledge; assuming the user already knows something can lead to a poor learning recommendation. <br>
Mitigation: Ask the user to confirm prior knowledge before using it as evidence for a learn, do-not-learn, or minimal-subset conclusion. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/li-evan/learn-occam) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, markdown] <br>
**Output Format:** [Markdown or plain text advisory response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No executable code, persistence, credential access, or sensitive data access is added by the skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
