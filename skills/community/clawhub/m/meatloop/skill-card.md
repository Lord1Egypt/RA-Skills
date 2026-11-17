## Description:

A real human reviews an agent's question, screenshot, or pair of images and returns a structured verdict by email for sanity checks, content verification, creative judgment, and A/B image comparison.

This skill is ready for commercial/non-commercial use.

## Publisher:

[meatloopservice](https://clawhub.ai/user/meatloopservice)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use MeatLoop to request human review of binary or near-binary questions, screenshots, generated content, document images, or two-image comparisons when automated interpretation is uncertain. It is intended for practical human-in-the-loop verification, not specialist legal, medical, or financial judgment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected questions, screenshots, or images are sent to an external human operator by email.

Mitigation: Submit only sanitized, non-confidential material and avoid secrets, credentials, regulated data, private documents, and confidential business information.

Risk: The service provides human judgment and is not suitable for specialist legal, medical, or financial decisions.

Mitigation: Use responses as review signals only and route specialist or high-impact decisions to qualified domain experts.

## Reference(s):

- [MeatLoop homepage](https://github.com/meatloopservice/MeatLoop)
- [ClawHub skill page](https://clawhub.ai/meatloopservice/skills/meatloop)
- [Public review log](https://docs.google.com/spreadsheets/d/e/2PACX-1vTNynmFGYxtUetqMgvGsO4VY6TE_i-ZDdotEFweE_9QsZo4njPpBhrHZ5aYbTC7Ql-8GnwgN2NHnHXi/pub)
- [Verification code CSV log](https://docs.google.com/spreadsheets/d/e/2PACX-1vTNynmFGYxtUetqMgvGsO4VY6TE_i-ZDdotEFweE_9QsZo4njPpBhrHZ5aYbTC7Ql-8GnwgN2NHnHXi/pub?gid=1119131304&single=true&output=csv)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Plain-text email request guidance and structured plain-text verdict fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Standard responses may include VERDICT, REASON, CONFIDENCE, NOTE, VERIFICATION, and REQUEST-ID; A/B responses include BETTER IMAGE.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
