## Description:

Install and configure BEE, the Belief Extraction Engine for OpenClaw, to give agents persistent structured memory across sessions through belief extraction, namespace scoping, deduplication, and recalled context injection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vashkartik](https://clawhub.ai/user/vashkartik)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw operators use this skill to install, configure, and verify persistent structured memory for agents. It is suited for agent memory setup, belief persistence configuration, namespace-scoped multi-agent memory, and troubleshooting BEE behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent belief extraction may store sensitive conversation-derived information in a SQLite database.

Mitigation: Disable extraction for sensitive conversations and periodically inspect or delete the SQLite belief database.

Risk: Global npm or GitHub installation introduces package supply-chain exposure.

Mitigation: Pin a reviewed package version and review the npm or GitHub package before installation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/vashkartik/skills/openclaw-bee)
- [GitHub Project](https://github.com/skysphere-labs/openclaw-bee)
- [npm Package](https://www.npmjs.com/package/@skysphere-labs/openclaw-bee)
- [Skysphere AI Labs](https://skysphere.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and JSON configuration blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes installation commands, OpenClaw extension configuration, verification steps, and multi-agent setup guidance.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
