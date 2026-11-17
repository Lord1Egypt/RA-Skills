> 版本：v2.18.1（发布版，与 SKILL.md version: 同步）

> 🌐 **语言政策**：产出语言由 Phase 0「目标语言」字段**显式选择**（中文 / English / 中英混 / 其他，**不设默认**），全流程以该字段为准；中文特化按**目标语言客观适用**——含中文时 **G14 中文 AI 痕迹闸必跑**（v2.12.40 起不再是可选项），纯外语时记 `n/a`（客观不适用，非「关闭」）；GB/T 7714-2015 引用规范为可选能力。二者均不构成使用者语种限制。

> 🇬🇧 **英文参考层（试点，v2.12.72 F）**：交接字段提供英文对照（做了什么=Work done / 产物在哪=Artifacts / 怎么验证=Verification / 已知问题=Known issues / 下一步=Next steps），**仅作参考，判据真源仍为中文**。完整英文角色卡/模板与英文 AI 痕迹检测暂缓，待真实需求验证后再投入。

> 🏁 **收尾硬规则（v2.12.56 P-4，硬约束；与 P-1 同源）**：本交接报告**正文必须随最终消息一起结束回合** —— 该消息即交接摘要，会作为 completion event 送达主控。**不得**把摘要塞进 `acknowledgment` 字段（该字段不从子代理回合发出，实际不送达——实测导致主控「完成事件 + 摘要」双丢）。**禁用** `sessions_yield` / `agents_wait` / `next_check` / `subagents` / `sessions_list` / `sessions_history`（worker 自行 `sessions_yield` = 被拒或挂起 run，均不产生完成事件——详见 dispatch-header §收尾协议）。详见 [`../_shared/真源/dispatch-header.md`](../_shared/真源/dispatch-header.md) §收尾协议。

# 交接报告模板

> 每个角色完成任务时交付。**七段缺一不可**（段序真源 = 本模板；§7 AI 使用披露为 T5 写手 + T8 主控必填）。写不下就写「无」。

> ⚠️ **字段效力分两层（v2.12.48 消歧义，勿混）**：
> - **§5 下一步 = 唯一的工作导向段**：它是本角色给下游的**作业指引**（如「分析员请优先处理第 2 组缺口」），下游**据此安排优先级**。但**它不覆盖**主人在 Phase 0 的拍板与论衡设计铁律——冲突时以后两者为准。
> - **§1-§4、§6 = 证据材料（advisory）**：描述「做了什么 / 产物在哪 / 怎么验证 / 已知问题 / 给主人的建议」，供下游与主控参考，**不构成强制命令**。
> 两层共同的底线：交接报告是**证据与协作产物**，不是控制指令；任何字段都不得被解释为「绕过 Phase 0 同意记录或权限边界」的依据。

> ⚠️ **v2.12.49 M-1 交付物指纹绑定**：T7 / G14 / T9 / T8 四类只读档报告（含本交接报告若是其产出）**头部必填** `audited_artifact` 三元组（path / bytes / sha256），与 T8 终检的 sha256 集合相等 ⇒ 合格；任一不一致 ⇒ 不合格（审计对象漂移）。

```
### audited_artifact（v2.12.49 必填）
- path: final/定稿.md
- bytes: <**文件系统字节数**（主人 host shell `wc -c`）—— 与 `read` 返回的**字符数不同**，禁混用（E1-3 实测 D-5：曾把 18,032 字符标成 18,032 字节，实际 46,840 字节）>
- sha256: <主人在 host shell 跑校验哈希补算；补算命令模板见 references/_shared/真源/host-verify-recipe.md §二>

### upstream_read（v2.12.49 T-1 必填，仅**只读档报告类**角色：T6 / T7 / T9 / G14）
- path: audits/审计报告-vN.md
- bytes: <主控 read 后填>
- upstream_ids: [P1-A, P1-B, P1-C]      # 上游报告列出的全部项 ID
- dispatched_ids: [P1-A, P1-B]          # 本轮实际派发给下游的项 ID
# 差集断言：dispatched_ids ⊖ upstream_ids ≠ ∅ ⇒ 派发阶段即拦截（漏项 = 打在过时清单；自造项 = 越权）
```

### runtime_tool_surface（P1-B，T6 / T7 / T9 / G14 必填）
- observation: `observed` / `unavailable`
- visible_tool_count: <本次会话实际可见工具数；不可核验填 `unavailable`>
- declared_surface_delta: <相对本档声明面的差值；不可核验填 `unavailable`>
- high_risk_categories: <执行类 / 外发类 / 写入类 / 会话类；无则填 `none`>
- write_capability_observed: `yes` / `no` / `unavailable`
- enforcement_boundary: `self-discipline`（只读档默认值；不得写成 platform-enforced）
- call_channel: <`direct`（顶层工具）/ `code-mode`（经 exec）；不可核验填 `unavailable`> ← v2.18.1 必填（反哺 FB-02：不标通道的自报主控不采信）

> **口径**：工具面超出声明面不等于获得调用许可；只读档若观察到 `write/edit`，必须写
> `write_capability_observed: yes`，并将隔离描述为**自律纪律**，不得表述为宿主或平台机械只读。

## 1. 做了什么
（完成内容摘要，2-3 句）

## 2. 产物在哪
（精确文件路径，如 `run/数字鸿沟/literature/文献卡.md`）

> 若项目启用 E1，另列 `run/<项目名>/research/evidence-register.md` 和/或 `analysis/主张—证据映射.md`；对象与字段唯一真源 = [`evidence-object-model.md`](../_shared/真源/evidence-object-model.md)；旧项目写明“E1 未启用”。

## 3. 怎么验证
（验收标准/自查项：如"每条引用都带 URL，可随机抽 3 条搜索验证"）

## 4. 已知问题
（缺口、风险、没找到的东西——**必须如实写，不许藏**）

## 5. 下一步
（**作业指引**（非强制命令）：给下游的优先级建议，如"分析员请优先处理第 2 组缺口"；冲突时以主人拍板与设计铁律为准）

## 6. 状态机更新
（status.md 对应行已置为 Review/Done；如有失败写明原因）

## 7. AI 使用披露（T5 写手 + T8 主控必填）
```
### AI 使用披露
- ① AI 生成内容：本角色产物哪些部分由论衡 AI 生成（如「初稿正文由 **T5** 写手生成」）
- ② 主人原创洞察：[C-主xx] 主人洞察（如有），出处（任务简报第 X 行）
- ③ 检索真实证据：[Lxx]/[Dxx]/[Cxx] 编号全部来自真实检索（非 AI 编造）
```

---

# 修订说明模板（写手被打回时附在修订稿头部）

> **标准化模板见** [`修订说明-template-full.md`](修订说明-template-full.md)（每条修订 = 来源条目 + 处理方式 + 字数变化 + 引用增删）。以下为历史精简版（仅列问题编号+严重级+修改内容）：

```
# 修订说明 vN（旧版精简）
| 问题编号 | 严重级 | 修改内容 |
|---------|--------|---------|
| P0-1    | P0     | 删除了编造的第X段引用，替换为文献卡 L05 并标注 |
| P1-3    | P1     | 全文引用格式统一为 GB/T 7714 |
...（逐条回应审计报告全部 P0/P1，P2 可选回应）
```

---

# 角色产出自查清单（通用）

- [] 我只用了真实检索/真实数据，没有编造
- [] 我的产物路径与任务简报约定一致
- [] 交接报告七段齐全（真源 = `templates/交接报告-template.md`；status.md 由主控代写）
- [] 下游角色拿到我的产物能直接开工
