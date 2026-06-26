## Description: <br>
PluginEval wraps plugineval-core to provide combined security and quality vetting, workflow support, and report generation for skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[donmeusi](https://clawhub.ai/user/donmeusi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use PluginEval to evaluate skills before installation or publication with combined security scans, quality scoring, anti-pattern checks, and report generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Runtime behavior depends on plugineval-core and referenced workspace scripts that are not bundled in the reviewed artifact. <br>
Mitigation: Install plugineval-core from a trusted source and verify any referenced workspace scripts before running vetting commands. <br>
Risk: Version references are inconsistent across the artifact files. <br>
Mitigation: Treat the server release and SKILL.md frontmatter version 2.0.0 as the release version, and review _meta.json and EXTERNAL.md if packaging or installation tooling uses those files. <br>


## Reference(s): <br>
- [External Dependencies](EXTERNAL.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/donmeusi/plugineval) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown or text report with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a combined security and quality report for a supplied skill name or path.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release and SKILL.md frontmatter; _meta.json lists 1.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
