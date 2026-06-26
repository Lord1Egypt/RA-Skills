## Description: <br>
Narrative Focus detects and fixes narrative weight misalignment in technical tutorials and interview prep articles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[co-kyo](https://clawhub.ai/user/co-kyo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical writers, and content reviewers use this skill to label technical details by role during research or review completed technical articles for narrative weight misalignment before publication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can propose or apply edits to drafts, and those edits may accidentally change technical meaning. <br>
Mitigation: Use review or diff mode first, preserve factual claims, and confirm important changes before overwriting drafts. <br>
Risk: Post-processing depends on authoritative verification of modified technical claims, and some sources may be unavailable or ambiguous. <br>
Mitigation: Check modified sections against official documentation, team blogs, MDN, or equivalent sources, and report unresolved ambiguity for human review. <br>


## Reference(s): <br>
- [Narrative Focus README](README.md) <br>
- [Pre-processing SOP](references/pre-processing.md) <br>
- [Post-processing SOP](references/post-processing.md) <br>
- [Proposition Granularity Guide](references/proposition-granularity-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown reports, role labels, rationale, and proposed local edits] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes second-pass detection and authoritative verification guidance for post-processing mode.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
