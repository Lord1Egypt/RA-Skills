## Description: <br>
Build, maintain, validate, and publish an evidence-backed asset graph or OKF-style resource map for operations, DevOps, SRE, platform engineering, infrastructure inventory, CMDB-like service catalogs, dependency mapping, incident handoff, and discovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qinyongliang](https://clawhub.ai/user/qinyongliang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, DevOps engineers, SREs, platform engineers, and operations teams use this skill to inventory operational assets, record evidence-backed relationships, and produce reusable Markdown records with structured frontmatter for asset graphs or service catalogs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages broad proactive infrastructure discovery from private entrypoints without enough scoping or confirmation. <br>
Mitigation: Before use, define target assets, allowed credentials, discovery depth, prohibited data reads, record locations, and sharing rules for generated catalogs. <br>
Risk: Generated asset records could expose private endpoints, credentials, account identifiers, or internal system names if shared publicly. <br>
Mitigation: Keep real-target artifacts outside public releases, sanitize examples, and publish only fictional or reserved-example assets. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/qinyongliang/skills/okf-asset-graph) <br>
- [Source Repository](https://github.com/qinyongliang/okf-asset-graph) <br>
- [Imported Commit](https://github.com/qinyongliang/okf-asset-graph/commit/cacbc2cd92d77e8b67e318aa332f016b6ccfd126) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Configuration, Shell commands, Guidance] <br>
**Output Format:** [Markdown with YAML frontmatter and inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces evidence-backed asset records and catalog guidance; mutating operations require explicit authorization and an operation log.] <br>

## Skill Version(s): <br>
0.1.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
