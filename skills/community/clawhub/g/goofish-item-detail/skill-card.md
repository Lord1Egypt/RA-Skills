## Description: <br>
Extracts detail data from a single Goofish item page, including title, price, seller information, description, image gallery, item attributes, and want count. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[browseract-cli](https://clawhub.ai/user/browseract-cli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to inspect a specific Goofish second-hand listing before purchase or to enrich a permitted list of item IDs with page-visible listing details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated batch extraction from Goofish can trigger anti-abuse controls or fall outside permitted use. <br>
Mitigation: Use only with a logged-in session you are authorized to use, keep request volume low, add delays between item pages, and stop when CAPTCHA or rate-limit challenges appear. <br>
Risk: Listing and seller fields may include personal or marketplace profile information. <br>
Mitigation: Collect only the fields needed for the task, avoid republishing unnecessary seller data, and follow applicable privacy, marketplace, and legal requirements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/browseract-cli/goofish-item-detail) <br>
- [Goofish item URL format](https://www.goofish.com/item?id={item_id}&categoryId={category_id}) <br>
- [Goofish home page](https://www.goofish.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Text] <br>
**Output Format:** [Markdown instructions with inline shell commands and JSON extraction output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an authenticated Goofish browser session; some listing fields may be null when not displayed on the page.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
