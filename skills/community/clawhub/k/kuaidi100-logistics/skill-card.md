## Description: <br>
Calls Kuaidi100 APIs with curl to query package tracking, identify carriers, estimate shipping costs, and estimate delivery times. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[peterlcm](https://clawhub.ai/user/peterlcm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer logistics questions, including shipment tracking, carrier identification, shipping cost estimates, and delivery time estimates through Kuaidi100. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shipment details, relevant phone numbers, addresses, and route history may be sent to Kuaidi100 during lookups. <br>
Mitigation: Use the skill only when sharing those logistics details with Kuaidi100 is acceptable, and provide only the fields needed for the requested lookup. <br>
Risk: The KUAIDI100_API_KEY value can be exposed if request URLs, shell history, or command output are shared. <br>
Mitigation: Store the API key in the environment, treat it as a secret, and avoid sharing logs or command output that include request URLs. <br>
Risk: Free API quota may be exhausted during normal use. <br>
Mitigation: Configure a dedicated Kuaidi100 API key for continued use and tell users when quota exhaustion prevents a lookup. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/peterlcm/kuaidi100-logistics) <br>
- [Publisher profile](https://clawhub.ai/user/peterlcm) <br>
- [Kuaidi100 API platform](https://api.kuaidi100.com) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown responses from Kuaidi100 API calls, with curl command guidance when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use KUAIDI100_API_KEY when configured; otherwise documented calls use the service's free quota path.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
