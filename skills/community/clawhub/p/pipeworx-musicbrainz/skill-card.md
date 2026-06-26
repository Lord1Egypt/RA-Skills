## Description: <br>
MusicBrainz MCP wraps MusicBrainz Web Service v2 for free artist and release lookup without API authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[b-gutman](https://clawhub.ai/user/b-gutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent users use this skill to connect an MCP client to Pipeworx MusicBrainz tools for artist and release lookup. It supports search and retrieval workflows for MusicBrainz data without requiring an API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an npm-based MCP helper to connect to a remote Pipeworx gateway. <br>
Mitigation: Install only if you trust Pipeworx, review the MCP configuration before use, and apply the same package execution controls used for other npm-based helpers. <br>
Risk: MusicBrainz artist and release searches may send user query text to remote services. <br>
Mitigation: Avoid putting private or sensitive information into MusicBrainz search queries. <br>


## Reference(s): <br>
- [Pipeworx MusicBrainz Pack](https://pipeworx.io/packs/musicbrainz) <br>
- [Pipeworx](https://pipeworx.io) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Configuration] <br>
**Output Format:** [MCP tool responses and JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses an npm-based MCP helper to connect to a remote Pipeworx MusicBrainz gateway; no API key is required.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
