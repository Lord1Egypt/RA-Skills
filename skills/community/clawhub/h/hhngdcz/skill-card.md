## Description: <br>
Generates a complete .claude configuration system for a project through guided prompts, including CLAUDE.md, settings.json, rules, and optional ClawHub skill installation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hhngdcz](https://clawhub.ai/user/hhngdcz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill in Claude Code to bootstrap or complete a project's .claude setup. It scans project structure, helps configure sensitive-file deny rules, creates or merges Claude configuration files, and can install additional skills from local sources or ClawHub. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill performs an automatic project scan and may list local skill metadata from ~/.claude. <br>
Mitigation: Review the scan posture before use, skip local skill import when local metadata should not be listed, and rely on the skill's sensitive-file deny configuration for project secrets. <br>
Risk: Generated or merged .claude configuration can affect future agent permissions and project guidance. <br>
Mitigation: Review .claude/settings.json, generated rules, and the directory preview before relying on the configuration. <br>
Risk: Online skill installation depends on the npm-installed ClawHub CLI and remote skills selected by the user. <br>
Mitigation: Install ClawHub only from a trusted npm source, review search results before installation, and install only skills the user trusts. <br>


## Reference(s): <br>
- [README](README.md) <br>
- [ClawHub CLI Reference](reference/clawhub.md) <br>
- [ClawHub Skills Catalog](https://clawhub.ai/skills) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Markdown, JSON, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown summaries plus generated .claude files, JSON settings, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create missing .claude directories, generate documentation and rule files, deep-merge settings.json, copy selected local skills, and optionally run ClawHub CLI install commands after user confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact metadata version 5.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
