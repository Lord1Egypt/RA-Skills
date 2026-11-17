## Description:

Validate and lint Maven pom.xml files for structure, dependencies, plugins, and best practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and build engineers use this skill to validate Maven pom.xml files, audit dependency and plugin declarations, and identify structural or best-practice issues before release or CI use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read whichever pom.xml path the agent asks it to validate and may echo dependency, plugin, and path details in its report.

Mitigation: Run it only on intended local Maven POM files and review generated reports before sharing them outside the project.

Risk: The security evidence describes this as a local Maven POM linter, not a full build security audit.

Mitigation: Use the results as Maven configuration linting and pair them with normal build, dependency, and security review processes.

## Reference(s):

- [Maven POM 4.0.0 namespace](http://maven.apache.org/POM/4.0.0)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Text, JSON, or Markdown validation report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exit code indicates pass or failure; --strict treats warnings as failure.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact STATUS.md lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
