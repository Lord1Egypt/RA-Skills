# 小说剧本转分镜

当前 AI 阅读用户提供的原文并完成实际改编，输出包含人物、场景、动作、对白、镜头和时长的分镜。辅助脚本只校验 AI 写好的 JSON 并生成 Markdown，不会读取小说、拆场或创作镜头。

## 使用

可以直接提供小说/剧本片段并说明目标时长、画幅和风格。要求 AI 忠于原文，并将未知动机、关系或因果标为待确认；新增创作表达要单独注明。

需要文件时，由 AI 按 `references/schema.md` 创建完整 `storyboard.json`，再运行：

```bash
python3 scripts/self_test.py render --input /absolute/ai-storyboard.json --output /absolute/new-output-dir
```

得到 `storyboard.json` 和 `storyboard.md`。脚本只校验结构、状态与时长合计，不证明原文对应关系或创作质量；已存在输出文件时拒绝覆盖。只有材料不足时才使用 `needs_more_source`，不生成占位分镜。

自测：

```bash
python3 scripts/self_test.py self-test
```

`examples/success-output.json` 是虚构示例，供理解字段，不是脚本从原文自动生成的成品。

## 许可

本 Skill 代码与说明采用 MIT License。它不包含第三方 Skill 的代码或文案。
