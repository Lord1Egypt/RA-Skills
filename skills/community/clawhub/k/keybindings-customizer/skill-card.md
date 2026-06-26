## Description: <br>
Helps users customize Claude Code keybindings, rebind shortcuts, add chords, or edit `~/.claude/keybindings.json` safely. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wimi321](https://clawhub.ai/user/wimi321) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Claude Code users use this skill to safely update keybinding configuration by merging requested shortcut changes, preserving existing bindings, and explaining conflicts or terminal limitations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A review helper associated with the release can launch a nested Codex review with full local access and approval bypass by default. <br>
Mitigation: Install only if the publisher is trusted; prefer the documented `--no-yolo` or `AUTOREVIEW_YOLO=0` option and require explicit confirmation before running moderation, publishing, or review-helper commands. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [configuration, guidance, text] <br>
**Output Format:** [Markdown with keybinding configuration guidance and conflict explanations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include merged keybinding configuration suggestions for `~/.claude/keybindings.json`.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
