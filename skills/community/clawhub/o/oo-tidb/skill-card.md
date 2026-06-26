## Description: <br>
Operate TiDB Cloud through an OOMOL-connected account using the oo CLI connector for TiDB Cloud read, create, and update workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to inspect TiDB Cloud resources and run supported TiDB Cloud connector actions through an OOMOL-connected account. It covers API keys, clusters, branches, imports, exports, regions, node specs, audit logs, providers, and quotas. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The connected account can expose TiDB Cloud resources and metadata, including API keys, clusters, audit logs, and related organization information. <br>
Mitigation: Install only when the user trusts OOMOL with the TiDB Cloud connection and understands what the connected account can read. <br>
Risk: Write or destructive connector actions can change or remove TiDB Cloud state if run with an incorrect payload or target. <br>
Mitigation: Confirm the exact payload and expected effect with the user before running actions tagged as write or destructive. <br>
Risk: First-time setup may require running an external oo CLI installer. <br>
Mitigation: Review the oo CLI installer before first-time setup and run setup steps only when an auth, connection, or missing-command error requires them. <br>


## Reference(s): <br>
- [TiDB Cloud ClawHub skill page](https://clawhub.ai/oomol/oo-tidb) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [TiDB Cloud homepage](https://www.pingcap.com/tidb/cloud/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands can return JSON responses from the oo CLI when run with --json.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
