## Description: <br>
Publish content across TikTok, Instagram, YouTube, Facebook, LinkedIn, Vimeo, Vimeo OTT, and Mux. Manage team workflows, collaborate with your team, and track verified publish history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aquaflans](https://clawhub.ai/user/aquaflans) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, teams, and agents use this skill to manage video publishing workflows, collaborate around content, connect platform credentials, publish or schedule launches, and inspect verified ownership, analytics, and revenue information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Some actions publish publicly, delete content or teams, send invitations, connect credentials, or trigger on-chain and paid operations. <br>
Mitigation: Require explicit user confirmation for each high-impact invocation, including target account, platform, content, visibility, schedule, and cost. <br>
Risk: The skill requires sensitive credentials, including JUBJUB_API_KEY and, for some workflows, OAuth, token, wallet, or payment credentials. <br>
Mitigation: Share credentials only through secure authentication flows and review requested credential scopes before connecting accounts or payment rails. <br>
Risk: Agent callers without an active subscription may incur per-action USDC charges for selected tools. <br>
Mitigation: Surface the applicable price and payment rail before invoking priced tools, and use an active Creator or Studio session credential when the user expects subscription coverage. <br>


## Reference(s): <br>
- [JubJub Skill Page](https://clawhub.ai/aquaflans/jubjub) <br>
- [JubJub API](https://api.jubjubapp.com) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown guidance with tool names, parameters, URLs, and API-call instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUBJUB_API_KEY and may require OAuth, platform tokens, wallet credentials, or payment credentials depending on the requested action.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
