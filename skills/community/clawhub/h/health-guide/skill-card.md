## Description: <br>
의료/건강 상담 스킬로, 10개 인텐트 라우팅을 통해 증상, 병원, 질환, 의약품, 응급, 건강검진, 예방접종, 생활습관, 정신건강, 의료 입문 질문에 Flash 및 Deep-Dive 형식의 정보를 제공합니다. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sw326](https://clawhub.ai/user/sw326) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to route Korean health-related questions, gather official-source or web-search-backed information, and produce concise health guidance with emergency and medical-disclaimer handling. It is for general health information, not diagnosis, prescription, or treatment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Health questions may include sensitive personal or medical information. <br>
Mitigation: Avoid entering identifying medical details and treat generated responses as general information rather than diagnosis, prescription, or treatment. <br>
Risk: Hospital search may call a separate local hira-hospital script with user-supplied location and specialty inputs. <br>
Mitigation: Review the hira-hospital dependency separately before deployment and inspect proposed shell commands before execution. <br>
Risk: The skill can send health-related queries to external official APIs or web search providers. <br>
Mitigation: Use official sources where possible, disclose web-search fallback when used, and review output for accuracy and recency before relying on it. <br>
Risk: API keys are configured in local files under user configuration directories. <br>
Mitigation: Protect configured API-key files with appropriate local file permissions and avoid sharing them in prompts, logs, or generated output. <br>


## Reference(s): <br>
- [Health Guide ClawHub page](https://clawhub.ai/sw326/health-guide) <br>
- [Intent Router](references/intent_router.md) <br>
- [Output Templates](references/output_templates.md) <br>
- [Source Tiers](references/source_tiers.md) <br>
- [Korea National Health Information Portal](https://health.kdca.go.kr) <br>
- [Korea public drug information API](https://www.data.go.kr/data/15075057/openapi.do) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown health-information reports with optional shell commands for hospital search delegation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Flash responses are always produced; Deep-Dive responses are used on request or for supported information-heavy intents.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; SKILL.md frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
