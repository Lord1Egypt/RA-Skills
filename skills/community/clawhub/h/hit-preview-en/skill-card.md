## Description: <br>
Hit Preview EN analyzes English short-form video scripts for TikTok, YouTube Shorts, and Instagram Reels, using configured AI providers when available and a local fallback when AI is unavailable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[makclaw](https://clawhub.ai/user/makclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, marketers, and production teams use this skill to evaluate short-form drama scripts, estimate hit potential, and receive platform-specific improvement guidance before publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AI mode may send the analyzed script to the configured external AI provider. <br>
Mitigation: For confidential or unpublished scripts, unset provider API key environment variables so the local fallback is used. <br>
Risk: AI mode depends on sensitive provider credentials supplied through environment variables. <br>
Mitigation: Store API keys outside shared scripts and avoid sharing command output that reveals credential prefixes. <br>


## Reference(s): <br>
- [Hit Preview EN ClawHub page](https://clawhub.ai/makclaw/hit-preview-en) <br>
- [Hit Preview web version](https://hit-preview.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown-style English analysis report with scored sections, predictions, and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports TikTok, YouTube, and Snapchat platform options; AI mode can use configured DeepSeek, OpenAI, Anthropic, or Google provider credentials and falls back to local analysis when AI is unavailable.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
