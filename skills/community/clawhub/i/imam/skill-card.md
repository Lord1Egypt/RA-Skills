## Description:

Virtual Imam that leads the five daily Islamic prayers via voice, delivers Friday Jumu'ah khutbahs, and interacts with mussalis in multiple languages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[almaas21](https://clawhub.ai/user/almaas21)

### License/Terms of Use:


## Use Case:

External users can use this skill to guide Islamic daily prayers, Jumu'ah khutbah flow, adhan, iqamah, and post-prayer adhkar with voice-oriented prompts and multilingual instructions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud or fallback TTS providers may receive generated prayer or sermon text.

Mitigation: Configure a trusted TTS provider intentionally and avoid sending sensitive personal content through provider-backed audio generation.

Risk: Fallback audio examples may require installing and running local playback tools.

Mitigation: Install audio dependencies from trusted sources and avoid running fallback examples with elevated privileges.

Risk: Voice prayer or khutbah guidance could start unexpectedly if the skill is always available.

Mitigation: Prefer explicit invocation and confirm the selected prayer or khutbah mode before beginning voice guidance.

## Reference(s):

- [Salah Steps Reference](references/salah-steps.md)
- [Adhan & Iqamah Text](references/adhan.md)
- [Friday Jumu'ah Khutbah Template](references/khutbah-template.md)
- [Post-Salah Adhkar](references/adhkar-post-salah.md)
- [Multi-Language Support](references/languages.md)
- [Prayer Times Script](scripts/prayer_times.py)
- [Google Cloud Console](https://console.cloud.google.com)
- [ClawHub Skill Page](https://clawhub.ai/almaas21/skills/imam)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and voice-recitation text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call a local prayer-times script and may guide TTS provider configuration.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
