## Description: <br>
Extracts and versions AI agent identity snapshots from memory files, scoring continuity and tracking changes to detect cognitive drift or fractures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[quriustus](https://clawhub.ai/user/quriustus) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to synthesize OpenClaw workspace memory files into versioned identity snapshots, compare continuity between snapshots, and flag drift before or after model upgrades. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends local identity and memory file contents to Google Gemini using a local Google API token. <br>
Mitigation: Use it only on workspaces approved for external Gemini processing, and add explicit consent, file preview or selection, and redaction before processing sensitive files. <br>
Risk: Workspace identity and memory files may contain secrets, credentials, private personal data, or confidential agent memory. <br>
Mitigation: Do not run the skill on confidential workspaces unless the input files have been reviewed and sanitized, or an offline score-only path is used. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/quriustus/identity-persistence) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Files, Shell commands] <br>
**Output Format:** [JSON files and terminal text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces identity snapshots, continuity scores, and diffs under the OpenClaw workspace identity directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
