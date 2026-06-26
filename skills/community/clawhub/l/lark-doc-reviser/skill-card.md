## Description: <br>
Read unresolved comments in a Feishu (Lark) document and apply targeted block-level edits based on those comments using an authenticated lark-cli account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[billzhuang6569](https://clawhub.ai/user/billzhuang6569) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and document editors use this skill to inspect unresolved Feishu/Lark document comments, prepare block-level text patches, apply edits, resolve addressed comments, and refresh document state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify live Feishu/Lark documents and resolve comments through an authenticated lark-cli account. <br>
Mitigation: Review fetched comments and generated patch JSON, verify the document token, and confirm before applying edits or resolving comments. <br>
Risk: Fetched document state may contain sensitive document content saved locally. <br>
Mitigation: Store state only in the intended workspace and delete state files when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill release: lark-doc-reviser](https://clawhub.ai/billzhuang6569/lark-doc-reviser) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, JSON, Files] <br>
**Output Format:** [Markdown instructions with bash commands and JSON patch files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires authenticated lark-cli access; may write document state JSON in the workspace and update live Feishu/Lark document blocks.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
