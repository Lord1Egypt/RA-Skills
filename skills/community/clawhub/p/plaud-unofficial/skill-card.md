## Description: <br>
Use when accessing Plaud voice recorder data, including recordings, transcripts, and AI summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leonardsellem](https://clawhub.ai/user/leonardsellem) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to configure Plaud credentials, list recordings, retrieve transcripts and AI summaries, and download audio from a Plaud account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to copy a long-lived Plaud browser session token into a local plaintext .env file. <br>
Mitigation: Treat the Plaud token as a password: keep .env private, avoid sharing logs or screenshots that include it, and rotate or revoke the session if exposed. <br>
Risk: The helper can access Plaud recordings, transcripts, summaries, tags, and bulk downloads for the authenticated account. <br>
Mitigation: Install and run it only when that local access is intended, and use bulk download commands only when copying all recordings onto the machine is acceptable. <br>


## Reference(s): <br>
- [PLAUD_API.md](artifact/PLAUD_API.md) <br>
- [Plaud Web App](https://web.plaud.ai) <br>
- [ClawHub Release Page](https://clawhub.ai/leonardsellem/plaud-unofficial) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands; the included CLI can emit JSON and downloaded MP3 files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local Plaud token and region-specific Plaud API domain supplied by the user.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
