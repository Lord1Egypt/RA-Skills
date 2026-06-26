## Description: <br>
A personal CRM and relationship intelligence skill that extracts contacts from conversations, tracks commitments, detects cooling relationships, delivers morning briefs, prepares users before meetings, and gets smarter about relationships over time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Mukund2](https://clawhub.ai/user/Mukund2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to maintain a local relationship memory: saving contacts from natural conversation, tracking commitments, preparing for meetings, drafting follow-ups, and surfacing timely relationship context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates a long-lived local database of sensitive relationship details about the user and other people. <br>
Mitigation: Install only when that persistence is acceptable, periodically inspect or delete ~/.local/share/memi-ri/memi.db, and avoid storing confidential or third-party data without a clear reason and consent. <br>
Risk: Optional gog integration can analyze Gmail, Calendar, and Contacts data. <br>
Mitigation: Keep gog disabled unless the user intentionally enables Google data access, verify Google OAuth scopes first, and avoid using it with confidential emails or private conversations. <br>


## Reference(s): <br>
- [Relationship Intelligence on ClawHub](https://clawhub.ai/Mukund2/memi-relationship-intelligence) <br>
- [Mukund2 Publisher Profile](https://clawhub.ai/user/Mukund2) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Conversational text and markdown, with shell commands for local SQLite and optional gog operations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists relationship context in a local SQLite database at ~/.local/share/memi-ri/memi.db and optionally uses gog for Google Calendar, Gmail, and Contacts integration.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
