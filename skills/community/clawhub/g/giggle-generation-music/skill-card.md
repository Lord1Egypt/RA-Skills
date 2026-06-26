## Description: <br>
Creates AI-generated music from text descriptions, custom lyrics, or instrumental background-music requests using Giggle.pro. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[patches429](https://clawhub.ai/user/patches429) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to submit music-generation requests to Giggle.pro from descriptions, lyrics, or instrumental prompts, then query for generated audio links when the asynchronous task completes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, lyrics, song titles, and style notes are sent to Giggle.pro. <br>
Mitigation: Avoid submitting confidential material or copyrighted material unless you have permission to use it with the service. <br>
Risk: The skill uses GIGGLE_API_KEY and can return signed audio URLs. <br>
Mitigation: Keep the API key in the system environment, do not expose it in command parameters, and keep generated signed audio links private. <br>
Risk: One localized artifact file names a different repository/source than the current server-resolved release evidence. <br>
Mitigation: Verify the publisher profile and source before installation, and do not treat artifact GitHub links as server-resolved provenance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/patches429/giggle-generation-music) <br>
- [Publisher profile](https://clawhub.ai/user/patches429) <br>
- [Giggle.pro](https://giggle.pro/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with shell commands and JSON task-status snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GIGGLE_API_KEY and returns task identifiers or signed audio links from Giggle.pro.] <br>

## Skill Version(s): <br>
0.0.10 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
