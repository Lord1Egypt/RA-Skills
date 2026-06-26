## Description: <br>
Obtains hidden and large-value takeout coupons for Meituan, Taobao Flash Sale, and Ele.me in China through a local Python command that calls a third-party coupon gateway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[moooai](https://clawhub.ai/user/moooai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to request takeout coupon tokens for supported Chinese delivery platforms. It is intended for coupon retrieval via a shell command, not for modifying or validating coupon contents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts a third-party coupon gateway to retrieve coupon data. <br>
Mitigation: Install and run only if the third-party gateway is acceptable for the intended environment. <br>
Risk: The platform selector is unreliable in this version because all supported sources are routed through the same coupon endpoint. <br>
Mitigation: Treat returned coupon data as gateway-provided output and verify that it matches the intended platform before use. <br>
Risk: Dependencies are installed from package managers without pinned versions. <br>
Mitigation: Use an isolated Python environment and review dependency versions before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/moooai/obtain-takeout-coupon) <br>
- [Third-party coupon gateway](https://agskills.moontai.top) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, Text, Guidance] <br>
**Output Format:** [Command output containing coupon gateway response data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires uv and Python package dependencies; source selects the requested coupon platform, although the artifact routes platforms through the same endpoint.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
