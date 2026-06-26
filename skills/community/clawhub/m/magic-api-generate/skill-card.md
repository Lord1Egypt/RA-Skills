## Description: <br>
Provides guidance and examples for using magic-api, a Java low-code framework that maps Web UI scripts to HTTP APIs without conventional Controller, Service, DAO, or Mapper layers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[webx32](https://clawhub.ai/user/webx32) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to integrate magic-api with Spring Boot, configure the Web UI, and draft database-backed REST API scripts. It is also useful for learning magic-script syntax, CRUD patterns, transactions, file handling, and endpoint examples before adapting them for a secured application. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes copyable examples for persistent database-backed APIs, including CRUD and destructive operations. <br>
Mitigation: Treat examples as learning material and add explicit authorization checks before endpoints perform CRUD, upload, export, or cleanup actions. <br>
Risk: Authentication examples may be unsafe if copied directly into production. <br>
Mitigation: Use modern password hashing, avoid returning sensitive user fields, and sanitize user objects in responses. <br>
Risk: The magic-api Web UI can allow script authors to create or change live HTTP endpoints. <br>
Mitigation: Restrict Web UI access, limit script authoring to trusted administrators, and manage scripts under version control before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/webx32/magic-api-generate) <br>
- [SKILL.md](SKILL.md) <br>
- [magic-script syntax reference](references/syntax.md) <br>
- [Database operations reference](references/database.md) <br>
- [Business examples reference](references/examples.md) <br>
- [Official magic-api documentation](https://www.ssssssss.org/magic-api/) <br>
- [magic-api GitHub repository](https://github.com/ssssssss-team/magic-api) <br>
- [magic-api Gitee repository](https://gitee.com/ssssssss-team/magic-api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with XML, YAML, SQL, and magic-script/JavaScript code snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Maven dependency snippets, application.yml configuration, HTTP endpoint patterns, database scripts, and security cautions for adapting examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
