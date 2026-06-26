## Description: <br>
Extracts X (Twitter) data including user profiles, posts, followers, followings, media, and search results through a TweeterPy-based Python interface. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[hardbrick21](https://clawhub.ai/user/hardbrick21) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI-agent builders use this skill to retrieve public and authenticated X data for profile lookup, tweet extraction, follower and following review, media lookup, and tweet search workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated features require access to a sensitive X session credential. <br>
Mitigation: Prefer guest mode for public profile and tweet lookup, and only provide an auth_token through a secure runtime secret when authenticated access is necessary. <br>
Risk: Copying browser cookies into prompts, source files, or shared machines can expose an account session. <br>
Mitigation: Do not paste cookies into prompts or commit them to files; avoid saved sessions on shared or untrusted systems. <br>
Risk: Automated X data extraction can trigger rate limits or violate platform terms if used carelessly. <br>
Mitigation: Use small result counts, keep request delays enabled, back off on rate-limit errors, and confirm that the intended workflow complies with X terms before use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/hardbrick21/omni-x) <br>
- [AI Agent Guide](references/AI_AGENT_GUIDE.md) <br>
- [Installation Guide](references/INSTALLATION.md) <br>
- [Login Guide](references/LOGIN_GUIDE.md) <br>
- [TweeterPy Repository](https://github.com/iSarabjitDhiman/TweeterPy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance and Python examples; runtime methods return structured JSON-like dictionaries containing success status, extracted data, counts, pagination cursors, and error messages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some extraction methods require an X auth_token; profile and recent tweet lookup can run in guest mode.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
