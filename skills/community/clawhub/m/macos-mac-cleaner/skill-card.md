## Description: <br>
Mac Cleaner is an automated macOS disk cleanup agent that removes caches, old logs, Trash contents, npm and Homebrew cache, stale build artifacts, and optional Mission Control cleanup state without requiring API keys or external services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[josephtandle](https://clawhub.ai/user/josephtandle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Mac users and support engineers use this skill to install and operate a local cleanup agent that previews and removes common macOS disk clutter. It is intended for routine disk-space recovery, with user confirmation before installation, scheduling, and real cleanup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The documented dry-run preview may still perform real deletions. <br>
Mitigation: Review and correct dry-run behavior before installation or execution, and require a successful preview plus explicit user confirmation before any real cleanup. <br>
Risk: The Mission Control dashboard can trigger cleanup actions. <br>
Mitigation: Expose the dashboard only in a trusted local environment and restrict use to trusted operators. <br>
Risk: A weekly cron job can run cleanup unattended. <br>
Mitigation: Keep scheduling disabled unless the user explicitly wants unattended weekly cleanup, and confirm the schedule before enabling it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/josephtandle/macos-mac-cleaner) <br>
- [Publisher profile](https://clawhub.ai/user/josephtandle) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash, JavaScript, TypeScript, JSON, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local setup steps, cleanup scripts, Mission Control dashboard files, cron configuration guidance, dry-run review guidance, and cleanup result summaries.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
