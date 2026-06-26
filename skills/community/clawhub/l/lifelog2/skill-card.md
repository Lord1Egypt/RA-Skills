## Description: <br>
碎片化日记记录和汇总技能。当用户想要记录当天碎片化的想法、心情、事件，或者需要汇总、存档日记时使用。触发场景包括：用户发送"记日记"记录碎片内容、发送"汇总日记"整理当天内容、发送"日记存档"将日记写入 flomo 和 ima。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[quanmengli777](https://clawhub.ai/user/quanmengli777) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to capture same-day diary fragments, preserve the original wording, summarize entries into a dated lifelog, and archive the summary to flomo and ima. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Diary fragments persist locally across sessions until archived. <br>
Mitigation: Install only if local draft storage is acceptable, and review or remove drafts when they should no longer remain on the device. <br>
Risk: Archiving sends the compiled diary to flomo and ima. <br>
Mitigation: Review the generated summary before archiving and confirm the connected flomo and ima skills use the intended accounts. <br>
Risk: Successful archival removes the local draft. <br>
Mitigation: Keep a separate copy before archiving if the local draft should be retained. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/quanmengli777/lifelog2) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [File storage demo](artifact/lifelog2-workspace/iteration-1/file_storage_demo.md) <br>
- [Test results](artifact/lifelog2-workspace/iteration-1/test_results.md) <br>
- [Evaluation config](artifact/evals/evals.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, API Calls, Guidance] <br>
**Output Format:** [Markdown and short confirmation text with local dated draft files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preserves user diary text verbatim, stores local drafts by date, and archives only after user request.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
