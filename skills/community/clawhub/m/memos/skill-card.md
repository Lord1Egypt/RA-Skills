## Description: <br>
Manage memos via the Memos API: create, retrieve, delete, and list memos with visibility and pagination support, requiring MEMOS_URL and MEMOS_TOKEN. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fty4](https://clawhub.ai/user/fty4) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and personal knowledge-base users use this skill to let an agent create, retrieve, list, and delete memos in a configured Memos account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses MEMOS_TOKEN to access the user's Memos account. <br>
Mitigation: Use a dedicated or least-privilege token where possible, keep the token out of prompts and public files, and rotate it if exposed. <br>
Risk: Create commands can publish memo content publicly unless a more restrictive visibility is selected. <br>
Mitigation: Use PRIVATE or PROTECTED visibility for sensitive memos before creating them. <br>
Risk: Delete and force-delete commands can remove the wrong memo if an incorrect ID is supplied. <br>
Mitigation: Double-check memo IDs before delete operations, especially when using force-delete. <br>


## Reference(s): <br>
- [Memos API documentation](https://usememos.com/docs/api) <br>
- [ClawHub Memos skill](https://clawhub.ai/fty4/memos) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MEMOS_URL and MEMOS_TOKEN environment variables; command results are JSON on success and JSON error messages on stderr.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
