## Description: <br>
Publish Markdown and HTML to huozi.app as beautiful, shareable web pages. Register, manage, and publish through conversation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dachein](https://clawhub.ai/user/dachein) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and teams use this skill to publish generated Markdown or self-contained HTML pages to Huozi, manage existing pages, and set up API-key based publishing from an agent conversation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an email address, verification code, and HUOZI_API_KEY for account setup and authenticated publishing. <br>
Mitigation: Install and use it only if you trust huozi.app, treat HUOZI_API_KEY like a password, and avoid sharing the key in published pages, logs, or prompts. <br>
Risk: Published Markdown or HTML can become publicly shareable content on huozi.app. <br>
Mitigation: Review content for secrets, private documents, and sensitive information before publishing or updating a page. <br>
Risk: Update and delete operations target pages by slug, so an incorrect slug can modify or remove the wrong page. <br>
Mitigation: Confirm the page slug and intended operation before update or delete requests. <br>


## Reference(s): <br>
- [Huozi homepage](https://huozi.app) <br>
- [Huozi agent API reference](https://huozi.app/docs4agent) <br>
- [Huozi setup](https://huozi.app/start) <br>
- [Huozi documentation](https://huozi.app/docs) <br>
- [ClawHub skill page](https://clawhub.ai/dachein/huozi) <br>
- [Publisher profile](https://clawhub.ai/user/dachein) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands, JSON API payloads, and publishing guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce public Huozi page URLs after authenticated API calls; published page content is limited to 2 MB per page.] <br>

## Skill Version(s): <br>
0.3.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
