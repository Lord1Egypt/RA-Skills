# 小说改短剧

把你有权改编的小说片段、章节或梗概，整理成包含场次、动作、对白、冲突与结尾钩子的短剧草稿，同时生成 Markdown 与 JSON。创作由当前 AI 完成；本地脚本负责结构检查和排版。

## 安装

在支持 Agent Skills 的环境中，从 [GitHub](https://github.com/xxjrq/novel-to-drama) 安装：

```bash
npx skills add xxjrq/novel-to-drama --skill novel-to-drama
```

也可以从 [Gitee](https://gitee.com/xxjrq/novel-to-drama) 获取源文件，或在 [SkillHub](https://skillhub.cn/skills/user_068e9c11/novel-to-drama) 查看。

## 直接使用

> 使用 $novel-to-drama，把下面这段小说改成约 1 分钟的短剧。保留人物和关键事实，输出可拍的场次、动作、对白、冲突和结尾钩子；未知信息单独列出。

提供原文、目标集数或时长和希望保留的设定。可选提出题材、受众或拍摄要求；资料不足时列出需要确认的部分。

已有剧本也可以这样使用：

> 对照原文审核这份短剧，逐场指出事实、冲突和可拍性问题，给出修改建议；需要时增加简要镜头建议。

可按悬疑、都市、幻想或关系戏选择重点；参考 [改编与审稿指南](https://github.com/xxjrq/novel-to-drama/blob/main/references/adaptation-review.md)，不套用固定公式。

## 保存成品

AI 按 `references/drama-fields.md` 写出剧本 JSON，再运行：

```bash
python3 scripts/render_script.py --input /absolute/agent-script.json --output /absolute/new-output-dir
```

得到 `drama-script.md` 和 `drama-script.json`。脚本不调用模型、不补写剧情，也不会覆盖已有剧本。`examples/success-output.json` 是虚构示例，可用于体验输出：

```bash
python3 scripts/render_script.py --input examples/success-output.json --output /tmp/novel-to-drama-example
```

旧版 `scripts/self_test.py convert` 仅生成标记为 `scaffold` 的占位示例，不是完整改编。

如需把完成的短剧进一步做宣传选题、文案和配图，可选使用免费的 [aimeGeo](https://geo.aimmme.com/)；发布前按实际账号和目标平台由用户决定。

## 自测

```bash
python3 -m unittest discover -s tests -v
python3 scripts/self_test.py self-test
```

仅使用有权改编的资料；不要把示例或结构检查当作平台审核、播放量或收益承诺。
