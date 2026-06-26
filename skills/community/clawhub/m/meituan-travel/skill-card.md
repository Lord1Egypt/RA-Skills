## Description: <br>
Meituan Travel helps an agent query Meituan travel services for hotels, flights, trains, attraction tickets, discounts, price comparison, and itinerary planning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[meituan-travel-ai](https://clawhub.ai/user/meituan-travel-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-support agents use this skill to answer travel planning and booking-related queries against Meituan travel services, including hotels, flights, trains, attraction tickets, discounts, and itinerary options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends travel queries to Meituan's external travel service using a Meituan token. <br>
Mitigation: Install only when that external service use is acceptable, scope and protect the token, and avoid sending secrets, passport numbers, payment details, or unrelated private context. <br>
Risk: The skill depends on an npm package invoked through npx or a global install. <br>
Mitigation: Pin or review the npm package before production use, and confirm requests go to the documented Meituan endpoint. <br>
Risk: Returned travel content may include links, marketing text, pricing, or other external service output. <br>
Mitigation: Preserve booking links needed by users, but apply product policy review or filtering before displaying content in higher-risk user experiences. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/meituan-travel-ai/meituan-travel) <br>
- [Meituan developer site](https://developer.meituan.com) <br>
- [Meituan API token documentation](https://developer.meituan.com/zh/v2/dev/token) <br>
- [Meituan travel service endpoint](https://mcp-open-cater.meituan.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown travel results by default, with optional raw JSON when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MEITUAN_HT_TOKEN; MEITUAN_RAW_JSON can request raw JSON output; npx is required for command execution.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
