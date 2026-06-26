## Description: <br>
Adds a Kazakh input method for OpenClaw and web pages, with English, Arabic-script Kazakh, Cyrillic-script Kazakh, keyboard shortcuts, and a draggable virtual keyboard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ayden76](https://clawhub.ai/user/ayden76) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install and operate a Kazakh IME in the OpenClaw control UI or another web page. It helps users enter Kazakh text in Arabic or Cyrillic script using an English keyboard or the included virtual keyboard. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The IME script changes behavior for text inputs on pages where it is loaded. <br>
Mitigation: Install it only on pages where Kazakh IME behavior is intended, and remove the script tag and copied script file when the IME should no longer be active. <br>
Risk: Incorrect installation paths or missing fonts can prevent the IME or Kazakh characters from displaying as expected. <br>
Mitigation: Confirm the script path in the target HTML and install a Kazakh-capable font such as UKK TZK1 or Microsoft Uighur before relying on the IME. <br>


## Reference(s): <br>
- [OpenClaw Kazakh IME documentation](references/README.md) <br>
- [ClawHub release page](https://clawhub.ai/ayden76/openclaw-kazakh-ime) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline code and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces installation steps, keyboard usage guidance, mapping references, and configuration notes for loading the IME script.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence and artifact documentation) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
