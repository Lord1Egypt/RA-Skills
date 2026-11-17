## Description:

libtv-skill helps agents generate and edit images or videos through LibTV session workflows and compatible Gemini, Sora, Veo, Grok, Doubao, and Vidu API paths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huguanjin](https://clawhub.ai/user/huguanjin)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and creator-facing agents use this skill to submit image and video generation or editing requests, upload reference media, poll job status, and retrieve generated assets from LibTV or compatible provider endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload local image or video files and download generated results.

Mitigation: Use non-sensitive input files, confirm transfer destinations, and confine downloads to a non-sensitive output directory.

Risk: The security summary flags weak validation and unvalidated network destinations.

Mitigation: Use only trusted HTTPS API endpoints and test with non-production credentials before broader use.

Risk: The skill relies on private or paid API credentials.

Mitigation: Keep credentials in environment variables, use least-privilege keys, and avoid sharing logs or artifacts that may contain secrets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huguanjin/skills/huguanjin-libtv-skill)
- [LibTV](https://www.liblib.tv)
- [Configuration Guide](CONFIG.md)
- [Usage Guide](references/usage-guide.md)
- [Workflows](references/workflows.md)
- [Output Format](references/output-format.md)
- [Smoke Tests](SMOKE_TESTS.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON result objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return generated media URLs, project URLs, local downloaded files, status JSON, and configuration guidance for required environment variables.]

## Skill Version(s):

1.0.4 (source: server release metadata; artifact metadata version is 1.0.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
