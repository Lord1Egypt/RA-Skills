## Description:

This skill helps create original algorithmic art using p5.js, seeded randomness, flow fields, particle systems, and interactive parameter exploration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moyu0032](https://clawhub.ai/user/moyu0032)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and creative practitioners use this skill to create original generative art workflows: a concise algorithmic philosophy followed by p5.js code for an interactive viewer with seeded variation and parameter controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML viewers load p5.js from cdnjs and fonts from Google, so opening them may contact third-party services and may not work fully offline.

Mitigation: For privacy-sensitive or offline use, bundle dependencies locally, add subresource integrity where remote assets remain, or remove remote fonts.

Risk: The artifact template asks agents to preserve Anthropic-styled UI branding in generated viewers.

Mitigation: Use neutral branding unless Anthropic-styled output is explicitly desired and permitted for the release context.

Risk: Requests for generative art can drift toward imitating a living artist or protected style.

Mitigation: Keep outputs original and frame user references as abstract algorithmic concepts rather than copying existing artists' work.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/moyu0032/skills/mo-test-1)
- [p5.js CDN dependency](https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.7.0/p5.min.js)
- [Google Fonts dependency](https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&family=Lora:wght@400;500&display=swap)

## Skill Output:

**Output Type(s):** [text, markdown, code, html, guidance]

**Output Format:** [Markdown philosophy plus self-contained HTML and JavaScript artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs emphasize seeded randomness, p5.js generative algorithms, interactive parameter controls, and reproducible visual variations.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
