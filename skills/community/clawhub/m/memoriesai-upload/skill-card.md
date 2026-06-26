## Description: <br>
Upload a video or image to memories.ai with capture time and location metadata when a user wants to add media to Luci memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[memories-ai-official](https://clawhub.ai/user/memories-ai-official) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to probe media metadata, collect any missing capture time or location details, and upload selected videos or images to memories.ai/Luci as visual memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Chosen photos or videos, capture timestamps, and location coordinates are sent to memories.ai during upload. <br>
Mitigation: Use --probe first, confirm the exact file and metadata, and upload only media the user has approved. <br>
Risk: Using --location can send a place name to a geocoding service before upload. <br>
Mitigation: Use --lat and --lon for sensitive places when a geocoding lookup is not desired. <br>
Risk: MEMORIES_AI_KEY is a sensitive credential required by the skill. <br>
Mitigation: Keep the key private, provide it through the environment or the skill-local .env file, and avoid exposing it in logs or shared transcripts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/memories-ai-official/memoriesai-upload) <br>
- [Publisher profile](https://clawhub.ai/user/memories-ai-official) <br>
- [memories.ai service endpoint](https://mavi-backend.memories.ai) <br>
- [Nominatim geocoding endpoint](https://nominatim.openstreetmap.org/search) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Text, JSON] <br>
**Output Format:** [Command-line output with a JSON upload response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MEMORIES_AI_KEY and ffprobe; --probe can inspect media metadata without uploading.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
