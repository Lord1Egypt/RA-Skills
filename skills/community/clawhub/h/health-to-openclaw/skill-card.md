## Description: <br>
Sync Apple Health data from iPhone to OpenClaw with QR-code pairing, local storage, and query support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[reffwu](https://clawhub.ai/user/reffwu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to pair an iPhone health-sync app, ingest Apple Health records into local SQLite storage, and answer health-data questions from the stored records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow reads a live OpenClaw gateway token and places pairing details in QR or manual JSON form. <br>
Mitigation: Treat the QR code and manual JSON as secrets, share them only with the intended device, and rotate the gateway token if they are exposed. <br>
Risk: Gateway pairing can expose access over a LAN, VPS, or public address. <br>
Mitigation: Prefer local-only access or HTTPS/tunneled access, and restrict firewall rules to trusted networks when remote access is required. <br>
Risk: The skill stores Apple Health records locally in SQLite. <br>
Mitigation: Keep the local database on trusted devices, apply normal disk and account protections, and remove the database when health records no longer need to be retained. <br>
Risk: Automatic ingest and dependency installation can run with broad behavior after trigger phrases or setup. <br>
Mitigation: Review the setup and ingest scripts before use, and disable or supervise automatic pip installation and auto-ingest behavior where that is not acceptable. <br>
Risk: Pairing depends on an external iOS app or sideloaded IPA. <br>
Mitigation: Use only a trusted app source and avoid unknown sideloaded builds. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/reffwu/health-to-openclaw) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/reffwu) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with inline shell commands and concise Chinese responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local SQLite health data and emits setup, ingest, status, summary, and query responses.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
