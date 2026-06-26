## Description: <br>
Build, test, and automate APIs with Postman collections, environments, and Newman CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and API engineers use this skill to design Postman collections, manage environment variables, add request assertions, and run automated API checks with Newman. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist API project names, authentication patterns, and environment conventions in local memory. <br>
Mitigation: Allow memory persistence only when those workflow details are acceptable to retain locally or in agent memory. <br>
Risk: API collections, environments, or test fixtures may expose private service details or credentials if real data is used. <br>
Mitigation: Use fake sample data, keep secrets in environment variables, and avoid committing environment files or fixtures that contain credentials. <br>
Risk: TLS-bypass options such as Newman insecure flags can weaken testing safeguards if used outside controlled debugging. <br>
Mitigation: Use TLS-bypass flags only in controlled debugging contexts and remove them from normal or CI test runs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/postman) <br>
- [Skill Homepage](https://clawic.com/skills/postman) <br>
- [Postman Collection v2.1.0 Schema](https://schema.getpostman.com/json/collection/v2.1.0/collection.json) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with JSON, JavaScript, YAML, and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local Postman collection and environment files under ~/postman/ when used by an agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
