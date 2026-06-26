## Description: <br>
Create a local Git bundle backup of the OpenClaw workspace repository. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Trumppo](https://clawhub.ai/user/Trumppo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to create a self-contained local Git bundle of the OpenClaw workspace repository and report the backup path and file size. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Git bundles can contain the full repository history and refs, including sensitive content already committed to the workspace. <br>
Mitigation: Treat each bundle like a full repository copy, store it securely, avoid casual sharing, and remove old backups when they are no longer needed. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files] <br>
**Output Format:** [Plain text status output with a generated Git bundle file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundle filename includes a UTC timestamp and older bundles are not deleted.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
