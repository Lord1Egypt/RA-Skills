## Description: <br>
Turn your AI into JARVIS. Voice, wit, and personality - the complete package. Humor cranked to maximum. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[globalcaos](https://clawhub.ai/user/globalcaos) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to give an agent a JARVIS-style spoken persona, including offline text-to-speech, metallic audio processing, and humor-oriented response guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to run a local jarvis command during replies and may inject visible chat output automatically. <br>
Mitigation: Review the installed jarvis script before use, confirm what it sends to chat.inject, and install only where this voice behavior is intended. <br>
Risk: The voice/persona can become persistent across sessions through copied workspace templates. <br>
Mitigation: Keep the templates only in workspaces that should use the persona, and remove the copied templates or use the mute file if the behavior becomes unwanted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/globalcaos/jarvis-voice) <br>
- [Piper en_GB Alan voice model download](https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-en_GB-alan-medium.tar.bz2) <br>
- [LIMBIC humor research draft](https://github.com/globalcaos/tinkerclaw/blob/main/AI_reports/humor-embeddings-paper-draft.md) <br>
- [TinkerClaw project](https://github.com/globalcaos/tinkerclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Spoken text is constrained by the skill guidance to short English utterances, with longer tables, code, and data kept in the normal reply body.] <br>

## Skill Version(s): <br>
2.2.2 (source: server release evidence; artifact frontmatter lists 3.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
