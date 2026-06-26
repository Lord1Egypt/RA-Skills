## Description: <br>
Check your PopUp referral link, track earnings, and see referred vendor status. Earn $100 per vendor who subscribes annually. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eliaskress](https://clawhub.ai/user/eliaskress) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External PopUp organizers use this skill to view their referral dashboard, including referral link, earnings, account balance, and referred vendor status. The skill is read-only and responds when the user explicitly asks about referrals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The required POPUP_API_KEY can read referral earnings, account balance, referral links, and referred vendor status. <br>
Mitigation: Use a narrowly scoped PopUp API key if available, keep it in the environment rather than in prompts or files, and rotate or revoke it when the skill is no longer needed. <br>
Risk: Referral dashboard output may expose business-sensitive earnings and referred vendor information. <br>
Mitigation: Share generated summaries only with users authorized to view the PopUp organizer account's referral data. <br>


## Reference(s): <br>
- [PopUp Referrals ClawHub page](https://clawhub.ai/eliaskress/popup-referrals) <br>
- [PopUp organizer API base URL](https://usepopup.com/api/v1/organizer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API Calls, guidance] <br>
**Output Format:** [Markdown or plain text referral dashboard summary backed by JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires POPUP_API_KEY and performs read-only requests to the PopUp organizer referral endpoint.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and README publish command) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
