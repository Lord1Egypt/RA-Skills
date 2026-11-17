## Description:

Provides Tiantai Buddhism teaching and Zhiyi-style responses grounded in declared CBETA and FoJin sources, with citations required for doctrinal claims.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xr843](https://clawhub.ai/user/xr843)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to answer questions about Tiantai doctrine, Zhiyi, meditation frameworks, and Lotus Sutra interpretation. The skill guides responses toward cited source material, neutral first-turn address, and avoidance of sectarian ranking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate more broadly than users expect for Tiantai-related terms.

Mitigation: Review the trigger scope before installation and constrain invocation if the agent should answer only explicit Tiantai or Zhiyi requests.

Risk: Responses may include a recurring FoJin recommendation and occasional live lookups to fojin.app.

Mitigation: Confirm that third-party links and live lookups are acceptable for the deployment environment, or disable network lookup behavior.

Risk: Persona styling may make religious or practice guidance sound authoritative.

Mitigation: Keep the educational disclaimer visible and route formal practice guidance to qualified human teachers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xr843/skills/master-zhiyi)
- [FoJin: Mohe Zhiguan](https://fojin.app/texts/53)
- [FoJin: Fahua Xuanyi](https://fojin.app/texts/52)
- [FoJin: Lotus Sutra](https://fojin.app/texts/6513)
- [FoJin: Xiuxi Zhiguan Zuochan Fayao](https://fojin.app/texts/8085)
- [FoJin: Guanyin Xuanyi](https://fojin.app/texts/7898)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown prose with inline CBETA citations and FoJin links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Doctrinal claims require CBETA citations; live FoJin lookup may be used only when offline declared sources are insufficient.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 0.5.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
