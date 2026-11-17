## Description:

Draft, prepare, and publish LinkedIn feed posts through OpenClaw browser automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yonghyeokrhee](https://clawhub.ai/user/yonghyeokrhee)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to standardize a prepare-then-post LinkedIn feed workflow: finalize post copy, open the feed composer, fill approved content, preview link unfurls, and publish only after explicit approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script can be aimed at arbitrary browser tabs or URLs even though the documented workflow is LinkedIn-only.

Mitigation: Use only with a trusted OpenClaw CLI and browser profile; do not allow untrusted callers or prompts to supply --open-url, --target-id, --profile, --config, or --publish, and validate that the active URL is https://www.linkedin.com/feed/ before filling or clicking.

Risk: Publishing is an external side effect that can post visible content to LinkedIn.

Mitigation: Keep prepare-only mode as the default and require explicit user approval of the exact body text, included links, and timing before running with --publish.

Risk: The workflow depends on a gateway token and an already-authenticated browser profile.

Mitigation: Use a trusted local token source, protect the OpenClaw configuration file, and avoid exposing credentials or authenticated browser control to untrusted prompts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yonghyeokrhee/skills/linkedin-post-openclaw-browser)
- [LinkedIn feed share composer](https://www.linkedin.com/feed/?shareActive=true)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and optional JSON status output from the helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OpenClaw CLI, an authenticated LinkedIn browser profile, and an OpenClaw gateway token; publishing should occur only after explicit user approval.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
