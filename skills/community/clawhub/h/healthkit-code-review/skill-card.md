## Description:

Reviews HealthKit code for authorization patterns, query usage, background delivery, and data type handling. Use when reviewing code with import HealthKit, HKHealthStore, HKSampleQuery, HKObserverQuery, or HKQuantityType.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review Swift code that integrates with Apple HealthKit. It focuses the review on authorization semantics, query safety, background delivery, data types, threading, and lifecycle handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HealthKit example snippets could be copied into production apps without sufficient consent, privacy disclosure, or minimum-permission review.

Mitigation: Treat snippets as review examples and require explicit user consent, clear privacy copy, and least-privilege HealthKit permissions before shipping app code.

Risk: Background delivery, sleep, characteristic, write, and server-sync examples touch sensitive health-data workflows.

Mitigation: Evaluate those patterns carefully against the target app's entitlements, user expectations, and secure health-data handling requirements.

## Reference(s):

- [HealthKit Authorization](references/authorization.md)
- [HealthKit Queries](references/queries.md)
- [HealthKit Background Delivery](references/background.md)
- [HealthKit Data Types](references/data-types.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Guidance]

**Output Format:** [Markdown review findings with code references and concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces review observations and questions; it does not execute HealthKit code or access health data.]

## Skill Version(s):

1.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
