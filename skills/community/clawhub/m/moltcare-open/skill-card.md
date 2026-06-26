## Description: <br>
Install and configure the MoltCare Agent Framework, a four-layer OpenClaw configuration system for structured personality, memory handling, proactive problem-solving, multi-expert decision modes, and token optimization workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[useens](https://clawhub.ai/user/useens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install workspace-level templates that shape agent behavior, memory, user preferences, task execution, and periodic token optimization checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persistently changes OpenClaw behavior and memory handling by installing workspace-level instruction and memory templates. <br>
Mitigation: Install only when this behavior is intended, inspect the templates first, and back up ~/.openclaw/workspace before installation. <br>
Risk: The installer may add a weekly cron entry that writes an audit trigger in the background. <br>
Mitigation: Review the cron entry during installation and remove or decline it unless weekly token optimization trigger writes are wanted. <br>
Risk: The README documents a remote curl-to-bash installation path that is not pinned to an immutable artifact. <br>
Mitigation: Inspect the script before running it and prefer a trusted, versioned, or local copy of the artifact. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/useens/moltcare-open) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [CONFIG_CHECKLIST.md](artifact/assets/CONFIG_CHECKLIST.md) <br>
- [TOKEN_AUDIT.md](artifact/assets/TOKEN_AUDIT.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown instructions with shell commands and installed Markdown configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Copies OpenClaw workspace templates and may configure a weekly cron trigger for token optimization audits.] <br>

## Skill Version(s): <br>
3.2.0 (source: server release metadata and SKILL.md heading) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
