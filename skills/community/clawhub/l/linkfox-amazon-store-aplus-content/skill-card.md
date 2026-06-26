## Description: <br>
Helps agents manage Amazon Seller Central A+ Content through LinkFox, including document search, creation, retrieval, updates, ASIN relation validation and replacement, publish record lookup, approval submission, and suspension. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, commerce operators, and their agents use this skill to inspect and manage Amazon A+ Content documents, ASIN associations, validation, publishing status, approval submission, and suspension workflows for authorized stores. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive Amazon seller API credentials through LinkFox. <br>
Mitigation: Install and run it only when the user trusts LinkFox with the seller API key and has confirmed the intended authorized seller account. <br>
Risk: Write operations can change live storefront A+ Content, including approval submission, suspension, and ASIN relationship replacement. <br>
Mitigation: Before executing write operations, confirm the seller, marketplace, contentReferenceKey, operation type, and ASIN set with the user. <br>
Risk: Replacing ASIN associations can remove ASINs from the document and suspend A+ Content display for those products. <br>
Mitigation: Review the current ASIN association state and compare it with the requested replacement set before submitting the operation. <br>
Risk: The skill passes complex contentDocument payloads through to Amazon and does not provide full model validation. <br>
Mitigation: Validate the contentDocument structure against Amazon's A+ Content Management model and use the validation operation before submitting for approval. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/linkfox-amazon-store-aplus-content) <br>
- [Amazon Store A+ Content Management API Reference](references/api.md) <br>
- [Amazon SP-API searchContentDocuments](https://developer-docs.amazon.com/sp-api/reference/searchcontentdocuments) <br>
- [Amazon SP-API createContentDocument](https://developer-docs.amazon.com/sp-api/reference/createcontentdocument) <br>
- [Amazon SP-API getContentDocument](https://developer-docs.amazon.com/sp-api/reference/getcontentdocument) <br>
- [Amazon SP-API updateContentDocument](https://developer-docs.amazon.com/sp-api/reference/updatecontentdocument) <br>
- [Amazon SP-API listContentDocumentAsinRelations](https://developer-docs.amazon.com/sp-api/reference/listcontentdocumentasinrelations) <br>
- [Amazon SP-API postContentDocumentAsinRelations](https://developer-docs.amazon.com/sp-api/reference/postcontentdocumentasinrelations) <br>
- [Amazon SP-API validateContentDocumentAsinRelations](https://developer-docs.amazon.com/sp-api/reference/validatecontentdocumentasinrelations) <br>
- [Amazon SP-API searchContentPublishRecords](https://developer-docs.amazon.com/sp-api/reference/searchcontentpublishrecords) <br>
- [Amazon SP-API postContentDocumentApprovalSubmission](https://developer-docs.amazon.com/sp-api/reference/postcontentdocumentapprovalsubmission) <br>
- [Amazon SP-API postContentDocumentSuspendSubmission](https://developer-docs.amazon.com/sp-api/reference/postcontentdocumentsuspendsubmission) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples, JSON command arguments, and JSON API responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a LinkFox API key and an authorized Amazon seller account; write operations can affect live A+ Content.] <br>

## Skill Version(s): <br>
0.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
