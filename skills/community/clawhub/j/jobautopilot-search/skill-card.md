## Description: <br>
Reads a user-selected resume pool to build a candidate profile, searches job sites and company career pages for matching roles, filters results by role, location, salary, and recency, and writes outcomes to a structured tracker. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jerronl](https://clawhub.ai/user/jerronl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Job seekers and career automation users use this skill to search job boards and company career pages against a resume-derived profile, screen roles against configured constraints, and maintain tracker and handoff notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads a configured resume folder and writes search history, job URLs, notes, and rejected roles to local tracker and handoff files. <br>
Mitigation: Point RESUME_DIR only at resumes or job-search documents intended for agent access, and choose tracker and handoff paths where retaining that information is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jerronl/jobautopilot-search) <br>
- [Project homepage](https://github.com/jerronl/jobautopilot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown tracker rows, handoff notes, search queries, and concise screening notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires browser search access and configured local environment variables; reads resumes only from the configured RESUME_DIR.] <br>

## Skill Version(s): <br>
1.3.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
