## Description:

根据商品参考图和可选卖点文案生成按顺序交付的电商详情页图片套图。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

电商运营人员和商家使用商品参考图、可选主题与卖点文案，制作新品或更新商品的详情页图片套图。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the external qhkit package can run unreviewed tooling.

Mitigation: Confirm the package is trusted and prefer a reviewed or pinned version when reproducibility matters.

Risk: Generation requires an API token and uploads product images to the iqinghu service.

Mitigation: Confirm the service is trusted and obtain consent before uploading sensitive product materials.

Risk: Adding tools to shell startup files changes future sessions.

Mitigation: Keep PATH changes limited to the current session unless persistent access is intentional.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/linkpix-detail-page)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [iqinghu API keys](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Image URLs, Text]

**Output Format:** [Text with ordered image URLs and credits charged]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Multiple images form one detail-page set; generated images cannot be edited in place.]

## Skill Version(s):

0.1.6 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
