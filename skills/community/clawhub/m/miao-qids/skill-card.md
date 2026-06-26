## Description: <br>
量子入侵检测系统技能喵～ 基于经典-量子混合神经网络的入侵检测系统，可以分析网络流量数据（PCAP 文件），检测多种攻击类型，并为每种攻击提供置信度喵～ 提供安全防护建议喵。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tsherryyann](https://clawhub.ai/user/tsherryyann) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security practitioners, developers, and network operators use this skill to analyze PCAP traffic, classify common attack patterns, review confidence scores, and receive defensive recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill loads model and PCA files that may not be verified by the release evidence. <br>
Mitigation: Install only from a trusted publisher and verify model artifacts from a trusted source before execution. <br>
Risk: Extracted public IP indicators may be sent to ip-api.com during geolocation. <br>
Mitigation: Avoid sensitive PCAPs unless external geolocation is acceptable; disable or replace online geolocation for production or confidential incident-response use. <br>
Risk: Feature caches may remain on disk after PCAP analysis. <br>
Mitigation: Run the skill in a contained environment and clean or redirect cache directories according to data-handling requirements. <br>


## Reference(s): <br>
- [MiaoQIDS ClawHub release page](https://clawhub.ai/tsherryyann/miao-qids) <br>
- [ip-api geolocation service](http://ip-api.com/json/{ip}?la) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, json, guidance, shell commands, configuration] <br>
**Output Format:** [JSON API responses and Markdown setup guidance with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns attack classification, confidence distribution, reconstruction error, IP analysis, defensive suggestions, processing time, and timestamp.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
