## Description: <br>
Product Picker helps evaluate home-furnishing product candidates for 尚品宅配 by combining Xiaohongshu, JD, and Taobao signals with brand-fit scoring, then delivering a Markdown report through Feishu. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yunni123](https://clawhub.ai/user/yunni123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business, product, and merchandising teams use this skill to compare candidate products for the 尚品宅配 home-furnishing scenario. It combines multi-platform popularity and conversion signals with brand-fit criteria, then returns a ranked Markdown evaluation report and optional PPT conversion workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reports may include confidential product, strategy, or third-party platform data when sent as Feishu attachments. <br>
Mitigation: Review report contents before sending, and avoid using sensitive inputs unless the Feishu conversation and recipients are appropriate. <br>
Risk: The optional PPT conversion hands the generated report to another workflow. <br>
Mitigation: Start PPT conversion only after explicit user confirmation and only when the referenced md-to-nanobanana-ppt workflow is trusted. <br>
Risk: Product rankings depend on collected platform data and the skill's scoring assumptions. <br>
Mitigation: Treat scores as decision support, check source data quality, and review the final recommendation before acting on it. <br>


## Reference(s): <br>
- [Report Template](references/report_template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Markdown report with summary text, Feishu file attachment instructions, optional PPT handoff, and supporting Excel output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The primary report is saved locally and sent to the current Feishu conversation; PPT generation starts only after user confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
