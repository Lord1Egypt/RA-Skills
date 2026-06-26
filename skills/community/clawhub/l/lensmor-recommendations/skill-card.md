## Description: <br>
Get AI-ranked exhibitors matching an ICP and shortlist the top accounts worth outreach at trade shows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weilun88313](https://clawhub.ai/user/weilun88313) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External B2B sales and event teams use this skill to rank exhibitors for a specific trade show against their ICP, then focus pre-show outreach on the strongest-fit accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Company profile, ICP filters, target-account names, and prospecting criteria may be sent to Lensmor. <br>
Mitigation: Confirm Lensmor is approved for this data, minimize confidential customer or internal sales strategy details, and avoid sending data outside approved vendor processes. <br>
Risk: The skill requires a Lensmor API key. <br>
Mitigation: Store LENSMOR_API_KEY in an approved secret mechanism and never include the key value in prompts, logs, or generated output. <br>
Risk: Returned ranking and funding fields may be stale or incomplete for outreach decisions. <br>
Mitigation: Review the ranked shortlist and treat funding data as a budget proxy rather than a verified current fact before acting on recommendations. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/weilun88313/lensmor-recommendations) <br>
- [Lensmor API Documentation](https://api.lensmor.com/) <br>
- [Lensmor Platform](https://platform.lensmor.com) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown tables and prose with inline shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Ranks returned exhibitors in API order and grounds ICP rationale in returned company fields.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
