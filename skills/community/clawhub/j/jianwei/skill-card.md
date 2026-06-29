## Description: <br>
Jianwei is a dual-engine strategic insight skill that generates hypotheses, verifies them with targeted evidence, and produces evidence-backed recommendations for strategy, market, industry, and competitive analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tuobadaidai](https://clawhub.ai/user/tuobadaidai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business leaders, strategists, consultants, and analysts use Jianwei to evaluate strategic decisions such as market entry, competitive threats, business model shifts, and strategic transformation. The skill routes the work through hypothesis generation, targeted verification, feasibility checks, red-team critique, and audit-oriented review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation wording may cause the skill to engage on general business, market, or competitive research prompts. <br>
Mitigation: Review and narrow trigger wording or require explicit invocation when deployment should be limited to intentional strategic-analysis requests. <br>
Risk: Strategic recommendations can depend on incomplete market, competitor, or organization evidence. <br>
Mitigation: Require source, method, timeliness, and confidence labels for important claims, and keep citation checks and human review before acting on recommendations. <br>
Risk: Long-form strategy reports may be mistaken for final business decisions. <br>
Mitigation: Treat outputs as decision support, keep red-team and audit sections visible, and require accountable stakeholder signoff for material actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tuobadaidai/jianwei) <br>
- [Coherent Actions](references/engine-judgment/coherent-actions.md) <br>
- [Diagnosis and Guidance](references/engine-judgment/diagnosis-guidance.md) <br>
- [Hypothesis Generation and Screening](references/engine-judgment/hypothesis-generation.md) <br>
- [Insight Generation Mechanisms](references/engine-judgment/insight-generation.md) <br>
- [Premise Check](references/engine-judgment/premise-check.md) <br>
- [Red-Team Protocol](references/engine-judgment/red-team.md) <br>
- [Constitutional Audit and Citation Check](references/engine-verification/constitutional-audit.md) <br>
- [Cost Quantification](references/engine-verification/cost-quantification.md) <br>
- [Directed Verification](references/engine-verification/directed-verification.md) <br>
- [Hypothesis Debate](references/engine-verification/hypothesis-debate.md) <br>
- [Complexity Routing](references/shared/complexity-routing.md) <br>
- [Output Specification](references/shared/output-spec.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown strategic analysis reports with evidence chains, Mermaid diagrams, action plans, validation records, and audit notes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce long-form Chinese strategic reports; S-level routing targets 8000-12000 Chinese characters and requires confidence labels and citation checks.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release, target metadata, artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
