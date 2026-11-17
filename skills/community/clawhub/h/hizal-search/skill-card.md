## Description:

Hizal Search prompts an agent to query Hizal context stores for prior decisions, conventions, memory, and related knowledge before beginning new work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parkerscobey](https://clawhub.ai/user/parkerscobey)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to retrieve prior decisions, conventions, memory, and related context before starting implementation or investigation work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can trigger broadly and retrieve prior agent memory or organization-level context that may include sensitive or cross-project information.

Mitigation: Install it only where AGENT, PROJECT, and ORG searches are access-controlled, and scope searches to the relevant project or organization when possible.

Risk: The skill recommends promoting broadly useful AGENT memory into persistent knowledge or conventions.

Mitigation: Treat any write-back through the related Hizal write workflow as a separately approved action and review the content before persistence.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, API Calls, Text]

**Output Format:** [Markdown guidance with inline tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only context retrieval is the primary behavior; any knowledge write-back is delegated to a separate skill and should be separately reviewed.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
