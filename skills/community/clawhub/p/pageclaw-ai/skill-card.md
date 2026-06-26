## Description: <br>
AI skills for managing Facebook business pages, including auto-reply, content posting, bookings, reviews, and lead capture across 9 industries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[proship1](https://clawhub.ai/user/proship1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External business operators and their agents use PageClaw to manage Facebook page conversations, posts, reviews, analytics, bookings, and lead capture through configured page credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Facebook page token can allow access to page messages, reviews, insights, and posting or reply capabilities. <br>
Mitigation: Use the least-privileged page token available, keep it private, and install only when the publisher and connected PageClaw/OneChat workflow are trusted. <br>
Risk: Public posts, customer replies, booking-related responses, or lead-handling actions can affect customers and the business page. <br>
Mitigation: Require explicit user approval before publishing posts, sending replies, handling bookings, or taking lead-related actions. <br>


## Reference(s): <br>
- [PageClaw ClawHub Release](https://clawhub.ai/proship1/pageclaw-ai) <br>
- [PageClaw Homepage](https://pageclaw.onechat.ai) <br>
- [OneChat.ai](https://onechat.ai) <br>
- [Meta Graph API](https://graph.facebook.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Markdown guidance with REST API call examples and environment variable configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PAGECLAW_PAGE_ID, PAGECLAW_PAGE_TOKEN, and PAGECLAW_NICHE environment variables. Public posts, customer replies, booking-related responses, and lead-handling actions should require explicit user approval.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
