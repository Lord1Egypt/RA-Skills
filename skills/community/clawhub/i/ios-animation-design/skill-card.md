## Description: <br>
Design and plan iOS animations with structured specs for transitions, micro-interactions, gesture-driven motion, loading states, and implementation-ready motion recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and designers use this skill to plan iOS animation approaches, decide between system-provided and custom motion, and produce implementation-ready animation specs covering triggers, timing, accessibility, haptics, interruption behavior, and recommended Apple APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary notes that skill workflows can run powerful local or authenticated commands when invoked. <br>
Mitigation: Review proposed actions before execution and avoid granting local credentials or authenticated CLI access unless those actions are explicitly intended. <br>
Risk: Animation guidance can create accessibility or usability issues if motion is excessive, non-interruptible, or used as the only signal. <br>
Mitigation: Require every animation spec to include Reduce Motion fallback, interruption behavior, and multimodal feedback such as haptics or announcements when needed. <br>


## Reference(s): <br>
- [Animation Pattern Library](references/animation-patterns.md) <br>
- [Timing & Easing Guidelines](references/timing-guidelines.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown with structured animation specs, option comparisons, tables, and Apple API references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include SwiftUI or UIKit API names and concise implementation notes; no external tool execution is required.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
