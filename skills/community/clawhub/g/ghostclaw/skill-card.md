## Description: <br>
Architectural code review and refactoring assistant that perceives code vibes and system-level flow issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ev3lynx727](https://clawhub.ai/user/Ev3lynx727) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use Ghostclaw to review repository architecture, identify cohesion and coupling issues, generate Markdown architecture reports, and receive stack-aware refactoring guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release security summary flags self-updating and broad background automation that can modify local installs or GitHub state without strong safeguards. <br>
Mitigation: Review the skill before installing, avoid --update, keep hook and cron modes disabled unless background scans are intended, and use watcher mode with --dry-run first. <br>
Risk: Pull-request automation can change GitHub state when enabled. <br>
Mitigation: Do not enable --create-pr or provide GitHub tokens unless they are least-privilege and limited to intended repositories. <br>
Risk: Repository scanning reads project contents and may run repeatedly in watcher or hook modes. <br>
Mitigation: Use the skill only on repositories it is intended to read and keep background modes disabled by default. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Ev3lynx727/ghostclaw) <br>
- [Ghostclaw Reference - Stack Patterns](ghostclaw/references/stack-patterns.md) <br>
- [Ghostclaw Stack Patterns - Machine-Readable Rules](ghostclaw/references/stack-patterns.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, raw JSON analysis data, CLI output, and refactoring guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write architecture reports into the analyzed repository and may open GitHub pull requests when explicitly configured.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
