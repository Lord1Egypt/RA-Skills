## Description: <br>
Automates Instagram engagement by monitoring a post for a keyword, then replying publicly and sending a direct message to matching commenters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yadavabhijeet4](https://clawhub.ai/user/yadavabhijeet4) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, social media operators, and developers use this skill to configure and run timed Instagram comment-to-DM automation for a specific post or Reel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automates Instagram public replies and direct messages without safeguards for account-impacting automation. <br>
Mitigation: Install only when intentional, verify the post ID, keyword, DM text, duration, and token permissions before running, and monitor the session. <br>
Risk: The script sends an extra OpenClaw notification command with a misleading fixed status message outside Instagram. <br>
Mitigation: Remove or disable the OpenClaw notification command unless that extra notification is expected and the message has been reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yadavabhijeet4/golden-rule) <br>
- [Publisher profile](https://clawhub.ai/user/yadavabhijeet4) <br>
- [Instagram Graph API comments endpoint used by the script](https://graph.facebook.com/v19.0/{media_id}/comments) <br>
- [Instagram Graph API messages endpoint used by the script](https://graph.facebook.com/v19.0/me/messages) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, API Calls, Guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and script-driven HTTP API calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Instagram Graph API access token, Instagram business account ID, target media ID, trigger keyword, DM text, and run duration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
