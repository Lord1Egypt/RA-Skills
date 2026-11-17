## Description:

Mines product review CSV data to clean feedback, classify it into bugs, suggestions, requirements, or other comments, cluster related needs, and produce a product optimization roadmap.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yz6214589-hash](https://clawhub.ai/user/yz6214589-hash)

### License/Terms of Use:

MIT-0

## Use Case:

Product managers, developers, and analysts use this skill to turn product review CSV files into cleaned feedback, categorized requirement data, clustered themes, and prioritized roadmap items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow writes review data and derived analysis files locally, which can retain sensitive personal, account, or confidential business data from input reviews.

Mitigation: Avoid processing sensitive reviews unless local retention is acceptable, or remove generated files after review according to the user's data-handling policy.

Risk: The CSV reader depends on chardet for encoding detection, which may affect reproducibility if dependency versions float.

Mitigation: Install in a virtual environment and pin or review the chardet dependency when reproducible execution matters.

## Reference(s):

- [Product Review Classification Guide](references/category_guide.md)
- [Cluster Report Template](assets/cluster_report_template.md)
- [Product Roadmap Template](assets/roadmap_template.md)
- [Product Requirement Miner on ClawHub](https://clawhub.ai/yz6214589-hash/skills/product-requirement-miner)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Plain text files, JSON classification records, Markdown reports, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates raw_reviews.txt, classified_reviews.json, filtered_data.txt, a cluster analysis report, and a product optimization roadmap.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
