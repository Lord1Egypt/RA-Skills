## Description: <br>
Blocks destructive Linux commands by enforcing allowlist execution, denylist checks, regex detection, protected paths, and approval for risky actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jurgenw81](https://clawhub.ai/user/jurgenw81) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill before Linux shell execution to check proposed commands against an allowlist-first safety policy and identify commands that should be blocked or manually approved. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The guard is an advisory local command-checking layer and is not a complete security boundary. <br>
Mitigation: Use it with sandboxing or microVM isolation, least privilege, restricted network access, and human approval for high-risk commands. <br>
Risk: Allowlist or rule configuration that is too broad can permit commands outside the intended safety posture. <br>
Mitigation: Keep the allowlist small and mostly read-only, and require separate approval or child policy for wrappers, interpreters, and system-changing tools. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jurgenw81/llm-shell-guard) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance and command-check results; CLI can also emit JSON decisions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces allow or block decisions with reasons, matched rules, and base command details.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
