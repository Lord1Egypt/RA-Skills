## Description: <br>
Analyzes GitHub repository releases and summarizes latest or recent release notes for manual use or cron-driven tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stoner-byte](https://clawhub.ai/user/stoner-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to check GitHub release changes, summarize selected formal releases, and optionally track unprocessed releases in cron workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: In cron mode, a crafted custom state key can redirect the state file outside the intended state folder. <br>
Mitigation: For cron use, avoid custom state keys containing slashes, backslashes, '..', or absolute paths until state-key validation constrains writes to the OpenClaw state directory. <br>
Risk: The skill fetches and summarizes public GitHub release content, so low-quality or misleading release notes can affect the final summary. <br>
Mitigation: Review the generated release summary against the linked release notes before using it for operational decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/stoner-byte/github-release-analyzer) <br>
- [Execution Modes](references/execution-modes.md) <br>
- [Summary Contract](references/summary-contract.md) <br>
- [State Format](references/state-format.md) <br>
- [Output Templates](references/templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown summaries and deterministic command-driven workflow output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Manual mode returns the latest formal release summary; cron mode emits NO_REPLY when no new formal release is available.] <br>

## Skill Version(s): <br>
0.0.4 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
