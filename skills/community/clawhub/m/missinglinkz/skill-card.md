## Description: <br>
MissingLinkz helps AI agents build UTM-tracked campaign links, validate destinations, and inspect landing pages for social sharing readiness in a single preflight workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andrewlamamills-tech](https://clawhub.ai/user/andrewlamamills-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing teams, developers, and AI agents use MissingLinkz before publishing or promoting URLs to create consistent UTM links, validate destinations, and check landing-page share readiness. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a MissingLinkz API key for account, storage, and campaign-management features. <br>
Mitigation: Treat MLZ_API_KEY as a secret, prefer environment variables or restricted config-file permissions, and avoid committing local configuration files. <br>
Risk: Checked URLs and campaign metadata may be sent through the MissingLinkz package or service. <br>
Mitigation: Avoid checking private, localhost, signed, or pre-release URLs unless sharing that URL and campaign metadata is acceptable. <br>
Risk: Use depends on trust in the MissingLinkz npm package and service. <br>
Mitigation: Install only when the package and service are trusted, and review generated preflight results before publishing or spending on campaigns. <br>


## Reference(s): <br>
- [MissingLinkz homepage](https://missinglinkz.io) <br>
- [ClawHub skill page](https://clawhub.ai/andrewlamamills-tech/missinglinkz) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and structured JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require MLZ_API_KEY for account, storage, and campaign-management features; offline UTM generation can run without an API key.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
