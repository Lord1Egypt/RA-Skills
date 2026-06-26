## Description: <br>
MDT Consultation coordinates multiple specialist agents to review complex tasks in parallel and synthesize their findings into a structured consultation report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luaqnyin](https://clawhub.ai/user/luaqnyin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to organize multi-agent review of contracts, official documents, campaign plans, strategic decisions, technical designs, medical-plan reviews, and other work that benefits from multiple viewpoints. It produces a combined report that highlights participating agents, agreements, disagreements, risks, and recommended actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive consultation content may be retained in memory without a clear consent or retention boundary. <br>
Mitigation: Before using the skill with contracts, medical plans, strategy documents, personnel matters, or other sensitive inputs, use a no-storage workflow or confirm what will be archived, retention duration, review access, and deletion options. <br>
Risk: Multi-agent consultation reports may include legal, medical, compliance, or strategy recommendations that are incomplete or unsuitable for the user's situation. <br>
Mitigation: Treat the report as decision support and require qualified human review before acting on high-impact recommendations. <br>


## Reference(s): <br>
- [Consultation Guide](references/consultation-guide.md) <br>
- [MDT Evaluation Standard](references/eval.md) <br>
- [MDT Templates](references/templates.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/luaqnyin/mdt-consultation) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown consultation report with structured sections, risk ratings, specialist-agent summaries, and action recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may be archived to memory/mdt-reports when the host agent supports that workflow.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
