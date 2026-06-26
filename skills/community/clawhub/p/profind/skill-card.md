## Description: <br>
ProFind helps agents automate macOS file search through AppleScript, URL scheme calls, shell wrappers, script hooks, and the optional local Media Server API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[steve-shi-web](https://clawhub.ai/user/steve-shi-web) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and macOS automation users use this skill to search local files by name, content, metadata, size, date, kind, path, or label, and to open ProFind workflows from an agent. It also supports optional batch operations through ProFind script hooks and local SOAP API queries when the user enables those workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad file-search access may expose local file names, paths, metadata, or search results. <br>
Mitigation: Install only when the user trusts ProFind, grant only needed macOS permissions, and avoid sharing generated search output without review. <br>
Risk: Script hooks can rename files, move files to Trash, copy paths, or email paths when the user enables and runs those workflows. <br>
Mitigation: Review each script before placing it in ~/Library/Scripts/ProFind and test batch operations on non-critical files first. <br>
Risk: The optional Media Server API can expose ProFind search results over the local SOAP interface. <br>
Mitigation: Keep the Media Server disabled unless needed and query only trusted local endpoints. <br>


## Reference(s): <br>
- [ClawHub ProFind Skill Page](https://clawhub.ai/steve-shi-web/profind) <br>
- [ProFind App Store Listing](https://apps.apple.com/app/id1559203395) <br>
- [API Reference](docs/API-REFERENCE.md) <br>
- [URL Scheme Reference](docs/URL-SCHEME.md) <br>
- [Sample Scripts Reference](docs/SAMPLE-SCRIPTS.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline AppleScript, shell, URL scheme, and SOAP examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires macOS, ProFind, and user-granted file access permissions for local search workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
