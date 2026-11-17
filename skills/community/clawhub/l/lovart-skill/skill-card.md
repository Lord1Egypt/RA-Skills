## Description:

Generate images, videos, and audio or music with Lovart AI, and manage Lovart projects, threads, and settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lovart-admin](https://clawhub.ai/user/lovart-admin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent to create visual or audio assets through Lovart, continue project threads, upload references, retrieve generated files, and manage Lovart project settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, selected reference files, project or thread metadata, and generated artifacts are sent to Lovart.

Mitigation: Use the skill only for content that is appropriate to process with Lovart, and avoid uploading private files unless that processing is intentional.

Risk: The skill persists and reuses local project and thread state.

Mitigation: Review or clear ~/.lovart/state.json and confirm the active project and thread before sensitive work.

Risk: Endpoint or TLS settings can weaken connection safeguards.

Mitigation: Keep LOVART_BASE_URL on the official endpoint and do not enable LOVART_INSECURE_SSL.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lovart-admin/skills/lovart-skill)
- [Lovart project canvas](https://www.lovart.ai/canvas?projectId={project_id})

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown responses with JSON command results, downloaded media file attachments, and Lovart project links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Lovart access credentials, persists local project and thread state, and can return images, videos, audio files, status details, warnings, and error messages.]

## Skill Version(s):

1.1.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
