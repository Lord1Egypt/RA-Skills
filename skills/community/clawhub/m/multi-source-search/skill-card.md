## Description: <br>
Confidence-scored multi-source retrieval across web, scholar, Tavily, and Perplexity-backed research for cross-source verification, consensus checks, and synthesis-ready comparisons. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baofeng-tech](https://clawhub.ai/user/baofeng-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and analysts use this skill to compare results from multiple search and research providers before producing recommendations, summaries, or decision-support reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms, research prompts, optional system instructions, and supplied URLs are sent to AIsa-backed external services. <br>
Mitigation: Use only approved inputs for external processing, and avoid secrets, private or internal URLs, regulated data, and proprietary research context unless that processing is authorized. <br>


## Reference(s): <br>
- [AIsa Documentation](https://aisa.one/docs) <br>
- [AIsa API Reference](https://aisa.one/docs/api-reference/) <br>
- [AIsa Verity](https://github.com/AIsa-team/verity) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>
- [ClawHub Skill Page](https://clawhub.ai/baofeng-tech/multi-source-search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell examples and JSON API responses from the bundled Python client] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and AISA_API_KEY; verity mode returns confidence scoring and per-source result counts.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
