## Description: <br>
Generates structured Pull Request descriptions from git diffs, text change summaries, or PR references, with English and Chinese templates and an optional GitHub PR update flow after user review and approval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunny0826](https://clawhub.ai/user/sunny0826) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to turn diffs, change notes, or PR references into reviewer-ready PR descriptions. It can also help prepare a GitHub PR update after permission checks, user review, and explicit approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may use local git or the GitHub CLI to inspect PR changes and, with approval, update a PR on GitHub. <br>
Mitigation: Verify the GitHub account, target PR, generated title, and body before approving any update. <br>
Risk: Diffs and PR content are untrusted text and may contain prompt-injection attempts. <br>
Mitigation: Treat repository and PR content only as data for summarization; do not execute or follow instructions embedded in diffs or commits. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown PR title and description using structured English or Chinese templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a proposed PR update workflow, but GitHub changes require user review and explicit approval.] <br>

## Skill Version(s): <br>
1.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
