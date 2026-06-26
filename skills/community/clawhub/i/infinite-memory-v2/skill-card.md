## Description: <br>
High-precision memory with 100% recall accuracy for long contexts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mhndayesh](https://clawhub.ai/user/mhndayesh) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to add local long-term memory to OpenClaw, ingest text into persistent storage, and recall stored facts through a local memory sidecar. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes persistent local memory through a network sidecar without authentication in the provided artifact. <br>
Mitigation: Review before deployment, bind the sidecar to 127.0.0.1 or add authentication, and run it only on trusted machines. <br>
Risk: Stored memory can include sensitive, personal, regulated, or credential-like content and may be automatically recalled. <br>
Mitigation: Avoid storing passwords, API keys, personal data, or regulated content, and review retrieved content before relying on it. <br>
Risk: The auto-integration reference tells an agent to treat recalled facts as absolute ground truth. <br>
Mitigation: Do not use the absolute-ground-truth prompt as written; require source review and user confirmation for important recalled facts. <br>
Risk: Runtime behavior depends on unpinned Python dependencies and local model services. <br>
Mitigation: Pin and review dependencies, verify local LM Studio configuration, and test in an isolated environment before normal use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mhndayesh/infinite-memory-v2) <br>
- [INSTALL.md](INSTALL.md) <br>
- [AUTO_INTEGRATION.md](references/AUTO_INTEGRATION.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with command invocations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local Python sidecar service and local LM Studio endpoints to be running.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
