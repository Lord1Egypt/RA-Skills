## Description:

用户指定 GPT Image 2.6 / 智慧模型2.6，要把商品图换成白底、清除背景、逐件处理一批商品或交付透明 PNG 时使用。按平台规范拆分任务并写好提示词，报价经用户确认后出图；没有 CLI 或密钥时交付可直接提交的出图方案。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

电商运营者可用此技能为商品参考图规划白底图、批量商品图或透明 PNG 处理。它会整理逐张提示词和参数；环境可用时先报价并等待用户确认，再生成和核对图片。

### Deployment Geography for Use:

中国（技能所述 API 流程要求使用 cn 站点）

## Known Risks and Mitigations:

Risk: CLI 包会在没有安装提示的情况下安装并运行，且本次安全分析覆盖不完整。

Mitigation: 安装和运行前检查包及版本并确认接受；将 benign 评估视为有限结论，因为扫描未覆盖所有引用。

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/linkpix-gpt-image-2-6-white-background)

## Skill Output:

**Output Type(s):** [Images, Markdown, JSON, Guidance]

**Output Format:** [商品图片；或 Markdown 出图方案与 JSON 参数文件]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [按商品逐项拆分任务；透明 PNG 需核验实际 Alpha 通道；出图前报价并等待用户确认。]

## Skill Version(s):

0.1.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
