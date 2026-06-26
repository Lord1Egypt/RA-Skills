## Description: <br>
Generates and edits design-token-based presentation decks with style packs, semantic slide templates, multi-source imports, exports, speaker notes, animation, and critique workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaobod1](https://clawhub.ai/user/zhaobod1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, business users, and developers use this skill to turn prompts, URLs, documents, PDFs, XMind files, or existing decks into styled presentations and related web, image, video, speaker-note, and critique artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PPT prompts, imported documents, slide text, URLs, and speaker-note inputs may be sent to configured third-party AI providers. <br>
Mitigation: Use non-confidential data unless provider settings are controlled; disable remote workflows when needed and review provider configuration before execution. <br>
Risk: The skill requires sensitive credentials for some providers and media workflows. <br>
Mitigation: Store API keys in environment or secret-management controls, limit key scope where possible, and rotate keys after shared or high-risk use. <br>
Risk: Generated files and local caches can contain user-provided or transformed presentation content. <br>
Mitigation: Review output paths and cache locations, and remove generated artifacts that contain confidential or regulated information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhaobod1/huo15-openclaw-ppt) <br>


## Skill Output: <br>
**Output Type(s):** [Files, JSON, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [PPTX, JSON deck specs, HTML, image or video files, Markdown reports, and command-oriented guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some workflows require configured API credentials and may use local output paths or caches.] <br>

## Skill Version(s): <br>
5.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
