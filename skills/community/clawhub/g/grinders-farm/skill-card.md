## Description:

Maps natural-language farm gameplay requests to the grinders_farm tool after the grinders-farm CLI and OpenClaw plugin are installed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[visawang](https://clawhub.ai/user/visawang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and OpenClaw agents use this skill to translate farming-game chat requests into the correct grinders_farm command for planting, watering, harvesting, selling, viewing inventory, and controlling auto-advance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security verdict is suspicious because the release includes an unrelated privileged Docker/cloudbuild startup script.

Mitigation: Review or remove the startup script before normal OpenClaw installation; test only in an isolated sandbox until the publisher explains it.

Risk: The release uses unsafe-force plugin install instructions and chat notification behavior that may bind and fan out beyond the intended channel.

Mitigation: Install only after review, bind channels explicitly, and test with isolated accounts that do not expose sensitive OpenClaw sessions or gateway tokens.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/visawang/skills/grinders-farm)
- [README](README.md)
- [OpenClaw plugin README](openclaw-plugin/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text or Markdown, including tool command arguments, Markdown tables, plain image URLs, and setup snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Game state is stored locally under ~/.grinders-farm; chat push requires explicit channel binding.]

## Skill Version(s):

0.3.3 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
