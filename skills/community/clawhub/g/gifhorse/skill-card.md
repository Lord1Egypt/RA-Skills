## Description: <br>
Search video dialogue and create reaction GIFs with timed subtitles from movie and TV video libraries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Coyote-git](https://clawhub.ai/user/Coyote-git) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use GifHorse to transcribe local video libraries, search dialogue, preview clips, and create subtitled reaction GIFs or meme GIFs from selected quotes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and uses an external GifHorse CLI from a third-party GitHub repository. <br>
Mitigation: Install only after trusting the external repository and reviewing the installed CLI behavior. <br>
Risk: GifHorse processes selected local video folders and stores dialogue transcriptions in a local database. <br>
Mitigation: Run it only on video folders you choose and keep GIFHORSE_DB in a location you control. <br>
Risk: Default transcription can download subtitles from online providers. <br>
Mitigation: Use --use-subtitles for local subtitle files or --use-whisper when you do not want default online subtitle lookup. <br>
Risk: The create command can optionally send GIFs through iMessage. <br>
Mitigation: Confirm the configured recipient before using --send or --send-to. <br>


## Reference(s): <br>
- [GifHorse ClawHub Page](https://clawhub.ai/Coyote-git/gifhorse) <br>
- [GifHorse GitHub Repository](https://github.com/Coyote-git/gifhorse) <br>
- [GifHorse Usage Guide](https://github.com/Coyote-git/gifhorse/blob/main/USAGE_GUIDE.md) <br>
- [GifHorse Roadmap](https://github.com/Coyote-git/gifhorse/blob/main/ROADMAP.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown with inline shell commands and CLI arguments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can generate GIF files through the external gifhorse CLI, update a local transcription database, and optionally send GIFs through iMessage.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
