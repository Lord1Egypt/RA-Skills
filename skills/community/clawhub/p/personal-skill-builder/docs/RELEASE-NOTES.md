# 个人技能工坊 1.0.2 · 正式版发布说明

作者：FueTsui。许可：[MIT-0](../LICENSE)。发布日期：2026-10-15（Asia/Shanghai）。发行标签：`v1.0.2`。

个人技能工坊通过一问一答，把工作经验、已有材料和重复任务整理成可复用的 AI 技能，支持补充要求、修改规则和记录验证结果。

本包为 ClawHub 同步分发版；GitHub 链接所指同版本包使用 MIT，当前 ClawHub 文件使用 MIT-0，沿用此前明确授权的分发方式。

## 本版内容与发布范围

本版将 `1.0.2-dev.10` 晋升为 `1.0.2` 正式版，统一版本标识、安装与下载说明、发布元数据和公开实测摘要。晋升过程中不修改技能行为、脚本、模板或行为资源，也未重新运行模型生成测试。

相较 1.0.1，开发阶段已加入数值与日期有效域检查、CSV 物理起始行号、冲突信息保留、需求强度与范围追溯、跨字段与交付视图的受限内容清理、规范拒坏矩阵及 Windows UTF-8 入口处理。开发过程见[更新记录](../CHANGELOG.md)。这些改动的当前证据和未通过项分别记录于[实测结果](TEST-RESULTS.md)及[已知问题](KNOWN-ISSUES.md)。

## 安装与下载

安装 Node.js 和 npm 后，在终端运行：

```text
npx skills add https://github.com/FueTsui/personal-skill-builder --skill personal-skill-builder --agent codex --global
```

安装目录为 `~/.agents/skills/personal-skill-builder`，其中 `~` 表示当前用户目录。命令读取仓库当前版本；安装后刷新技能列表，并读取实际目录的 `VERSION` 和 `SKILL.md`，确认本次发行版本为 `1.0.2`。详见[1.0.2 安装说明](https://github.com/FueTsui/personal-skill-builder/blob/v1.0.2/docs/INSTALL.md)。

[v1.0.2 发布页](https://github.com/FueTsui/personal-skill-builder/releases/tag/v1.0.2)提供 `personal-skill-builder-1.0.2.zip` 和 `SHA256SUMS.txt`。ZIP 根目录为 `personal-skill-builder/`，含完整技能资源、公开文档及包内 `MANIFEST.sha256` 文件清单。

## 实测摘要与尚存问题

2026-10-15 对 `1.0.2-dev.10` 进行 Sol / high 与 Terra / high 各一次独立生成。每份生成程序分别使用 2026-10-15 和 2026-10-10 两个截止日运行冻结业务回归，两模型在每个截止日均为 **321/321**；金额专项均为 **13/13**。两个截止日是同一程序的两次运行，不是两次模型生成。

仍有两项问题：

- **DEV10-P1：** Terra 的生成程序在输入 CSV 与输出 `list.csv` 同路径时覆盖源文件。执行前备份输入，并把输入与输出目录分开。
- **DEV10-P2：** Terra 漏掉需求追溯档案中的规则弱化、规则删除、范围缩窄三类拒坏变异。逐项核对任务全部适用档案，补齐缺失证据；现有矩阵通过不能代替完整覆盖。

以上为临时规避和核对方法，问题未在本次晋升中修复。正式版标签表示发行状态，不代表全部验收通过；每模型仅有一次生成样本，不能推算长期可靠率。完整多轮访谈、冷恢复、宿主自动发现、无技能对照及任意中文金额表达等未在本轮验证。历史 1.0.1 / RC7 结果在实测与已知问题文档中单列保留，不计入本轮通过数。

原始对话、私人材料、账号信息及完整实验日志不随公开包分发。公开摘要见[实测结果](TEST-RESULTS.md)、[已知问题](KNOWN-ISSUES.md)和[机器可读结果](../evidence/RESULTS.json)。
