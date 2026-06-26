## Description: <br>
Send LinkedIn connection requests to a list of people via browser automation and track status in a CSV/TSV file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[10Madh](https://clawhub.ai/user/10Madh) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and operators use this skill to send reviewed LinkedIn connection requests from a spreadsheet or list of profile URLs, then track each person's status in a CSV/TSV file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill operates a logged-in LinkedIn session and can send real connection requests from the user's account. <br>
Mitigation: Use small reviewed batches, confirm recipients or batches before sending, and stop if the account receives platform warnings or reaches LinkedIn limits. <br>
Risk: The workflow uses bulk outreach data that may contain confidential lead lists or personal information. <br>
Mitigation: Avoid confidential lists unless the user has approved their use, keep a backup of the spreadsheet, and review file changes before continuing. <br>
Risk: The artifact includes anti-detection steps for LinkedIn automation. <br>
Mitigation: Do not use the workflow to bypass LinkedIn warnings, limits, or platform rules; pause or stop when the platform signals concern. <br>


## Reference(s): <br>
- [LinkedIn Connect browser workflow](references/browser-workflow.md) <br>
- [ClawHub skill page](https://clawhub.ai/10Madh/linkedin-bulk-connect) <br>
- [Publisher profile](https://clawhub.ai/user/10Madh) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Files] <br>
**Output Format:** [Markdown guidance with inline browser commands, Python snippets, and CSV/TSV or JSON status updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational steps for browser automation and updates tracking files such as the source CSV/TSV and linkedin_progress.json.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
