## Description: <br>
ML-powered DOM pruning for 95% smaller browser prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rcholic](https://clawhub.ai/user/rcholic) <br>

### License/Terms of Use: <br>
MIT OR Apache-2.0 <br>


## Use Case: <br>
Developers and agent users use this skill in OpenClaw browser sessions to capture compact, ranked DOM snapshots for LLM browser automation and to click, type, or scroll by Predicate element ID. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API-backed snapshots and demos can send page-derived content to external services. <br>
Mitigation: Use predicate-snapshot-local for sensitive pages and avoid API-backed snapshots or LLM demos on private or account pages unless external processing is acceptable. <br>
Risk: The skill can click, type, or scroll in the active browser page when invoked. <br>
Mitigation: Install and invoke it only in browser sessions where this level of page control is intended, and review snapshot IDs before using action commands. <br>
Risk: API keys may be exposed if stored in shared files or committed to version control. <br>
Mitigation: Prefer environment variables or local configuration and keep keys out of shared files and repositories. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/rcholic/predicate-snapshot) <br>
- [Predicate Snapshot Homepage](https://predicate.systems/skills/snapshot) <br>
- [Predicate Documentation](https://predicatesystems.ai/docs) <br>
- [OpenClaw + Predicate Snapshot Skill Installation Guide](docs/INSTALL_AND_TEST.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style text with pipe-delimited DOM element rows and plain action status messages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Snapshot output is capped by a configurable element limit and can run in API-backed or local-only mode.] <br>

## Skill Version(s): <br>
0.4.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
