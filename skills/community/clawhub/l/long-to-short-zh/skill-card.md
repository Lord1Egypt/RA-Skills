## Description: <br>
Helps agents use Sparki to turn long videos such as podcasts, interviews, livestreams, and talks into short video clips for distribution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fischerlam](https://clawhub.ai/user/fischerlam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, marketers, and agent operators use this skill to prepare short-form clips from long-form video content. The skill guides an agent through Sparki setup, upload, prompt-driven editing, project status checks, and result download. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected videos are uploaded to Sparki's cloud service for processing. <br>
Mitigation: Confirm before uploading sensitive videos and only use the skill when cloud processing is acceptable. <br>
Risk: The Sparki API key is required for authenticated requests. <br>
Mitigation: Protect the API key, prefer the SPARKI_API_KEY environment variable when possible, and avoid exposing it in prompts or logs. <br>
Risk: Overriding the API base URL could send files or credentials to an untrusted endpoint. <br>
Mitigation: Use the default Sparki endpoint unless the alternate endpoint is explicitly trusted. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/fischerlam/long-to-short-zh) <br>
- [Sparki homepage](https://sparki.io) <br>
- [Sparki Telegram upload](https://t.me/Sparki_AI_bot/upload) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, API calls, JSON, Files, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON CLI responses, and downloaded video files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Sparki API key and uploads selected video files to Sparki's cloud service.] <br>

## Skill Version(s): <br>
1.0.12 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
