## Description:

Recognizes K12 arithmetic and math-problem images, including handwritten or printed operations, vertical calculations, fractions, and equations, and returns structured OCR text results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hzheigege](https://clawhub.ai/user/hzheigege)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to convert math-problem images or image URLs into editable text and structured OCR detection data. It is suited for arithmetic recognition workflows that can use Tencent Cloud OCR and configured Tencent Cloud credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Math-problem images or image URLs are sent to Tencent Cloud OCR.

Mitigation: Use the skill only with images appropriate for Tencent Cloud processing, and avoid submitting sensitive student or personal information unless policy allows it.

Risk: The skill requires Tencent Cloud credentials.

Mitigation: Configure credentials through environment or platform secrets, rotate them as needed, and avoid exposing them in prompts, logs, or shared configuration.

Risk: The release evidence flags malformed plugin.json and dependency pinning concerns.

Mitigation: Fix the plugin manifest JSON and pin dependency versions before production deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hzheigege/skills/math-arithmetic-orc)
- [Tencent Cloud OCR API endpoint](https://ocr.tencentcloudapi.com)

## Skill Output:

**Output Type(s):** [text, JSON]

**Output Format:** [JSON object containing success status, a human-readable message, recognized text, text detection details, image angle, and request ID when available.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill may return Tencent Cloud OCR errors or an empty result when no text is detected.]

## Skill Version(s):

1.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
