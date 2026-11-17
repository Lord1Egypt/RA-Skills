## Description:

Provides string manipulation and transformation operations for working with text, including formatting, case conversion, escaping, encoding, and similarity checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to transform and format text, including case conversion, trimming, padding, truncation, slug generation, escaping, encoding, template interpolation, and string similarity checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Input-validation bugs can cause unexpected behavior when chunking strings or using custom trim characters with untrusted input.

Mitigation: Validate argument types and ranges, and escape custom trim characters before exposing these helpers to untrusted input.

Risk: HTML escaping can be mistaken for complete protection in complex web contexts.

Mitigation: Treat the HTML escaping helper as convenience encoding only and use context-aware sanitization for web output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/skills/jpeng-string-utils)

## Skill Output:

**Output Type(s):** [text, code, guidance]

**Output Format:** [Plain text or Markdown with optional JavaScript snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: evidence release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
