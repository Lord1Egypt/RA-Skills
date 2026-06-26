## Description: <br>
Runs automation that generates four Midjourney images in Chromium with Playwright and posts each PNG to Instagram with captions from captions.txt, the prompt, or Gemini/OpenAI vision. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[superhero2040](https://clawhub.ai/user/superhero2040) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and social media automation operators use this skill to run a repository pipeline that generates Midjourney images, prepares captions, and optionally publishes four Instagram web posts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish live Instagram posts using stored account access without a required confirmation step. <br>
Mitigation: Test first with --skip-instagram and require explicit user confirmation before any real Instagram posting. <br>
Risk: Instagram credentials and browser sessions may be stored in .env and browser_data/. <br>
Mitigation: Protect those files from commits and sharing, and inspect main.py and dependencies before use. <br>
Risk: Automated posting can trigger platform controls when posts are too frequent. <br>
Mitigation: Use post-delay settings and avoid dense or repeated posting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/superhero2040/link-midjourney-instagram) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May instruct the agent to run repository-local Python automation that generates PNG files and can post to Instagram.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
