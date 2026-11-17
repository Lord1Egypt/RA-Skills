## Description:

Analyzes a user's OpenClaw chat history to infer an MBTI-style personality profile, produce structured JSON, and show the result in a visualization page.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archangelxu](https://clawhub.ai/user/archangelxu)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users run this skill to analyze their own chat history, extract user-authored messages, and generate an MBTI-style JSON profile with a short visual summary link. It is intended for personal insight and should be used only where the user is comfortable processing local conversation history through the configured agent LLM backend.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads broad OpenClaw chat history and writes extracted user messages to _mbti_work.

Mitigation: Run it only in a private workspace, review the extracted files before using the result, and delete _mbti_work after the analysis.

Risk: The analysis processes private conversation text through the user's configured agent LLM backend.

Mitigation: Avoid running it on accounts or workspaces that contain secrets, work data, or sensitive personal conversations unless that backend is approved for the data.

Risk: The derived profile and short quotes are opened in a third-party visualization page via URL hash.

Mitigation: Inspect the generated result.json and only open the visualization link when the derived content is acceptable to display in the browser.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/archangelxu/skills/mbti-from-ai)
- [Visualization page](https://www.mingxi.tech/)
- [RFC 3986 Section 3.5](https://datatracker.ietf.org/doc/html/rfc3986#section-3.5)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown instructions and terminal text with bash commands, plus local JSON files under _mbti_work.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates _mbti_work/session_list.txt, _mbti_work/user_messages.txt, and _mbti_work/result.json, then opens a browser URL with the derived profile encoded in the URL hash.]

## Skill Version(s):

0.2.0 (source: SKILL.md frontmatter, skill.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
