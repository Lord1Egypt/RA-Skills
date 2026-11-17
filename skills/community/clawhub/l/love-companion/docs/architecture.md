# Love Companion v2 架构设计

> 依据：《LoveCompanion_开发与优化交接方案》
> 里程碑拆解见：`../love-companion-v2-里程碑拆解.md`（工作区根目录）
> 状态：**M0–M8 全部实现**（2026-09）。296 项回归测试全绿，develop 分支。

## 实施记录（一句话）

形态仍是 Skill 包（SKILL.md + references/ + scripts/），向 Agent 级进化：
`scripts/` 从单文件 `manager.py` 长成一套离线引擎，SKILL.md 只承载在线轻注入策略。
v1 的 8 套人设、`/恋人…` 指令、manager.py API、数据目录全部保留，升级无损可回退。

## 能力全景（各模块解决什么问题）

| 能力 | 解决的问题 | 落地位置 |
|---|---|---|
| 人格三层提取 | 从聊天记录/日记/社媒里提炼声线、思维、性格，让伴侣说话像本人 | `scripts/persona/extract.py` |
| 人设适配 | 提取结果一律回写进 v1 `persona.json`，保证人设只有一个真相源 | `scripts/persona/adapt.py` |
| 人格库进化 | 增量 merge、对话纠偏即时生效、每次更新自动存档可回滚 | `scripts/persona/library.py` |
| 趋势感知 | 把离线抓到的热点提炼成一句能开口的话题，按可聊度取舍 | `scripts/trends/` |
| 语气控制 | 回复贴合对方语气，并拦下中文恋爱对话里的 AI 腔 | `scripts/style/` |
| 双向镜像 | 关系阶段、共鸣、演化建模、一致性自检、元认知反馈 | `scripts/persona/mirror.py` |
| 极简注入 | 「能不注入就不注入」的分级预算阶梯 | `scripts/pipeline/injector.py` |

## 设计取舍——为什么这样定，而不是那样

> 下表记录已经**定稿**的关键决策。改动前先读，避免把推翻过的方案又改回来。

| 备选做法 | 为什么不适合 love-companion | 这里的做法 |
|---|---|---|
| 另建一套人格文件，与 v1 `persona.json` 并存 | v1 已有 `persona.json` 人设体系 + 8 套预设。两套并存会出现**两个人设**：`/恋人配置` 改的是 A，蒸馏出来的是 B，谁也说不清谁生效 | 三层提取只是**中间产物**，一律经 `persona/adapt.py` 回写进 v1 字段；在线注入的是 `lover_card()` 编译的**恋人行为卡**（含亲密尺度与内容边界） |
| 把伴侣人格当成对陌生人的观察记录 | love-companion 是恋人陪伴，且用户已有显式安全设置 | 蒸馏**无权改动**亲密尺度 / 内容边界 / 对用户的称呼（`adapt.IMMUTABLE_FIELDS`）；这三样只认用户显式设置 |
| 用「双轴」等另一套组织方式描述人格 | 方案 3.3 已规定三层：声线 / 思维 / 性格 | 只保留「增量 merge + 实时纠错 + 版本回滚」的机制外壳，本体严格按三层来 |
| 追求 13+ 平台的抓取覆盖与安装器 | 恋人陪伴不需要全网接入能力，只需要**一句能开口的话**；平台清单没人看得懂也没人用 | 只留 3 个真用得上的源；核心是 `talkability()` 可聊度 + `opener()` 聊天切口，而非平台数量 |
| 沿用英文写作的 AI 特征词表 | 英文论文腔的词汇表搬到中文恋爱对话几乎无用 | 词表换成**中文恋爱对话**真正的 AI 腔：空洞安慰、客服式共情、替用户断言情绪、万能陪伴宣言 |
| 按通用审美构图来配图 | 恋人发图不是配图，是**把此刻的生活递给对方看** | 拍什么由 v1「关心方式」决定，能拍多近由「亲密尺度」决定，不能拍什么由「内容边界」决定 |

**love-companion 的硬性需求**（方案原文，必须守）：

- 依恋差异化关怀（方案 4.3）：焦虑型给确定性、回避型给空间、安全型自然陪伴、恐惧型两者都给
  → `care/templates.py::ATTACHMENT_TWEAK`
- 内容边界一票否决：用户写的是祈使句「不谈前任」，真正的禁区是「前任」
  → `core/boundary.py` 把祈使句还原成关键词，被 回复自检 / 趋势取舍 / 配图元素 三处复用
- 8 套预设即人设：没蒸馏过素材的用户，`prepare()` 直接从 `persona.json` 出行为卡；
  反之人设为空壳时不注入（默认值不是用户意图，注入了就是噪音）

---

## 一、形态与边界

**仍是 Skill 包**，不是独立应用。这一点决定了所有架构选择：

| 维度 | 约束 |
|---|---|
| 分发 | SKILL.md + references/ + scripts/ 的文件集合，ClawHub / SkillHub / 虾评分发渠道不变 |
| 依赖 | **只依赖 Python 标准库**，零第三方库（用户装不上，也不能要求装） |
| 存储 | 本地文件，沿用 `~/.love-companion/data/`（可用 `LOVE_COMPANION_DATA_DIR` 覆盖） |
| 执行 | 离线管线由宿主机（Agent 框架 / 系统任务）触发；在线只读取离线产物 |
| 兼容 | v1 的 8 套人设、`/恋人…` 指令、manager.py API、数据目录全部保留 |

---

## 二、核心原则（红线，贯穿所有模块）

1. **离线重处理、在线轻注入**——特征提取、记忆抽取、人格编译、网页抓取、Humanizer 改写全部后台完成，原始内容绝不进对话
2. **单轮额外系统开销 ≤ 300–500 Token**
3. **真实性零容忍**——注入的每条记忆 / 人设特征 / 画像必须可溯源（条目 id + 原文），禁止编造
4. **隐私优先**——采集经隐私过滤，支持单条删除、批量导出、一键清除

---

## 三、在线 / 离线边界

```
┌─────────────── 离线（重活，不占对话 Token）───────────────┐
│ pipeline/   任务队列：注册 · 调度 · 重试 · 落盘          │
│ memory/     无感采集 → 六类记忆 → 检索索引               │
│ persona/    素材摄取 → 三层提取 → 人格库 → 编译人格摘要   │
│ user/       流式采集 → 两级分析 → User Persona → 相处指南 │
│ style/      Humanizer 三层黑名单校验（后处理）            │
│ trends/     抓取 → 解析 → 流行语/热点提炼                │
└────────────────────────┬───────────────────────────────┘
                         │ 产出「注入摘要」（短文本 + Token 计数）
                         ▼
┌─────────────── 在线（轻注入）────────────────────────────┐
│ SKILL.md 运行时读取摘要 → 拼进 System Prompt             │
│ 预算：相处指南<200 · 记忆Top-3<150 · 人格指令<100       │
│       趋势<50 · 关怀话术<80    合计 ≤500 Token           │
└──────────────────────────────────────────────────────────┘
```

Token 预算定义与校验入口：`scripts/core/schema.py::DEFAULT_INJECTION_BUDGET`。
注入前统一走 `pipeline/` 的注入器做计数与超限时截断/拒注——**预算不是建议值，是硬约束**。

---

## 四、目录结构

```
love-companion/
├── SKILL.md                  # 技能主文件（v1 指令体系 + v2 轻注入策略）
├── README.md
├── LICENSE
├── references/               # 人设预设（唯一数据源）、指令手册、教程
├── docs/
│   └── architecture.md       # 本文件
├── tests/
│   ├── test_manager.py       # v1 能力 + v2 schema/迁移（20 项）
│   ├── test_v2.py            # M1 + M2
│   ├── test_v3.py            # M3b + M4
│   ├── test_v4.py            # M3a + M5 + M6
│   ├── test_v5.py            # M7a + M7b + M7c
│   └── test_v6.py            # M8 联调与压测
└── scripts/
    ├── manager.py            # v1 配置与记忆管理（保留，向后兼容）
    ├── core/
    │   ├── schema.py         # v2 数据 schema：记忆/画像/人格库/设置/预算
    │   └── privacy.py        # 隐私过滤（手机号/身份证/银行卡/邮箱/微信号…）
    ├── migrate/
    │   └── migrate_v1.py     # v1→v2 数据迁移（自带备份，无损可回退）
    ├── pipeline/
    │   ├── queue.py          # M1 任务队列：优先级 · 重试 · 死信
    │   ├── injector.py       # M1 注入器：预算硬约束，超限截断/丢弃
    │   ├── runner.py         # M1 对话间隙调度（run_idle）+ 任务注册表
    │   ├── orchestrator.py   # M8 端到端编排：prepare → after_reply → proactive
    │   └── audit.py          # M8 Token 审计与最坏情况压测
    ├── memory/               # M2 记忆系统（store/extract/retrieve）
    ├── persona/              # M3a 人格克隆（parser/extract/library）+ M5 mirror.py
    ├── user/                 # M3b 恋人式用户理解（profile/guide）
    ├── style/                # M4 语气贴合（voice）+ AI 腔守门（humanizer）
    ├── care/                 # M6 主动关怀（trigger/templates）
    ├── trends/               # M7a 趋势感知（sources/store）
    ├── multimodal/           # M7b 多模态（image_plan）
    └── panel/                # M7c 控制与安全感（explain/controls）
```

---

## 五、数据 schema（v2.0）

定义：`scripts/core/schema.py`。要点：

- **6 类记忆**：事实 / 偏好 / 里程碑 / 共享事件 / 情绪 / 人设特征
- **记忆条目字段**：`id · type · content · source · importance · valence · recall_count ·
  created_at · updated_at · last_recalled_at · conversation_id · schema_version`
- **v2 是 v1 的超集**：v1 条目只有 `id/content/created_at`，v2 完整保留并追加元数据 →
  v1 的 `manager.py` 可直接读取 v2 数据，升级无损、可回退（测试里有断言覆盖）
- **User Persona**：沟通风格 / 大五 / 依恋类型 / 情绪模式 / 互动偏好（均带置信度）
- **克隆人格**：声线 / 思维 / 性格 三层 + 版本（「关系面」由 mirror.py 的阶段参数表达，不落进人格文件）
- **衰减参数**：重要性半衰期 30 天、每次召回 +0.05、下限 0.05（默认值；用户在 settings.json 里可调，代码真实读取）
- **注入预算**：同上——settings.json 里的「注入预算」深合并进默认表，orchestrator 每轮按它分配
- **采集开关**：settings.json「隐私.采集开关」关闭后，记忆与信号一条不采

### 数据文件可靠性（排查整改后）

- 所有 JSON 读写统一走 `scripts/core/storage.py`：`read_json` 坏文件自动备份为 `.bad-<时间戳>` 并返回默认值；`write_json` 临时文件 + `os.replace` 原子替换
- settings 统一走 `scripts/core/settings.py`：深合并（用户只覆盖写明的叶子），坏文件降级为默认模板
- 数据目录解析统一走 `core/settings.resolve_data_dir`（入参 > 环境变量 > 默认路径）

---

## 六、迁移策略

`python scripts/migrate/migrate_v1.py --data-dir ~/.love-companion/data`

1. 整目录备份到 `backup_v1_<时间戳>/`
2. `memory.json` 条目补齐为 v2 结构（content 一字不改）
3. 缺失则生成 `settings.json`
4. **不删除任何原文件**；出问题用备份覆盖即可回退
5. `--dry-run` 可先预演，不落盘

---

## 七、里程碑映射与完成状态

| 模块 | 里程碑 | 方案阶段 | 优先级 | 状态 |
|---|---|---|---|---|
| pipeline/（队列·注入器·调度） | M1 | 阶段 1 | P0 | ✅ |
| memory/ | M2 | 阶段 2 | P0 | ✅ |
| persona/（克隆） | M3a | 阶段 3 | P0 | ✅ |
| user/ | M3b | 阶段 4 | P0 | ✅ |
| style/ | M4 | 阶段 6 | P0 | ✅ |
| persona/mirror.py（融合 persona × user） | M5 | 阶段 5 | P0 | ✅ |
| care/ | M6 | 阶段 7 | P0 | ✅ |
| trends/ | M7a | 阶段 8 | P1 | ✅ |
| multimodal/ | M7b | 阶段 9 | P1 | ✅ |
| panel/ | M7c | 阶段 10 | P1 | ✅ |
| pipeline/orchestrator.py + audit.py（联调） | M8 | — | P0 | ✅ |

---

## 八、技术决策（实施时已拍板）

| # | 决策点 | 结论 | 理由 |
|---|---|---|---|
| 1 | 记忆语义检索选型 | 零依赖打分（字符重叠 + 时间 + 重要性 + 关系路径） | 不能要求用户装第三方库 |
| 2 | 依恋 / 情绪识别 | 可解释的规则引擎 | 能给用户看「为什么这么判断」，也便于 `/恋人修正` 覆盖 |
| 3 | 三个开源依赖接入方式 | **按理念自研**，复用其规则集与决策逻辑 | 拿不到可直接嵌入的源码；自研保证零依赖与可维护 |
| 4 | 多模态图片来源 | 本模块只产出**配图规格 + 提示词 + 衔接话术**，出图交给上层图像能力 | 保持零依赖，审美由人格字段决定而非临场发挥 |
| 5 | 离线管线触发方式 | **对话间隙自动跑**（用户拍板） | 单次调用有上限（默认 8 个任务），绝不让离线活儿拖慢对话 |
| 6 | 方案 Token 数字冲突 | 单模块上限降级为「最多能给多少」，**总预算 500 为硬约束**，空模块不占额度 | 原表 580 > 红线 500，两者无法同时成立 |

---

## 九、已知外部约束（不是代码能解决的）

1. **主动消息**：`care/` 与 `multimodal/` 的「主动开口 / 主动发图」能否真的发出去，
   取决于 IM 通道是否支持主动推送。不支持时退化为「下次对话开头带一句」。
2. **趋势抓取**：`trends/sources.py` 只产出抓取计划（primary + fallback 链），
   不发网络请求——小红书/B站/微博都需要登录态或 JS 渲染，标准库抓不到。
   抓回来的原文交给 `trends/store.py` 离线提炼。
3. **人格蒸馏质量**：规则层提取可复现，但语义层蒸馏仍依赖 LLM 按模板跑。
   语料量越大置信度越高（`置信度 ≈ 语料量/200`）。

---

## 十、测试

```bash
python -m unittest discover -s tests -t .
```

| 文件 | 覆盖 |
|---|---|
| `test_manager.py` | v1 能力回归：8 套预设逐字段一致、称呼回归、缓存隔离、坏 JSON 定位、方案与记忆 CRUD、CLI 冒烟；v2 schema 校验、预算红线、v1→v2 迁移无损与向下兼容 |
| `test_v2.py` | M1 管线（队列/重试/死信）+ M2 记忆（采集脱敏/检索/衰减/数据主权） |
| `test_v3.py` | M3b 用户理解（流式信号/两级分析/依恋识别/相处指南）+ M4 语气与 Humanizer 三层守门 |
| `test_v4.py` | M3a 人格克隆（三种导出排版/三层提取/merge/纠偏/版本回滚）+ M5 镜像（演化/共鸣/一致性/反馈）+ M6 关怀（三道闸门/四类信号/声线话术） |
| `test_v5.py` | M7a 趋势（源路由/故障转移/提炼/预算）+ M7b 配图（闸门/风格/衔接）+ M7c（可解释/权重/遗忘/导出清除） |
| `test_v6.py` | M8 联调：端到端一轮、模块开关生效、预算压测、全链路溯源与纠偏生效 |

全程使用临时数据目录，不触碰用户真实数据。
