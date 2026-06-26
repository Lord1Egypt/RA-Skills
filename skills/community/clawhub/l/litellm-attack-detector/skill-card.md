## Description: <br>
Detect the LiteLLM supply chain attack (v1.82.7/1.82.8) by scanning for compromised packages, malicious .pth files, backdoor persistence, suspicious network connections, and Kubernetes IoCs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tjefferson](https://clawhub.ai/user/tjefferson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security teams, developers, and incident responders use this skill to run a bash-based detector for LiteLLM 1.82.7/1.82.8 compromise indicators across Python packages, persistence artifacts, network connections, Kubernetes pods, and dependency relationships. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The detector may make outbound DNS queries for known malicious domains when run, which can be inappropriate in sensitive incident-response or containment environments. <br>
Mitigation: Run it only where outbound DNS activity is acceptable, or review and disable the DNS-resolution block before execution. <br>


## Reference(s): <br>
- [LiteLLM issue 24512](https://github.com/BerriAI/litellm/issues/24512) <br>
- [Original LiteLLM detection script](https://gist.github.com/sorrycc/30a765b9a82d0d8958e756b251828a19#file-check-litellm-sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with a bash command and terminal-style diagnostic output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs without required arguments; exits 0 when no indicators are found and 1 when compromise indicators are detected.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
