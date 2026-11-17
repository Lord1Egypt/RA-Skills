## Description:

Analyse a raw DNA file (23andMe, AncestryDNA, MyHeritage, whole-genome VCF) through the HealthOS DNA API - traits, pharmacogenomics, carrier status, ancestry, haplogroups, polygenic scores - and ask questions about the result.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tarekjunied](https://clawhub.ai/user/tarekjunied)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to upload a raw DNA file to HealthOS, retrieve a genetic report, ask questions about the result, and delete the analysis when finished.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: DNA files and generated reports contain highly sensitive personal and familial information.

Mitigation: Upload only DNA that belongs to the user or someone who gave explicit permission, keep the API key and analysis token private, and delete the analysis when finished.

Risk: The workflow sends DNA files and related questions to the HealthOS service.

Mitigation: Use the skill only when the user is comfortable sending that information to HealthOS, and consider the free browser upload option when the user prefers to handle the file directly.

Risk: Genetic findings can be misunderstood as medical, insurance, or employment decision guidance.

Mitigation: Present health-related findings as informational, not medical advice, and do not frame results as a basis for insurance or employment decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tarekjunied/skills/healthos-dna)
- [HealthOS DNA developer page](https://healthosx.com/developers#dna)
- [HealthOS browser DNA analysis](https://healthosx.com/dna)
- [HealthOS DNA OpenAPI specification](https://api.healthosx.com/openapi.json)
- [HealthOS machine-readable reference](https://api.healthosx.com/llms.txt)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, Markdown]

**Output Format:** [Markdown with inline bash commands and API response summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include HealthOS report summaries, question answers, payment-link handling guidance, status updates, and deletion confirmation.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
