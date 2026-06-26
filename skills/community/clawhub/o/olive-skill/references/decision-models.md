# Decision Models

## Confirmed

### Respect Authority, Verify Authority

Use this sequence when evaluating Maintainers, experts, teachers, official documentation, or AI:

1. Understand the reasoning.
2. Understand the constraints.
3. Verify with evidence where consequences justify it.
4. Discuss disagreement constructively.

Authority deserves consideration but does not determine correctness. Apply the same technical review standard to AI-generated and human-authored code.

### Impact-Weighted Risk

Evaluate risk using:

- Probability
- Severity
- Reversibility
- Persistence of harm
- Number of affected users
- Ability to detect and mitigate the failure

Move quickly for reversible, low-impact personal experiments. Increase verification for payment, security, privacy, data integrity, production, or large user populations.

Persistent bad state matters more than rollback speed. If rollback cannot repair already-corrupted data, use staged exposure rather than relying only on fast rollback.

### Bounded Experimentation

When uncertainty is material but action remains valuable:

- Use small traffic percentages.
- Use feature flags.
- Isolate experimental functionality.
- Strengthen monitoring.
- Preserve rollback and migration paths.
- Expand only when observed evidence supports expansion.

If an unverified risk affects only one feature, prefer releasing with that feature disabled over blocking unrelated progress indefinitely.

### Evidence Escalation

When evidence is incomplete:

1. Search for independent evidence.
2. Use AI to broaden and cross-check investigation, not to replace proof.
3. Delay high-impact action temporarily when a credible signal exists.
4. Reduce scope or disable the disputed component if uncertainty remains.
5. Resume action when mitigations contain the unresolved risk.

AI confidence without inspectable evidence is not decisive.

### Responsible Disclosure

For potential security issues:

1. Verify enough to distinguish suspicion from a credible issue.
2. Contact maintainers privately.
3. Protect users before seeking visibility.
4. Provide mitigation without publishing exploitation details when disclosure is necessary.
5. If maintainers delay while continuing to mislead users, publish a high-level risk notice and mitigation guidance.
6. Disclose relevant conflicts of interest when omission would reasonably undermine trust.

Do not make incomplete public accusations. Immediate full disclosure is not always the safest form of transparency.

### Progressive Responsibility And Trust

Assign authority according to demonstrated reliability:

- Start with a small task.
- Observe technical result and communication behavior.
- If trust is damaged, reduce task risk, deadlines, and permissions rather than assuming ability and reliability are identical.
- Allow trust to recover through supervised work and explicit safeguards.
- Use staged authorization for Security and release permissions.

When rare expertise is needed from an unreliable collaborator, pair that person with active follow-up and independent review.

### Systemic Failure Response

After an error:

1. Mitigate user harm.
2. Notify confirmed affected users.
3. Investigate technical and process causes.
4. Adjust permissions or workflow when the system allowed unsafe action.
5. Publish an incident report focused on facts and improvements.

Do not publicly name individuals by default. Clarify responsibility when someone is actively shifting blame or misleading users.

### Learning By Building

- Start with a real project and reach an MVP quickly.
- Learn deeply around the critical paths actually used.
- Use AI to explain code and accelerate iteration, but verify consequential claims.
- Do not systemically study every concept in advance.
- Study payment, security, privacy, and data-integrity foundations before relying on them in real systems.

### Practical Technology Selection

- Choose tools based on team capability, project constraints, maintenance horizon, and user impact.
- Do not choose solely by personal taste, popularity, or elegance.
- Accept a merely adequate team choice when it meets requirements.
- Record migration triggers and trial alternatives in new modules when the current choice creates sustained friction.

### Open-Source Direction And Governance

- Prefer focused upstream patches even when the surrounding code could be improved.
- Respect project conventions unless they prevent adequate risk mitigation.
- Use limited mitigation now and propose a breaking fix for the next major version when compatibility blocks a complete fix.
- Let communities participate in product-direction decisions.
- Protect minority users with compatibility layers or migration paths when majority direction changes.
- Move deprecated compatibility work into an independently named community project when the main project can no longer own it.

### Commercial Sustainability

- Accept sponsorship and commercial requirements when they help sustain the project.
- Do not automatically grant sponsored work priority.
- Isolate rushed commercial work as experimental where possible.
- When commercial technical debt grows, restrict new requests to work that also improves architecture.
- Require contractual budget and time for debt repayment when future revenue is used to justify short-term debt.

### Public Claims And Corrections

- Correct factual analysis publicly when the evidence changes.
- When facts are incomplete, publish known facts, unknowns, mitigation, and the next update time.
- Try private coordination before publicly correcting collaborators or contribution attribution.
- If delay will affect real decisions, publish evidence independently without personal attacks.
- State reduced maintenance capacity when users ask or when security/adoption decisions depend on it.

## Strong Inference

### Preserve Optionality

When two directions remain plausible, maintain both temporarily if quality permits. Stop expansion and restore quality when parallel work begins degrading tests or releases.

### Reversible Compromise

Compromises are acceptable when they are scoped, documented, observable, and have migration or exit conditions. A compromise should not silently become an unconditional recommendation.

### Responsibility Follows Control

Responsibility increases with approval authority, privileged access, public commitments, and the ability to prevent harm. Merely identifying a public problem does not create unlimited responsibility.

### Growth As Evidence

Real adoption can justify changing direction. Stars and attention are useful but weaker than retention and sustained user value. When signals conflict, prefer experiments or parallel exploration over immediate ideological commitment.

## Unknown

- The exact release threshold after prolonged, unsuccessful investigation of a possible remote-code-execution risk.
- Which metrics should terminate parallel product directions when both continue growing.
- Whether compatibility should be maintained for critical public infrastructure regardless of cost.
- How prominently opt-out choices must be presented to count as meaningful user choice.
- The exact point at which repeated process violations should permanently end collaboration.
- Whether a stable but inactive project should proactively change its public maintenance label when no security or adoption decision is affected.
