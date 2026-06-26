## Description: <br>
Diagnoses sudden performance drops in Meta Ads campaigns when CTR, ROAS, or conversions decline without an obvious cause. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elias-didoo](https://clawhub.ai/user/elias-didoo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing operators, analysts, and agents use this skill to diagnose week-over-week Meta Ads performance drops, identify likely root causes from campaign metrics, and produce a concise recovery plan for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Meta access token and ad account identifier, giving the agent read-only visibility into campaign performance data for the specified account. <br>
Mitigation: Use the narrow ads_read scope, avoid broader Meta permissions, and install only for ad accounts the user intends the agent to inspect. <br>
Risk: Recovery-plan language may include pause, scale-down, refresh, or budget-shift recommendations that could affect ad spend if applied directly. <br>
Mitigation: Treat recovery-plan output as guidance for review and confirm any changes in Meta Ads Manager before execution. <br>
Risk: The skill hands off action recommendations to a separate Meta Ads recommendation workflow, which may be confused with diagnosis-only behavior. <br>
Mitigation: Keep this skill's output focused on data-supported diagnosis and require a separate reviewed workflow before making campaign changes. <br>


## Reference(s): <br>
- [Meta Ads Drop Diagnosis on ClawHub](https://clawhub.ai/elias-didoo/meta-ads-drop-diagnosis) <br>
- [Didoo AI Blog](https://didoo.ai/blog) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown diagnosis with a performance snapshot table, root-cause analysis, and recovery-plan sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires META_ACCESS_TOKEN and META_AD_ACCOUNT_ID with read-only ads_read access to the relevant Meta ad account.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
