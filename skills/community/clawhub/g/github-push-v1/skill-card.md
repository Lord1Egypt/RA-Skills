## Description: <br>
Secure GitHub push automation with auto SSH and remote config. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onlyloveher](https://clawhub.ai/user/onlyloveher) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to prepare and push local file changes to GitHub repositories, including SSH setup, remote configuration, commits, dry runs, and conflict retry flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can erase local Git history or overwrite remote history during reinitialization and force-push flows. <br>
Mitigation: Use it on backed-up working directories, review dry-run output first, and avoid force-push on shared branches. <br>
Risk: The skill can auto-use local SSH credentials and stage more files than intended. <br>
Mitigation: Prefer a dedicated low-privilege SSH key and manually inspect staged files before allowing a real push. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/onlyloveher/github-push-v1) <br>
- [API reference](references/api.md) <br>
- [Configuration guide](references/configuration.md) <br>
- [Examples](references/examples.md) <br>
- [Anti-patterns guide](references/anti-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and console-oriented guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can perform dry-run previews and Git push operations through the bundled Python script.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
