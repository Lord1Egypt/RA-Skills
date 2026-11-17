## Description:

Plate Recognizer (platerecognizer.com). Use this skill for ANY Plate Recognizer request — searching and reading data. Whenever a task involves Plate Recognizer, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve Plate Recognizer usage statistics and analyze an image for number-plate detections through a connected Plate Recognizer account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fallback setup can execute remote installers that have not been verified.

Mitigation: Review the oo CLI and its installer before permitting setup, and check which agent skills the CLI installs or updates.

Risk: Image recognition sends images to a remote service and may consume credits.

Mitigation: Use images approved for remote processing and review usage and credit requirements before submitting them.

## Reference(s):

- [Plate Recognizer](https://platerecognizer.com)
- [Snapshot API Reference](https://guides.platerecognizer.com/docs/snapshot/api-reference/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [JSON connector results with concise natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes current-month usage statistics or normalized number-plate detections from one image.]

## Skill Version(s):

1.0.5 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
