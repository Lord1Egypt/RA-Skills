## Description: <br>
Persistent per-project coding terminal (tmux). Run Codex CLI (codex exec) inside a stable session; mobile/SSH friendly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Justinzhq](https://clawhub.ai/user/Justinzhq) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to run coding, build, test, commit, and push workflows inside persistent tmux sessions so work can continue across SSH or mobile disconnects. It is also useful for OpenClaw workflows that need status, summaries, JSON output, or serial multi-project routing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically run Codex and shell workflows that modify code. <br>
Mitigation: Install it only for repositories where persistent local terminal automation is intended, and keep autoCodeRouting disabled unless automatic routing is deliberate. <br>
Risk: Automated workflows can commit or push changes to a branch. <br>
Mitigation: Use feature branches, review diffs plus branch and remote targets before commits or pushes, and do not force push unless explicitly requested. <br>
Risk: Terminal sessions can preserve or expose sensitive command output. <br>
Mitigation: Avoid printing secrets in the session, review summaries before sharing them, and kill tmux sessions when work is finished. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Justinzhq/persistent-code-terminal) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Changelog](artifact/CHANGELOG.md) <br>
- [Case study: patch to push](artifact/examples/case-study-patch-to-push.md) <br>
- [Manual quickstart example](artifact/examples/quickstart-manual.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Markdown, Guidance, Configuration] <br>
**Output Format:** [Terminal text, JSON status or summary output, and Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires tmux on macOS or Linux; Codex CLI integration is optional but used for codex-exec workflows.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and CHANGELOG.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
