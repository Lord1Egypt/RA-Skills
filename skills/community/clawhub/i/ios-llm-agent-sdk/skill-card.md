## Description:

Map Agent is an AMap MALLMKit SDK integration skill for iOS that helps agents generate code and guidance for natural-language map queries, route planning, POI search, navigation control, and IPC with the AMap app.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lbs-amap](https://clawhub.ai/user/lbs-amap)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to integrate AMap MALLMKit into iOS applications, including Agent SDK setup, natural-language map interactions, navigation lifecycle handling, and Link SDK communication with the AMap app.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles location, navigation, IPC, and logs, which can expose privacy and safety risks if generated code is adopted without review.

Mitigation: Review generated code before deployment, add explicit user consent for location use and route-changing commands, and redact or disable raw logs in production.

Risk: Custom Agent URLs and persisted IPC authorization state can weaken integration safety if used without validation.

Mitigation: Avoid untrusted custom Agent URLs and revalidate IPC authorization instead of relying only on NSUserDefaults.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lbs-amap/skills/ios-llm-agent-sdk)
- [AMap Open Platform Console](https://console.amap.com/)
- [Quick Start](api/quick-start.md)
- [Integrate Agent](api/integrate-agent.md)
- [Link Quick Start](api/link-quick-start.md)
- [Agent Core Classes Reference](references/core-classes.md)
- [Link Core Classes Reference](references/link-core-classes.md)
- [Link Error Codes Reference](references/link-error-codes.md)
- [Troubleshooting](references/troubleshooting.md)
- [Voice Commands Reference](references/voice-commands.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with Objective-C code examples, shell commands, configuration snippets, and integration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are sample integration material for iOS projects and should be reviewed before use in production apps.]

## Skill Version(s):

1.0.2 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
