## Description: <br>
Virtual Imam that leads the five daily Islamic prayers via voice, delivers Friday Jumu'ah khutbahs, and interacts with mussalis in multiple languages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[almaas21](https://clawhub.ai/user/almaas21) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to receive voice-guided Islamic prayer support, including salah steps, optional adhan and iqamah, post-prayer adhkar, Friday khutbah flow, and multilingual translations or instructions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad voice triggers may cause the skill to react to prayer-related phrases unexpectedly. <br>
Mitigation: Keep the confirmation step enabled before beginning prayer guidance. <br>
Risk: Text-to-speech setup may require cloud credentials. <br>
Mitigation: Use dedicated TTS credentials with minimal permissions and avoid sharing broader cloud-service credentials. <br>
Risk: Location and local-time context may be used to determine the current prayer. <br>
Mitigation: Use manual prayer selection when location-based or time-based prayer determination is not desired. <br>
Risk: The fallback playback example includes an os.system call. <br>
Mitigation: Do not copy the playback example into production code without replacing it with a safer, reviewed audio playback path. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/almaas21/imam) <br>
- [Adhan and Iqamah text](references/adhan.md) <br>
- [Post-Salah Adhkar](references/adhkar-post-salah.md) <br>
- [Friday Jumu'ah Khutbah Template](references/khutbah-template.md) <br>
- [Multi-Language Support](references/languages.md) <br>
- [Salah Steps Reference](references/salah-steps.md) <br>
- [Prayer times script](scripts/prayer_times.py) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and spoken-response text with inline configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use local time and location inputs for prayer-time selection, and may use text-to-speech credentials when configured.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
