## Description:

Generates OpenClaw model inventory and model-card images from openclaw.json for listing configured models, checking default and fallback chains, and sharing a visual card.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdsdsdff](https://clawhub.ai/user/sdsdsdff)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to inspect OpenClaw model configuration, verify default and fallback chains, and produce a shareable model card from openclaw.json.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The screenshot renderer can treat configuration text as active HTML, which may create unexpected rendering or network-resource risk for untrusted configs.

Mitigation: Use text mode for trusted OpenClaw configs, and run image rendering only in a sandbox with no network access when the config comes from another person.

Risk: Generated images can be influenced by attacker-controlled openclaw.json content.

Mitigation: Treat generated images as untrusted output, review them before sharing, and do not rely on current sanitization claims.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, guidance]

**Output Format:** [CLI text or Markdown, with optional PNG image output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can run consistency checks for missing model references, alias conflicts, and suspicious contextWindow values.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
