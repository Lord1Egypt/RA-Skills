## Description:

Use Microsoft Text Translate to translate and process text, detect languages, convert scripts, and look up dictionary terms and examples.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use the skill to translate and process text, identify languages, convert scripts, and retrieve dictionary examples or alternatives through Microsoft Text Translate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: If the oo CLI is missing, setup instructions can run an online installer that the security review did not verify and that lacks a clear approval step.

Mitigation: Review and approve CLI installation separately, and verify a fixed release before installing it.

Risk: Automatic skill synchronization can affect other agent hosts.

Mitigation: Review synchronization settings and the affected hosts before enabling or running synchronization.

Risk: Translation text passes through OOMOL to Microsoft, and the hosted connector implementation was not verified.

Mitigation: Review data handling and connector details before sending sensitive text.

## Reference(s):

- [Microsoft Text Translate on ClawHub](https://clawhub.ai/oomol/skills/oo-microsoft-text-translate)
- [Microsoft Translator](https://azure.microsoft.com/en-us/products/ai-services/ai-translator)
- [Microsoft Translator API reference](https://learn.microsoft.com/en-us/azure/ai-services/translator/text-translation/reference/v3/reference)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain-text translation and language results, JSON action responses, and Markdown guidance with inline shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected action, input text, and supported languages.]

## Skill Version(s):

1.0.4 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
