## Description: <br>
Gong API for searching calls, transcripts, and conversation intelligence. Use when working with Gong call recordings, sales conversations, transcripts, meeting data, or conversation analytics. Supports listing calls, fetching transcripts, user management, and activity stats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jdrhyne](https://clawhub.ai/user/jdrhyne) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, sales operations teams, and agent operators use this skill to query Gong users, calls, transcripts, call details, and activity statistics through the Gong API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad Gong credentials can expose sensitive call, transcript, user, and activity data. <br>
Mitigation: Use a dedicated least-privilege Gong API key and limit installation to agents that need access to Gong data. <br>
Risk: The credentials file contains an access key and secret key. <br>
Mitigation: Store ~/.config/gong/credentials.json with restrictive file permissions and avoid sharing it in prompts, logs, or repositories. <br>
Risk: A misconfigured base URL could send credentials or requests to an unintended endpoint. <br>
Mitigation: Confirm the configured base_url points to the official Gong API domain before use. <br>
Risk: Raw call transcripts may contain confidential customer or employee information. <br>
Mitigation: Review transcript outputs before forwarding, storing, or pasting them into systems without appropriate access controls. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jdrhyne/gong) <br>
- [Publisher Profile](https://clawhub.ai/user/jdrhyne) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Gong API request patterns and jq-based summaries for users, calls, transcripts, call details, and activity statistics.] <br>

## Skill Version(s): <br>
1.1.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
