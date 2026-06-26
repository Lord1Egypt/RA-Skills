## Description: <br>
Generates vertical miniature build and reveal videos using WeryAI from text briefs or finished-shot images, with prompt expansion and confirmation before paid generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zoucdr](https://clawhub.ai/user/zoucdr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, designers, and developers use this skill to turn miniature scene briefs or reference images into vertical WeryAI video generations, including shallow-depth push-ins, lights-on reveals, and diorama motion shots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paid runs send prompts, public image URLs, and explicitly uploaded local images to WeryAI with WERYAI_API_KEY authentication. <br>
Mitigation: Use dry-run first, avoid sensitive prompts or images, and set the API key only in an environment where the publisher and WeryAI are trusted. <br>
Risk: Local image paths can be read and uploaded by the bundled script when used for image-to-video generation. <br>
Mitigation: Prefer public HTTPS image URLs; use local paths only after reviewing the script and confirming the exact file path with the user. <br>
Risk: Each confirmed generation can consume WeryAI credits. <br>
Mitigation: Show the full expanded prompt and all generation parameters, then wait for explicit confirmation before submitting a paid run. <br>


## Reference(s): <br>
- [WeryAI video CLI and JSON reference](resources/WERYAI_VIDEO_API.md) <br>
- [Miniature Build Video on ClawHub](https://clawhub.ai/zoucdr/miniature-build-video) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown with parameter tables, inline shell commands, and JSON-derived video URLs or error details.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WERYAI_API_KEY and Node.js 18+ for paid API calls; dry-run can inspect requests without the key.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence; artifact frontmatter reports 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
