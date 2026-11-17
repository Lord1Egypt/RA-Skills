## Description:

Uploads vocabulary words to the K241 class self-study website and can fetch translations and pinyin automatically.

This skill is ready for commercial/non-commercial use.

## Publisher:

[veelove](https://clawhub.ai/user/veelove)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to add or update vocabulary entries on the K241 class word self-study website, including translations and pinyin when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Published reusable website credentials could allow unauthorized access to the K241 website.

Mitigation: Treat the listed password as compromised, rotate it, and replace embedded credentials with per-user or secret-managed authentication.

Risk: The skill can make authenticated remote changes to class vocabulary data.

Mitigation: Require explicit user confirmation before any upload or update operation.

Risk: Loose trigger language could activate the skill when the user did not intend to change the K241 website.

Mitigation: Limit activation to requests that clearly mention uploading or updating vocabulary on the K241 website.

## Reference(s):

- [K241 Word Upload skill page](https://clawhub.ai/veelove/skills/k241-word-upload)
- [Publisher profile](https://clawhub.ai/user/veelove)
- [K241 word self-study website](https://k241.wooomooo.com)
- [K241 word pinyin reference](references/pinyin.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text]

**Output Format:** [Markdown with HTTP request examples and workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include website login, upload, verification, and update steps for K241 vocabulary entries.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
