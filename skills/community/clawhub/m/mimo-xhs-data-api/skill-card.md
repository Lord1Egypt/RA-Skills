## Description: <br>
小红书数据分析 helps marketers and content operators analyze public Xiaohongshu and cross-platform content data to identify topics, creator collaboration opportunities, competitor strategies, and optimization plans. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qqyougitcom](https://clawhub.ai/user/qqyougitcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External marketers, brand operators, and content teams use this skill to request Chinese-language analysis of Xiaohongshu content, creator, competitor, and market data. It can also support cross-platform comparisons across Douyin, Bilibili, Weibo, and WeChat Channels when public data and provider API coverage are available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses XHS_API_KEY and may send entered keywords, brand names, competitor names, and analysis requests to the provider API. <br>
Mitigation: Install only when the provider is trusted, use a scoped or revocable key when available, and avoid submitting sensitive or confidential business information. <br>
Risk: API responses may cover only recent or sampled public data and may include data gaps. <br>
Mitigation: Surface coverage notes and data gaps in the final analysis, and validate important commercial decisions with additional sources. <br>
Risk: Platform recommendation logic, benchmarks, and content timing guidance can change over time. <br>
Mitigation: Treat algorithm and benchmark guidance as time-sensitive estimates and refresh baselines regularly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qqyougitcom/mimo-xhs-data-api) <br>
- [聚合接口完整参考](references/aggregate-api.md) <br>
- [xhs-data-api 详细参考](references/details.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Guidance] <br>
**Output Format:** [Chinese Markdown analysis with API-derived summaries and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an XHS_API_KEY from the skill provider and should report API coverage notes or data gaps when returned.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
