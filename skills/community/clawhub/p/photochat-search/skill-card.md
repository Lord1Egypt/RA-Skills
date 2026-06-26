## Description: <br>
Search for photos in PhotoCHAT using natural language via the CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PhotoCHAT](https://clawhub.ai/user/PhotoCHAT) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to search a local PhotoCHAT photo library with natural language, parse JSON results, and present matching file paths or images when requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad local photo searches may expose private library contents, absolute file paths, or images. <br>
Mitigation: Keep searches scoped to the user's request, limit returned results by default, and display images only when the user asks. <br>
Risk: Ambiguous requests for pictures may refer to web image search instead of the local PhotoCHAT library. <br>
Mitigation: Clarify whether the user wants local PhotoCHAT search or web image search when intent is unclear. <br>
Risk: Ambiguous dates may be interpreted using DD/MM parsing. <br>
Mitigation: Use the documented day-first option and clarify date intent when DD/MM format may not be what the user meant. <br>


## Reference(s): <br>
- [Search Examples](references/search-examples.txt) <br>
- [ClawHub Skill Page](https://clawhub.ai/PhotoCHAT/photochat-search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown with PowerShell commands and parsed JSON result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include absolute local file paths, match counts, filters, and similarity scores from PhotoCHAT search results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
