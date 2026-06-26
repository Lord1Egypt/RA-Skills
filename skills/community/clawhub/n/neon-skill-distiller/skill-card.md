## Description: <br>
Fit more skills in your context window by compressing skill text without losing what matters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leegitw](https://clawhub.ai/user/leegitw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use Skill Distiller to compress Agent Skills markdown into smaller variants while preserving triggers, core instructions, constraints, and visible trade-offs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Calibration logging can preserve details from analyzed skill work in .learnings/skill-distiller/calibration.jsonl. <br>
Mitigation: Review or disable logging before using the skill on proprietary or sensitive skill content. <br>
Risk: Provider auto-detection may use an API-backed LLM provider when GEMINI_API_KEY or OPENAI_API_KEY is present. <br>
Mitigation: Confirm the intended model backend and environment variables before running the skill on sensitive material. <br>
Risk: Compression decisions and functionality percentages are LLM-estimated and may remove context that matters for a specific deployment. <br>
Mitigation: Review the compressed output, compare removed sections against deployment needs, and test critical workflows before release. <br>


## Reference(s): <br>
- [ClawHub Release](https://clawhub.ai/leegitw/neon-skill-distiller) <br>
- [Publisher Profile](https://clawhub.ai/user/leegitw) <br>
- [Source Homepage](https://github.com/live-neon/skills/tree/main/skill-distiller) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown skill content with metrics, summaries, and optional inline commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include functionality estimates, token reduction estimates, removed-section summaries, and local calibration metadata.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
