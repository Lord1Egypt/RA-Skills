## Description:

Perceptron helps agents analyze images and video frames with visual Q&A, object detection, OCR, captioning, counting, and grounded spatial outputs such as boxes, points, and polygons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[subraiz](https://clawhub.ai/user/subraiz)

### License/Terms of Use:


## Use Case:

Developers and agents use Perceptron to inspect user-provided images, image URLs, and extracted video frames for descriptions, OCR, detection, spatial localization, and structured visual analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Images, videos, prompts, OCR outputs, and URLs are sent to Perceptron's external service.

Mitigation: Use only data approved for that service; avoid regulated, confidential, or internal-only content without approval.

Risk: PERCEPTRON_API_KEY exposure could grant access to the external service.

Mitigation: Keep the API key scoped and private, use environment variables, and do not commit secrets.

Risk: The external SDK package or service behavior may change after installation.

Mitigation: Use a virtual environment and pin and review the perceptron package version before deployment.

## Reference(s):

- [Perceptron Docs](https://docs.perceptron.inc/)
- [Perceptron API Reference](https://docs.perceptron.inc/api-reference/endpoint/chat-completions)
- [Perceptron Capabilities Reference](https://docs.perceptron.inc/capabilities/)
- [Perceptron Prompting Reference](https://docs.perceptron.inc/best-practices/prompting-reference)
- [Capabilities Reference](references/capabilities.md)
- [Prompting Reference](references/prompting.md)
- [API Reference](references/api.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown prose with Python and shell examples; CLI output may be plain text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PERCEPTRON_API_KEY and sends selected media, prompts, OCR outputs, and URLs to the external Perceptron service.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
