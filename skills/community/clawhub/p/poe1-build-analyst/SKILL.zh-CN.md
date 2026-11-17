---
name: poe1-build-analyst-zh-cn
description: 简体中文参考版：生成、比较并验证指定版本或赛季的 PoE1 BD，支持 PoE 3.29、PoE Ninja 与 qpooqp777/pob-cli。
---

# PoE1 BD 生成器与验证器

## 目标与边界

根据用户指定的版本、赛季、职业、升华、主技能、玩法、模式、预算和目标，生成可复现的 PoE1 BD。PoE Ninja 只代表公开统计快照；Path of Building Community 通过 `pob-cli` 的 headless 计算，才是伤害与防御数值的权威来源。没有兼容 XML 和 PoB root 时，不得把估算值标成官方 PoB 结果。

用户说“PoE 3.29”时，以 **Curse of the Allflame** 作为默认的人类可读示例，但仍需核对实际赛季标识与数据快照。Standard、Hardcore、SSF 必须分开处理，并记录获取时间、赛季、筛选条件、样本数量、PoB／Tree 版本和限制。

## 执行流程

1. **确认输入。** 获取版本／赛季、主技能、职业／升华、SC／HC、Trade／SSF、预算和目标。主技能不能误判为位移、Guard、Aura 或触发技能；如果不明确，先提出候选。
2. **获取 Ninja 数据。** 优先使用合法公开 JSON、数据转储、用户导出文件、公开角色数据或 PoB code。构筑页面是动态前端，不可依赖静态 HTML，也不可绕过登录、速率限制或私人角色权限。记录 URL、时间、schema、筛选条件和样本数量。
3. **标准化并排名。** 每行至少保存 `league`、`patch`、`class`、`ascendancy`、`main_skill`、`level`、`skills`、`items`、`passives`、`keystones` 和来源。排名不可只看 DPS，还要考虑生命／ES、抗性、法术压制／格挡、TotalEHP／MaximumHitTaken、成本和转换难度。
4. **执行 PoB 验证。** 先执行：

```bash
pob skills BUILD.xml --format json
pob skills BUILD.xml --details --pob-root "$POB_ROOT" --format json
pob tree BUILD.xml --all
pob items BUILD.xml
pob analyze BUILD.xml --pob-root "$POB_ROOT" --skill "主技能" --format json
pob calc BUILD.xml --pob-root "$POB_ROOT" --skill "主技能" --format json
```

如果缺少 LuaJIT、PoB root、技能 metadata、兼容 XML 或版本不符，保留 stdout／stderr，标记为 `blocked` 或 `failed`，不要自行重写 PoB 公式。

5. **建立三个阶段。** 初期涵盖剧情至初入地图；中期涵盖稳定黄图／红图；后期涵盖成熟刷图、终局 Boss 或高预算。每个阶段必须列出等级范围、完整技能连接、辅助／防御技能、天赋路线、装备目标、属性／抗性门槛、升级顺序、转换条件、PoB 指标、假设和警告。
6. **生成 JSON 与 code。** 可使用 `scripts/poe1_build_pipeline.py` 保存候选和警告。`pob share BUILD.xml --dry-run` 只生成 code，不得自动上传。`pobb.in` 是公开内容，必须另外取得明确确认。

## 3.29 推荐示例规则

可以把 `Vortex Occultist`、`Kinetic Fusillade Totems Hierophant`、`Static Strike Slayer` 作为查询候选，但只有在指定的 3.29 快照实际包含它们时才能纳入比较。示例名称不是固定 Tier List；最终推荐必须由 Ninja 快照、用户限制和 PoB 验证共同决定。

## 固定输出

报告依次使用：数据来源与假设、推荐与替代方案、初期配置、中期配置、后期配置、Ninja 证据、PoB 验证、角色 JSON／code、风险与下一步。清楚区分 Ninja 观察、官方 PoB 计算、人工建议和未验证估算。每个 DPS 必须说明敌人、Charges、Flask、Buff、Shock／ailment 和 uptime 假设。

## 资源

`references/api_reference.md` 说明端点与命令；`references/research_notes.md` 保存 3.29 与限制；`scripts/poe1_build_pipeline.py` 负责 JSON 标准化和非上传式 PoB 分析；`templates/character_build.json` 是输出模板。英文 [`SKILL.md`](SKILL.md) 是实际加载的默认技能文件。

## 参考资料

[1]: https://www.pathofexile.com/forum/view-thread/3985332 "Content Update 3.29.0 — Path of Exile: Curse of the Allflame"
[2]: https://poe.ninja/poe1/builds "PoE Ninja — Path of Exile 1 Builds"
[3]: https://github.com/qpooqp777/pob-cli "qpooqp777/pob-cli"
