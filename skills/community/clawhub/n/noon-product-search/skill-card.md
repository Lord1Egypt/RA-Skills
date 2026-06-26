## Description: <br>
Noon 商品搜索工具。输入阿拉伯语关键词，使用 Chrome 浏览器在 noon.com/saudi-ar 搜索，返回商品标题、评分、评价数和价格。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freemanwangfuhan-coder](https://clawhub.ai/user/freemanwangfuhan-coder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search Noon Saudi Arabia with Arabic keywords and collect product listing details such as title, rating, review count, and price from browser-based search results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports under-disclosed stealth browser automation and browsing behavior broader than the description promises. <br>
Mitigation: Review the skill before installing, treat the output scope as broader than first-page search results unless the implementation is changed, and confirm the behavior matches your intended use. <br>
Risk: The skill relies on Chrome automation and may use Chrome remote debugging or browser sessions. <br>
Mitigation: Run it only in a clean browser profile with no logged-in accounts and avoid leaving Chrome remote debugging enabled after use. <br>
Risk: The skill depends on Node browser-automation packages. <br>
Mitigation: Pin or inspect the Node dependencies before running the skill in a trusted environment. <br>


## Reference(s): <br>
- [Noon Saudi Arabia](https://www.noon.com/saudi-ar/) <br>
- [ClawHub skill page](https://clawhub.ai/freemanwangfuhan-coder/noon-product-search) <br>


## Skill Output: <br>
**Output Type(s):** [text] <br>
**Output Format:** [Plain text product listing summaries printed to the terminal] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Attempts to return deduplicated product entries with title, rating, review count, and price when detected.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
