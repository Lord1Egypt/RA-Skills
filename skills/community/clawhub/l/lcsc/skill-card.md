## Description: <br>
通过 camoufox-cli 浏览器自动化操作立创商城，完成元器件搜索、查看详情、加入购物车、BOM 配单、PCB/SMT 下单等操作。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SinKy-Yan](https://clawhub.ai/user/SinKy-Yan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, electronics engineers, and procurement users use this skill to automate LCSC component search, product detail review, cart management, BOM matching, PCB/SMT ordering, and order lookups through a browser. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct an agent through shopping, cart, file-upload, account, and order workflows where unintended changes may have financial or account impact. <br>
Mitigation: Use it only for clearly requested LCSC tasks, require a summary of planned changes, and obtain explicit approval before modifying carts, uploading BOM or PCB files, submitting orders, exporting cookies, or using an authenticated session. <br>
Risk: Browser automation can act on stale or misread page state during component selection, pricing, inventory checks, or order steps. <br>
Mitigation: Re-read the current page state after navigation or clicks, present key item, quantity, price, stock, and destination details to the user, and wait for confirmation before committing changes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/SinKy-Yan/lcsc) <br>
- [LCSC Storefront](https://www.szlcsc.com/) <br>
- [LCSC BOM Tool](https://bom.szlcsc.com/bom.html) <br>
- [JLC PCB Order Page](https://www.jlc.com/newOrder/#/pcb/pcbPlaceOrder) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and browser-action summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May operate authenticated shopping, upload, and order workflows through camoufox-cli; summarize intended changes and obtain explicit approval before cart, file upload, order, cookie, or account-session actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
