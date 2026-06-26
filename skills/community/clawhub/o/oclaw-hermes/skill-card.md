## Description: <br>
Oclaw Hermes bridges OpenClaw, Hermes, and DeerFlow to provide memory-driven agent routing, multi-agent collaboration, deep research workflows, and expert distillation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ruiyongwang](https://clawhub.ai/user/ruiyongwang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to coordinate OpenClaw skills, Hermes-style memory, and DeerFlow-style multi-agent workflows for chat, research, coding, browser-assisted tasks, expert distillation, and memory synchronization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory capture and cross-platform synchronization can store conversation-derived data beyond a single session. <br>
Mitigation: Review what memory is captured, avoid entering secrets into sessions, and confirm how to delete stored memories before use. <br>
Risk: Bridge and Docker services may expose local services, tokens, or profile data if deployed broadly. <br>
Mitigation: Use least-privilege tokens, bind services to localhost or firewall them, and stop unused Docker services. <br>
Risk: Container images and service dependencies may change independently of the skill release. <br>
Mitigation: Pin and inspect container images before deployment. <br>


## Reference(s): <br>
- [Oclaw Hermes ClawHub listing](https://clawhub.ai/ruiyongwang/oclaw-hermes) <br>
- [OpenClaw platform](https://openclawmp.stepfun.com) <br>
- [Hermes Agent](https://github.com/NousResearch/hermes) <br>
- [DeerFlow](https://github.com/bytedance/deerflow) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with code blocks, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist and synchronize memory or task state across local services when enabled.] <br>

## Skill Version(s): <br>
3.0.0 (source: evidence release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
