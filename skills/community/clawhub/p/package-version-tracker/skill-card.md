## Description: <br>
Package Version Tracker looks up npm and PyPI package version information, release history, package metadata, and basic version comparisons without requiring an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SxLiuYu](https://clawhub.ai/user/SxLiuYu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to check current npm and PyPI package versions, recent releases, package metadata, and simple version ordering while working on dependency updates or package audits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queried package names are sent to public npm and PyPI registries. <br>
Mitigation: Avoid querying sensitive private package names when registry disclosure is a concern. <br>
Risk: Broad trigger phrases such as "pip show" or "package version" may activate the skill unintentionally. <br>
Mitigation: Use explicit /version commands for deliberate package lookups. <br>
Risk: Registry metadata can change or be incomplete at lookup time. <br>
Mitigation: Review package details before making dependency or release decisions. <br>


## Reference(s): <br>
- [Package Version Tracker on ClawHub](https://clawhub.ai/SxLiuYu/package-version-tracker) <br>
- [npm Registry API](https://registry.npmjs.org/) <br>
- [PyPI JSON API](https://pypi.org/pypi/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown-formatted text with package metadata, latest version, and recent release entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public npm and PyPI registry lookups; skill documentation states a maximum of 10 packages per batch and up to 5 requests per second.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
