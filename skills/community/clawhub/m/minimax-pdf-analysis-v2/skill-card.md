## Description: <br>
Analyze PDF files using MiniMax API. Supports text extraction, keyword search, and image-based VLM analysis (converts PDF pages to images first). Requires MiniMax Coding Plan API key (sk-cp-*). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jlin53882](https://clawhub.ai/user/jlin53882) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to extract text from PDFs, search PDF text for snippets, and analyze selected PDF pages with MiniMax vision models after converting pages to images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Vision analysis sends selected PDF pages, prompts, and converted page images to MiniMax using MINIMAX_API_KEY. <br>
Mitigation: Use the vision mode only with PDFs and prompts approved for external processing, scope API credentials appropriately, and prefer extract or search mode when external model analysis is not required. <br>
Risk: The bundled JavaScript helper includes web search and arbitrary image upload capabilities beyond the documented PDF workflow. <br>
Mitigation: Review or remove scripts/minimax_coding_plan_tool.js when the deployment only needs PDF text extraction, PDF search, or the Python vision workflow. <br>
Risk: Local image files passed to the helper can be uploaded to MiniMax for image understanding. <br>
Mitigation: Restrict helper access to trusted local files and require user approval before sending non-PDF images or sensitive document pages to the API. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jlin53882/minimax-pdf-analysis-v2) <br>
- [MiniMax platform](https://platform.minimaxi.com) <br>
- [MiniMax Coding Plan VLM endpoint](https://api.minimax.io/v1/coding_plan/vlm) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with inline shell commands, plain-text PDF extraction and search results, and text analysis returned from MiniMax VLM calls.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python, node, PyMuPDF, and MINIMAX_API_KEY. Vision mode converts selected PDF pages to PNG images before sending them with the prompt to MiniMax.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
