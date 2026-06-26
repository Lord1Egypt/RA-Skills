## Description: <br>
Unified heterogeneous knowledge QA system that automatically routes natural language queries to SQL databases, Knowledge Graphs, or table files using 4-layer detection, multi-LLM providers, and bilingual query support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bahuia](https://clawhub.ai/user/bahuia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data engineers use this skill to answer structured data questions by routing natural language queries across SQL databases, SPARQL knowledge graphs, and tabular files. It is suited for workflows that need source detection, query generation, result fusion, and concise natural language answers over heterogeneous knowledge sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Python, SQL, and SPARQL may perform unintended actions or return misleading results if executed without review. <br>
Mitigation: Treat generated code and queries as untrusted; require human approval or a real sandbox before live execution. <br>
Risk: Database credentials, API keys, local files, and SPARQL endpoints may be exposed or misused during heterogeneous source access. <br>
Mitigation: Use isolated environments, read-only database credentials, explicit table paths, trusted endpoints, and approved LLM providers for sensitive data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bahuia/heteromind) <br>
- [README](README.md) <br>
- [Usage guide](USAGE.md) <br>
- [Security documentation](SECURITY.md) <br>
- [Comprehensive test report](tests/comprehensive_test_report.md) <br>
- [Source detection configuration](config/source_detection.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Configuration, Guidance] <br>
**Output Format:** [Natural language answers with generated SQL, SPARQL, or Python code when applicable] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require LLM API keys, database credentials, explicit table paths, and trusted SPARQL endpoints depending on the selected engine.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
