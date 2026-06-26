## Description: <br>
Product Requirement Miner analyzes product review CSVs to clean, classify, cluster, and prioritize customer feedback into product requirement reports and roadmaps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yz6214589-hash](https://clawhub.ai/user/yz6214589-hash) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Product managers, product operations teams, and developers use this skill to convert CSV product reviews into categorized feedback, clustered requirement themes, and a prioritized optimization roadmap. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local output files may contain raw or derived customer review content. <br>
Mitigation: Use non-sensitive or redacted CSVs when possible, work in a controlled directory, and delete generated intermediate files when they are no longer needed. <br>
Risk: Generated classifications, clusters, and priority recommendations may be incomplete or inaccurate for product planning decisions. <br>
Mitigation: Review the generated JSON, cluster report, and roadmap before using them for product decisions. <br>


## Reference(s): <br>
- [Product Comment Category Guide](references/category_guide.md) <br>
- [Cluster Report Template](assets/cluster_report_template.md) <br>
- [Roadmap Template](assets/roadmap_template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Text files, JSON classification data, and Markdown analysis and roadmap reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates local files including raw review extracts, classified reviews, filtered review data, cluster reports, and product optimization roadmaps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
