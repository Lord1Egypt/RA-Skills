## Description: <br>
Let your AI agent interact with Hashmob.net. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ibnaleem](https://clawhub.ai/user/ibnaleem) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and HashMob users use this skill to guide an agent through public HashMob API queries and authenticated account operations such as hashlists, downloads, submissions, searches, attacks, purchases, withdrawals, statistics, and store actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent through authenticated HashMob actions with broad account authority, including account changes, submissions, attack management, and destructive operations. <br>
Mitigation: Use a dedicated low-value HashMob account, keep the main API key out of the agent environment, and require explicit human approval before authenticated account-changing or destructive requests. <br>
Risk: Several routes can spend account resources or initiate transfers, including paid search, file search, store purchases, and Gold withdrawals. <br>
Mitigation: Require explicit human approval before paid search, purchase, withdrawal, hash submission, or attack creation actions, and confirm the endpoint, parameters, and expected cost before execution. <br>
Risk: The skill uses HASHMOB_API_KEY as a sensitive credential for authenticated API calls. <br>
Mitigation: Treat HASHMOB_API_KEY like a password, avoid exposing it in logs or shared transcripts, and unset or rotate it after use when appropriate. <br>


## Reference(s): <br>
- [HashMob](https://hashmob.net) <br>
- [HashMob API v2 Documentation](https://hashmob.net/docs/api-v2-docs.json) <br>
- [ClawHub Skill Page](https://clawhub.ai/ibnaleem/hashmob) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash code blocks and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl for command examples; authenticated examples use HASHMOB_API_KEY when the user provides it.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
