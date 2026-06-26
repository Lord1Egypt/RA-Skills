## Description: <br>
Record and verify cryptographically signed, tamper-proof judgment, delegation, termination, and verification events for AI agent decision audits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[schchit](https://clawhub.ai/user/schchit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to create or verify signed audit events for decisions, delegations, terminations, and verification chains. It is intended for accountability trails where private signing keys are supplied from a secure environment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [Protocol Documentation](https://github.com/hjs-spec) <br>
- [HJS Foundation](https://humanjudgment.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce signed JEP receipt JSON when the agent runs user-approved code with user-provided keys; use a pinned jep-protocol package and provide signing keys only from secure secret storage.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
