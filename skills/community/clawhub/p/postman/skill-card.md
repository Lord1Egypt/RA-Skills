## Description:

Build, test, and automate APIs with Postman collections, environments, and Newman CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and API engineers use this skill to create Postman collections and environments, organize authentication and variables, and run automated API tests with Newman in local or CI workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist API project details and authentication patterns in local memory without making that persistence obvious.

Mitigation: Review what is saved under the local Postman memory path and avoid storing secrets or sensitive API details there unless the user has explicitly approved it.

Risk: The security review flags the documented Newman setup as unpinned npm execution.

Mitigation: Prefer pinned, project-local npm dependencies or reviewed lockfiles instead of global installs or unpinned npx commands.

Risk: API tokens can be exposed through command-line arguments or committed environment files.

Mitigation: Pass secrets through trusted environment variables or secret managers, and keep real credentials out of collection and environment files committed to source control.

## Reference(s):

- [Postman skill page](https://clawhub.ai/ivangdavila/skills/postman)
- [Postman collection v2.1 schema](https://schema.getpostman.com/json/collection/v2.1.0/collection.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON, JavaScript, YAML, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local Postman collection, environment, and memory files when the user asks for project setup or automation help.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
