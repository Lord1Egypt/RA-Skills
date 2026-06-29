## Description: <br>
Improves a voice profile by learning from manual edits after generated text is edited, refining registers and reducing voice drift over time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and writers use this skill after manual edits to generated text to identify recurring voice patterns, maintain a local learning accumulator, and propose updates to voice-profile rules for user approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Writing samples and edit history may be stored locally in the voice-profile learning directory. <br>
Mitigation: Use the skill only on material appropriate for local retention, manage local access to the profile directory, and delete or archive snapshots when they are no longer needed. <br>
Risk: Broad trigger terms may cause the skill to be invoked when the user did not intend to run the learning workflow. <br>
Mitigation: Invoke the skill deliberately and review its proposed changes before allowing any profile updates. <br>
Risk: Weak or one-off edit patterns could overfit the voice profile and reduce future output quality. <br>
Mitigation: Keep the documented evidence thresholds and user-approval step before modifying register or craft rules. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-scribe-voice-learn) <br>
- [Plugin homepage from ClawHub metadata](https://github.com/athola/claude-night-market/tree/master/plugins/scribe) <br>
- [Pattern analysis module](modules/pattern-analysis.md) <br>
- [Snapshot management module](modules/snapshot-management.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces proposed profile-rule edits and accumulator updates for user review; may read and write local snapshot and profile files when used.] <br>

## Skill Version(s): <br>
1.9.13 (source: ClawHub release evidence; artifact frontmatter reports 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
