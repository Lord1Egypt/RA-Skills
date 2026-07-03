## Description: <br>
Automatically generate AI videos on Google Flow (labs.google/fx/tools/flow) via Chrome CDP. Supports 16:9 aspect ratio, 10s duration, auto-download MP4. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hitjcl](https://clawhub.ai/user/hitjcl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to automate a logged-in Chrome session for generating Google Flow videos from prompt text and saving the resulting media locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill controls a logged-in Chrome session through CDP. <br>
Mitigation: Use a dedicated temporary Chrome profile, keep only Google Flow open, and close Chrome after the run. <br>
Risk: The automation can confirm credit-consuming Google Flow actions. <br>
Mitigation: Run it only on an account where automatic credit use is acceptable, and prefer one-video runs before batch use. <br>
Risk: Screenshots and generated media may be written to /tmp or configured output folders. <br>
Mitigation: Review and delete temporary screenshots and output files after use. <br>


## Reference(s): <br>
- [Google Flow](https://labs.google/fx/tools/flow) <br>
- [ClawHub skill page](https://clawhub.ai/hitjcl/google-flow-video-automation) <br>
- [Publisher profile](https://clawhub.ai/user/hitjcl) <br>
- [QUICKSTART.md](artifact/QUICKSTART.md) <br>
- [prompts-example.txt](artifact/examples/prompts-example.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration, and downloaded media files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates one or more Google Flow video outputs from prompt text; default scripts save MP4 media to a configured output directory when download succeeds.] <br>

## Skill Version(s): <br>
1.1.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
