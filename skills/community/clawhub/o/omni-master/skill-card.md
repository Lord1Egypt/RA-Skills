## Description: <br>
OMNI is an all-in-one routing skill that helps an agent classify broad or cross-domain requests and load targeted references for automation, coding, data, communications, systems, creative work, and general problem-solving. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eternal0404](https://clawhub.ai/user/eternal0404) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to route ambiguous or multi-domain requests to relevant guidance, then execute with domain-specific references for tasks such as coding, automation, data work, messaging, deployment, research, and content creation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is intentionally broad and may route an agent toward high-impact actions such as file writes, command execution, deployments, public messages, camera or screen capture, credential use, or background automation. <br>
Mitigation: Require explicit confirmation for high-impact actions and keep host-agent permissions scoped to the current task. <br>
Risk: The skill encourages persistent memory behavior, which can create privacy risk if sensitive data is logged. <br>
Mitigation: Disable or tightly scope memory logging, and prevent passwords, tokens, private communications, health data, financial data, and other sensitive information from being written to memory files. <br>
Risk: The skill covers sensitive domains such as finance, health, security, and system administration using general guidance. <br>
Mitigation: Prefer specialized skills and human review for sensitive tasks, and treat domain guidance as operational assistance rather than professional advice. <br>


## Reference(s): <br>
- [Skill definition](SKILL.md) <br>
- [Advanced Prompting Engine](references/advanced-prompting.md) <br>
- [API Design & Testing](references/api-design.md) <br>
- [Automation & Workflows](references/automation.md) <br>
- [Brain — Adaptive Cognitive Engine](references/brain.md) <br>
- [Calendar & Scheduling](references/calendar-scheduling.md) <br>
- [Career](references/career.md) <br>
- [Coding](references/coding.md) <br>
- [Communication Platforms](references/communications.md) <br>
- [Creative & Content Engine](references/creative.md) <br>
- [Data & Databases](references/data-databases.md) <br>
- [Data Literacy](references/data-literacy.md) <br>
- [Deployment & DevOps](references/deployment-devops.md) <br>
- [Documents](references/documents.md) <br>
- [Email & Messaging](references/email-messaging.md) <br>
- [Ethics, Safety & Boundaries](references/ethics-safety.md) <br>
- [Finance](references/finance.md) <br>
- [Health & Fitness](references/health-fitness.md) <br>
- [IoT & Smart Home](references/iot-smarthome.md) <br>
- [Knowledge Management](references/knowledge-mgmt.md) <br>
- [Learning](references/learning.md) <br>
- [Math Engine](references/math-engine.md) <br>
- [Media Generation](references/media-generation.md) <br>
- [Multi-Agent](references/multi-agent.md) <br>
- [Music & Audio](references/music-audio.md) <br>
- [Network & Cloud](references/network-cloud.md) <br>
- [Performance](references/performance.md) <br>
- [Project Management](references/project-management.md) <br>
- [Quality Assurance](references/quality-assurance.md) <br>
- [Realtime](references/realtime.md) <br>
- [Reasoning](references/reasoning.md) <br>
- [Research](references/research.md) <br>
- [Security & Hardening](references/security.md) <br>
- [System Administration](references/system-admin.md) <br>
- [Translation](references/translation.md) <br>
- [Web Scraping](references/web-scraping.md) <br>
- [Writing & Content](references/writing-content.md) <br>
- [Router script](scripts/router.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline code and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Routes user requests to selected domain references; concrete actions depend on the host agent's tools and user approvals.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
