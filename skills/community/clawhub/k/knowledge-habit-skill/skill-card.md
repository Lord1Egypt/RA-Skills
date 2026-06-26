## Description: <br>
Knowledge Habit Skill helps knowledge workers run a local, privacy-first habit and event tracker for focused work, timed sessions, node-candidate generation, and JSON backups across web, desktop, and Android overlay modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[puppetcat-fire](https://clawhub.ai/user/puppetcat-fire) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Knowledge workers and developers use this skill to install, launch, and operate a local habit tracker that records focused work events, timer sessions, and exportable JSON backups. It is suited to privacy-conscious personal productivity workflows where habit data should remain under local user control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installation may fetch and run unpinned external code that was not included in the reviewed artifact. <br>
Mitigation: Review or trust the upstream repository and npm dependencies before installing, and prefer a pinned release or bundled source. <br>
Risk: Habit history, work events, exported JSON backups, Electron data, browser storage, and local logs may contain sensitive work-history data. <br>
Mitigation: Treat local storage, exported backups, and logs as private data and restrict access before sharing or deploying the skill. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/puppetcat-fire/knowledge-habit-skill) <br>
- [Publisher profile](https://clawhub.ai/user/puppetcat-fire) <br>
- [Dragon Palace Knowledge Hub](https://github.com/puppetcat-fire/dragon-palace-knowledge-hub) <br>
- [OpenClaw skill issues](https://github.com/puppetcat-fire/openclaw-skills/issues) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands and local JSON backup files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node, npm, and bash; runtime data is described as local browser, Electron, backup, and log data.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release evidence, SKILL.md frontmatter, and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
