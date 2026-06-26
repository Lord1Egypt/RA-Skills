## Description: <br>
OCC (Origin Controlled Computing) provides cryptographic proof of OpenClaw agent actions and helps users install, configure, and audit those proofs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mikeargento](https://clawhub.ai/user/mikeargento) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install the OCC audit-proof plugin, configure local or notary-backed proof modes, and interpret audit results for agent tool activity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Default remote notarization sends audit metadata to an external notary. <br>
Mitigation: Review the documented proof payload before enabling remote mode, and use stub mode or a self-hosted notary when audit metadata should remain local. <br>
Risk: Global npm installation executes third-party package code in the user's environment. <br>
Mitigation: Verify the npm package and publisher before running the global install command. <br>


## Reference(s): <br>
- [OCC for OpenClaw documentation](https://occprotocol.com/openclaw) <br>
- [openclaw-occ npm package](https://www.npmjs.com/package/openclaw-occ) <br>
- [ClawHub skill page](https://clawhub.ai/mikeargento/openclaw-occ) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may include local file paths, npm commands, notary URLs, and audit interpretation steps.] <br>

## Skill Version(s): <br>
1.1.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
