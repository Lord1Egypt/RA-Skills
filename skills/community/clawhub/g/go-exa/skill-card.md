## Description:

Use the unofficial go-exa client for web search, page contents, cited answers, agent runs and Websets in Go. Applies when adding Exa integration or working with an existing github.com/psyb0t/go-exa import.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Go developers use this skill to integrate the unofficial go-exa client with Exa for web search, page contents, cited answers, agent runs, and Websets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security analysis was partial because two local path-like references in SKILL.md could not be resolved.

Mitigation: Review the unresolved references and inspect the skill before installation.

Risk: The skill's API key and the queries, URLs, or prompts sent to Exa could expose credentials or private information if handled carelessly.

Mitigation: Read EXA_API_KEY from the environment, do not hardcode, commit, or log it, and avoid sending secrets or private data to the API.

Risk: Exa API calls can incur account charges, and agent runs may take longer and cost more.

Mitigation: Make calls only when requested and review endpoint cost information before starting agent runs.

## Reference(s):

- [Setup and API reference](references/setup.md)
- [Go package documentation](https://pkg.go.dev/github.com/psyb0t/go-exa)
- [Project homepage listed in skill metadata](https://github.com/psyb0t/go-exa)
- [Exa dashboard](https://dashboard.exa.ai)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with Go code examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Integration guidance for Go code that calls the Exa API.]

## Skill Version(s):

0.2.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
