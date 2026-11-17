# 小说转推文分镜

由当前 AI 阅读原文并实际创作推广方案，包括标题、人物/场景、口播与镜头的音画时间线和来源锚点。脚本只校验 AI 写好的 JSON 并排版 Markdown，不会从小说文本机械生成内容。

提供原文或梗概，并说明平台、受众、目标和时长等已知要求，也可明确要求无口播。AI 应把未提供的偏好标记为未提供；原文未知的事实列为待确认；创作补充与原文依据分开。方案至少包含一个镜头；无口播任务可使用空口播时间线并将镜头口播引用设为 `null`。行动引导只在用户要求或明确标注为 AI 建议时加入，不使用固定 CTA。

## 生成文件

由 AI 根据 `references/output-schema.md` 编写完整的 `promo-package.json`，再执行：

```bash
python3 scripts/self_test.py render --input /absolute/ai-promo-package.json --output /absolute/new-output-dir
```

结果包含 `promo-package.json` 和 `promo-package.md`。脚本校验结构、口播/镜头时间、对应引用和缺口状态，不验证引文是否忠于原文。目标文件已存在时拒绝覆盖。

```bash
python3 scripts/self_test.py self-test
```

`examples/success-output.json` 是虚构示例；它展示缺少用户偏好时如何标记未知，以及不默认添加 CTA。
