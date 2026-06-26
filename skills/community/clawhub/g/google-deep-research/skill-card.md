## Description: <br>
Uses Gemini Deep Research Agent to perform autonomous multi-step research and produce detailed Markdown research reports with citations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[juan-xin-cai](https://clawhub.ai/user/juan-xin-cai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent users use this skill to run long-form Gemini Deep Research sessions, refine vague research topics, and return cited Markdown reports with optional follow-up questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research prompts and follow-up questions are sent to an external Gemini service. <br>
Mitigation: Use explicit user-approved research topics and avoid sending secrets, regulated data, or confidential material unless the deployment policy allows it. <br>
Risk: GOOGLE_GENAI_SDK_PATH can point the runtime at locally selected executable SDK code. <br>
Mitigation: Prefer the npm-published @google/genai package; set GOOGLE_GENAI_SDK_PATH only to a trusted, reviewed SDK path. <br>
Risk: Deep research runs can be broad and long-running, which may create cost, latency, or scope surprises. <br>
Mitigation: Confirm the research scope before execution and use timeout or narrower queries when the task needs bounded runtime. <br>


## Reference(s): <br>
- [@google/genai npm package](https://www.npmjs.com/package/@google/genai) <br>
- [ClawHub release page](https://clawhub.ai/juan-xin-cai/google-deep-research) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown research report on stdout, with progress and interaction status on stderr] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GEMINI_API_KEY; optional GOOGLE_GENAI_SDK_PATH, timeout, streaming, and follow-up settings are supported.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
