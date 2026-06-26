## Description: <br>
Analyzes short-drama scripts for hook strength, episode-ending suspense, similarity to hit shorts, viral potential, simulated audience comments, emotion heatmaps, and platform-specific recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[makclaw](https://clawhub.ai/user/makclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, marketers, and development teams use this skill to evaluate short-drama scripts, estimate audience response, and generate optimization guidance for platforms such as Douyin, Bilibili, Kuaishou, and Xiaohongshu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read local OpenClaw model configuration or AI API environment variables. <br>
Mitigation: Use a limited API key or profile and review the configured provider before running the skill. <br>
Risk: Script text may be sent to the configured external AI provider for analysis. <br>
Mitigation: Avoid confidential or unreleased scripts unless the selected provider and account are approved for that content. <br>
Risk: The security scan reports inconsistent package or runtime metadata. <br>
Mitigation: Inspect the release files before production use and prefer a corrected release when available. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/makclaw/hit-preview) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown or plain-text analysis with scores, simulated audience comments, heatmaps, and platform recommendations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use the configured OpenClaw AI provider when available and fall back to local analysis when AI access is unavailable.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter, package.json, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
