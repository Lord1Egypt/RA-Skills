## Description: <br>
Multi-Agent collaborative system for writing ultra-long feasibility study reports, from requirements confirmation and outline planning through parallel chapter writing, consistency review, and styled document generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jinqiu193](https://clawhub.ai/user/jinqiu193) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, business users, and report-writing teams use this skill to coordinate long-form feasibility reports and proposals with structured requirements gathering, outline planning, parallel chapter drafting, review, and final document assembly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can persist raw reference material and generated report content locally. <br>
Mitigation: Use non-sensitive materials unless storage behavior has been reviewed, and back up or isolate existing output files before running the workflow. <br>
Risk: The workflow may use Feishu or web search and send WeChat progress messages. <br>
Mitigation: Confirm or disable external search and messaging behavior before processing confidential or regulated project information. <br>
Risk: Automated multi-agent drafting may produce inaccurate, inconsistent, or misleading business content. <br>
Mitigation: Require human review of outlines, chapter drafts, consistency checks, and final documents before relying on or distributing outputs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jinqiu193/long-doc-agent) <br>
- [Phase 0 Requirements Confirmation Guide](references/phase0_guide.md) <br>
- [Phase 1 Planner Guide](references/phase1_guide.md) <br>
- [Phase 2 Sub-Agent Writing Guide](references/phase2_guide.md) <br>
- [Markdown Table Format Guide](references/table_format_guide.md) <br>
- [Bug Troubleshooting and Forced Rebuild Guide](references/bug_fix_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown report drafts, styled DOCX files, progress updates, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local state files and chapter outputs under F:/agent/chapters when run as documented.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact metadata and changelog describe long-doc-agent v3.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
