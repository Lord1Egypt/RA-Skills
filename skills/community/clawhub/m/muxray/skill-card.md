## Description: <br>
Inspect tmux panes as JSON: snapshot, diff, and classify Claude/Codex/Copilot agent state across the whole fleet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dandriscoll](https://clawhub.ai/user/dandriscoll) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use Muxray to supervise local tmux panes running terminal coding agents, check program state, wait for settled states, and summarize changes without pasting raw terminal dumps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tmux pane text may include secrets or sensitive terminal output. <br>
Mitigation: Inspect only panes relevant to the user request, prefer classification summaries, and redact obvious secrets before sharing pane excerpts. <br>
Risk: The skill depends on an external muxray binary installed via Go. <br>
Mitigation: Review or trust the upstream muxray project before installation and ensure both muxray and tmux are available in the host or sandbox where the agent runs. <br>
Risk: Raw snapshot and diff output can expose more terminal content than needed. <br>
Mitigation: Use read-only wrapper commands, prefer no-raw snapshots where practical, and summarize only the few relevant changed lines. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dandriscoll/muxray) <br>
- [Publisher Profile](https://clawhub.ai/user/dandriscoll) <br>
- [Muxray Homepage](https://github.com/dandriscoll/muxray) <br>
- [JSON Contract Reference](references/json-contract.md) <br>
- [Inspect Agent Example](examples/inspect-agent.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prefers classification summaries and redacted pane excerpts over raw pane dumps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
