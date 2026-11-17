## Description: <br>
Provides read-only Pipedrive CRM lookup guidance for agents to query deals, contacts, organizations, activities, pipelines, stages, notes, and current user information through a third-party API proxy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales teams and agent developers use this skill to retrieve Pipedrive sales information in conversational or command-line workflows. It is intended for CRM lookup and search tasks, not deterministic critical decisions or write operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends potentially sensitive CRM data through api.maton.ai/MATON as a third-party proxy. <br>
Mitigation: Install only after reviewing the proxy provider's privacy, logging, retention, and data-processing terms. <br>
Risk: The skill requests local execution permissions and uses shell-invoked Python examples to make network API calls. <br>
Mitigation: Review commands before execution, keep MATON_API_KEY in environment or secret storage, and avoid writing credentials into code or logs. <br>
Risk: Free-edition behavior is described as read-only, but some generic artifact wording mentions create, export, save, or import actions. <br>
Mitigation: Treat this release as read-only and avoid broad list, pagination, export, or mutation-style requests unless the user has explicitly approved the data access. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/thcjp/skills/pipedrive-toolkit-free) <br>
- [SkillHub homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with Python command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MATON_API_KEY, a Pipedrive account, and a Pipedrive OAuth connection through the API proxy.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
