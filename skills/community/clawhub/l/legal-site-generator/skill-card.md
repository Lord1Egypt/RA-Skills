## Description:

Generates a Cloudflare Pages-ready legal website for apps, including privacy, terms, support, and account deletion content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chentuan7963-afk](https://clawhub.ai/user/chentuan7963-afk)

### License/Terms of Use:

MIT

## Use Case:

Developers and app publishers use this skill to generate static legal and support pages for an application before deploying them to Cloudflare Pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated legal site may under-deliver on the promised multi-page compliance output.

Mitigation: Review the generated files before publication and confirm that required privacy, terms, support, and data deletion pages are present and complete.

Risk: User-provided input may produce unsafe HTML if escaping or validation is incomplete.

Mitigation: Validate and escape appName, companyName, and contactEmail before relying on generated pages for a real compliance site.

Risk: Generated files may overwrite an existing dist/ output without clear disclosure.

Mitigation: Run the skill in a clean workspace or back up existing dist/ content before generation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chentuan7963-afk/skills/legal-site-generator)

## Skill Output:

**Output Type(s):** [text, code, configuration]

**Output Format:** [Static HTML files in a dist/ directory plus a text status message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires appName, companyName, and contactEmail inputs.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
