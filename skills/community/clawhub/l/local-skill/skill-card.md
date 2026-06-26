## Description: <br>
Local-skill supports local skill repository inspection and release preparation with check, dry-run publish, and summary utilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[li-chi](https://clawhub.ai/user/li-chi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release maintainers use this skill to inspect a local skill package and run pre-publish checks and dry-run publish workflows before release. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may mistake this third-party local helper for an official OpenClaw package. <br>
Mitigation: Verify the publisher handle, package identity, and release intent before installing or running the release workflow. <br>
Risk: The release workflow can publish the package when run without the dry-run flag. <br>
Mitigation: Run the check script and dry-run publish command first, then review package metadata and release notes before publishing. <br>
Risk: Server evidence marks the skill as low quality and quarantined for moderation review. <br>
Mitigation: Complete moderation review and confirm the package is intended for release before listing or distributing it. <br>


## Reference(s): <br>
- [Release Process](docs/release.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/li-chi/local-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No external service calls or credential inputs are indicated by the evidence.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata, frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
