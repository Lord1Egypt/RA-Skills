## Description: <br>
Build a personal gift system for tracking ideas, occasions, and gift-giving history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to help an agent maintain local Markdown notes for gift ideas, occasions, gift history, and personal wishlists before suggesting or logging gifts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Gift notes may include personal details about the user or other people in local files. <br>
Mitigation: Avoid storing highly sensitive details, periodically review or delete old entries, and keep the ~/gifts/ folder protected with normal local file permissions. <br>
Risk: Casual remarks could be saved as gift preferences when the user did not intend long-term retention. <br>
Mitigation: Ask the agent to confirm before saving casual remarks when privacy or consent matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/gifts) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/ivangdavila) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown notes and concise conversational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local files under ~/gifts/ when the user asks the agent to store gift details.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
