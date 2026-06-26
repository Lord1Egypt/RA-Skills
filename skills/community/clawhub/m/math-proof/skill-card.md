## Description: <br>
Automated step-by-step proof generation and review for user-submitted theorems with iterative refinement until acceptance or retry limit is reached. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaoyu20011021-hub](https://clawhub.ai/user/xiaoyu20011021-hub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, students, and mathematical writers use this skill to ask an agent to draft a proof, have a second agent review it for logical gaps and constraint violations, and iterate until accepted or stopped. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional reference files may expose sensitive or unrelated local content to spawned proof and review agents. <br>
Mitigation: Use specific non-sensitive files as references and avoid whole folders, credentials, private notes, or unrelated documents. <br>
Risk: The generated proof may still contain mathematical errors if the review loop accepts an invalid argument. <br>
Mitigation: Treat final proofs as drafts for human mathematical review, especially for high-stakes or publication use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiaoyu20011021-hub/math-proof) <br>
- [Publisher profile](https://clawhub.ai/user/xiaoyu20011021-hub) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown proof text with round-by-round status and review feedback] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include LaTeX-formatted mathematical notation and concise revision summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
