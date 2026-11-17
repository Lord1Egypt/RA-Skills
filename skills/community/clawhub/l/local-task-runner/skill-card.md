## Description:

Executes Node.js code snippets or scripts locally with timeout handling and cleanup for agent-side utility tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[d-wwei](https://clawhub.ai/user/d-wwei)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to run trusted local JavaScript snippets for calculations, utility scripting, or system checks without spawning a separate subagent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run local Node.js code with broad access to the host system.

Mitigation: Use only with trusted code and avoid code derived from untrusted webpages, prompts, files, or users unless it runs inside a real sandbox such as a disposable container with limited files, scrubbed environment variables, and restricted networking.

Risk: The release depends on an unpinned semver dependency range.

Mitigation: Pin dependencies before deployment and review dependency changes during updates.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/d-wwei/skills/local-task-runner)
- [ClawHub Publisher Profile](https://clawhub.ai/user/d-wwei)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Guidance]

**Output Format:** [Markdown and plain text with command examples and structured stdout/stderr task results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs trusted Node.js snippets locally with configurable timeout behavior.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
