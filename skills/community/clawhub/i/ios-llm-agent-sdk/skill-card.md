## Description: <br>
Map Agent - iOS LLM Agent SDK guides AI coding tools through AMap MALLMKit integration for natural-language map queries, route planning, POI search, navigation control, and IPC communication with the AMap app. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lbs-amap](https://clawhub.ai/user/lbs-amap) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers building iOS map experiences use this skill to integrate AMap MALLMKit Agent SDK and Link SDK behavior. It helps generate code and guidance for natural-language map queries, route and POI handling, navigation controls, authorization, IPC connection management, data transfer, and troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated iOS code may include AMap SDK credentials or custom backend URLs. <br>
Mitigation: Review credential handling before release, keep secrets out of client-visible logs and source control, and verify custom backend URLs against the app's production configuration. <br>
Risk: Map, navigation, and IPC flows may process location data or change navigation state. <br>
Mitigation: Use clear location permission prompts and require user confirmation before actions that start navigation, change destinations, add waypoints, or alter route behavior. <br>
Risk: IPC authorization, callback URLs, and reconnect behavior can be fragile if copied without validation. <br>
Mitigation: Validate callback URLs and authorization state, test reconnect and disconnect handling, and persist only the minimum authorization state needed by the app. <br>
Risk: SDK or IPC logs may expose sensitive route, POI, location, or authorization details. <br>
Mitigation: Redact logs before sharing or storing them and avoid copying production logs to the clipboard without user intent. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lbs-amap/ios-llm-agent-sdk) <br>
- [Publisher profile](https://clawhub.ai/user/lbs-amap) <br>
- [AMap Open Platform Console](https://console.amap.com/) <br>
- [Agent SDK quick start](artifact/api/quick-start.md) <br>
- [Integrate Agent](artifact/api/integrate-agent.md) <br>
- [Link SDK quick start](artifact/api/link-quick-start.md) <br>
- [Agent core classes](artifact/references/core-classes.md) <br>
- [Link core classes](artifact/references/link-core-classes.md) <br>
- [Link error codes](artifact/references/link-error-codes.md) <br>
- [Troubleshooting](artifact/references/troubleshooting.md) <br>
- [Voice commands](artifact/references/voice-commands.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Objective-C, plist, JSON command, text prompt, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces iOS SDK integration guidance and example code for Agent SDK queries, Link SDK authorization and IPC, navigation command handling, logging, and troubleshooting.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
