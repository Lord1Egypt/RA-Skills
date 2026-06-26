## Description: <br>
Installs and enables Honcho with the @alloralabs/honcho-memory-mux extension, migrates legacy file memory, and updates workspace instructions so agents use Honcho-first memory retrieval with local-file fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spooktheducks](https://clawhub.ai/user/spooktheducks) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to install an OpenClaw memory extension, connect it to Honcho, migrate existing markdown memory, and document Honcho-first retrieval with local fallback behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Conversations and selected memory files may be stored in Honcho, including the hosted Honcho API when configured as the default endpoint. <br>
Mitigation: Review HONCHO_BASE_URL and HONCHO_API_KEY before use, confirm migration previews before upload, and avoid sensitive deployments until retention, deletion, opt-out, and session scoping controls are clear. <br>
Risk: The release security summary reports that a session-history tool may not fully match its stated access scope. <br>
Mitigation: Inspect the session-history behavior during validation and limit use to workspaces where the memory access model is acceptable. <br>
Risk: The skill updates agent instruction files to change memory retrieval and write behavior. <br>
Mitigation: Review all generated edits before accepting them and keep local memory files unchanged unless an explicit deletion or migration policy is approved. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/spooktheducks/honcho-memory-mux) <br>
- [Honcho homepage](https://honcho.dev) <br>
- [Honcho documentation](https://docs.honcho.dev) <br>
- [Honcho repository](https://github.com/plastic-labs/honcho) <br>
- [honcho-memory-mux repository](https://github.com/allora-network/honcho-memory-mux) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and workspace documentation edits] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write workspace memory files and agent instruction documents during setup.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
