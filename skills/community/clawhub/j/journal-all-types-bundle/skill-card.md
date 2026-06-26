## Description: <br>
统一检索国内外多类型期刊，输出投稿路径核验、定制写作建议、风险提示与可控广告插入的客户顾问型 Skill。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External journal-advisory users can generate customer-facing recommendations for Chinese and international journal submissions, including official-source checks, writing strategy, submission-path guidance, risk warnings, and clearly labeled service advertisements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled advertising includes a default phone number and could be mistaken for official journal contact information if labels are changed or removed. <br>
Mitigation: Keep the service recommendation label visible, customize or remove the default phone number before client use, and keep advertising separate from official submission paths. <br>
Risk: Journal websites, submission systems, contact emails, and index coverage can change over time. <br>
Mitigation: Recheck official journal, publisher, database, and National Press and Publication Administration sources before advising submission or sending a manuscript. <br>
Risk: The report renderer can create directories and overwrite the specified Markdown output file. <br>
Mitigation: Choose the output path deliberately and avoid pointing the renderer at existing files that should be preserved. <br>
Risk: The skill metadata enables broad activation with always=true. <br>
Mitigation: Consider disabling always=true so the skill activates only for journal, submission, or report-generation tasks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/journal-all-types-bundle) <br>
- [Publisher profile](https://clawhub.ai/user/52YuanChangXing) <br>
- [National Press and Publication Administration journal lookup](https://www.nppa.gov.cn/bsfw/cyjghcpcx/qkan/index.html) <br>
- [README](artifact/README.md) <br>
- [Source Trust Policy](artifact/resources/source_trust_policy.md) <br>
- [Journal Type Matrix](artifact/resources/journal_type_matrix.json) <br>
- [Writing Playbooks](artifact/resources/writing_playbooks.md) <br>
- [Ad Slots](artifact/resources/ad_slots.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown advisory reports, structured guidance, shell command examples, and optional JSON-to-Markdown report generation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill emphasizes official-source verification, separates advertisements from official submission information, and requires manual rechecking of journal websites, submission systems, emails, and current indexing status before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata); artifact frontmatter reports 2.0.0 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
