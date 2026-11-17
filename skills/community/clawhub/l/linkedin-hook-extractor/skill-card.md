## Description:

Reverse-engineer the hook formula from a viral LinkedIn post URL, identifying the matching canonical formula, why it worked, and a blank template for adapting the structure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sergebulaev](https://clawhub.ai/user/sergebulaev)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing operators, creators, and content strategists use this skill to study viral LinkedIn posts, classify hook structure, understand why the post worked, and produce a reusable template for their own topic.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the APIFY_TOKEN path may send the LinkedIn post URL to Apify for fetching.

Mitigation: Leave APIFY_TOKEN unset and paste the post text manually when the URL should not be sent to Apify.

Risk: Non-English posts may not receive full formula classification.

Mitigation: Treat non-English outputs as structural analysis and verify any formula classification manually before reuse.

## Reference(s):

- [Hook Formula Classification Rules](artifact/references/classification-rules.md)
- [Examples - LinkedIn Hook Extractor](artifact/references/examples.md)
- [ClawHub skill page](https://clawhub.ai/sergebulaev/skills/linkedin-hook-extractor)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown with structured classification, rationale, cautions, and template text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask the user to paste LinkedIn post text when APIFY_TOKEN is unset; non-English posts may receive structural breakdown rather than full formula classification.]

## Skill Version(s):

1.0.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
