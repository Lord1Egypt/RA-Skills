## Description: <br>
PPTX Analysis helps agents analyze PowerPoint (.pptx) presentations with MinerU and return structured Markdown that captures slide content, headings, layout, and hierarchy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mzlzyca](https://clawhub.ai/user/mzlzyca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content reviewers, presentation auditors, and automated quality checks use this skill to inspect PowerPoint decks, understand slide structure, and extract Markdown summaries or fuller structured content via MinerU. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Full extraction may send slide contents to MinerU, which can expose confidential presentation content to external processing. <br>
Mitigation: Use the skill only for presentations approved for MinerU processing; prefer flash-extract for quick tokenless analysis and avoid full extraction on confidential decks unless external processing is approved. <br>
Risk: The MINERU_TOKEN credential is required for full extraction and could be exposed if pasted into shared logs or files. <br>
Mitigation: Keep MINERU_TOKEN in a private environment variable or the MinerU auth flow and do not include token values in prompts, outputs, commits, or shared logs. <br>


## Reference(s): <br>
- [PPTX Analysis on ClawHub](https://clawhub.ai/mzlzyca/pptx-analysis) <br>
- [MinerU](https://mineru.net) <br>
- [MinerU GitHub Repository](https://github.com/opendatalab/MinerU) <br>
- [MinerU API Token Management](https://mineru.net/apiManage/token) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Quick flash extraction can run without a token; full extraction requires MINERU_TOKEN and may process slide contents with MinerU.] <br>

## Skill Version(s): <br>
0.4.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
