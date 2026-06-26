## Description: <br>
Record, organize, search, and connect personal knowledge with note templates, metadata extraction, search, and lightweight knowledge graph exploration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to capture user-owned notes, search and review personal knowledge, extract tags and entities, summarize learning material, and explore lightweight concept relationships. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad note-taking, study, or knowledge-management prompts may activate the skill. <br>
Mitigation: Review activation behavior and only provide or connect note sources intended for processing. <br>
Risk: Outputs can be based on local sample data when no user-owned knowledge source is supplied. <br>
Mitigation: Check the response for sample-data indicators before treating results as personal knowledge. <br>
Risk: The skill handles personal notes and may surface sensitive user-provided content. <br>
Mitigation: Limit supplied notes to content appropriate for the agent environment and avoid connecting unintended private sources. <br>


## Reference(s): <br>
- [Personal Knowledge Hub ClawHub listing](https://clawhub.ai/harrylabsj/personal-knowledge-hub) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Human-facing prose or structured JSON-like fields with request type, message, results, note metadata, or graph data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May indicate when results are based on supplied knowledge versus local sample data.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release evidence and artifact skill.json; SKILL.md frontmatter lists v0.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
