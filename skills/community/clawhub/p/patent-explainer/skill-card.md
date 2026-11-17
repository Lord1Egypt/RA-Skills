## Description:

Explains a single patent in plain language, covering its claims, legal status, key technical features, and similar patents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

External users provide a patent publication or application number to receive a plain-language explanation of the patent, its independent-claim features, legal status, and comparable patents. The skill does not determine infringement and directs users to official records for authoritative legal status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential handling and request destinations warrant review; API keys or technical details could be exposed.

Mitigation: Do not share API keys in chat; use securely supplied credentials, restrict authenticated requests to approved HTTPS destinations, block unsafe redirects, and confirm fees and confidentiality before submitting technical details.

Risk: The security review reports cache-path flaws that warrant review before installation.

Mitigation: Use a version that validates patent filenames and review cache-path handling before enabling file output.

## Reference(s):

- [PatentMax API Platform](https://api.ip930.com/features/api-platform)
- [API Reference](artifact/references/api-reference.md)
- [Search Workflow](artifact/references/search-workflow.md)
- [Frequently Asked Questions](artifact/references/faq.md)
- [ClawHub Skill Page](https://clawhub.ai/ip930/skills/patent-explainer)

## Skill Output:

**Output Type(s):** [Text, CSV]

**Output Format:** [Plain-language patent explanation and UTF-8 CSV file that can be opened in spreadsheet software]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes patent-summary text, claim-feature explanations, legal-status information, and similar-patent comparisons; legal conclusions are not provided. Some queries may incur fees.]

## Skill Version(s):

1.0.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
