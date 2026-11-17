## Description:

Helps agents use LinkFox to manage Amazon store A+ Content, including searching, creating, updating, validating, submitting, associating ASINs, reviewing publish records, and suspending A+ display.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, operators, and developers use this skill to manage Amazon A+ Content workflows through LinkFox and Amazon SP-API. It is intended for storefront content operations where the user needs structured guidance, shell commands, API calls, and saved JSON responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform live Amazon A+ storefront changes, including create, update, ASIN replacement, approval submission, and suspension actions.

Mitigation: Confirm user intent before each write, replacement, approval, suspension, or payment action, and review target seller, region, marketplace, ASINs, and contentReferenceKey.

Risk: The skill handles LinkFox credentials, phone/SMS login, and payment or order flows.

Mitigation: Use the expected LinkFox authentication flow, keep API keys out of shared logs or chats, and avoid custom endpoint environment variables unless they are trusted.

Risk: Saved JSON response files may contain sensitive seller or storefront data.

Mitigation: Review saved response files for sensitive seller data and restrict workspace access and retention according to the user's operational policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-amazon-store-aplus-content)
- [Amazon A+ Content Management API reference](artifact/references/api.md)
- [Authentication and billing onboarding](artifact/references/onboarding.md)
- [searchContentDocuments](https://developer-docs.amazon.com/sp-api/reference/searchcontentdocuments)
- [createContentDocument](https://developer-docs.amazon.com/sp-api/reference/createcontentdocument)
- [getContentDocument](https://developer-docs.amazon.com/sp-api/reference/getcontentdocument)
- [updateContentDocument](https://developer-docs.amazon.com/sp-api/reference/updatecontentdocument)
- [listContentDocumentAsinRelations](https://developer-docs.amazon.com/sp-api/reference/listcontentdocumentasinrelations)
- [postContentDocumentAsinRelations](https://developer-docs.amazon.com/sp-api/reference/postcontentdocumentasinrelations)
- [validateContentDocumentAsinRelations](https://developer-docs.amazon.com/sp-api/reference/validatecontentdocumentasinrelations)
- [searchContentPublishRecords](https://developer-docs.amazon.com/sp-api/reference/searchcontentpublishrecords)
- [postContentDocumentApprovalSubmission](https://developer-docs.amazon.com/sp-api/reference/postcontentdocumentapprovalsubmission)
- [postContentDocumentSuspendSubmission](https://developer-docs.amazon.com/sp-api/reference/postcontentdocumentsuspendsubmission)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON files, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON API responses saved to files or summarized on stdout]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may include LinkFox gateway status, parsed Amazon SP-API response bodies, saved response file paths, and summaries for large responses.]

## Skill Version(s):

1.0.8 (source: evidence.json release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
