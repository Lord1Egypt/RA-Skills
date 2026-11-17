## Description:

Generates AI music, background tracks, and songs from text prompts using IMA Studio models including Suno and DouBao.

This skill is ready for commercial/non-commercial use.

## Publisher:

[allenfancy-gan](https://clawhub.ai/user/allenfancy-gan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content creators use this skill to generate songs, background music, jingles, and soundtrack-style audio from text prompts for media, marketing, social, and prototype workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports that the API base URL can be changed even though credential notes say the IMA_API_KEY is sent only to api.imastudio.com.

Mitigation: Use a fixed or allowlisted api.imastudio.com endpoint before providing IMA_API_KEY, and do not let untrusted instructions set --base-url.

Risk: The security evidence reports inconsistent voice-versus-music descriptions.

Mitigation: Present this release as a music generation skill and confirm user expectations before using it for voiceover or TTS tasks.

Risk: The security guidance recommends dependency pinning before production use.

Mitigation: Pin and review Python dependencies before deploying the skill in production environments.

## Reference(s):

- [IMA homepage](https://www.imaclaw.ai)
- [ClawHub skill page](https://clawhub.ai/allenfancy-gan/skills/ima-voice-ai)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text status messages and optional JSON containing the task ID, audio URL, model, and credit information.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The generated audio is returned as a remote media URL; the skill does not require local downloads for normal use.]

## Skill Version(s):

1.0.14 (source: ClawHub release metadata; artifact frontmatter reports 1.2.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
