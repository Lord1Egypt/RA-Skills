# 个人技能工坊 · 1.0.2 正式版

通过一问一答，把你的工作经验、材料和重复任务整理成可复用的 AI 技能。

**版本：1.0.2 · 作者：FueTsui · 许可：[MIT-0](LICENSE)**

本包为 ClawHub 分发版，沿用已授权的 MIT-0 许可；下方 GitHub 安装命令与发布页提供 MIT 分发版。两者版本均为 1.0.2，技能行为、脚本、模板和行为资源相同，许可证与分发说明有所区别。

## 它能帮你做什么

描述一件想让 AI 反复完成的工作，提供已有材料或好坏样例。工坊会逐次补问关键缺口，吸收你主动补充的要求，整理输入、步骤、输出和完成标准，生成 `SKILL.md` 及必要资源。以后可以使用生成的业务技能完成重复工作，也可以继续通过工坊调整规则。

无需自己编写复杂提示词或填写整套问卷。实际的文件生成、脚本执行和模型能力由所用 AI 工具提供。详见[功能介绍](docs/FEATURES.md)。

## 安装与开始使用

安装 Node.js 和 npm 后，在终端运行这一条全局安装命令：

```text
npx skills add https://github.com/FueTsui/personal-skill-builder --skill personal-skill-builder --agent codex --global
```

技能会安装到当前用户的通用技能目录：`~/.agents/skills/personal-skill-builder`，其中 `~` 表示当前用户目录。

安装后刷新所用 AI 工具的技能列表，在下一轮对话或新会话中读取该目录的 `VERSION` 和 `SKILL.md`，确认版本为 `1.0.2`。不同工具是否支持该目录及调用语法，以实际支持情况为准。详见[安装使用说明](docs/INSTALL.md)。

> 使用 personal-skill-builder，帮我把每周整理工作周报的流程制作成可复用技能。每次只问一个关键问题，信息足够后生成，并用样例验证。

你可以随时补充材料和要求。生成完成后，日常工作调用生成的业务技能；需要改变工作规则时再用工坊升级它。

## 日常使用与升级

假设工坊生成了名为 `weekly-report` 的周报技能，之后每周直接调用它，并提供本次材料：

> 使用 weekly-report，根据附件中的本周记录生成周报，沿用已确认的格式，标出缺少依据的内容。

工作规则或模板变化时，让工坊更新已有技能：

> 使用 personal-skill-builder，根据这份新模板升级已有技能，保留仍有效的要求，保存旧版，并重新验证受影响的场景。

[下载 1.0.2 正式版](https://github.com/FueTsui/personal-skill-builder/releases/tag/v1.0.2)。测试记录和使用限制分别见[实测结果](docs/TEST-RESULTS.md)与[已知问题](docs/KNOWN-ISSUES.md)；本版保留输入保护和自检覆盖方面的已知问题。
