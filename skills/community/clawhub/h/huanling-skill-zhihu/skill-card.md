## Description: <br>
Huanling Skill Zhihu helps readers discuss AI灵魂的边界, prepare reader interviews, draft chapter release notes, and stay within the book's stated conversation boundaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ai-innopower](https://clawhub.ai/user/ai-innopower) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External readers and content creators use this skill to converse about AI灵魂的边界, generate interview questions and follow-ups, and produce short Zhihu-oriented chapter announcements. The skill is intentionally narrow and refuses unrelated general-assistant tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The onboarding and persona flow asks about reading status, relationship to AI, emotional state, and other personal signals. <br>
Mitigation: Review the onboarding before installation, avoid sharing sensitive personal information, and keep persona matching limited to the active conversation. <br>
Risk: Voice support may install a Python package and use a third-party TTS service despite local-only wording. <br>
Mitigation: Skip or disable voice setup unless the data flow is acceptable, and review package installation commands before running them. <br>
Risk: The security review verdict is suspicious due to under-disclosed profiling and voice-related environment changes. <br>
Mitigation: Install only after reviewing the security guidance and artifact behavior, especially in managed or privacy-sensitive environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ai-innopower/skills/huanling-skill-zhihu) <br>
- [Publisher profile](https://clawhub.ai/user/ai-innopower) <br>
- [Installation instructions](artifact/焕灵Skill-知乎内测版-安装说明.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text responses with optional inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Short Chinese prose for normal replies; optional voice setup may configure a local voice preference file and generate audio through edge-tts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
