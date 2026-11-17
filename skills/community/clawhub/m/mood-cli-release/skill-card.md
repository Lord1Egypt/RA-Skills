## Description:

Mood CLI analyzes Chinese or English mood text with a DeepSeek-backed CLI and returns a weather icon, emotion label, confidence score, and supportive copy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wanwan2qq](https://clawhub.ai/user/wanwan2qq)

### License/Terms of Use:

MIT-0

## Use Case:

End users and agent builders use this skill to trigger mood analysis from chat phrases such as mood, 心情, or 情绪, then convert short mood text into a weather-themed emotional summary. It is intended for lightweight self-reflection and agent responses, not clinical or medical assessment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mood-related text may be sent to DeepSeek and could include sensitive personal information.

Mitigation: Avoid submitting highly sensitive personal or mental-health details until the CLI's privacy and retention behavior has been reviewed.

Risk: The install path uses a globally installed npm package that has not been independently reviewed in the supplied evidence.

Mitigation: Prefer a pinned, locally installed, fully reviewed CLI implementation before deployment.

Risk: Broad chat triggers can invoke the CLI unexpectedly.

Mitigation: Confirm trigger behavior in the target agent environment and keep users informed when mood text will be analyzed externally.

Risk: The DeepSeek API key is stored in an environment variable or user-level configuration file.

Mitigation: Restrict API-key file permissions and rotate the key if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wanwan2qq/skills/mood-cli-release)
- [Artifact README](artifact/README.md)
- [Artifact SKILL.md](artifact/SKILL.md)
- [npm package: mood-weather-cli](https://www.npmjs.com/package/mood-weather-cli)
- [DeepSeek platform](https://platform.deepseek.com/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text with a weather icon, emotion label, confidence score, and short supportive copy; may also return CLI help or health-check guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the mood CLI binary and a DEEPSEEK_API_KEY value.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, CHANGELOG.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
