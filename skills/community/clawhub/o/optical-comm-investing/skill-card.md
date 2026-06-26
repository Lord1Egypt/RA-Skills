## Description: <br>
AI optical-communications investment analysis framework that helps analyze related stocks, compare technology routes, map supply-chain positions, evaluate target quality, and optionally refresh its reference notes from public Xueqiu posts when explicitly triggered. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seanweisean](https://clawhub.ai/user/seanweisean) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to structure optical-communications sector research, compare InP, silicon photonics, TFLN, CPO, NPO, XPO, and OCS themes, and assess companies mentioned in its reference pack. Users can also explicitly trigger an update workflow to append new public-post summaries to local reference notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional update workflow can use a logged-in browser session and modify local reference notes. <br>
Mitigation: Run update mode only when explicitly intended, avoid sensitive shared browser profiles where possible, and review appended reference-file changes afterward. <br>
Risk: Investment-analysis outputs can become stale or reflect source-specific viewpoints. <br>
Mitigation: Treat outputs as research support, check current market and company disclosures, and preserve uncertainty when newer information conflicts with existing references. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/seanweisean/optical-comm-investing) <br>
- [Core Framework](references/core-framework.md) <br>
- [Technology Landscape](references/tech-landscape.md) <br>
- [Supply Chain](references/supply-chain.md) <br>
- [Methodology](references/methodology.md) <br>
- [Update Log](references/update-log.md) <br>
- [闷得而蜜 Xueqiu Profile](https://xueqiu.com/u/5672579962) <br>
- [查尔斯大风车 Xueqiu Profile](https://xueqiu.com/u/8755156034) <br>
- [查尔斯大风车 2026-04-21 Article](https://xueqiu.com/8755156034/384873103) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands, configuration] <br>
**Output Format:** [Markdown text with structured investment-analysis sections and optional reference-update instructions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Core analysis uses static reference files; optional updates may append summarized public-post content to local reference notes when explicitly requested.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
