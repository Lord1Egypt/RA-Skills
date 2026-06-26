## Description: <br>
Find night markets, food streets, and local culinary hotspots with real-time FlyAI/Fliggy CLI results and booking links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and travel-planning agents use this skill to find night markets, food streets, and street-food hotspots for a city, then return Markdown recommendations with provider booking links from FlyAI/Fliggy CLI output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs the agent to install and run a third-party global npm CLI. <br>
Mitigation: Approve the CLI installation yourself, review @fly-ai/flyai-cli before use, and run it only in an environment where FlyAI/Fliggy provider access is acceptable. <br>
Risk: Booking links and travel results come from FlyAI/Fliggy and may reflect commercial provider availability rather than neutral rankings. <br>
Mitigation: Treat booking links as provider links and independently verify prices, availability, and suitability before purchase. <br>


## Reference(s): <br>
- [ClawHub Night Market Guide release](https://clawhub.ai/xiejinsong/night-market-guide) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with comparison tables, booking links, and FlyAI CLI command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a city name and FlyAI CLI output; recommendations should include detailUrl booking links from the provider results.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
