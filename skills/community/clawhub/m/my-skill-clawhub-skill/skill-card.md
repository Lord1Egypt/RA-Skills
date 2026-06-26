## Description: <br>
Standardizes ClawHub skill publishing with required versions and changelogs, and supports searched installation with optional version selection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[canonxu](https://clawhub.ai/user/canonxu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to publish ClawHub skills with consistent version and changelog metadata, and to search for and install skills by slug with an optional explicit version. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper can publish or install skills through the local clawhub CLI when invoked. <br>
Mitigation: Install and run it only when the local clawhub CLI is trusted, and review the target path, slug, version, and changelog before publishing. <br>
Risk: Installing without a version requests the latest matching skill, which may change over time. <br>
Mitigation: Prefer an explicit version when reproducibility matters, and review search results before installation. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/canonxu/my-skill-clawhub-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a trusted local clawhub CLI; install supports an optional version argument.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
