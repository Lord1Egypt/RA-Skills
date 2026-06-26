## Description: <br>
Fetches Hong Kong Jockey Club race cards with horse details, odds, and recommended picks per race, including date selection, class filtering, exclusions, single-race fetch, advanced scoring, and enhanced form analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stevenho1394](https://clawhub.ai/user/stevenho1394) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to fetch public Hong Kong horse-racing race-card data, inspect horse details and odds, and generate informational recommended picks with reasoning. Betting decisions should be verified independently against official race and odds sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an unofficial HKJC API package, so race data, odds, or availability may be incomplete, delayed, or unavailable. <br>
Mitigation: Verify race cards, odds, dividends, and official results against authoritative sources before relying on the output. <br>
Risk: The skill produces gambling-related recommendations that could be mistaken for financial or betting advice. <br>
Mitigation: Treat recommendations as informational analysis only and ensure users comply with applicable betting laws and responsible gambling practices. <br>
Risk: Advanced scoring and form analysis use heuristics, and place odds may be estimated when live data is missing. <br>
Mitigation: Review the reasoning and scoring settings before use, and compare recommendations against independent data or human judgment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/stevenho1394/hk-horse-racing) <br>
- [hkjc-api npm package](https://registry.npmjs.org/hkjc-api/-/hkjc-api-1.0.3.tgz) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Guidance] <br>
**Output Format:** [JSON object with meeting details, race entries, odds, recommendations, estimated win probabilities, and reasoning] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [English output; recommendations depend on available HKJC data, odds, and scoring settings.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
