## Description: <br>
A Chinese-language guide that helps agents verify news claims, check sources, assess media reliability, and present evidence-based fact-check conclusions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KrisLiu16](https://clawhub.ai/user/KrisLiu16) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and employees use this skill to structure news verification: extract claims, compare authoritative sources, check official statements and fact-checking sites, assess source reliability, and report a supported conclusion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fact-checking may require consulting linked third-party sites that can receive submitted text, images, video, or search queries. <br>
Mitigation: Avoid uploading private documents, personal photos, confidential messages, or other sensitive content unless you are comfortable with those services handling it. <br>
Risk: News verification can produce an uncertain or incomplete conclusion when sources are limited, stale, biased, or contradictory. <br>
Mitigation: Cross-check multiple authoritative and official sources, preserve uncertainty labels such as unable to verify or misleading, and cite the evidence used for the conclusion. <br>


## Reference(s): <br>
- [Fact-checking methods and tools](references/methods.md) <br>
- [Snopes](https://snopes.com) <br>
- [PolitiFact](https://politifact.com) <br>
- [FactCheck.org](https://factcheck.org) <br>
- [中国谣言粉碎机](https://piyao.sina.cn/) <br>
- [腾讯新闻较真](https://news.qq.com/zt2020/page/feiyan.htm) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown fact-check report with conclusion, key findings, evidence sources, and caveats] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Non-executable guidance; may include links to external fact-checking and image-search services.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
