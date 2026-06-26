## Description: <br>
Queries Chinese vehicle plate numbers or at least the first two plate-prefix characters to return the plate prefix, province abbreviation, province, and city using Jike Data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to answer questions about Chinese vehicle plate origin by extracting a full plate number or at least a two-character prefix, running the lookup script, and returning the province, city, and prefix details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queried plate numbers and the Jike AppKey are sent to Jike's API. <br>
Mitigation: Use this skill only when that third-party API disclosure is acceptable, and provide credentials through the documented environment variables. <br>
Risk: Setting JIKE_API_BASE_URL redirects both the plate number and AppKey to another host. <br>
Mitigation: Leave JIKE_API_BASE_URL unset unless intentionally testing or operating against a trusted alternate endpoint. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jikeapi-cn/jike-vehicle-plate-query) <br>
- [Jike Data homepage](https://www.jikeapi.cn/) <br>
- [Jike vehicle plate query API](https://api.jikeapi.cn/v1/vehicle/plate/query) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text lookup results or JSON API response, with Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a JIKE_VEHICLE_PLATE_QUERY_KEY or JIKE_APPKEY credential.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
