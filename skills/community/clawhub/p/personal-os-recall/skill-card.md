## Description: <br>
Load context from past sessions through temporal recall, topic search, and graph visualization, ending each recall with a single highest-leverage next action. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[borodich](https://clawhub.ai/user/borodich) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to recover useful context from prior workspace sessions, memory files, session state, and notes. It helps answer temporal or topic-based recall questions, produce relationship graphs when requested, and synthesize one concrete next action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can surface sensitive information from local memory files, session state, and workspace notes. <br>
Mitigation: Install it only in workspaces where that context is appropriate to recall, use explicit recall requests, and avoid broad topic queries in projects containing secrets or private notes. <br>
Risk: Optional QMD indexing or graph output may expose more session context than intended. <br>
Mitigation: Review optional indexing and generated graph output before using them with sensitive material. <br>


## Reference(s): <br>
- [Recall skill page](https://clawhub.ai/borodich/personal-os-recall) <br>
- [Publisher profile](https://clawhub.ai/user/borodich) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional generated HTML graph file references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local memory files, session state, workspace notes, and optional recall graph output.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
