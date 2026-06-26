## Description: <br>
PharmaAI helps agents run molecule toxicity predictions from SMILES inputs and return structured risk summaries for single-molecule, batch, and screening workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xxxrobot](https://clawhub.ai/user/xxxrobot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and drug-discovery teams can use this skill to prototype molecule toxicity triage from SMILES inputs and compare candidate compounds. Outputs require expert review and should not be treated as dependable drug-safety determinations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill advertises ADMET and Lipinski analysis that server security evidence says is not actually computed by the code. <br>
Mitigation: Treat those fields as prototype placeholders unless they are replaced with validated calculations and reviewed by qualified domain experts. <br>
Risk: The skill is a suspicious, review-needed prototype for drug-discovery decisions. <br>
Mitigation: Do not rely on its outputs for research, clinical, safety, regulatory, or investment decisions without independent validation. <br>
Risk: Bundled ClawHub token and publishing instructions can affect credentials or publication workflows if followed unintentionally. <br>
Mitigation: Follow those instructions only when intentionally maintaining or publishing the skill, and keep tokens secret and scoped. <br>
Risk: Runtime behavior depends on Python dependencies and local model files. <br>
Mitigation: Install in a controlled environment with pinned dependencies and trusted model files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xxxrobot/pharma-ai) <br>
- [README](README.md) <br>
- [Skill definition](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, analysis, guidance] <br>
**Output Format:** [Structured JSON prediction results and formatted human-readable text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns toxicity risk labels and probabilities for hERG, hepatotoxicity, and Ames predictions; ADMET-style fields and Lipinski status need validation before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
