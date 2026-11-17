## Description:

PowPow 계정 가입과 이메일 인증, 원클릭 로그인을 대화로 지원하고 필요하면 선택적 멤버십 결제 주문을 돕습니다.

This skill is ready for commercial/non-commercial use.

## Publisher:

[durenzidu](https://clawhub.ai/user/durenzidu)

### License/Terms of Use:

MIT-0

## Use Case:

PowPow에 가입하려는 사용자가 대화 중 계정을 만들고 이메일 인증 후 원클릭으로 로그인하도록 돕습니다. 사용자가 원하거나 무료 이용이 종료된 경우 멤버십 주문과 결제 상태 확인도 지원하며, 결제 자체는 사용자가 진행합니다.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Account passwords and email verification codes may be exposed during assisted signup.

Mitigation: Provide them only when you intend to register; keep passwords out of command-line arguments and files, and use verification codes only for the official signup flow.

Risk: One-click login links and temporary session data can grant account access.

Mitigation: Treat login links as active sessions, avoid sharing them, and run cleanup after the signup flow.

Risk: Optional membership orders may lead to a payment or recurring subscription.

Mitigation: Create an order only with the user's consent; have the user complete payment on the official checkout and review the selected plan before approving it.

Risk: Remote screenshot fallbacks may be less dependable than packaged assets.

Mitigation: Prefer the screenshots packaged with the skill.

## Reference(s):

- [PowPow 공식 사이트](https://global.powpow.online)
- [ClawHub 스킬 페이지](https://clawhub.ai/durenzidu/skills/powpow-register-ko)
- [가입 절차](references/registration-flow.md)
- [에이전트 가입 흐름](references/agent-flow.md)
- [결제 및 계정 활성화](references/payment-and-activation.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Korean conversational Markdown with signup guidance and login or checkout links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes optional product screenshots and an account summary; requires Node.js 18 or later for assisted signup, with a guidance-only fallback.]

## Skill Version(s):

2.2.0 (source: skill frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
