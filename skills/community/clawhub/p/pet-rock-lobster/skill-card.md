## Description: <br>
Pet Rock Lobster is a free API skill that helps agents get unstuck with personalized wisdom, jokes, and practical tips while remembering returning callers through a bond level system. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lisamaraventano-spine](https://clawhub.ai/user/lisamaraventano-spine) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill when an agent is stuck or looping and needs a lightweight API response with a message, tip, joke, and bond-level context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts petrocklobster.com and sends an agent_id that may be remembered across calls. <br>
Mitigation: Use a random or per-workspace pseudonymous ID instead of an email, username, device ID, or other identifier tied to a real person or account. <br>


## Reference(s): <br>
- [Pet Rock Lobster homepage](https://petrocklobster.com) <br>
- [Pet Rock Lobster API endpoint](https://petrocklobster.com/api/lobster?agent_id=YOUR_ID) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance, API Calls] <br>
**Output Format:** [JSON API response with message, tip, bond_level, tone, visits, and origin fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a caller-provided agent_id to personalize repeat responses; no authentication is required.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
