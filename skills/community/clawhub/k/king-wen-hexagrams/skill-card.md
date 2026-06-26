## Description: <br>
以文王六十四卦为根本，依用户所问定卦、排卦、解卦，并以庄重克制的口吻给出趋势判断、风险提醒与行止建议。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wjp-cn](https://clawhub.ai/user/wjp-cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to run a King Wen hexagram workflow for first-run profile setup, question framing, hexagram lookup, divination-style interpretation, daily fortune prompts, and follow-up guidance. It is intended as reflective guidance and does not replace professional advice for high-risk medical, legal, financial, or safety decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can save optional profile details such as lunar birthday, gender, birth hour, and daily fortune timing to local state. <br>
Mitigation: Install only if local storage of those details is acceptable; use the provided state script to inspect or clear saved data. <br>
Risk: Suggested scheduled reminders can include profile details in the scheduled task message. <br>
Mitigation: Review generated cron commands before adding them and remove profile details from the message when they are not needed. <br>
Risk: Hexagram readings may be mistaken for deterministic advice in high-risk decisions. <br>
Mitigation: Treat outputs as reflective guidance and rely on qualified professional advice for medical, legal, financial, or safety-critical matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wjp-cn/king-wen-hexagrams) <br>
- [README](artifact/README.md) <br>
- [Usage guide](artifact/guide.md) <br>
- [Daily fortune and scheduled task guidance](artifact/daily-fortune.md) <br>
- [Onboarding guidance](artifact/onboarding.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include structured reading sections, clarification prompts, profile setup prompts, and scheduled task examples.] <br>

## Skill Version(s): <br>
1.1.0 (source: evidence.release.version, artifact/package.json, artifact/skill.json, artifact/README.md, artifact/CHANGELOG.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
