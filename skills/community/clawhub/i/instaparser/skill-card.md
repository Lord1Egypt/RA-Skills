## Description: <br>
Use the Instaparser API to parse articles, PDFs, and generate summaries from URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[donohue](https://clawhub.ai/user/donohue) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve parsed article text, parse PDF content, and request article summaries through Instaparser when a user provides a URL or local PDF. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Instaparser receives submitted URLs, article content, and PDFs for third-party processing. <br>
Mitigation: Use the skill only for content you are comfortable sending to Instaparser, and avoid private URLs, confidential article content, or sensitive PDFs unless that processing is acceptable. <br>
Risk: The skill requires an Instaparser API key. <br>
Mitigation: Provide INSTAPARSER_API_KEY through the environment or a secure secrets feature instead of pasting the key into chat. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/donohue/instaparser) <br>
- [Instaparser website](https://www.instaparser.com) <br>
- [Instaparser API base](https://www.instaparser.com/api/) <br>
- [Instaparser Article API](https://www.instaparser.com/api/1/article) <br>
- [Instaparser PDF API](https://www.instaparser.com/api/1/pdf) <br>
- [Instaparser Summary API](https://www.instaparser.com/api/1/summary) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and parsed API response summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires INSTAPARSER_API_KEY and network access to Instaparser.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
