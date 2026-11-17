## Description:

Huo15 Markdown Export converts existing Markdown into styled PDF, DOCX, HTML, long-image PNG, WeChat inline HTML, live previews, and share-ready publishing outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobod1](https://clawhub.ai/user/zhaobod1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and content teams use this skill to turn existing Markdown into polished multi-format documents for technical blogs, customer reports, social posts, WeChat articles, release notes, and shareable previews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Rendering active Markdown or Mermaid content can execute browser-side HTML or fetch remote Mermaid code.

Mitigation: Use trusted Markdown only and pass --no-mermaid for sensitive, offline, or network-restricted documents.

Risk: Preview or share URLs can point to localhost or private LAN hosts that external recipients cannot access.

Mitigation: Check returned URLs before sharing and fall back to file delivery or a local path when the host is loopback or private network.

Risk: Publishing workflows can create public links and local knowledge-base archives for source documents.

Mitigation: Avoid confidential inputs, use --no-archive for sensitive documents, and set short share-link lifetimes when public links are needed.

Risk: The workspace installer can copy the skill into multiple OpenClaw workspaces.

Mitigation: Run the installer with a dry run first, back up affected workspaces, and review each target before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaobod1/skills/huo15-markdown-export)
- [Artifact README](README.md)
- [Theme design guide](themes/DESIGN.md)
- [Template README](templates/README.md)
- [Package manifest](package.json)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash commands and JSON handoff data; rendered artifacts include PDF, DOCX, HTML, PNG, and inline HTML.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Node >=18 is required; Pandoc is required for DOCX output; WeasyPrint is optional for the Pandoc PDF path.]

## Skill Version(s):

0.4.4 (source: SKILL.md frontmatter, package.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
