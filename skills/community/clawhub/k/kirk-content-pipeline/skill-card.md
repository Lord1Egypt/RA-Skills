## Description: <br>
Create KSVC-validated Twitter content from analyst research PDFs, including long threads, quick takes, breaking news posts, personal commentary, and victory-lap posts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lukerspace](https://clawhub.ai/user/lukerspace) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Analysts and content operators use this skill to turn research PDFs into source-checked social media drafts. The workflow combines extraction, cross-document synthesis, KSVC holdings checks, claim audits, cross-validation, stylization, human review, and publication artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow uses symlinks to expose local PDF folders to subagents. <br>
Mitigation: Approve symlinks only to the specific PDF folder needed for the run, and remove the symlink after the task is complete. <br>
Risk: The extraction-cache helper loads pickle state, which can execute unsafe payloads if the state file is untrusted. <br>
Mitigation: Run the helper only on RLM state files generated locally for the current task and kept in a trusted task folder. <br>
Risk: Drafts may contain incorrect holdings, source excerpts, chart details, or market claims before review. <br>
Mitigation: Manually review holdings, source excerpts, generated metadata, and any chart decisions before publishing or sharing externally. <br>


## Reference(s): <br>
- [Kirk Content Pipeline source](artifact/SKILL.md) <br>
- [RLM Extraction Cache System](artifact/scripts/README-extraction-cache.md) <br>
- [Extraction Cache Builder](artifact/scripts/build_extraction_cache.py) <br>
- [Kirk Voice Guide](artifact/references/kirk-voice.md) <br>
- [Citrini7 Style Reference](artifact/references/citrini7-style.md) <br>
- [Jukan05 Patterns Reference](artifact/references/jukan05-patterns.md) <br>
- [Serenity Style Reference](artifact/references/serenity-style.md) <br>
- [Zephyr Patterns Reference](artifact/references/zephyr-patterns.md) <br>
- [TWSE Code Query API](https://www.twse.com.tw/en/api/codeQuery?query=3443) <br>
- [KSVC Holdings API](https://kicksvc.online/api/twse-model2) <br>
- [Yahoo Finance Chart API](https://query1.finance.yahoo.com/v8/finance/chart/6285.TW?interval=1d&range=1d) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown drafts and metadata, shell command snippets, JSON extraction caches, and review checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires human approval before publication; generated caches should remain task-specific.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
