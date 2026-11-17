## Description:

Turns a product still image into a short, polished ad or promo video, with guidance for image-to-video generation or product replacement in existing footage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runware](https://clawhub.ai/user/runware)

### License/Terms of Use:

MIT-0

## Use Case:

External users, creators, and marketing teams use this skill to turn clean product media into short promotional video concepts, either by generating a new product hero clip or by swapping a product into existing footage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided product images or source videos may be uploaded to the configured external video generation provider.

Mitigation: Confirm the provider account and data handling terms before use, and avoid confidential unreleased product media unless those terms are acceptable.

Risk: Generated ads can introduce unsupported claims, ratings, testimonials, logos, badges, or readable copy.

Mitigation: Review outputs for brand safety and only include factual claims or on-screen wording supplied by the user.

Risk: Live model schemas, input field names, and supported duration or resolution values can change.

Mitigation: Confirm the current model schema and exact input fields before making video generation calls.

## Reference(s):

- [Product Ad Video examples](references/examples.md)
- [ClawHub skill page](https://clawhub.ai/runware/skills/product-ad-video)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Markdown guidance with JSON request examples and command-oriented workflow steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces async video task guidance; final video URLs are returned by the selected external video generation provider.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
