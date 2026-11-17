## Description:

Imgur API CLI for agents that uploads images by file path or URL, fetches image metadata, deletes uploads by delete-hash, and creates or manages albums with JSON output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chloepark85](https://clawhub.ai/user/chloepark85)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to turn local image files or remote image URLs into public Imgur links, retrieve image metadata, delete uploads, and organize hosted images into albums for downstream posting or pipeline workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploaded images and image URLs are sent to Imgur and may become externally reachable.

Mitigation: Use the skill only for images intended for external hosting; avoid sensitive screenshots, private files, credentials, and personal data.

Risk: Authenticated actions use an Imgur OAuth access token tied to a user account.

Mitigation: Keep IMGUR_ACCESS_TOKEN scoped to the intended account and avoid sharing it in prompts, logs, or artifacts.

Risk: Anonymous uploads can be difficult to remove without the returned delete hash.

Mitigation: Store anonymous delete hashes when uploads may need later cleanup.

## Reference(s):

- [Imgur API Documentation](https://apidocs.imgur.com/)
- [Imgur OAuth Client Registration](https://api.imgur.com/oauth2/addclient)
- [ClawHub skill page](https://clawhub.ai/chloepark85/skills/imgur-cli)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Indented JSON from CLI commands, with setup and usage guidance in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires IMGUR_CLIENT_ID for anonymous use or IMGUR_ACCESS_TOKEN for authenticated account actions.]

## Skill Version(s):

0.1.0 (source: CHANGELOG.md, pyproject.toml, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
