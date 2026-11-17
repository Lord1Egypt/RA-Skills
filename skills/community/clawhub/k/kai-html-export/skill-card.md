## Description:

Export HTML files to PPTX or PNG, or publish HTML to a public share URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaisersong](https://clawhub.ai/user/kaisersong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to convert HTML presentations or reports into PPTX or PNG outputs, and optionally publish HTML as a public URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HTML sharing can publish local files or folders more broadly than intended.

Mitigation: Before running share-html.py, review the target folder and remove secrets, hidden files, backups, source maps, and confidential material.

Risk: Rendering or native export of untrusted HTML can expose users to unsafe or unexpected local content handling.

Mitigation: Use local export on trusted HTML when possible and avoid native export on untrusted HTML.

Risk: Vercel sharing may make a linked project public.

Mitigation: Prefer the Cloudflare default or trusted preinstalled CLIs, and verify project visibility before using the Vercel helper.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kaisersong/skills/kai-html-export)
- [Publisher Profile](https://clawhub.ai/user/kaisersong)
- [Skill Definition](artifact/SKILL.md)
- [README](artifact/README.md)
- [PPTX Export Strategy](artifact/PPTX_EXPORT_STRATEGY.md)
- [Cloudflare HTML Share Specification](artifact/docs/superpowers/specs/2026-04-04-share-html-cloudflare.md)

## Skill Output:

**Output Type(s):** [files, text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, generated PPTX or PNG files, and optional public share URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [PPTX export can be image-based or editable native PPTX; HTML sharing may require authenticated Cloudflare or Vercel CLI setup.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
