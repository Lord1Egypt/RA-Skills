## Description: <br>
Queries Chinese couplets by upper- or lower-line keyword and can return random couplets using the Jike Data API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to search for Chinese couplets by keyword or retrieve a random couplet for writing, recommendation, or explanation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Couplet search keywords and the Jike AppKey are sent to jikeapi.cn. <br>
Mitigation: Install only when that data sharing is acceptable and avoid placing the AppKey in shared environments. <br>
Risk: Setting JIKE_API_BASE_URL can redirect requests to an alternate API endpoint. <br>
Mitigation: Leave JIKE_API_BASE_URL unset unless the alternate endpoint is intentionally trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jikeapi-cn/jike-couplet-query) <br>
- [Jike Data homepage](https://www.jikeapi.cn/) <br>
- [Jike couplet query API endpoint](https://api.jikeapi.cn/v1/couplet/query) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Terminal table text or JSON API response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a JIKE_COUPLET_QUERY_KEY or JIKE_APPKEY credential; JSON output is available with --json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
