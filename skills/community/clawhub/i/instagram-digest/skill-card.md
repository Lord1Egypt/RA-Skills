## Description: <br>
Scrape recent Instagram reels, transcribe audio, summarize with OpenRouter, and save a digest.html file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sirimaddala99](https://clawhub.ai/user/sirimaddala99) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to collect recent reels from configured Instagram accounts, transcribe reel audio, summarize transcripts with OpenRouter, and produce a local HTML digest for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store a reusable Instagram login session on disk when optional Instagram credentials are used. <br>
Mitigation: Use a throwaway Instagram account when login is needed and delete scripts/.instagram_session.json when finished or when access should be revoked. <br>
Risk: Tracked Instagram content and transcripts are sent to OpenRouter for summarization. <br>
Mitigation: Only track content that is acceptable to send to OpenRouter and avoid using the skill for sensitive accounts or private material. <br>
Risk: The skill runs Python dependencies and browser automation against external services. <br>
Mitigation: Review before installing, run in an isolated Python environment, and pin or lock dependencies before regular use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sirimaddala99/instagram-digest) <br>
- [OpenRouter API endpoint](https://openrouter.ai/api/v1) <br>
- [Instagram profile URL pattern](https://www.instagram.com/{username}/) <br>


## Skill Output: <br>
**Output Type(s):** [text, HTML file, shell commands, configuration] <br>
**Output Format:** [Local digest.html file plus console text and command guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OPENROUTER_API_KEY; optional Instagram credentials can enable login-gated access.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
