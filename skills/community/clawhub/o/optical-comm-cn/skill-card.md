## Description: <br>
AI光通信产业链投资分析框架，用于分析光模块、光芯片、PCB、CPO/NPO/OCS相关股票，判断技术路线、供应链位置、标的质量和知识更新需求。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pcchris1995](https://clawhub.ai/user/pcchris1995) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to structure optical-communications investment analysis, compare CPO/NPO/XPO, InP/silicon photonics/TFLN and OCS routes, map companies to the supply chain, and assess thesis quality. The optional update workflow can help refresh local reference notes from specified Xueqiu sources when the user explicitly requests it. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional update workflow can use a logged-in Xueqiu/browser session. <br>
Mitigation: Run updates only after explicit user request, confirm the target URLs, and avoid exposing private browser data or credentials. <br>
Risk: The update workflow can modify local reference files. <br>
Mitigation: Review proposed file edits before deployment and keep updates limited to the skill's documented reference files. <br>
Risk: Investment analysis content is time-sensitive opinion and may be incomplete or misleading. <br>
Mitigation: Treat outputs as analytical guidance, verify current market and company data independently, and do not present outputs as financial advice. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pcchris1995/optical-comm-cn) <br>
- [Core framework](references/core-framework.md) <br>
- [Methodology](references/methodology.md) <br>
- [Supply chain](references/supply-chain.md) <br>
- [Technology landscape](references/tech-landscape.md) <br>
- [Update log](references/update-log.md) <br>
- [Xueqiu profile: 闷得而蜜](https://xueqiu.com/u/5672579962) <br>
- [Xueqiu profile: 查尔斯大风车](https://xueqiu.com/u/8755156034) <br>
- [Xueqiu article: 查尔斯大风车 2026-04-21](https://xueqiu.com/8755156034/384873103) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands] <br>
**Output Format:** [Markdown guidance with structured analysis steps and optional shell/browser workflow instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose edits to local reference files during user-triggered knowledge updates.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
