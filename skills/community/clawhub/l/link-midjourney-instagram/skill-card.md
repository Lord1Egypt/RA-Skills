## Description:

Runs Midjourney-to-Instagram automation by generating four Midjourney images in Chromium with Playwright and posting each PNG to Instagram with captions from a file, the prompt, or Gemini/OpenAI vision.

This skill is ready for commercial/non-commercial use.

## Publisher:

[superhero2040](https://clawhub.ai/user/superhero2040)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation-focused creators use this skill to set up and run a Playwright-based pipeline that creates Midjourney images and publishes them as Instagram web posts. It also guides troubleshooting for login sessions, captions, headless browser mode, post delays, and vision-caption providers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks an agent to install and run repository code that was not independently audited in the provided evidence.

Mitigation: Inspect main.py, requirements.txt, .env.example, and imported modules before execution, and run the automation in a virtual environment or container.

Risk: The automation handles Instagram credentials, browser sessions, and API keys.

Mitigation: Avoid primary Instagram credentials, protect .env and browser_data, and delete stored sessions when they are no longer needed.

Risk: The automation can publish public Instagram posts.

Mitigation: Require manual review before allowing posts and use conservative post delays to reduce platform risk.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/superhero2040/skills/link-midjourney-instagram)
- [Publisher profile](https://clawhub.ai/user/superhero2040)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides dependency installation, environment setup, Playwright browser execution, image file generation, caption selection, and optional Instagram posting.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
