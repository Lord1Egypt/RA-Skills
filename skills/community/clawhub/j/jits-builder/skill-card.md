## Description:

Instantly build, deploy, and access single-page, vanilla JavaScript mini-apps from voice or text descriptions via a Cloudflare tunnel URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dannyshmueli](https://clawhub.ai/user/dannyshmueli)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to turn short voice or text requests into temporary, shareable, single-page web tools. It is suited for quick client-side utilities such as timers, calculators, formatters, converters, and small decision aids.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated apps may be exposed publicly through Cloudflare tunnel URLs.

Mitigation: Do not use the skill with secrets, private data, authentication flows, or content that should remain local unless tunnel creation is changed to require explicit opt-in.

Risk: The bundled shell workflow has review-worthy risks around unsafe arguments, Node command interpolation, wildcard cleanup, and process ownership checks.

Mitigation: Validate app names and ports, avoid node -e interpolation, remove wildcard cleanup, and verify PID ownership before stopping or deleting app files.

Risk: The skill can rely on remotely downloaded executable files.

Mitigation: Pin or verify downloaded executable files before running them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dannyshmueli/skills/jits-builder)
- [Publisher profile](https://clawhub.ai/user/dannyshmueli)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with single-file HTML, CSS, and JavaScript code plus shell commands for serving and managing generated apps.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated apps are intended to be client-side, dependency-free, mobile-friendly single-page tools and may return a temporary public Cloudflare tunnel URL.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
