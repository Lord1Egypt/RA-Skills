## Description: <br>
IC Search helps users query electronic component pricing, inventory, quotes, and spot purchasing information from a supplier lookup service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wordgao](https://clawhub.ai/user/wordgao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Procurement and engineering users use this skill to search electronic component models, quantities, prices, inventory, quotes, and spot availability. The skill is intended for component lookup workflows that can use the Ningkewode supplier response data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Component part numbers, quantities, and procurement intent are sent to an external supplier service over unencrypted HTTP. <br>
Mitigation: Use only non-confidential searches unless the API moves to HTTPS; avoid confidential BOMs, customer-specific requirements, and sensitive purchasing plans. <br>


## Reference(s): <br>
- [API Documentation](references/api.md) <br>
- [Search Examples](references/examples.md) <br>
- [Error Codes](references/errors.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/wordgao/ic-search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Guidance] <br>
**Output Format:** [Plain text responses derived from JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns the API data field when available; error responses may be short Chinese status messages such as unauthorized or query failed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
