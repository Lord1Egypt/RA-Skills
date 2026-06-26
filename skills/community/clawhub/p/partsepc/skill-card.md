## Description: <br>
通过 17 位 VIN 车架号 与 待查询的配件名称或配件编码, 精准查询对应的EPC 图组信息 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[polaris2013](https://clawhub.ai/user/polaris2013) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External automotive parts users and agent developers use this skill to look up EPC diagram group information for a 17-character VIN combined with a part name or OE part code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: VIN and parts-query data are sent to an external EPC provider. <br>
Mitigation: Install only when the EPC provider is trusted for those queries, and avoid submitting VINs the user is not authorized to share. <br>
Risk: The script requires an API key for the EPC service. <br>
Mitigation: Use a dedicated JZ_API_KEY where possible and keep it in the execution environment rather than embedding it in prompts or files. <br>
Risk: The skill depends on Python requests behavior and an external service response. <br>
Mitigation: Run it in an environment with trusted Python dependencies and review returned EPC data before relying on it for parts decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/polaris2013/partsepc) <br>
- [Publisher profile](https://clawhub.ai/user/polaris2013) <br>
- [EPC group lookup API endpoint](https://erp.qipeidao.com/jzOpenClaw/getPartsEpcGroup) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration] <br>
**Output Format:** [JSON returned from the EPC lookup script, with command-line usage and environment-variable configuration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, the requests dependency, and JZ_API_KEY; accepts VIN, part name, and part code command-line inputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
