## Description: <br>
Helps agents optimize Amazon listings by gathering competitor product data and reviews, then drafting titles, bullet points, backend search terms, VOC analysis, and optional IP-risk reports with Pangolinfo tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pangolinfo](https://clawhub.ai/user/pangolinfo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, operators, and agent users use this skill to rewrite and optimize Amazon listing copy from competitor listings, review signals, category data, and optional IP checks. It is intended for listing optimization workflows, not product research, daily monitoring, or single-ASIN lookup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Pangolinfo credentials and may cache access in local configuration or environment variables. <br>
Mitigation: Prefer API keys over account passwords, store keys only in the intended Pangolinfo configuration path or environment variable, and remove cached keys when access is no longer needed. <br>
Risk: Tool calls can consume Pangolinfo credits, especially review, AI search, and Rufus-style query workflows. <br>
Mitigation: Use the skill's fast mode by default, present cost and time estimates before slow or higher-cost calls, and monitor Pangolin credit usage. <br>
Risk: Generated listing and IP-risk guidance may be incomplete or unsuitable for final legal or marketplace compliance decisions. <br>
Mitigation: Review copy before publishing, verify trademark or design-patent concerns independently, and consult qualified IP counsel before major production or inventory decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pangolinfo/pangolinfo-amazon-listing-optimization) <br>
- [Pangolinfo publisher profile](https://clawhub.ai/user/pangolinfo) <br>
- [Pangolinfo website](https://www.pangolinfo.com) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, API Calls, Guidance] <br>
**Output Format:** [Markdown with structured listing drafts, tables, and inline tool-call guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Amazon title drafts, five bullet points, backend search terms, VOC matrices, category warnings, IP-risk notes, and setup guidance for Pangolinfo credentials.] <br>

## Skill Version(s): <br>
3.1.0 (source: evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
