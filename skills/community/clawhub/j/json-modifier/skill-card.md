## Description: <br>
Safely apply structured JSON patches (RFC 6902) to files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wanng-ide](https://clawhub.ai/user/wanng-ide) <br>

### License/Terms of Use: <br>
ISC <br>


## Use Case: <br>
Developers and agents use this skill to make precise JSON edits to configuration files, package manifests, and memory JSONs using RFC 6902 patch operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can overwrite JSON files selected by the user. <br>
Mitigation: Confirm the target path and patch contents before execution, and use --out or a backup for important configuration, package, or memory files. <br>
Risk: Untrusted patch content may make unintended structured changes. <br>
Mitigation: Avoid applying patches from untrusted text and review the patch operations before running the tool. <br>


## Reference(s): <br>
- [JSON Patch reference](https://jsonpatch.com/) <br>
- [ClawHub release page](https://clawhub.ai/wanng-ide/json-modifier) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration] <br>
**Output Format:** [JSON patches and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can update files in place or write patched JSON to a separate output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
