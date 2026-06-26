## Description: <br>
Redirect: jingdong has been merged into jd-shopping. Use jd-shopping for JD.com search, review checks, price comparison, SKU selection, and safe cart preparation. Safe boundary: no login, no order submission, no payment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this legacy entry point to route old jingdong requests to the maintained jd-shopping skill for JD.com search, review checks, price comparison, SKU selection, and safe cart preparation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The legacy redirect may activate on broad JD.com or Jingdong mentions. <br>
Mitigation: Use it to route users to jd-shopping and keep purchase, login, payment, and final order actions manual. <br>
Risk: Shopping guidance can become stale because prices, stock, delivery terms, coupons, and after-sales terms change. <br>
Mitigation: Rely on browser-visible or user-provided information and have the user recheck final purchase details before acting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/harrylabsj/jingdong) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance] <br>
**Output Format:** [Markdown or plain text handoff guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Redirects legacy jingdong requests to jd-shopping while preserving manual checkout and payment boundaries.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release evidence and package metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
