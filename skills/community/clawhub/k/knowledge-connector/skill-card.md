## Description: <br>
Knowledge Connector helps agents import local notes and documents, build relationship maps, answer cross-document questions, and suggest concrete next actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users, developers, and knowledge workers use this skill to turn a local note or document collection into source-aware import results, relationship maps, cross-document answers, and follow-up actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated HTML graph output loads third-party code while displaying note-derived data. <br>
Mitigation: Use JSON or DOT output when offline or when third-party loading is not acceptable; open generated HTML only after accepting the unpkg.com dependency. <br>
Risk: Imported paths and excerpts are retained locally, which can expose sensitive note or document metadata on shared systems. <br>
Mitigation: Use a dedicated KC_DATA_DIR for each project and avoid importing private, client, medical, legal, or enterprise notes unless the user explicitly accepts the storage behavior. <br>


## Reference(s): <br>
- [Knowledge Connector on ClawHub](https://clawhub.ai/harrylabsj/knowledge-connector) <br>
- [Publisher profile](https://clawhub.ai/user/harrylabsj) <br>
- [Release notes](artifact/RELEASE.md) <br>
- [Changelog](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; CLI commands may produce terminal text, JSON, DOT, or HTML files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local JSON stores under KC_DATA_DIR or the default user data directory; generated HTML graph files may load third-party JavaScript from unpkg.com.] <br>

## Skill Version(s): <br>
1.4.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
