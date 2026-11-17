## Description:

Mingjing provides offline, zero-dependency health monitoring for LLM agents with framework adapters, real-time diagnostics, health grading, and a local web dashboard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wulun811](https://clawhub.ai/user/wulun811)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to install and operate a local AI-agent health center that monitors agent activity, diagnoses runtime issues, grades health states, and displays live telemetry in a web panel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install and run unpinned external components that observe agent activity and run as background services.

Mitigation: Review package and plugin provenance before installing, prefer exact pinned versions or verified artifacts, and run the daemon and web panel under a least-privileged account.

Risk: Collected agent telemetry may include sensitive local operational data and may be exposed through local storage or the web panel.

Mitigation: Treat telemetry as sensitive data and confirm storage, retention, web-panel exposure, and uninstall or disable steps before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wulun811/skills/mngjing)
- [Mingjing GitHub repository](https://github.com/wulun811/Ming_qiankun)
- [Mingjing issue tracker](https://github.com/wulun811/Ming_qiankun/issues)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell command examples and configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides local installation, daemon startup, web-panel access, diagnostic coverage, and health-grading workflows.]

## Skill Version(s):

0.11.14 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
