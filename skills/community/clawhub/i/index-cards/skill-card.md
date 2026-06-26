## Description: <br>
Index Cards helps an agent design and mail physical greeting cards through the Index Cards API, including artwork generation, previews, checkout, and order placement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jonwheatley](https://clawhub.ai/user/jonwheatley) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill when they want an agent to help create, preview, purchase, and send a real greeting card by mail. The skill is intended for occasions such as birthdays, holidays, thank-yous, and other personal messages, with explicit confirmation before using personal data or placing an order. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recipient names, mailing addresses, phone numbers, card artwork URLs, and occasion text may be sent to Index Cards to fulfill physical card orders. <br>
Mitigation: Use the skill only when comfortable sharing delivery details, confirm recipient and address information with the user, and place orders only after explicit approval. <br>
Risk: The skill may use a configured Gemini API key for image generation, which can send prompts to Google and consume the user's quota. <br>
Mitigation: Require explicit approval before using a Gemini API key and make clear that prompt content may be sent to Google and billed against the user's quota. <br>
Risk: The optional contacts cache can store names, birthdays, addresses, phone numbers, notes, and prior card history locally. <br>
Mitigation: Create, read, or reuse the contacts cache only after opt-in consent, and confirm saved address details before reusing them. <br>
Risk: The security review notes conflicting privacy wording around contact and address data. <br>
Mitigation: Review the current privacy terms and the data sent for delivery before installing or deploying the skill. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jonwheatley/index-cards) <br>
- [Index Cards Homepage](https://indexcards.com) <br>
- [Index Cards Privacy Policy](https://indexcards.com/privacy) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API calls, Configuration, Text] <br>
**Output Format:** [Markdown instructions with API request examples and user-facing text guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use an opt-in local contacts cache and may guide authenticated API calls for card generation, checkout, and ordering.] <br>

## Skill Version(s): <br>
1.3.1 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
