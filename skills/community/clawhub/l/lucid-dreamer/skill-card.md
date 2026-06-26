## Description: <br>
Lucid Dreamer schedules an agent to review recent memory notes, detect stale facts, unresolved tasks, recurring issues, and optional cleanup candidates, then produce review reports or memory updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[robbyczgw-cla](https://clawhub.ai/user/robbyczgw-cla) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users with markdown-based long-term memory use Lucid Dreamer to run scheduled memory hygiene, generate review reports, and optionally apply high-confidence memory updates. It is most appropriate when the workspace owner is comfortable with a scheduled agent reading personal or project memory notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A scheduled agent can read personal or workspace memory notes. <br>
Mitigation: Run it only in workspaces intended for memory maintenance, and avoid markdown workspaces containing plaintext secrets or credentials. <br>
Risk: Optional auto-apply, session debrief, and cleanup behavior can directly change long-term memory and create local commits. <br>
Mitigation: Review the nightly and debrief prompts before enabling cron, keep auto-apply and aggressive cleanup disabled unless accepted, and remove direct-write or auto-commit steps if review-only operation is required. <br>
Risk: Incorrect high-confidence updates could pollute long-term memory. <br>
Mitigation: Review generated reports and source citations before accepting suggestions, and use local git history to revert unwanted changes. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/robbyczgw-cla/lucid-dreamer) <br>
- [README](README.md) <br>
- [Architecture](ARCHITECTURE.md) <br>
- [Lucid configuration](config/lucid.config.json) <br>
- [Auto-apply configuration](config/auto-apply.md) <br>
- [Nightly review prompt](prompts/nightly-review.md) <br>
- [Session debrief prompt](prompts/session-debrief.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON state, configuration snippets, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local memory files and local git commits when optional auto-apply or debrief behavior is enabled.] <br>

## Skill Version(s): <br>
0.7.8 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
