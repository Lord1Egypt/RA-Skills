## Description:

Search Korean patents, utility models, trademarks, and designs through KIPRIS Plus OpenAPI and return results in agent-friendly formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chloepark85](https://clawhub.ai/user/chloepark85)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, IP analysts, and agents use this skill to run Korean prior-art searches, competitor IP monitoring, brand availability checks, and IP diligence workflows from shell commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default KIPRIS endpoint uses plain HTTP, which can expose API keys and query contents in transit.

Mitigation: Use the skill only after changing or verifying the endpoint to HTTPS, and test that requests fail closed if HTTPS is unavailable.

Risk: Passing the API key with --key can expose it through shell history, logs, or process listings.

Mitigation: Provide the key through KIPRIS_PLUS_KEY in a protected environment and avoid command-line key arguments.

Risk: KIPRIS_BASE can redirect requests to an untrusted host.

Mitigation: Keep KIPRIS_BASE unset or pin it to a reviewed KIPRIS Plus HTTPS endpoint before installation.

Risk: Scheduled watch examples can expose or mix local state if run from a shared directory.

Mitigation: Run scheduled examples with a private state directory and restrict file permissions.

## Reference(s):

- [KIPRIS Plus](https://plus.kipris.or.kr)
- [ClawHub skill page](https://clawhub.ai/chloepark85/skills/kipris-cli)
- [Skill documentation](SKILL.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, code]

**Output Format:** [JSONL by default, with optional JSON or XML; examples may produce Markdown or CSV summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a KIPRIS_PLUS_KEY; callers manage pagination, quota, throttling, and any local state.]

## Skill Version(s):

0.1.0 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
