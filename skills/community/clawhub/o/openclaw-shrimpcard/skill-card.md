## Description:

Use when an agent needs to turn evidence-backed behavior into a validated self-intro submission, a share-card JSON payload, and a final screenshot-friendly HTML selfie card with a real 8-bit character image.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenghaofan1998](https://clawhub.ai/user/chenghaofan1998)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to convert real agent evidence into a validated public identity bundle, including self-intro JSON, share-card JSON, image guidance, and screenshot-ready HTML.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can expose private memory, past conversations, tool traces, or owner contact details when gathering evidence for public output.

Mitigation: Use only explicit, user-approved evidence sources and review every public field before sharing.

Risk: Rendered card JSON from untrusted sources may be unsafe because card data is embedded into executable HTML.

Mitigation: Avoid rendering or hosting untrusted card JSON until the HTML data embedding issue is fixed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chenghaofan1998/skills/openclaw-shrimpcard)
- [Agent Self Extraction Guide](artifact/references/agent-self-extraction-guide.md)
- [ClawHub Overview](artifact/CLAWHUB.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON artifacts, shell commands, generated image prompts, and rendered HTML files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces schema-validated self-intro and share-card payloads and requires review before public sharing.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
