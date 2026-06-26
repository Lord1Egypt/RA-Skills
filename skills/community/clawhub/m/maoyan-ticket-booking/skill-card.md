## Description: <br>
猫眼电影票购票助手帮助用户通过猫眼查询影片、影院和场次，查看座位、创建订单、获取支付链接并查询出票状态。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maoyan-tech](https://clawhub.ai/user/maoyan-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to complete a guided Maoyan movie-ticket purchase flow, from movie and cinema discovery through seat selection, order creation, payment handoff, and ticket-status checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create Maoyan ticket orders and pass payment links to the user. <br>
Mitigation: Review the selected movie, cinema, showtime, seats, ticket count, and payment recipient before proceeding with payment. <br>
Risk: The skill stores a short-lived Maoyan session token locally. <br>
Mitigation: Use only trusted environments, rely on the skill's token-expiry behavior, and clear the stored AuthKey when account access should be revoked. <br>
Risk: Login and payment QR links may be sent through the current chat channel. <br>
Mitigation: Confirm the channel and recipient before sending links, and avoid forwarding authentication or payment links to unintended recipients. <br>
Risk: The skill shares location, account, movie, cinema, seat, order, and ticket-status data with Maoyan services. <br>
Mitigation: Use the skill only when that data sharing is acceptable for the user and deployment context. <br>


## Reference(s): <br>
- [Scripts API Reference](references/scripts-api.md) <br>
- [Error Codes Reference](references/error-codes.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/maoyan-tech/maoyan-ticket-booking) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance] <br>
**Output Format:** [Conversational Markdown with tables, command-backed JSON exchanges, payment or login links, and QR handoff guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May store a short-lived Maoyan session token locally and may create purchase orders after user confirmation.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
