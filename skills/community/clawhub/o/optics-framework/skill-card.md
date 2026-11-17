## Description:

Drive Android, iOS, smart TV and browser sessions with the Optics (optics-framework) MCP server, and write or fix Optics CSV/YAML test suites (test_cases, modules, elements, error_definitions). Use when automating or testing a real app UI with Optics, or when an Optics keyword name, parameter or default is uncertain.

This skill is ready for commercial/non-commercial use.

## Publisher:

[optics-framework](https://clawhub.ai/user/optics-framework)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and test engineers use Optics to automate real Android, iOS, smart TV, and browser interfaces, and to create or repair Optics CSV/YAML test suites.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optics sessions can interact with real application or browser interfaces and target URLs.

Mitigation: Review target URLs, app/device capabilities, and intended actions before starting a session; inspect the interface before acting and verify the result after each action.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/optics-framework/skills/optics-framework)
- [Optics project homepage](https://optics-framework.org)
- [Optics documentation index for agents](https://optics-framework.org/docs/llms.txt)
- [Optics keyword reference](https://optics-framework.org/docs/reference/keywords/index.md)
- [Optics MCP server reference](https://optics-framework.org/docs/reference/mcp.md)
- [Writing Optics suites](https://optics-framework.org/docs/create/write.md)
- [Optics YAML rules](https://optics-framework.org/docs/create/yaml.md)
- [Optics configuration reference](https://optics-framework.org/docs/reference/config.md)
- [Optics CLI reference](https://optics-framework.org/docs/reference/cli.md)
- [Optics error codes](https://optics-framework.org/docs/reference/errors.md)

## Skill Output:

**Output Type(s):** [CSV, YAML, Shell commands, Guidance]

**Output Format:** [Optics CSV/YAML test-suite files, shell commands, and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide automation sessions that interact with real app, device, or browser interfaces.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
