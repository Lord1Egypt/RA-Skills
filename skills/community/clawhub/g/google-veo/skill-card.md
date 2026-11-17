## Description:

Generate text-to-video clips with Google Veo models through the inference.sh CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[okaris](https://clawhub.ai/user/okaris)

### License/Terms of Use:


## Use Case:

Developers and creators use this skill to ask an agent for inference.sh commands, examples, and prompt guidance for generating Google Veo videos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The quick start pipes a remote installer into a shell before login.

Mitigation: Prefer a manual, version-pinned download with checksum or signature verification, inspect the installer before running it, and run infsh login only after confirming the installed binary.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/okaris/skills/google-veo)
- [inference.sh](https://inference.sh)
- [inference.sh CLI Installer](https://cli.inference.sh)
- [Manual Install and Checksum Verification](https://dist.inference.sh/cli/checksums.txt)
- [Running Apps](https://inference.sh/docs/apps/running)
- [Streaming Results](https://inference.sh/docs/api/sdk/streaming)
- [Content Pipeline Example](https://inference.sh/docs/examples/content-pipeline)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include infsh CLI commands and JSON input examples for Google Veo app runs.]

## Skill Version(s):

0.1.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
