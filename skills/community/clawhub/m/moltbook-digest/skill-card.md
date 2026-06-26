## Description: <br>
Collect Moltbook posts and comments, build an evidence pack, and interpret it through either the calling agent or LiteLLM. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mtics](https://clawhub.ai/user/mtics) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and analysts use this skill to collect Moltbook posts and comments for topic research, feed digests, or monitoring, then turn the evidence pack into a structured report through the calling agent or a configured LiteLLM provider. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: LiteLLM or another configured provider may receive the query and collected evidence during interpreted runs. <br>
Mitigation: Use collection-only or agent mode to keep analysis local; when provider mode is required, use a user-specific config and protect API keys. <br>
Risk: Unpinned dependency ranges can reduce reproducibility across installs. <br>
Mitigation: Review or pin dependencies before deploying in workflows that require reproducible installs. <br>
Risk: Public Moltbook endpoint behavior, rate limits, or per-item availability can change. <br>
Mitigation: Check diagnostics and warnings, treat collection errors as data limits, and avoid claiming exhaustive coverage unless the collected sample supports it. <br>


## Reference(s): <br>
- [Moltbook API Notes](references/api.md) <br>
- [Moltbook](https://www.moltbook.com) <br>
- [MoltBook Digest on ClawHub](https://clawhub.ai/mtics/moltbook-digest) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports plus JSON evidence files and shell commands/configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces fixed local filenames including digest.md, evidence.json, analysis_input.md, agent_handoff.md, and analysis_report.md; LiteLLM mode may call a configured external provider.] <br>

## Skill Version(s): <br>
0.1.2 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
