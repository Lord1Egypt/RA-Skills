## Description: <br>
Poll Houston TranStar incidents RSS every 10 minutes and WhatsApp me when there are changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vijay-murugan](https://clawhub.ai/user/vijay-murugan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Houston residents and logistics or operations teams use this skill to monitor Greater Houston traffic incidents and receive WhatsApp summaries when new, cleared, or updated incidents appear. <br>

### Deployment Geography for Use: <br>
United States (Greater Houston, Texas) <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports that the installed entrypoint is wired to an unrelated placeholder external-script runner outside the reviewed package. <br>
Mitigation: Review before installing; remove the placeholder runner and register the included TranStar watcher directly. <br>
Risk: Network access, local state, schedule, delivery, and execution permissions are not clearly declared. <br>
Mitigation: Declare Houston TranStar RSS polling, local snapshot storage, the 10-minute schedule, WhatsApp delivery, and execution permissions before deployment. <br>


## Reference(s): <br>
- [Houston TranStar Incidents RSS Feed](https://traffic.houstontranstar.org/data/rss/incidents_rss.xml) <br>
- [ClawHub Skill Page](https://clawhub.ai/vijay-murugan/houston-transtar-watch) <br>


## Skill Output: <br>
**Output Type(s):** [text] <br>
**Output Format:** [Plain text incident summary, NO_CHANGES status, or error message] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summaries include counts of new, cleared, and updated incidents and list up to five items per category.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
