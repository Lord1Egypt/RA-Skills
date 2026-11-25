## Description:

Generates printable Chinese legal-document drafts for labor arbitration, rental disputes, and consumer complaints, including legal citations, compensation calculations, evidence lists, and user-facing cautions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mcheisenberg](https://clawhub.ai/user/mcheisenberg)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to draft common Chinese personal legal documents for employment, rental, and consumer disputes. It helps structure facts, requests, evidence lists, legal citations, next steps, and disclaimers for documents that users may print or submit after review.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The skill uses an off-platform payment QR code and asks users to send payment proof to an external seller.

Mitigation: Install only if the user accepts that payment flow, and avoid sending unnecessary personal or financial details in payment proof.

Risk: The Pro activation flow requires local script execution and stores a plaintext activation marker in the user's home directory.

Mitigation: Review the activation script before running it, run only the bundled script from the installed skill, and remove the marker file when uninstalling or rotating access.

Risk: Legal filings or notices may contain inaccurate, outdated, or incomplete citations for the user's specific facts.

Mitigation: Verify current legal citations and local filing requirements before relying on generated documents, and consult a qualified lawyer for high-stakes matters.

Risk: Document generation may request sensitive personal data such as ID numbers, addresses, phone numbers, or payment account details.

Mitigation: Minimize sensitive information entered into chat and fill highly sensitive fields locally in the final document where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mcheisenberg/skills/legal-doc-generator)
- [Labor arbitration document reference](references/01_劳动仲裁申请书.md)
- [Rental dispute document reference](references/02_租房纠纷文书.md)
- [Consumer rights document reference](references/03_消费维权文书.md)
- [Common legal-document errors and cautions](references/04_常见错误与注意事项.md)
- [Legal article quick reference](references/05_法律条文速查.md)
- [Reference index](references/README.md)
- [China laws and regulations database](https://flk.npc.gov.cn/)
- [National Enterprise Credit Information Publicity System](https://www.gsxt.gov.cn/)
- [National 12315 consumer complaint platform](https://www.12315.cn/)
- [People's Court online services](https://www.court.gov.cn/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown legal-document drafts with structured facts, claims, legal citations, evidence lists, compensation calculations, cautions, and follow-up guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes an AI-assistance disclaimer and may ask users to validate Pro activation locally before generating full cited documents.]

## Skill Version(s):

1.1.0 (source: evidence.json release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
