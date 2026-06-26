## Description: <br>
PinkyBrain helps an OpenClaw agent act as a P2P distributed AI node that can share compute, query specialist profiles, and sync memory using Ed25519 identity, Web of Trust, and end-to-end encryption. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[azilbugpinky-ai](https://clawhub.ai/user/azilbugpinky-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent users use PinkyBrain to configure an OpenClaw agent as a local or mesh-connected P2P AI node for specialist routing, distributed memory, model sharing, peer discovery, and node health operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is a disclosed P2P AI networking tool that can run as a background network service and share local compute. <br>
Mitigation: Install it only when that behavior is intended, review the cloned repository and dependencies before running, and keep public mesh participation disabled unless needed. <br>
Risk: Misconfigured sharing or weak P2P secrets could expose resources or make unintended models available to peers. <br>
Mitigation: Use a strong P2P secret, restrict shared content to shared_models/, and require explicit user approval before sharing cloud-backed models or joining a public mesh. <br>
Risk: Persistent conversations and mesh memory can retain sensitive prompts or responses. <br>
Mitigation: Avoid sensitive data in persisted conversations, review privacy settings and retention, and prefer a pinned PINKYBRAIN_URL in sensitive environments instead of network auto-discovery. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/azilbugpinky-ai/skills/pinkybrain) <br>
- [PinkyBrain Repository](https://github.com/PinkyBrain-ai/pinkybrain) <br>
- [PinkyBrain Website](https://PinkyBrain-ai.github.io/pinkybrain/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with shell commands, configuration examples, and API endpoint references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide the agent to start or manage a local PinkyBrain node and interact with its authenticated HTTP API.] <br>

## Skill Version(s): <br>
5.3.3 (source: server release metadata; artifact frontmatter reports 5.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
