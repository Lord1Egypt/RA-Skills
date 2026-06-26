## Description: <br>
Scrapes and returns captions from public Instagram post or reel URLs so an agent can display, summarize, translate, or analyze the caption. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rdk14](https://clawhub.ai/user/rdk14) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill when a public Instagram post or reel URL is provided and the user needs the raw caption, basic post metadata, or a follow-on summary or translation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Credential exposure if users add Instagram usernames or passwords directly to the scraper script. <br>
Mitigation: Use the skill only for public Instagram posts unless the credential flow is redesigned, and do not hardcode Instagram credentials in the script. <br>
Risk: Unsafe command construction could occur if a user-provided Instagram URL is interpolated into a shell command. <br>
Mitigation: Invoke the URL as a quoted or structured argument and avoid raw shell interpolation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rdk14/instagram-caption-scraper) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Plain text caption with post metadata or an error message] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3.8+ and instaloader==4.14.1; intended for public Instagram post and reel URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
