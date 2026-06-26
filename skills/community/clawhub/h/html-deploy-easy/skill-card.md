## Description: <br>
Instantly publish a single self-contained HTML page to htmlcode.fun for fast live URLs. Alias of html-deploy, updated for the current versioned htmlcode.fun API and safer agent workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[520xiaomumu](https://clawhub.ai/user/520xiaomumu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to publish, inspect, update, and manage single-file HTML pages on htmlcode.fun when fast sharing is more important than full project hosting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Publishing selected HTML can expose secrets or private information embedded in the page. <br>
Mitigation: Review HTML content for secrets and sensitive data before upload. <br>
Risk: Overwriting, unpublishing, switching the current version, fetching existing content, or deleting a version can affect public content. <br>
Mitigation: Require explicit user intent for these operations and inspect version history before modifying a release. <br>
Risk: Liked versions are preserved snapshots and should not be overwritten or deleted. <br>
Mitigation: Check likeCount before edits or deletion; append a new version when the target version has likes. <br>
Risk: htmlcode.fun is a fast single-file publication channel, not full production hosting. <br>
Mitigation: Use a dedicated app or static-site host when the project needs multi-file assets, build steps, backend services, secrets, or custom domains. <br>


## Reference(s): <br>
- [htmlcode.fun guide](https://www.htmlcode.fun/s/htmlcode-fun-guide) <br>
- [html-deploy-easy ClawHub page](https://clawhub.ai/520xiaomumu/html-deploy-easy) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, Markdown, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write fetched HTML content to files when explicitly requested; deployment responses include URL and version metadata.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
