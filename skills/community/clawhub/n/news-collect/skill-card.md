## Description: <br>
Runs a repo-local scan through `skills/news-aggregator-skill` and normalizes the result into a collect-layer report contract for repeatable `news-report.md` output with raw JSON archived under `content-production/inbox/raw/news/`. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abigale-cyber](https://clawhub.ai/user/abigale-cyber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content teams use News Collect to run broad overseas or domestic news scans from a markdown request and turn the results into standardized local reports and raw JSON archives for topic selection or follow-on research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes reports and raw archives under content-production/inbox/. <br>
Mitigation: Install and run it only in repositories where creating files in that path is acceptable. <br>
Risk: Request notes, fetched content, and vendor stderr may be saved in local report or raw archive files. <br>
Mitigation: Do not put secrets or private notes in request files, and review generated artifacts before sharing them. <br>
Risk: The repo-local news-aggregator-skill dependency performs the external news fetching. <br>
Mitigation: Review that dependency and its source behavior before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/abigale-cyber/news-collect) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [runtime.py](artifact/runtime.py) <br>
- [skill.json](artifact/skill.json) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown report plus raw JSON archive written to local files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes standardized reports under content-production/inbox/ and raw fetch results under content-production/inbox/raw/news/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
