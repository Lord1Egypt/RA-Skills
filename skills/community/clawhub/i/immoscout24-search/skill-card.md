## Description: <br>
Searches German ImmoScout24 real estate listings through the ImmoScout24 mobile API and retrieves listing or expose details such as price, rooms, heating, energy, parking, condition, and location. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mihaimacarie98](https://clawhub.ai/user/mihaimacarie98) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to search German residential real estate listings, fetch expose details, and assemble property reports with listing URLs, prices, location data, and property attributes. <br>

### Deployment Geography for Use: <br>
Global, for searches of German ImmoScout24 listings. <br>

## Known Risks and Mitigations: <br>
Risk: The skill is a third-party scraping and search helper that evidence says may bypass anti-bot controls. <br>
Mitigation: Use it only where ImmoScout24 access is permitted and do not deploy it in environments that prohibit bypassing access controls. <br>
Risk: The security guidance says activation is not scoped narrowly enough and external network access is not clearly declared. <br>
Mitigation: Restrict use to explicit ImmoScout24 requests and approve network access to api.mobile.immobilienscout24.de before execution. <br>
Risk: The artifact includes package installation guidance that can modify the system Python environment. <br>
Mitigation: Install dependencies in an isolated virtual environment and review the package before running the skill. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/mihaimacarie98/immoscout24-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; script output is text or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search requires a region for listing queries; expose lookup requires an expose ID; network calls target the ImmoScout24 mobile API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
