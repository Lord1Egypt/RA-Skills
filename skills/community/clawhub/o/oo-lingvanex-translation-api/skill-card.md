## Description:

Lingvanex Translation API (lingvanex.com). Use this skill for any Lingvanex Translation API request, including searching and reading data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and users with an OOMOL-connected Lingvanex account use this skill to check supported languages, detect the language of text, and translate text through Lingvanex.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute unverified remote code and can add other agent skills during startup.

Mitigation: Review and verify the CLI installer before setup. Set OO_SKILLS_SYNC_DISABLED=1 before running oo if you do not want startup skill writes.

Risk: Text submitted for translation may be processed by OOMOL and Lingvanex.

Mitigation: Submit only text you intend both services to process.

## Reference(s):

- [Lingvanex Translation API](https://lingvanex.com/products/translationapi/)
- [Lingvanex API documentation](https://docs.lingvanex.com/)
- [oo CLI controls](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [ClawHub skill release](https://clawhub.ai/oomol/skills/oo-lingvanex-translation-api)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Connector results in JSON, including translated text or language information, with usage guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions can accept one text value or a bounded list of text values.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
