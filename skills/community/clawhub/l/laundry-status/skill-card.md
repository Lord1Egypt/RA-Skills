## Description: <br>
Use when the user wants to check washing machine or dryer status, laundry room availability, or which machines are free at Shanghai Jiao Tong University Minhang campus. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rexeno56](https://clawhub.ai/user/rexeno56) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students, residents, and campus users at Shanghai Jiao Tong University Minhang campus use this skill to check washing machine and dryer availability, status, and estimated finish times for supported dormitory buildings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using the skill sends selected SJTU building queries to Haier's laundry-status service. <br>
Mitigation: Review the endpoint and network behavior before installation, especially in environments with strict external request policies. <br>
Risk: The skill depends on the availability and accuracy of the external Haier status service. <br>
Mitigation: Treat returned machine status and estimated finish times as service-provided operational data and retry later if the API is unavailable. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/rexeno56/laundry-status) <br>
- [Haier IoT laundry status endpoint](https://yshz-user.haier-ioc.com/position/deviceDetailPage) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text status report with grouped machine availability and optional estimated finish times] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The script can query the default building, a supported specific building, or all supported buildings.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server-resolved release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
