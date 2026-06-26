## Description: <br>
Analyze ad material videos and produce a markdown report with framework, material traits, acquisition keywords, new material production frameworks, and detailed storyboard tables. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fevolq](https://clawhub.ai/user/fevolq) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, marketers, and creative operators use this skill to analyze local ad video assets, identify reusable creative patterns, and generate markdown storyboard guidance for new performance-ad material. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local ad videos and extracted frame images may contain sensitive material. <br>
Mitigation: Use only videos suitable for local analysis and run the skill from a directory where generated frame images are acceptable. <br>
Risk: Unsafe shell construction around video paths could expose command-injection risk when invoking ffmpeg. <br>
Mitigation: Invoke ffmpeg with the video path as a file argument rather than interpolating raw shell text. <br>


## Reference(s): <br>
- [Report template](artifact/references/report_template.md) <br>
- [Material Report on ClawHub](https://clawhub.ai/fevolq/material-report) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, Shell commands, Files] <br>
**Output Format:** [Markdown report with storyboard tables and optional local frame image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use ffmpeg to extract frames from a user-provided local video path before producing the report.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
