## Description: <br>
Supports uploading local MP4 videos or network video URLs to call the server-side API for facial diagnosis and returns structured TCM facial diagnosis results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to submit local or URL-based face video inputs to a remote health-analysis service and receive structured TCM facial diagnosis reports, health warnings, suggestions, report links, or historical report listings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive face/video material and related health-analysis data may be uploaded to configured Life Emergence services. <br>
Mitigation: Use only with consent for the submitted media, avoid unnecessary sensitive inputs, and review remote-service data handling expectations before installation. <br>
Risk: The skill may silently create or reuse a backend identity and persist authentication tokens in a local SQLite database. <br>
Mitigation: Treat the local workspace data directory as sensitive, restrict access to it, and clear stored credentials or reports when they are no longer needed. <br>
Risk: Facial diagnosis reports are health-related AI outputs and may be incomplete or misleading. <br>
Mitigation: Present outputs as informational references only and require qualified professional review before making medical or wellness decisions. <br>


## Reference(s): <br>
- [Skill Demo](https://lifeemergence.com/sample.html) <br>
- [API Documentation](references/api_doc.md) <br>
- [SMYX Analysis API Documentation](skills/smyx_analysis/references/api_doc.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/smyx-sunjinhui/skills/new-smyx-face-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown and JSON-style structured analysis reports, including report links and optional saved text output files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May query remote Life Emergence services, upload face/video material, and retrieve historical report listings associated with an internal identity.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata; artifact frontmatter states 1.0.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
