## Description: <br>
Enriches a company or person lead from public-web signals before outreach, producing an ICP-fit verdict, key facts, red flags, and optional structured output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jernejcicorbin-hub](https://clawhub.ai/user/jernejcicorbin-hub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales, marketing, and operations users use this skill to verify existing company or person leads, assess ICP fit, surface public evidence, and flag ambiguity before outreach or routing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Lead names, company details, targeting criteria, or similar prospecting data are sent to Prismfy during enrichment. <br>
Mitigation: Use the skill only for data that is appropriate to share with Prismfy, and avoid submitting sensitive prospecting data unless that transfer is approved. <br>
Risk: The setup examples show exporting the Prismfy API key in shell startup files. <br>
Mitigation: Prefer a managed secrets mechanism when available, avoid committing shell configuration files containing credentials, and rotate the key if exposure is suspected. <br>
Risk: The helper produces preliminary, keyword-scored public-web fit verdicts that can be incomplete or ambiguous. <br>
Mitigation: Review high-value outreach decisions manually, use full query coverage for stronger verdicts, and preserve ambiguity when identity or fit evidence is weak. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jernejcicorbin-hub/lead-enrichment-skill) <br>
- [Prismfy homepage](https://prismfy.io) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Concise markdown-style chat summaries with optional structured JSON report files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PRISMFY_API_KEY plus curl and jq; sends lead and qualification queries to Prismfy and limits returned source URLs in the helper output.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release, target metadata, and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
