## Description:

Helps agents save, check, and publish Onimi Pages and Slides through browser-authorized access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mariohazy](https://clawhub.ai/user/mariohazy)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Creators and developers use this skill to save private drafts, check a fixed revision, and explicitly publish a Page or Slides release to an existing or newly chosen Onimi project. It can also manage project access and optional private participation when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The connection can access private drafts or change releases and project access.

Mitigation: Review browser consent scopes, confirm the exact project and requested access, and revoke the connection in the Onimi dashboard when no longer needed.

Risk: A canceled or uncertain publishing request may still have taken effect.

Mitigation: Preserve the task, check the server's current state, and retry only the original request after reconciliation.

Risk: Optional stage reporting can disclose limited task telemetry.

Mitigation: Keep reporting optional and limited to observed stages and the documented fixed fields.

## Reference(s):

- [ClawHub release](https://clawhub.ai/mariohazy/skills/onimi-pages-publish)
- [Onimi Pages connection](https://onimi.ai/mcp)
- [Onimi dashboard](https://onimi.ai/dashboard)
- [Installation and connection guide](references/installation.md)
- [Agent stage reporting guide](references/stage-observer.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with project and release links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports actual draft or publication status and access; does not treat a saved draft as published.]

## Skill Version(s):

0.3.1 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
