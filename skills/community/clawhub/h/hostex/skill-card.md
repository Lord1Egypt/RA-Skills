## Description: <br>
Hostex is an OpenAPI v3.0 skill for querying and managing vacation rental properties, room types, reservations, availability, listing calendars, guest messaging, reviews, and webhooks via the Hostex API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AnsonFreeman](https://clawhub.ai/user/AnsonFreeman) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to let an agent make intent-level Hostex API calls for vacation rental operations, including property lookup, reservation review, availability checks, guest messaging, listing price updates, reservation creation, and availability changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access sensitive Hostex account, reservation, conversation, and availability data when given a Hostex token. <br>
Mitigation: Use a read-only or least-privilege Hostex token where possible and avoid broad reservation or conversation reads unless needed. <br>
Risk: Write operations can change guest messages, listing prices, reservations, or property availability. <br>
Mitigation: Leave HOSTEX_ALLOW_WRITES unset except for a specific approved change, review dry-run or planned changes, and require explicit confirmation before writes. <br>
Risk: Changing HOSTEX_BASE_URL could send requests to an untrusted endpoint. <br>
Mitigation: Do not set HOSTEX_BASE_URL unless it points to a trusted Hostex endpoint. <br>


## Reference(s): <br>
- [Hostex OpenAPI configuration](https://hostex.io/open_api/v3/config.json) <br>
- [Cached OpenAPI reference](references/openapi.json) <br>
- [ClawHub release page](https://clawhub.ai/AnsonFreeman/hostex) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Write operations are gated by HOSTEX_ALLOW_WRITES and explicit confirmation; scripts redact tokens in errors.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
