## Description: <br>
Collect Korean government support programs (TIPS, Small Business, R&D grants) into structured JSONL files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lifeissea](https://clawhub.ai/user/lifeissea) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to collect Korean government support program listings into append-only JSONL datasets and inspect collection totals. It supports incremental scraping with checkpoints for repeated updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scraper contacts public Korean government sites and writes local output files. <br>
Mitigation: Install only where outbound scraping and local file writes are acceptable, and use a simple trusted output path such as ./data. <br>
Risk: The stats helper has a local path-handling flaw that could run unintended code with crafted directory names. <br>
Mitigation: Run scripts/stats.sh only against trusted, ordinary directory names and avoid untrusted or unusual paths. <br>
Risk: Package metadata mismatch may make it unclear whether the installed package contains the reviewed scripts. <br>
Mitigation: Verify the installed package includes the reviewed SKILL.md, scripts/collect.py, and scripts/stats.sh before use. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/lifeissea/korean-gov-programs) <br>
- [BizInfo support program listings](https://www.bizinfo.go.kr/sii/siia/selectSIIA200View.do) <br>
- [NIA public listing source](https://www.nia.or.kr/site/nia_kor/ex/bbs/List.do?cbIdx=78336) <br>


## Skill Output: <br>
**Output Type(s):** [Files, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSONL files with terminal status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Appends records to soho_programs.jsonl and gov_programs.jsonl, and maintains .checkpoint.json in the selected output directory.] <br>

## Skill Version(s): <br>
1.0.8 (source: SKILL.md frontmatter and server release evidence; package.json reports 1.0.7) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
