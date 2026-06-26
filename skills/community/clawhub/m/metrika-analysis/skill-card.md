## Description: <br>
Analyzes Yandex.Metrika API data when a user asks about site traffic, conversions, visitor behavior, or site reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nimblemarketingapex-netizen](https://clawhub.ai/user/nimblemarketingapex-netizen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and site operators use this skill to retrieve and interpret Yandex.Metrika metrics such as visits, bounce rate, conversion performance, traffic sources, and weak points in a conversion funnel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on Yandex.Metrika credentials and counter identifiers to read analytics data. <br>
Mitigation: Use a read-only or least-privilege token, confirm ambiguous analytics requests before using credentials, and rotate the token when it is no longer needed. <br>
Risk: Analytics interpretation can produce misleading recommendations if the requested metric, time range, or counter is ambiguous. <br>
Mitigation: Ask clarifying questions before analysis and present findings as hypotheses when the supporting data is incomplete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nimblemarketingapex-netizen/metrika-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown analysis with concise recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference Yandex.Metrika metrics retrieved with METRIKA_TOKEN and COUNTER_ID.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
