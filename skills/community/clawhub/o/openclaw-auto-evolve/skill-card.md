## Description: <br>
OpenClaw 自动进化系统帮助 agents perform lightweight local health checks, summarize learned rules, and record learning notes for an OpenClaw workspace. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejianjun000](https://clawhub.ai/user/xiejianjun000) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to inspect workspace health, review locally stored learned rules, and capture learning notes in a controlled OpenClaw workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores learning notes and reads workspace status from local files. <br>
Mitigation: Set OPENCLAW_WORKSPACE to a dedicated directory you control and periodically review or delete files under .learnings and state. <br>
Risk: The self-evolution wording may overstate the governance value of the helper. <br>
Mitigation: Treat its outputs as lightweight local note-taking and status checks, not as a complete autonomous governance system. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiejianjun000/openclaw-auto-evolve) <br>
- [Publisher profile](https://clawhub.ai/user/xiejianjun000) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [JSON responses and Markdown learning files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read workspace state files and append local learning notes under the configured OpenClaw workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and OpenClaw metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
