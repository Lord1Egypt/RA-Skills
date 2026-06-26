## Description: <br>
Use JD Logistics (Jingdong Express) for shipment tracking, shipping guidance, service-type comparison, outlet lookup, and delivery-time or fee estimation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and support agents use this skill to get JD Logistics shipment guidance, compare JD Express service tiers, estimate delivery timing or fees, and prepare return pickup workflows. It provides practical guidance and cautions users when exact shipping actions or live prices cannot be confirmed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local runtime features may store shipment query history, subscription records, saved address records, encrypted helper files, and privacy exports under ~/.openclaw/data/jdl-express/. <br>
Mitigation: Use local persistence only when needed, disclose the storage paths for privacy-sensitive workflows, and use the documented privacy info, clear, and export controls when appropriate. <br>
Risk: The skill can provide shipping estimates and workflow guidance, but exact fees, timing, tracking status, or real shipping actions may require live JD Logistics tools. <br>
Mitigation: State assumptions for estimates, ask for only the missing shipment details, and do not claim to complete real shipping actions unless live tools are available and confirmed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/harrylabsj/jdl-express) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown guidance with concise estimates, comparisons, and workflow steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include assumptions, pickup instructions, service-tier comparisons, and privacy disclosures when local runtime persistence is relevant.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
