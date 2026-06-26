## Description: <br>
Personal place intelligence that helps an agent save, update, and search local markdown records for places worth revisiting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ilyabelikin](https://clawhub.ai/user/ilyabelikin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals using agent-supported workflows use Nooks to save cafes, coworking spaces, restaurants, libraries, and other places as private local notes, then search those notes by city, vibe, features, or purpose when deciding where to work, eat, meet, or return. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Nooks stores durable local records of places a user visits or may revisit, which can reveal sensitive locations or routines if shared, committed, or exposed. <br>
Mitigation: Keep the mind/nooks folder private, avoid saving sensitive locations, and review files before sharing or committing them. <br>
Risk: Optional Google Places, image lookup, Haah dispatch, and heartbeat or cron reminders can add data sharing or recurring prompts beyond local note keeping. <br>
Mitigation: Restrict any Google Places API key, enable optional enrichment or dispatch features only intentionally, and keep reminders opt-in. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ilyabelikin/nooks) <br>
- [Google Places API Text Search endpoint](https://places.googleapis.com/v1/places:searchText) <br>
- [Google Cloud Console](https://console.cloud.google.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown place files, concise text responses, shell command examples, YAML configuration, and optional HTTP request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores one markdown file per place under mind/nooks; optional Google Places lookup uses a locally configured API key.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
