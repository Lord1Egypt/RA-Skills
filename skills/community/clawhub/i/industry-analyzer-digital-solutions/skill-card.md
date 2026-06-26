## Description: <br>
Analyzes digital transformation solutions for an industry across major Chinese cloud and technology vendors plus vertical solution providers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zrxparley](https://clawhub.ai/user/zrxparley) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and research agents use this skill to compare industry digital transformation offerings from Huawei, Alibaba, Baidu, Tencent, and vertical vendors, then produce a local industry solution report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes local report and session files, which may overwrite or replace existing analysis work in the target output folder. <br>
Mitigation: Check whether output/{industry-slug}/03-digital-solutions.md or session.json already contain work that should be preserved before running the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zrxparley/industry-analyzer-digital-solutions) <br>
- [Major vendors list](references/major-vendors-list.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration] <br>
**Output Format:** [Markdown report with session.json status updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes output/{industry-slug}/03-digital-solutions.md and updates output/{industry-slug}/session.json.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
