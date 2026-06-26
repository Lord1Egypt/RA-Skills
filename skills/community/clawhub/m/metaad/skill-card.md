## Description: <br>
This skill automates the creation of Meta (Facebook/Instagram) ads using the Marketing API, including campaign setup, audience targeting, media upload, and ad creation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zine1993](https://clawhub.ai/user/Zine1993) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, marketers, and advertising operators use this skill to create Meta ad campaigns, ad sets, creatives, and ads programmatically through the Marketing API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store Meta access tokens and advertising account details in a local configuration file. <br>
Mitigation: Use the least-privileged token available, protect the local credential file, rotate credentials when finished, and delete credentials that are no longer needed. <br>
Risk: The skill can create paid advertising campaigns, ad sets, creatives, and ads through the Meta Marketing API. <br>
Mitigation: Keep created ads paused until intentionally reviewed and activated, and verify budgets, targeting, creative content, and destination links before running scripts. <br>


## Reference(s): <br>
- [Meta Marketing API documentation](https://developers.facebook.com/docs/marketing-api/) <br>
- [Meta Marketing API limits](https://developers.facebook.com/docs/marketing-api/overview/limits) <br>
- [Meta audience targeting reference](https://developers.facebook.com/docs/marketing-api/audiences/reference/targeting) <br>
- [Meta Marketing API reference](references/meta_api.md) <br>
- [ClawHub skill page](https://clawhub.ai/Zine1993/metaad) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, Python examples, and JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local configuration files and paid Meta advertising objects when executed with valid credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
