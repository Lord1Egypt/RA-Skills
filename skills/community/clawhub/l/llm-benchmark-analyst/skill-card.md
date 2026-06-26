## Description: <br>
Search and analyze LLM benchmark results within a fixed benchmark universe, then produce evidence-based model strength and weakness reports, domain-leader summaries, benchmark explanations, and predecessor comparisons. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Chekhovin](https://clawhub.ai/user/Chekhovin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and decision makers use this skill to compare LLMs across approved benchmark sources, identify domain leaders, explain benchmark meaning and trustworthiness, and write benchmark reports with exact model versions, variants, scores, dates, and caveats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Benchmark reports may rely on public leaderboard pages or image-rendered tables that are stale, ambiguous, or difficult to extract accurately. <br>
Mitigation: Verify important cited scores against the linked source, preserve access dates and benchmark variants, and mark unclear image-extracted values instead of treating them as definitive. <br>
Risk: Some benchmarks in the approved universe have known methodology or data-quality caveats. <br>
Mitigation: Apply the artifact's data-defect warnings inline for affected benchmarks and summarize their impact in the report limitations and confidence section. <br>
Risk: The release has limited publisher provenance because no server-resolved GitHub import provenance is stored. <br>
Mitigation: Review the artifact contents and ClawHub publisher profile before installation, and keep security scan guidance visible for deployment decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Chekhovin/llm-benchmark-analyst) <br>
- [Core Dimensions](artifact/references/core-dimensions.md) <br>
- [Data Defect Warnings](artifact/references/data-defect-warnings.md) <br>
- [Report Templates](artifact/references/report-template.md) <br>
- [Search Playbook](artifact/references/search-playbook.md) <br>
- [Benchmark Source](artifact/references/benchmark-source.md) <br>
- [Epoch AI: Benchmark Correlations](https://epoch.ai/data-insights/benchmark-correlations) <br>
- [Epoch AI: Why Benchmarking Is Hard](https://epoch.ai/gradient-updates/why-benchmarking-is-hard) <br>
- [Fantastic Bugs and Where to Find Them in AI Benchmarks](https://arxiv.org/abs/2511.16842) <br>
- [Anthropic: Infrastructure Noise in Agentic Coding Evals](https://www.anthropic.com/engineering/infrastructure-noise) <br>
- [Hugging Face Evaluation with inspect-ai](https://huggingface.co/docs/inference-providers/guides/evaluation-inspect-ai) <br>
- [Hugging Face lighteval](https://huggingface.co/docs/lighteval/main/en/index) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown reports with evidence tables, comparisons, limitations, and cited benchmark provenance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports preserve exact benchmark variants, score units, model row names, dates or access time points, source quality notes, and data-defect warnings.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
