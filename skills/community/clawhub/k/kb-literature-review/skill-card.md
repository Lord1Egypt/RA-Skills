## Description: <br>
Produce a focused literature/knowledge review using only selected Research KB contents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[myd2002](https://clawhub.ai/user/myd2002) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge-base users use this skill to synthesize selected personal or team Research KB repositories into source-grounded literature reviews, method comparisons, thematic surveys, and research-gap analyses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can write generated review pages into a selected repository by default. <br>
Mitigation: Require explicit user confirmation before writes and consider setting writeReview to false by default. <br>
Risk: The skill uses a Gitea admin token for repository access. <br>
Mitigation: Use a narrowly scoped bot token with only the repository permissions needed for the selected task. <br>
Risk: Unpinned dependencies may change behavior across installations. <br>
Mitigation: Pin production dependencies and review updates before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/myd2002/skills/kb-literature-review) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Sample literature review task](artifact/tests/sample_literature_review_task.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, files] <br>
**Output Format:** [JSON result containing a concise answer, citations, read page traceability, and an optional generated Markdown review path.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write a Markdown review page to reviews/<topic>-专项综述.md when writeReview is enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
