## Description:

This skill helps agents write, review, and debug C# trading strategies for the IRS (SunnyQuant Investment Research System) framework.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dameng324](https://clawhub.ai/user/dameng324)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and quantitative trading teams use this skill to create, modify, review, and troubleshoot IRS/SunnyQuant C# strategy projects, including backtesting and live or simulated trading workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports reusable database and web-service credentials in the published skill material.

Mitigation: Install only in an authorized internal environment after the publisher removes the exposed credentials, rotates affected secrets, and replaces them with secure secret-retrieval instructions.

Risk: The security evidence reports under-scoped setup and live-trading guidance for trader projects and account-affecting order examples.

Mitigation: Require explicit user confirmation before running trader projects or producing account-affecting order steps, and review strategy code before simulated or live execution.

Risk: The security evidence calls for pinning or verification of the private NuGet template version.

Mitigation: Pin or verify the IRS template package version before using generated projects in an internal environment.

## Reference(s):

- [IRS Algorithm Reference](references/algorithms.md)
- [IRS Data Access Reference](references/data.md)
- [IRS Strategy Code Examples](references/examples.md)
- [JYDB Data Dictionary Index](references/jydb.md)
- [CommonStrategy API Reference](https://irs_doc.shengguanda.com/docs/api/IRS.Common/CommonStrategy)
- [.NET SDK Download](https://dotnet.microsoft.com/download)
- [Stock.Indicators Documentation](https://dotnet.stockindicators.dev/indicators/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with C# code snippets, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include trading strategy examples, setup commands, parameter suggestions, and troubleshooting steps.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata, released 2026-03-31)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
