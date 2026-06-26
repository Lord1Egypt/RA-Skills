## Description: <br>
Deploy an automated release management pipeline with three agents for changelog generation, version coordination, and release announcements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release engineers use this skill to configure a three-agent release management workflow that generates changelogs, manages version tags, and sends release announcements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Release data may be sent to Slack channels, email services, documentation endpoints, or webhooks that are not approved for confidential or embargoed release notes. <br>
Mitigation: Confirm approved announcement destinations before setup and avoid sending confidential or embargoed content through the announcer unless those destinations are approved. <br>
Risk: Peer-agent handshakes could exchange release workflow data with the wrong agent identity. <br>
Mitigation: Verify peer agent identities before exchanging handshakes and before subscribing to release-note or release-tag topics. <br>
Risk: Downstream pilot-* skills installed by this setup may add their own data handling or operational risks. <br>
Mitigation: Review the downstream skills before installation and confirm their expected Slack, email, documentation, and webhook integrations. <br>


## Reference(s): <br>
- [Pilot Protocol Homepage](https://pilotprotocol.network) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides the agent to ask for role and prefix choices, install role-specific skills, set hostnames, write setup manifests, and initiate peer handshakes.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
