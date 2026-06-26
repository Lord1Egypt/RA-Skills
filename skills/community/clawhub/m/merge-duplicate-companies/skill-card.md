## Description: <br>
Identify duplicate HubSpot company records by domain and name, export audit CSVs for review, and guide manual or third-party assisted merging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tomgranot](https://clawhub.ai/user/tomgranot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Revenue operations, sales operations, and CRM administrators use this skill to find duplicate HubSpot company records, produce audit CSVs, and plan safe manual or third-party assisted cleanup before changing live CRM data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exports sensitive HubSpot CRM data to local CSV files. <br>
Mitigation: Use a narrowly scoped HubSpot private app token, run in a trusted workspace, write outputs to an access-controlled location, and delete or protect CSV files after review. <br>
Risk: HubSpot company merges are irreversible and may discard conflicting property values from the non-primary record. <br>
Mitigation: Review the exported audit CSVs with the responsible team, choose the surviving record deliberately, and require explicit human confirmation before any merge. <br>
Risk: Name-based duplicate matching can produce false positives for distinct organizations with similar names. <br>
Mitigation: Prioritize domain-based groups, manually inspect name-only matches, and skip uncertain pairs until a CRM owner confirms they refer to the same company. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tomgranot/merge-duplicate-companies) <br>
- [HubSpot CRM API](https://api.hubapi.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, CSV files, guidance] <br>
**Output Format:** [Markdown guidance with Python code, setup commands, environment configuration, and CSV audit outputs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces audit files for review and does not automatically merge company records.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
