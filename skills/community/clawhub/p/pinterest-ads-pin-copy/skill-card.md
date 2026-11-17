## Description:

Creates Pinterest ad pin-copy drafts from product-sheet details, placing the primary keyword within the first 40 title characters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce teams and affiliate publishers use this skill to draft Pinterest ad copy from product-sheet details and check it against stated copy limits and claim-support requirements.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Crafted product names can cause the script to overwrite files outside the selected output folder.

Mitigation: Use trusted product data and a fresh output folder; reject path separators, enforce output-folder containment, and prevent unintended overwrites before processing untrusted sheets.

Risk: The optional Windows toolkit is a separate, unsigned executable that is not needed for this workflow.

Mitigation: Review it separately before use, verify its download hash, keep it isolated, and avoid running it as administrator without a reason.

## Reference(s):

- [Pinterest ad field limits and pin copy rules](references/pinterest-ad-specs.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown pin-copy draft with a title, description, image overlay text, call to action, destination, and claim checks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Title up to 100 characters with the keyword in the first 40; description up to 500 characters; overlay text up to 10 words.]

## Skill Version(s):

1.0.7 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
