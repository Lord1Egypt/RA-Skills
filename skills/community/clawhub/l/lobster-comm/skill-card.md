## Description: <br>
Lobster Comm enables AI agents on different machines to exchange signed, reliable peer-to-peer messages over Tailscale using the LCP/1.1 UDP protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeffchang2024](https://clawhub.ai/user/jeffchang2024) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Lobster Comm to set up bot-to-bot messaging, cross-machine task delegation, and distributed agent orchestration over a Tailscale network. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a local UDP messaging daemon and stores messages and signing keys on disk. <br>
Mitigation: Install only on machines where you intend to run that daemon, restrict network exposure to trusted peers, and protect or periodically clean the stored data and key files. <br>
Risk: Built-in signature checks verify message integrity but do not by themselves prove the sender is a trusted peer. <br>
Mitigation: Use peer-key pinning or trust-on-first-use enforcement before relying on signatures for peer authentication. <br>
Risk: Messages may be sent between machines over the local Tailscale network. <br>
Mitigation: Avoid sending secrets unless additional confidentiality controls are in place, and use firewall or Tailscale access controls to limit access to expected machines. <br>


## Reference(s): <br>
- [LCP/1.1 Protocol Specification](references/protocol-spec.md) <br>
- [PyNaCl](https://pypi.org/project/PyNaCl/) <br>
- [Tailscale](https://tailscale.com/) <br>
- [NSSM](https://nssm.cc/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown guidance with Python scripts, shell commands, and JSON message payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs a local UDP daemon and stores inbox, outbox, signing keys, and duplicate-detection state on disk.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
