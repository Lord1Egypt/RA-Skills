## Description: <br>
Query biomedical databases for drug repurposing, target discovery, clinical trials, literature research, genetic associations, safety data, and compound bioactivity through a unified MCP endpoint. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[pascalwhoop](https://clawhub.ai/user/pascalwhoop) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External biomedical researchers, developers, and analysts use this skill to build evidence-oriented workflows for drug repurposing, target discovery, clinical evidence review, literature mining, and safety checks across public biomedical data sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Medical research outputs may be incomplete, outdated, or unsuitable for diagnosis, treatment, drug safety, or clinical decisions. <br>
Mitigation: Have qualified medical professionals validate any drug, diagnosis, safety, or treatment-related conclusions before use. <br>
Risk: Queries to the hosted endpoint could expose patient identifiers, PHI, confidential study details, or proprietary hypotheses. <br>
Mitigation: Do not submit sensitive or regulated information unless the operator is trusted and appropriate data-handling approval is in place. <br>
Risk: OMIM and optional higher-rate-limit services require API keys that could be exposed through prompts, shared logs, or examples. <br>
Mitigation: Keep API keys out of shared prompts and logs, and use secret-management practices when running workflows locally. <br>
Risk: Artifact testing indicates some databases and workflows were not fully tested and some reference examples may need updates. <br>
Mitigation: Verify database-specific examples and cross-check results against primary biomedical sources before relying on them. <br>


## Reference(s): <br>
- [PubMed & PubTator3 Guide](references/pubmed.md) <br>
- [ClinicalTrials.gov Guide](references/clinical-trials.md) <br>
- [ChEMBL Guide](references/chembl.md) <br>
- [OpenTargets Platform Guide](references/opentargets.md) <br>
- [OpenFDA Guide](references/openfda.md) <br>
- [OMIM Guide](references/omim.md) <br>
- [Additional Biomedical Databases](references/other-apis.md) <br>
- [Drug Repurposing Workflow](scripts/drug-repurposing-workflow.md) <br>
- [Unified MCP Endpoint](https://mcp.cloud.curiloo.com/tools/unified/mcp) <br>
- [OMIM API Access](https://omim.org/api) <br>
- [OpenFDA API](https://open.fda.gov) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown guidance with curl and JSON-RPC examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces research workflow suggestions and request examples; API responses are returned by the selected biomedical data services.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
