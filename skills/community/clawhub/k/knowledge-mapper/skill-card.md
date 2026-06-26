## Description: <br>
Notes Knowledge Mapper ingests Markdown/TXT notes or topic folders, extracts entities, similar ideas, relationships, and map views, and outputs searchable JSON or graph summaries plus follow-up questions with local-first analysis unless the user chooses otherwise. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to convert local Markdown/TXT notes into searchable entity lists, relationship maps, JSON summaries, text summaries, and GraphViz DOT exports for research, note-taking, and knowledge management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documents added to the knowledge base are retained locally in the OpenClaw data directory. <br>
Mitigation: Avoid adding highly sensitive notes on shared systems unless local file permissions and retention behavior have been reviewed. <br>
Risk: The documented workflow can write GraphViz DOT or generated image files to user-selected paths. <br>
Mitigation: Review output paths before running export or rendering commands, especially when redirecting output to existing files. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/harrylabsj/knowledge-mapper) <br>
- [Publisher Profile](https://clawhub.ai/user/harrylabsj) <br>
- [Artifact Documentation](artifact/SKILL_EN.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; the described tool can produce text, JSON, and GraphViz DOT exports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local SQLite-backed storage in the OpenClaw data directory and can export map files when requested.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
