## Description:

Create viral short-form videos using AI by analyzing trending patterns, generating original branded content, rendering videos, and downloading MP4s.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andyluvis](https://clawhub.ai/user/andyluvis)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and developers use this skill to operate the OpenFun CLI for trend discovery, branded short-form video script generation, rendering, account review, and MP4 download workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on an unpinned global npm CLI installation.

Mitigation: Verify the npm package source before installation and prefer an isolated environment.

Risk: OpenFun uses a persistent login token stored in ~/.openfun/config.json.

Mitigation: Protect the local config file and avoid using shared machines for authenticated workflows.

Risk: Rendering or batching videos may consume account credits.

Mitigation: Have the agent confirm before rendering or batching account-using actions.

Risk: Video prompts and brand details are sent to an external service.

Mitigation: Install only if external processing of this content is acceptable for the intended use case.

## Reference(s):

- [OpenFun skill page](https://clawhub.ai/andyluvis/skills/openfun)
- [OpenFun website](https://www.openfun.ai)
- [OpenFun CLI repository](https://github.com/andyluvis/openfun-cli)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Files]

**Output Format:** [Markdown guidance with inline shell commands and JSON-producing CLI workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The OpenFun CLI outputs JSON by default, writes downloaded videos as MP4 files, and stores a login token in ~/.openfun/config.json.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
