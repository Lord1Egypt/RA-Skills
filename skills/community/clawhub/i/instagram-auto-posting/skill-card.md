## Description: <br>
Automate creation and direct posting of promotional images to Instagram Business accounts using Meta Graph API without third-party schedulers or paid tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pawanshekhawat](https://clawhub.ai/user/pawanshekhawat) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create promotional Instagram creatives, upload them for public hosting, and publish them to Instagram Business accounts with user-provided Meta and Cloudinary credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish publicly to an Instagram Business account once credentials and posting inputs are provided. <br>
Mitigation: Use least-privilege or test Meta credentials and manually confirm the target account, image URL, and caption before running the posting script. <br>
Risk: Cloudinary uploads may expose generated media through a public URL used for Instagram publishing. <br>
Mitigation: Restrict Cloudinary upload presets and review uploaded media before sharing its URL with the posting step. <br>
Risk: The optional scraper may extract public business details, including contact information, from a user-provided website URL. <br>
Mitigation: Only provide public business URLs, avoid internal or private URLs, and review scraped details before using them in promotional content. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/pawanshekhawat/instagram-auto-posting) <br>
- [Meta Graph API Explorer](https://developers.facebook.com/tools/explorer/) <br>
- [Cloudinary](https://cloudinary.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [When the bundled scripts are run, they can create image files, upload media, scrape a user-provided public website URL, and publish to Instagram through external APIs.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
