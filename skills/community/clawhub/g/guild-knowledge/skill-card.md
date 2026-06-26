## Description: <br>
Guild Knowledge helps OpenClaw agents consult local Guild experience documents, search for current information, compare older guidance with newer options, and propose document updates for user approval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pipiy416](https://clawhub.ai/user/pipiy416) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to make agents consult project experience documents before tasks, check newer technical information, compare recommendations, and propose updates to Guild knowledge files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger phrases may activate the skill during ordinary tasks and cause the agent to consult local Guild documents or search the web. <br>
Mitigation: Review and narrow broad triggers if accidental activation would be disruptive. <br>
Risk: Guild and .learnings files may contain sensitive information that the agent could consult while preparing guidance. <br>
Mitigation: Keep Guild and .learnings files free of secrets and confidential data. <br>
Risk: Proposed document or index updates could preserve outdated or incorrect advice. <br>
Mitigation: Review proposed updates before approval and keep the skill's compare-against-current-information workflow enabled. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pipiy416/guild-knowledge) <br>
- [Publisher profile](https://clawhub.ai/user/pipiy416) <br>
- [Project homepage](https://github.com/Pipiy416/guild-knowledge) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown guidance, comparison notes, review reports, and update proposals] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guild document and index changes are proposed for user approval before application.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
