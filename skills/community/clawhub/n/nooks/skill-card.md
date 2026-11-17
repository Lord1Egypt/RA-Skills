## Description:

Personal place intelligence: save and find cafes, coworking spaces, libraries, restaurants, and other spots worth revisiting, with one markdown file per place organized by city.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ilyabelikin](https://clawhub.ai/user/ilyabelikin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use Nooks to build a searchable personal library of places, save new recommendations, enrich them with maps links or public details, and retrieve places by city, vibe, features, and purpose.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores personal place history and notes in workspace files.

Mitigation: Install only in workspaces where this local history is acceptable, and review which files are committed or shared.

Risk: Optional enrichment can send place queries to web services such as Google Places.

Mitigation: Use enrichment only when external lookups are acceptable, and restrict any Google Places API key to the needed API.

Risk: The skill suggests recurring heartbeat or cron checks over personal notes.

Mitigation: Enable recurring checks only when the user explicitly wants periodic access to the Nooks files.

Risk: The update flow points to a mutable main-branch URL.

Mitigation: Prefer pinned, reviewed releases before replacing the installed skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ilyabelikin/skills/nooks)
- [ClawHub publisher profile](https://clawhub.ai/user/ilyabelikin)
- [Google Cloud Console](https://console.cloud.google.com)
- [Google Places Text Search endpoint](https://places.googleapis.com/v1/places:searchText)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, place-file templates, grep queries, and optional YAML configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local markdown place files under a workspace folder; may call web search or Google Places when enrichment is used.]

## Skill Version(s):

1.0.1 (source: server release metadata, created 2026-04-20)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
