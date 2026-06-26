## Description: <br>
This skill lets agents reverse-geocode longitude and latitude coordinates into a full address and administrative location fields using the Jike API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and external users use this skill when a user provides coordinates and needs a readable address, country, province, city, district, township, and street. It is useful for reverse-geocoding prompts such as asking where a longitude and latitude are located. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Coordinate queries and API-key-authenticated requests are sent to jikeapi.cn, and precise coordinates can be personal location data. <br>
Mitigation: Use the skill only when sending the requested coordinates to Jike API is acceptable, keep the API key private, and avoid including unnecessary personal context in coordinate lookups. <br>
Risk: JIKE_API_BASE_URL can redirect requests to an alternate endpoint if set. <br>
Mitigation: Leave JIKE_API_BASE_URL unset unless the alternate endpoint is intentionally trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jikeapi-cn/jike-map-geocode-query) <br>
- [Jike API homepage](https://www.jikeapi.cn/) <br>
- [Jike reverse-geocoding API endpoint](https://api.jikeapi.cn/v1/map/geocode/query) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/jikeapi-cn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Plain text address fields or JSON API response, with command-line usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a Jike API key supplied through JIKE_MAP_GEOCODE_QUERY_KEY, JIKE_APPKEY, or the --key option.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
