## Description: <br>
Queue coding plans during the day, approve them, execute later in isolated worktrees, and inspect reports. Background agentic execution requires an explicitly configured non-interactive runner. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vardhineediganesh877-ui](https://clawhub.ai/user/vardhineediganesh877-ui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use Night Shift to queue reviewed coding work, run approved multi-phase tasks later in isolated git worktrees, and inspect reports or diffs before merging, retrying, or continuing work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review flags broad unattended execution and repository mutation authority. <br>
Mitigation: Install first in a disposable or low-risk git workspace, prefer dry-run, and inspect reports and diffs before merging. <br>
Risk: Queued phases may run shell commands, verification commands, or optional coding runners with credentials available in the host environment. <br>
Mitigation: Review every generated plan and phase before approval, keep production credentials out of the runner environment, and use explicit non-interactive runner configuration. <br>
Risk: The external-repo copying workflow can reuse source material the user may not own or be licensed to reuse. <br>
Mitigation: Avoid plan-steal workflows unless the user owns the source or has confirmed permission to reuse it. <br>


## Reference(s): <br>
- [Night Shift package page](https://clawhub.ai/vardhineediganesh877-ui/night-shift) <br>
- [Publisher profile](https://clawhub.ai/user/vardhineediganesh877-ui) <br>
- [Install and setup](INSTALL.md) <br>
- [Operational reference](REFERENCE.md) <br>
- [Security model](SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports, JSON queue and checkpoint files, shell command invocations, and code diffs in git worktrees] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes runtime state under data/night-shift and may call optional host-provided coding runners when configured.] <br>

## Skill Version(s): <br>
1.0.5 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
