## Description: <br>
Analyze Douyin Creator Marketplace (Xingtu) workflows with JustOneAPI, including creator Profile, creator Link Structure, and creator Visibility Status across 46 operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and analysts use this skill to select and run JustOneAPI endpoints for Douyin Creator Marketplace (Xingtu) creator profile, link structure, visibility, channel metrics, and campaign-planning data. It helps agents ask for missing identifiers, call the smallest matching operation, and summarize decision-relevant API results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API token exposure through pasted commands, full request URLs, screenshots, or logs. <br>
Mitigation: Keep JUST_ONE_API_TOKEN in an environment variable, avoid sharing command logs or full URLs, and rotate the token if it may have been exposed. <br>
Risk: Incorrect creator-marketplace analysis if required identifiers are missing, guessed, or routed to the wrong operation. <br>
Mitigation: Ask for missing required parameters, choose the smallest matching operation from generated/operations.md, and echo key filters such as oAuthorId, acceptCache, kolId, platform, or range in the answer. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/justoneapi-douyin-xingtu) <br>
- [JustOneAPI Homepage](https://api.justoneapi.com) <br>
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu&utm_content=project_link) <br>
- [Operations Reference](generated/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown prose with selected fields, operation IDs, shell command examples, and optional raw JSON payloads.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and a JUST_ONE_API_TOKEN environment variable for authenticated read-only JustOneAPI requests.] <br>

## Skill Version(s): <br>
1.0.9 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
