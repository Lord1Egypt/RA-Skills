## Description: <br>
Automate complex web workflows with fast, deterministic browser control using accessibility tree snapshots and session isolation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[projectamazonph](https://clawhub.ai/user/projectamazonph) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to automate complex web workflows through the agent-browser CLI, including navigation, ref-based interactions, snapshots, session isolation, state persistence, screenshots, PDFs, and network controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundle includes unrelated self-improvement hook files that can inject reminders during agent bootstrap. <br>
Mitigation: Review or remove the hook files before installation, and enable them only when the self-improvement behavior is intentionally desired. <br>
Risk: Global hook activation can make the reminder behavior apply across projects. <br>
Mitigation: Prefer project-local scoped hook configuration and avoid global activation unless that cross-project behavior is explicitly wanted. <br>
Risk: Saved browser authentication state can contain sensitive cookies or local storage. <br>
Mitigation: Keep saved state files private, exclude them from source control, and rotate or delete them when no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/projectamazonph/projectamazonph-agent-browser) <br>
- [Agent Browser Skill Guide](artifact/SKILL.md) <br>
- [Vercel Labs agent-browser](https://github.com/vercel-labs/agent-browser) <br>
- [OpenClaw Integration](artifact/references/openclaw-integration.md) <br>
- [Hooks Setup Guide](artifact/references/hooks-setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with command examples and JSON browser snapshot output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes ref-based element identifiers, session-scoped browser state guidance, and optional browser artifact commands for screenshots and PDFs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
