## Description: <br>
Analyzes a user's chat history with AI to infer an MBTI personality type from communication style and thinking patterns, then generates structured JSON and opens a visual profile page. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ArchangelXu](https://clawhub.ai/user/ArchangelXu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this skill to scan their local chat history, extract user-authored messages, and produce an MBTI-style behavioral profile with structured evidence and a browser-rendered visualization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill broadly scans local OpenClaw history and consolidates user-authored messages into local plaintext files. <br>
Mitigation: Run it only on chat history you are comfortable profiling; use a reviewed subset of sessions when possible and delete _mbti_work after use if the extracted messages and result should not be retained. <br>
Risk: The extracted messages are analyzed through the user's configured LLM backend. <br>
Mitigation: Install only if that matches the user's expected OpenClaw privacy model and the selected LLM backend is acceptable for the chat content being analyzed. <br>
Risk: The derived profile is opened through a third-party visualization URL containing the encoded result in the URL hash. <br>
Mitigation: Review _mbti_work/result.json before opening or sharing the URL, and avoid sharing the generated link if the profile should remain private. <br>


## Reference(s): <br>
- [mbti-from-ai on ClawHub](https://clawhub.ai/ArchangelXu/mbti-from-ai) <br>
- [Visualization site](https://www.mingxi.tech/) <br>
- [RFC 3986 Section 3.5](https://datatracker.ietf.org/doc/html/rfc3986#section-3.5) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, plus a local structured JSON result and a URL hash for browser visualization] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local _mbti_work files containing discovered session paths, extracted user messages, and the final MBTI profile JSON.] <br>

## Skill Version(s): <br>
0.2.0 (source: server evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
