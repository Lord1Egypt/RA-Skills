## Description: <br>
Memphis helps OpenClaw agents keep local memory chains, retrieve knowledge, track decisions, use local LLMs, and coordinate with multi-agent workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elathoxu-crypto](https://clawhub.ai/user/elathoxu-crypto) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, teams, researchers, and agent builders use Memphis to add persistent local memory, semantic recall, decision tracking, encrypted secret storage, and multi-agent sharing workflows to OpenClaw agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill describes broad memory, secret storage, network sharing, background daemon, self-loop, auto-repair, backup restore, and learning features without enough documented boundaries or safety controls. <br>
Mitigation: Review the actual Memphis CLI source before use, keep daemon, self-loop, auto-repair, backup restore, learning, share-sync, and network features disabled until their scope is confirmed, and approve each state-changing action. <br>
Risk: Vault and ingestion workflows may involve secrets or sensitive local files. <br>
Mitigation: Avoid storing real credentials until vault handling is understood, and ingest only narrow non-sensitive folders. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/elathoxu-crypto/memphis) <br>
- [Memphis Repository](https://github.com/elathoxu-crypto/memphis) <br>
- [Memphis Documentation](https://github.com/elathoxu-crypto/memphis/tree/master/docs) <br>
- [Quickstart](QUICKSTART.md) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs guide agent setup and use of Memphis CLI workflows; no structured machine-readable output contract is specified.] <br>

## Skill Version(s): <br>
3.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
