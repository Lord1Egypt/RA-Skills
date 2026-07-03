## Description: <br>
Searches Google to discover social media profiles associated with a person, brand, or username and returns platform names, profile URLs, usernames, bio snippets, and follower counts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[browseract-cli](https://clawhub.ai/user/browseract-cli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to find public social media profiles for a person, brand, or username through Google search results and summarize the matching public profile data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill performs browser automation and the security summary flags possible encouragement of stealth rate-limit evasion. <br>
Mitigation: Use it only for public data collection that respects site restrictions and rate limits; do not use it to bypass access controls. <br>
Risk: The skill can maintain local operational memory, which could retain sensitive identifiers or private page content if misused. <br>
Mitigation: Review or disable the memory file before use, and do not store credentials, private page contents, or sensitive identifiers in it. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/browseract-cli/google-social-media-finder-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON extraction results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs public search-result fields such as platform, URL, username, title, snippet, and follower text when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
