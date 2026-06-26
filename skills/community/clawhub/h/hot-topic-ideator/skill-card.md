## Description: <br>
Generates Xiaohongshu hot-topic ideas and content concepts for brand social media operations, content planning, and trend-based marketing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yyobject](https://clawhub.ai/user/yyobject) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Brand marketers, social media operators, and content strategists use this skill to research Xiaohongshu notes and hot-trend data, then generate 5-10 actionable topic briefs for brand campaigns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends brand, campaign, and keyword data to the external ChatDAM/Tezign API. <br>
Mitigation: Install only if that API is trusted for the provided data, and use a scoped CHATDAM_API_TOKEN. <br>
Risk: The workflow writes report files and can run a local PDF conversion command. <br>
Mitigation: Verify the local html_to_pdf.py converter before running the uv command, and review the output directory before generating files. <br>
Risk: If the primary API fails, the skill may use web search as fallback data collection. <br>
Mitigation: Confirm fallback web searches before sending sensitive brand or campaign inputs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yyobject/hot-topic-ideator) <br>
- [ChatDAM note search API](https://asset.tezign.com/chatdam/api/notes/search) <br>
- [ChatDAM note detail API](https://asset.tezign.com/chatdam/api/notes/detail) <br>
- [ChatDAM hot trends API](https://asset.tezign.com/chatdam/api/hot-trends) <br>
- [Tailwind CSS CDN](https://cdn.tailwindcss.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Single-file HTML report with optional PDF conversion command] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a report.html file under a brand-specific output directory and may invoke a local html_to_pdf.py converter through uv.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
