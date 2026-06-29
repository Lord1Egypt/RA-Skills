## Description: <br>
Keji Skill Showcase is a curated research-skills entry point that guides agents toward literature search, citation checking, and academic knowledge-base skills based on the user's research task. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[j-levee](https://clawhub.ai/user/j-levee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and research-focused agents use this skill to select an appropriate specialized skill for finding papers, checking citation authenticity, downloading PDFs, conducting literature research, or building an academic knowledge base. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill recommends downstream research skills that may have their own permissions, account access, file access, or external-service behavior. <br>
Mitigation: Review each suggested downstream skill separately before installation or use. <br>
Risk: Broad research triggers could route a user to a skill that is not the best fit for a specific task. <br>
Mitigation: Confirm the user's need against the skill's categories before recommending a downstream installation command. <br>


## Reference(s): <br>
- [Keji Skill Showcase on ClawHub](https://clawhub.ai/j-levee/skills/keji-skill-showcase) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown guidance with inline installation commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Routes users to downstream research skills; no code execution or credential handling is included in the artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
