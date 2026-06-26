## Description: <br>
GDPR and AVG (Belgian data protection law) compliance handler for agency operators, data controllers, and organizations managing data subject requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nexaiguy](https://clawhub.ai/user/nexaiguy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agency operators, data controllers, and compliance staff use this skill to register and manage GDPR/AVG data subject requests, scan local OpenClaw-related data stores for personal data, produce exports and response letters, and maintain audit records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can broadly scan sensitive local data paths for personal data. <br>
Mitigation: Configure scan paths narrowly, run scans manually, and review all findings before using exported results. <br>
Risk: The skill can delete matched user-owned files when processing erasure requests. <br>
Mitigation: Verify the data subject identity first, keep backups, and review findings before processing erasure requests. <br>
Risk: Security evidence warns not to rely on its encryption, immutable audit, or retention-cleanup claims without independent controls. <br>
Mitigation: Apply independent access controls, encryption, backup, and audit-retention processes around generated exports and logs. <br>


## Reference(s): <br>
- [Nex AI homepage](https://nex-ai.be) <br>
- [ClawHub skill page](https://clawhub.ai/nexaiguy/nex-gdpr) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with CLI commands, JSON reports, ZIP exports, response-letter text, and local audit records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may contain personal data discovered in local files or databases and should be reviewed before processing or sharing.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
