## Description: <br>
创意工作台启动器。当用户说「启动创意工作台」「打开工作台」「开启工作台」时激活。负责启动工作台服务并返回访问链接，创意生成由用户在工作台网页中操作。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunnyxiaoli](https://clawhub.ai/user/sunnyxiaoli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this skill to launch a local visual workbench for iterative marketing idea generation. The workbench collects a topic and requirements, coordinates web-supported idea generation, scores candidate ideas, and displays progress in a browser. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill starts a local web server and exposes workbench endpoints on port 50000. <br>
Mitigation: Run it only on a trusted machine and keep the service bound to localhost or otherwise inaccessible from untrusted networks. <br>
Risk: The workbench can start OpenClaw agent runs and stop or cancel stored OpenClaw tasks. <br>
Mitigation: Review the server and startup scripts before installation, and use it only in an OpenClaw workspace where task-control actions are expected. <br>
Risk: The idea-generation workflow requires live web searches and may incorporate incorrect or misleading search results into marketing ideas. <br>
Mitigation: Review search findings, scoring feedback, and selected ideas before using them in production planning. <br>


## Reference(s): <br>
- [Creative Standards](references/creative-standards.md) <br>
- [Scoring Guide](references/scoring-guide.md) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [ClawHub Skill Page](https://clawhub.ai/sunnyxiaoli/idea-generator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON-oriented API payload guidance with shell commands for local service startup] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces browser-facing progress, idea records, scoring feedback, and local service control guidance.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
