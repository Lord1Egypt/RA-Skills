## Description: <br>
Creates and manages draft sales listings on kleinanzeigen.de for users who want to sell an item, excluding buying, buyer communication, and other platforms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simon83s](https://clawhub.ai/user/simon83s) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to prepare a Kleinanzeigen sales listing by collecting product details, researching comparable prices, drafting listing text, selecting categories, and saving the listing as a draft for human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the assistant to handle Kleinanzeigen account credentials and an SMS code. <br>
Mitigation: Have the user log in directly in the browser instead of sharing a password, SMS code, or recovery details with the assistant. <br>
Risk: Draft listings can contain incorrect product details, price, location, shipping settings, or images that the user may not have rights to use. <br>
Mitigation: Review the draft, photos, price, location, shipping settings, and image rights before publishing; prefer user-owned photos. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/simon83s/kleinanzeigen-de-skill) <br>
- [Kleinanzeigen Kategorien](references/categories.md) <br>
- [Preisrecherche](references/pricing.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown or plain text with product questions, price rationale, listing copy, and a draft listing link.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill saves listings as drafts and requires human review before publication.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
