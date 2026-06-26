## Description: <br>
Generates AI music, instrumental background tracks, lyrics, or task status responses from natural language through the Musicful API, returning preview and final audio links when available. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[boner-bbb](https://clawhub.ai/user/boner-bbb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn plain-language music requests into lyrics, instrumental tracks, vocal songs, or Musicful task status updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Music prompts, lyrics, task IDs, and generation metadata are sent to Musicful. <br>
Mitigation: Avoid confidential or regulated content unless Musicful is approved for that use. <br>
Risk: The skill requires a Musicful API key stored in environment configuration. <br>
Mitigation: Use a revocable API key and keep the .env file private. <br>
Risk: Python dependencies are declared with lower bounds rather than pinned versions. <br>
Mitigation: Pin dependency versions in managed or production environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/boner-bbb/musicful-music-generator) <br>
- [Musicful API key documentation](https://www.musicful.ai/api/authentication/interface-key/) <br>
- [Musicful API service endpoint](https://api.musicful.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, shell commands] <br>
**Output Format:** [Text or JSON-style command results containing lyrics, task status, preview links, and final audio links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MUSICFUL_API_KEY; sends prompts, lyrics, task IDs, and related generation metadata to Musicful.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
