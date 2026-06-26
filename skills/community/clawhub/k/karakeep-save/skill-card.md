## Description: <br>
Save bookmarks to Karakeep (self-hosted bookmark manager). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nickian](https://clawhub.ai/user/nickian) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to save URLs and optional notes to a configured self-hosted Karakeep bookmark manager. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A misconfigured or untrusted KARAKEEP_URL can send bookmark URLs and notes to an unintended server. <br>
Mitigation: Configure only a trusted Karakeep instance, prefer HTTPS, and verify the URL before saving bookmarks. <br>
Risk: KARAKEEP_API_KEY is a credential for the configured Karakeep instance. <br>
Mitigation: Use a revocable API key, store it as an environment variable, and rotate or revoke it if exposed. <br>
Risk: Saved bookmark URLs and notes are stored on the configured Karakeep server. <br>
Mitigation: Avoid saving confidential URLs or notes unless they are intended to be stored on that server. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, text] <br>
**Output Format:** [Markdown with inline bash commands and plain-text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires KARAKEEP_URL, KARAKEEP_API_KEY, curl, and jq in the execution environment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
