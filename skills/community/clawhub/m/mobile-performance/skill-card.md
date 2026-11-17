## Description:

Measures and fixes Android, iOS and Flutter app performance: startup (Baseline Profiles, App Startup, iOS launch time), jank (Compose recomposition, SwiftUI body cost, Flutter UI vs raster thread), memory leaks, app size, battery and network use. Uses Macrobenchmark, Perfetto, LeakCanary, Instruments, MetricKit, Flutter DevTools and Android vitals. Use when an app is slow to start, janky, leaking, too big or draining battery, or when asked to profile or benchmark.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahmadhussain0335](https://clawhub.ai/user/ahmadhussain0335)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and mobile engineers use this skill to profile and improve Android, iOS, and Flutter app startup, frame performance, memory, size, battery, and network use through repeatable measurements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Android performance testing can leave app-specific testing settings altered after the test.

Mitigation: Use a dedicated test device, record the settings changed for testing, and restore them afterward. Review any background capability changes before release.

Risk: Telemetry uploads may include device identifiers or other personal data.

Mitigation: Follow the skill's privacy guidance and disclose or handle uploaded identifiers as personal data.

## Reference(s):

- [Android performance reference](references/android.md)
- [iOS performance reference](references/ios.md)
- [Flutter performance reference](references/flutter.md)
- [Performance measurement reference](references/measuring.md)
- [ClawHub skill page](https://clawhub.ai/ahmadhussain0335/skills/mobile-performance)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown performance report with measured metrics, code examples, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports device, OS, build, tool, run count, before-and-after metrics, evidence, unmeasured items, and follow-up; do not estimate unavailable measurements.]

## Skill Version(s):

1.0.1 (source: frontmatter, ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
