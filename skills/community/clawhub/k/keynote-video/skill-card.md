## Description: <br>
Converts PPT or presentation files into narrated videos through interactive content assessment, LLM-generated scripts, style-aware narration, user confirmation, and automated media synthesis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vincentlau2046-sudo](https://clawhub.ai/user/vincentlau2046-sudo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, trainers, and developers use this skill to turn presentation decks and optional supporting notes into Chinese narrated presentation videos. It guides the agent through input review, script generation, style selection, user approval, video synthesis, and quality checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local media commands with weak argument isolation. <br>
Mitigation: Run it only in a controlled project workspace, review input file paths and video_design_spec.json values before generation, and avoid untrusted filenames or configuration values. <br>
Risk: Narration text derived from presentations may be sent to edge-tts. <br>
Mitigation: Do not use confidential decks unless the edge-tts data flow is acceptable for the content. <br>
Risk: Generated scripts and narration can misrepresent source presentation content. <br>
Mitigation: Keep the documented Phase 2 user confirmation gate and review video_design_spec.md plus representative page scripts before running technical synthesis. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/vincentlau2046-sudo/keynote-video) <br>
- [README](artifact/README.md) <br>
- [Design specification](artifact/DESIGN.md) <br>
- [Skill workflow](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, plain-text narration scripts, JSON video design specifications, shell commands, and generated media files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces project-local working files, rewritten page scripts, video_design_spec.md, video_design_spec.json, MP4 output, and a completion report when the workflow succeeds.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
