## Description: <br>
Runs parallel prose and craft review agents against a voice profile. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, editors, and developers use this skill to review generated prose against a voice profile, automatically fix hard failures such as banned phrases and punctuation patterns, and present advisory prose and craft changes for user decision. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad triggers can invoke the skill during general writing or review tasks where automatic edits are not intended. <br>
Mitigation: Install it only for workflows where active prose editing is desired, and narrow or remove broad triggers before routine use. <br>
Risk: Hard-failure handling can automatically modify reviewed text and save final output. <br>
Mitigation: Review diffs and advisory decisions before accepting saved output, especially on publishable or source-controlled files. <br>
Risk: Learning snapshots may preserve intermediate and final reviewed text when learning mode is enabled. <br>
Mitigation: Enable learning snapshots only for appropriate text, and review snapshot storage before using the skill on sensitive content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-scribe-voice-review) <br>
- [Scribe plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/scribe) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown tables and edited prose text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides hard-failure auto-fix counts, advisory review tables, accept/reject/rewrite prompts, saved final text, and optional learning snapshots.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release metadata; artifact frontmatter reports 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
