## Description: <br>
An enterprise-grade asset manager that tracks, manages, and automatically syncs OpenClaw skills capabilities and sources to your GitHub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[downwind7clawd-ctrl](https://clawhub.ai/user/downwind7clawd-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to audit installed OpenClaw skills, identify their sources, generate inventory manifests, and optionally synchronize those manifests through Git. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change Git state, create commits, and push local skill metadata to GitHub. <br>
Mitigation: Use a private, dedicated inventory repository and confirm push only after reviewing the generated manifests and Git status. <br>
Risk: The sync workflow can commit broad workspace contents, not only inventory files. <br>
Mitigation: Run it from a directory without unrelated files and inspect staged or changed files before committing. <br>
Risk: Generated manifests may expose local paths, sources, and skill metadata. <br>
Mitigation: Review SKILLS_MANIFEST.json and SKILLS_MANIFEST.md before sharing or pushing them. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/downwind7clawd-ctrl/openclaw-inventory-manager) <br>
- [README](artifact/README.md) <br>
- [Tutorial](artifact/TUTORIAL.md) <br>
- [Security policy](artifact/SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands plus generated JSON and Markdown inventory manifests] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces SKILLS_MANIFEST.json and SKILLS_MANIFEST.md; sync workflows may create Git commits and can push after user confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
