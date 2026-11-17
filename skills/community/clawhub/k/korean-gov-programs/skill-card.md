## Description:

Collect Korean government support programs (TIPS, Small Business, R&D grants) into structured JSONL files. Supports incremental collection with checkpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lifeissea](https://clawhub.ai/user/lifeissea)

### License/Terms of Use:

MIT

## Use Case:

Developers, operators, and program analysts use this skill to collect Korean government support program listings into local JSONL datasets and inspect collection totals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The status script has a local code-execution risk when given a crafted data directory path.

Mitigation: Review before installing or running, use only trusted data directory paths, and fix scripts/stats.sh to pass the checkpoint path as data rather than interpolating it into python3 -c.

Risk: The collector performs outbound requests to Korean public program listing sites and writes JSONL and checkpoint files under the selected output directory.

Mitigation: Run it in an approved network environment, choose a controlled output directory, and review generated records before downstream use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lifeissea/skills/korean-gov-programs)
- [BizInfo program listing](https://www.bizinfo.go.kr/sii/siia/selectSIIA200View.do)
- [NIA program listing](https://www.nia.or.kr/site/nia_kor/ex/bbs/List.do?cbIdx=78336)
- [SEMAS board](https://www.semas.or.kr/web/board/boardList.do)
- [MSS](https://www.mss.go.kr/)
- [K-Startup](https://www.k-startup.go.kr/)
- [Innopolis](https://www.innopolis.or.kr/)
- [KISED](https://www.kised.or.kr/)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, JSONL files, guidance]

**Output Format:** [JSONL files with local checkpoint JSON and terminal status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Append-only local writes with title-based deduplication and checkpointed incremental collection.]

## Skill Version(s):

1.0.8 (source: release metadata and SKILL.md frontmatter; package.json reports 1.0.7)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
