## Description: <br>
Drafts precise LinkedIn comment replies from a given comment URL, handling thread structure so replies post under the correct top-level comment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sergebulaev](https://clawhub.ai/user/sergebulaev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and social media operators use this skill to draft and approve concise LinkedIn replies from comment URLs while preserving the correct thread context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can post public LinkedIn reactions and replies when a posting backend is configured. <br>
Mitigation: Review the target comment, reaction, reply text, and parent comment URN before approving any post. <br>
Risk: Configuring posting credentials enables actions on the user's LinkedIn workflow. <br>
Mitigation: Leave posting backends unconfigured when only copy-paste drafts are desired. <br>


## Reference(s): <br>
- [Reply Templates](references/reply-templates.md) <br>
- [Threading Rules](references/threading-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown approval card with short reply drafts, reaction suggestion, thread context, and posting target details.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reply drafts are 150-300 characters; posting requires explicit user approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
