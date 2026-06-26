## Description: <br>
Generates HTML intelligence briefings from multiple news sources with scoring, deduplication, and categorization across international affairs, AI, society, and trends. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lodligos](https://clawhub.ai/user/lodligos) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to manually gather, score, deduplicate, and publish current intelligence briefings as mobile-friendly HTML reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Manual or scheduled runs can publish briefings without a fresh human review. <br>
Mitigation: Configure cron only when automatic briefings are intended, and review the generated HTML before sharing it externally. <br>
Risk: The skill reads and updates daily notes or memory to deduplicate briefing content. <br>
Mitigation: Run it only in a workspace where that note access is acceptable, and review memory changes after use. <br>
Risk: Generated reports can be staged for QQ delivery. <br>
Mitigation: Confirm the generated report and destination channel before external distribution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lodligos/intel-briefing) <br>
- [Scoring rules](references/scoring.md) <br>
- [Architecture review](references/architecture-review.md) <br>
- [Version history](references/version-history.md) <br>
- [HTML briefing template](references/template.html) <br>
- [CLS telegraph feed](https://www.cls.cn/telegraph) <br>
- [36Kr newsflashes](https://36kr.com/newsflashes) <br>
- [Wallstreetcn](https://wallstreetcn.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [HTML files plus brief text summaries and optional shell or cron commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes dated briefing files under download/ and may update daily notes or stage a QQ media file when configured.] <br>

## Skill Version(s): <br>
1.5.3 (source: server release metadata; artifact version history dated 2026-04-12) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
