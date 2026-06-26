## Description: <br>
Paper to Slides deep-reads academic papers from local PDFs, arXiv links, DOI URLs, or direct PDF URLs and produces a structured research report, an HTML slide deck, or both. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangguanghao523](https://clawhub.ai/user/zhangguanghao523) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, educators, and external users use this skill to turn academic PDFs, arXiv links, DOI URLs, or direct PDF URLs into structured paper-reading reports and presentation-ready HTML slide decks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can download user-provided PDF URLs and run local PDF extraction tools. <br>
Mitigation: Prefer local PDFs for confidential work and avoid untrusted PDF URLs. <br>
Risk: Generated slides may load remote fonts and can persist browser edits in localStorage when editing is enabled. <br>
Mitigation: Review or disable remote fonts and localStorage behavior for offline or privacy-sensitive use. <br>
Risk: The generated report and slides may contain inaccurate or misleading paper analysis. <br>
Mitigation: Review the report and slide content against the source paper before using it for teaching, meetings, or publication. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhangguanghao523/paper2slides) <br>
- [Publisher profile](https://clawhub.ai/user/zhangguanghao523) <br>
- [Poppler](https://poppler.freedesktop.org/) <br>
- [frontend-slides](https://github.com/zarazhangrui/frontend-slides) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report plus self-contained HTML slide deck with inline CSS and JavaScript] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May optionally include browser-based slide editing with localStorage persistence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
