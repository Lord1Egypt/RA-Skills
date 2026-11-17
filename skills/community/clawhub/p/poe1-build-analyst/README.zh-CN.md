# PoE1 BD 生成器与验证器

本技能会针对指定版本或赛季，生成可复现的《Path of Exile 1》**仅限终局**分析。它使用用户提供的 PoE Ninja DB 记录、公开角色数据或完整 PoB character code，固定被动树、技能、连接、装备、珠宝和配置来源，然后通过 `qpooqp777/pob-cli` 执行 Path of Building Community 计算。主动工作流程不再生成初期或中期配置。

主动技能默认语言为英文。本地化文档请参考 [`README.zh-TW.md`](README.zh-TW.md)、[`README.zh-CN.md`](README.zh-CN.md)、[`SKILL.zh-TW.md`](SKILL.zh-TW.md) 和 [`SKILL.zh-CN.md`](SKILL.zh-CN.md)。

## 仓库版本

本仓库目前追踪的发布候选版本为 **0.1.2**，版本来源记录在 [`VERSION`](VERSION)。在明确发布更新包之前，ClawHub 仍保持 `0.1.1`；不可将此文件的版本直接视为 ClawHub registry 版本。

## 功能

生成器可以接收赛季、主技能、职业／升华、游戏模式、经济环境、预算和目标。它会取得或接收合法的 Ninja JSON 快照、筛选候选、解释排名，并在本机具备 PoB Community 根目录与 LuaJIT 时验证选定的 PoB XML。

每个结果都会输出一条固定的终局记录。导入的角色数据不会被静默优化或改写：用户提供的被动树、技能、连接、装备、珠宝和配置保持为权威来源。报告包含来源出处、PoB 指标、防御门槛、警告和限制；初期与中期配置会有意省略。

## PoE 3.29 示例

当用户要求“推荐 PoE1 3.29 BD”时，生成器以 **Curse of the Allflame** 作为人类可读的赛季示例，然后核对实际赛季标识并取得带时间戳的数据快照。不可从视频、搜索摘要或人气图表硬编码一个“最强 BD”。

当指定的 3.29 快照确实包含这些候选时，报告可以比较 `Vortex Occultist`、`Kinetic Fusillade Totems Hierophant` 和 `Static Strike Slayer` 等流派家族。这些名称只是查询假设，并不是预先认证的 Tier List；最终选择必须反映用户要求的模式、预算、主技能、防御期望和 PoB 验证状态。

> GGG 官方 3.29.0 公告将挑战赛季列为 Curse of the Allflame，并提供 Standard、Hardcore 和 Solo Self-Found 变体。[1]

## 数据与验证模型

PoE Ninja 被视为统计证据。由于公开构筑页主要由前端动态加载，生成器优先使用合法的 JSON 端点、数据转储、用户提供的导出文件、公开角色数据或 PoB code。它会记录来源 URL、获取时间、赛季、筛选条件、响应 schema 和样本数量，不会绕过身份验证、速率限制或私人角色访问控制。

PoB Community 被视为计算权威。生成器先检查技能、天赋树和装备，再使用明确指定的主技能执行 `pob analyze` 和 `pob calc`。如果缺少 LuaJIT、PoB root 无效、XML 不受支持或计算失败，流程会输出警告并标记为未验证，而不是自行编造数字。

## 终局角色 code 命令

```bash
python scripts/poe1_build_pipeline.py endgame-analyze \
  --pob-code CHARACTER_CODE.txt \
  --pob-root "$POB_ROOT" \
  --skill "Vortex" \
  --class "Witch" \
  --ascendancy "Occultist" \
  --league "Curse of the Allflame" \
  --xml-output endgame_imported.xml \
  --output endgame_report.json
```

此命令会解码完整的 PoB character code，保留导入的天赋树、技能和装备，并调用 `pob analyze` 与 `pob calc`。短的 `https://pobb.in/<id>` 网址不是 character code，会被拒绝；请提供完整 code 或包含完整 code 的文本文件。此命令永远不会上传 BD。

如果要从现有 XML 生成不公开的 code，请使用：

```bash
pob share BUILD.xml --dry-run
```

公开的 `pobb.in` 链接必须另外取得明确确认。“已生成 code”和“已公开 URL”是不同状态。

## 可选的被动树研究工具

`optimize-tree` 子命令仍可用于离线研究与候选比较，但它不会被终局 character-code 工作流程调用。主动工作流程绝不会用优化器结果替换导入的天赋树、技能、连接或装备。

```bash
python scripts/poe1_build_pipeline.py optimize-tree \
  --pob-root "$POB_ROOT" \
  --tree-version 3_29 \
  --class-id 3 \
  --target-nodes 112 \
  --objective cold-dot \
  --objective energy-shield \
  --objective curse \
  --required-node 32417 \
  --build BASELINE.xml \
  --skill Vortex \
  --output-xml optimized.xml \
  --output-json optimized.json
```

可用的 objective 是 `cold-dot`、`energy-shield`、`life`、`curse`、`spell`、`defence` 和 `damage`。必选节点的连接路径会计入节点预算。无法连接的必选路径、断开的候选或无效的 TreeData 版本都会造成硬性失败。此命令是按 objective 加权的 frontier search，不是全局最优解证明；做出最终推荐时，应比较多组 objective。

## 输出 schema

机器可读报告包含赛季、BD 概念、来源 metadata、Ninja 候选、阶段记录、PoB 验证状态、角色 code 状态和警告。人类可读报告会分开四类证据：**Ninja 观察结果**、**官方 PoB 计算**、**人工推荐**和**未验证估计**。

| 主动记录 | 来源 | 决策闸门 |
| --- | --- | --- |
| 仅限终局 | PoE Ninja DB／公开角色数据／完整 PoB character code | 保留导入的天赋树、技能、连接和装备；使用 `pob analyze` 和 `pob calc` 验证。 |

## 内含资源

| 路径 | 用途 |
| --- | --- |
| `SKILL.md` | Manus 加载的英文主动指令。 |
| `scripts/poe1_build_pipeline.py` | JSON 标准化、非上传式 PoB 分析包装器，以及 `optimize-tree` 子命令分派器。 |
| `scripts/poe1_tree_optimizer.py` | 支持必选／排除节点与可选 PoB 计算的连通被动树优化器。 |
| `references/api_reference.md` | API 与 CLI 使用说明。 |
| `references/research_notes.md` | 已验证的限制与 3.29 研究笔记。 |
| `templates/character_build.json` | 机器可读的角色／BD 模板。 |

## 参考资料

[1]: https://www.pathofexile.com/forum/view-thread/3985332 "Content Update 3.29.0 — Path of Exile: Curse of the Allflame"
[2]: https://poe.ninja/poe1/builds "PoE Ninja — Path of Exile 1 Builds"
[3]: https://github.com/qpooqp777/pob-cli "qpooqp777/pob-cli"
