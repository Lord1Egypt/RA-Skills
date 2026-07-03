## Description: <br>
Provides Chinese-language primary-market industrial investment analysis for China-focused industrial funds, covering founder, industry, government fit, financial, industrial capability, comparison, sensitivity, and investment memo workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[perrykono-debug](https://clawhub.ai/user/perrykono-debug) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Investment professionals, fund analysts, and industrial capital teams use this skill to structure public-data due diligence, compare candidate projects, identify deal killers and missing information, and draft investment memos for China-focused industrial fund decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Analysis history and memory behavior may retain confidential deal information. <br>
Mitigation: Disable or modify automatic memory/history saving, and use the skill with confidential materials only when storage has been explicitly approved. <br>
Risk: External searches, exported reports, and Tencent Docs collaboration can disclose sensitive investment context. <br>
Mitigation: Require user confirmation before external searches, exports, or Tencent Docs sharing, and avoid sending non-public deal materials to external tools. <br>
Risk: The skill relies on public data and estimates when verified financial or company data is unavailable. <br>
Mitigation: Treat outputs as decision support, require source review and human investment committee validation, and label estimates or unknowns in final analysis. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/perrykono-debug/industrial-fund-investment-advisor) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [AGENTS.md](artifact/references/agents.md) <br>
- [IDENTITY.md](artifact/references/identity.md) <br>
- [SOUL.md](artifact/references/soul.md) <br>
- [TOOLS.md](artifact/references/tools.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration, files] <br>
**Output Format:** [Chinese-language Markdown investment memos, comparison matrices, sensitivity tables, due-diligence checklists, and optional exported report files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs distinguish known facts from estimates, cite source types, and may save analysis history or export reports when enabled.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
