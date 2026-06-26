---
name: 变更日志
description: MktClaw 版本演进历史 — 仅作参考，不影响运行时行为
version: "5.2.1"
---

# MktClaw 变更日志

> **本文档仅作历史参考**。运行时不需要加载。当前版本信息以 `SKILL.md` 和 `config.yaml` 为准。

---

## v5.5.0-b（当前 — 九维评审优化）

> 本版本基于 VC + CTO + CPO + AI Agent 架构师联合评审结果实施

| 类别 | 变更 | 文件 | 评审维度 |
|------|------|------|:-------:|
| **开源生态** | 新增 CONTRIBUTING.md / CODE_OF_CONDUCT.md / Issue Templates / pyproject.toml | 新增 4 文件 | 开源生态 |
| **CI/CD** | 重写 harness-ci.yaml 指向 mktclaw 路径，集成 version_sync 检查 | `.github/workflows/harness-ci.yaml` | 技术架构 |
| **版本管理** | 新增 `scripts/version_sync.py` — SSOT 驱动版本一致性检查 + 自动修复 | 新增脚本 | 风险隐患 |
| **Triple Loop 安全** | 新增 Learning Gate（置信度计算 + 安全降级 + 回滚计划 + A/B 评估建议） | `scripts/learning_engine.py` | 风险隐患 |
| **管道集成** | harness_runner 集成 gate_verdict 驱动 L6.5 行为决策 | `scripts/harness_runner.py` | 风险隐患 |
| **Agent 通信** | 新增字段透传合约（8 字段 + 三层验证 + 交接门禁） | `agents/transition-agent.md` | Agent 体系 |
| **审计日志** | 新增 `scripts/audit_logger.py` — WHO/WHAT/WHEN/RESULT 四维审计 | 新增脚本 | 企业落地 |
| **API 服务** | 新增 `scripts/server.py` — FastAPI 骨架（/v1/health + /v1/intake） | 新增脚本 | 商业化 |
| **版本同步** | 修复 config.yaml runtime_harness.version 5.4.0→5.5.0 | `config.yaml` | 技术架构 |
| **版本同步** | shared refs 组件版本未动（独立组件版本号，不与 SSOT 同步） | — | 风险隐患 |

## v5.2.1（历史）

| 类别 | 变更 | 影响 | 改进来源 |
|------|------|------|:-------:|
| **懒加载** | 从 prompt-based 升级为 **tools/ 目录 + Read 工具联动的实际工具化** | 解决 MarTech 评估"概念的工具化而非工程的工具化" | MarTech |
| **隐私合规** | 新增 `privacy-compliance.md`（GDPR/CCPA/PIPL）+ 数据留存/删除机制 | 解决 CMO/MarTech 评估"缺少隐私合规声明" | CMO/MarTech |
| **国际化** | 新增 3 个海外行业库（日本/东南亚/北美）→ **扩展至 8 个市场**（+韩国/欧洲/中东/中亚/非洲） | 解决 CMO 评估"仅中国市场" → 覆盖全球主要区域 | CMO |
| **品牌安全** | 新增 `brand-safety.md`（三层安全过滤 + 调性匹配矩阵 + 平台安全） | 解决 CMO 评估"缺少 Brand Safety" | CMO |
| **API 接口** | 新增 `api-spec.md`（RESTful API + MCP Server + Webhook） | 解决 MarTech/Agency 评估"没有 API" | MarTech/Agency |
| **方法论** | 新增 Byon Sharp / IPA Databank / VBFS / Effie 四套核心方法论 | 解决 Agency CEO 评估"方法论覆盖不够深" | Agency |
| **可观测性** | 新增 `telemetry.md`（性能埋点 + 自动降级触发联动） | 解决 MarTech 评估"缺少性能监控" | MarTech |
| **多租户** | Campaign Vault 按 Brand/BU 隔离 | 解决 CMO/MarTech 评估"多品牌隔离缺失" | CMO/MarTech |
| **同质化检测** | 新增 `fingerprint.md`（4 维指纹向量 + 阈值告警） | 解决 Agency CEO 评估"方案结构趋同风险" | Agency |
| **运行时护栏** | Layer 3 重写为与 tools/ 目录联动 + 质检门禁新增懒加载验证 | 解决评估"仍依赖 Agent 自觉" | MarTech |
| **Campaign Vault** | 自动捕获机制（Agent 自动输出 JSON 块） | 解决 CMO 评估"严重依赖手动 YAML" | CMO |
| **data-connector** | 数据生命周期声明（原始上传 30 天 vs Vault 24 月） | 解决语义张力 | — |
| **Pitch 模式** | 新增自动降级策略（Token > 35K 自动降级） | 解决 CEO 评估"Token 消耗增加" | CEO |
| **Eval 用例** | 40 → **50 条**（+10 条 v5.2.1 新场景） | 测试覆盖更全面 | 全体 |

---

## v5.2

| 维度 | v5.1 | v5.2 | 改善 |
|------|------|------|------|
| 合规执行 | Agent 自检 | **框架层硬拦截**（runtime-guard.md） | Blocker 命中即阻断，用户不可豁免 |
| 懒加载 | 提示词规约 | **工具化加载**（load_industry_knowledge / load_shared_protocol） | 从软约束升级为工具调用 |
| 行业覆盖 | 3 行业 | **10 行业全覆盖**（+ 教育/母婴/医美/汽车/SaaS/服饰/金融） | 85% → 100% 行业覆盖 |
| 工作模式 | 串联 | **+ Pitch 模式**（N Agent 并行 + Tournament） | 从"串联咨询"升级为"虚拟 Agency Pitch Day" |
| 数据壁垒 | 无 | **Campaign Vault**（用户私有投放数据库） | 越用越懂你 |
| 能力边界 | 未声明 | **明确声明**（客户政治/战略决策/突破性创意等豁免） | 不夸大能力 |
| 共享协议数 | 5 | **8**（+ runtime-guard / parallel-generate / campaign-vault） | 工程化程度 +60% |
| Eval 用例 | 30 条 | **40 条**（+10 条 v5.2 新场景） | 测试覆盖 +33% |

---

## v5.1

| 类别 | 变更 | 影响 |
|------|------|------|
| **行业垂直层** | 新增 `references/industries/`（3 行业 + 扩展规范） | 解决"通用框架套所有行业"导致的平庸 |
| **合规护栏** | 新增 `compliance-protocol.md`（三层合规） | 解决品牌安全护栏不足 |
| **创意多样性** | 新增 `creative-diversity-protocol.md` | 解决创意同质化风险 |
| **数据接入** | 新增 `data-connector.md` | 解决数据闭环缺失 |
| **Tournament 升级** | Swiss-System + 置信区间交叉验证 | 解决"冷门爆冷" |
| **评估升级** | + LLM-as-Judge 语义评分 | 解决 regex 无法评估方案质量 |
| **路由升级** | + embedding 语义兜底 | 解决长尾场景漏判 |
| **Intake 升级** | industry 必检 + data_sources 推荐 + compliance_risk 标记 | 上下文透传更完整 |
| **Router 升级** | industry 字段透传 + 合规风险标记 | 串联全链路 |
| **Type Agent 升级** | 引用行业知识库 + 合规前置 | 输出更专业 |
| **Eval 扩充** | 21 → 30 条（+9 条行业/创意/合规/数据） | 测试覆盖更全面 |

---

## v5.0

| 类别 | 变更 |
|------|------|
| **架构** | 三层冷热分层（Hot/Warm/Cold） | 全量加载 Token 降 ~76% |
| **共享层** | 新增 `references/_shared/quality-protocol.md` + `brief-output-spec.md` | 消除 10 份 screener + 10 份 evaluator 重复 |
| **Agent 精简** | 33 文件 → 13 文件（每 type 从 3 → 2） | 维护成本降 ~60% |
| **用户界面** | 工作流从 5 阶段黑盒为 3 阶段（Clarify→Deliver→Confirm） | 学习曲线降 ~60% |
| **模式简化** | 3 种（Fast/Expert/Standard）→ 2 种（Fast/Standard） | 用户决策负担 -33% |
| **质检抽取** | Tournament + Adversarial 抽到共享层 + 领域专属叠加 | 单点优化全局生效 |

---

## v4.3

| 类别 | 变更 |
|------|------|
| 新增资源 | Creative Brief 模板 / 营销方法论库 / 平台实操手册 / Benchmark 数据库 / CLM / 品牌架构 / A/B 测试 / 市场调研 / AI 创意工具 / 品牌健康追踪 |
| Brief 升级 | Intake Agent 输出从"需求摘要"升级为"标准 Creative Brief" |
| 方法论引用 | 10 个 Agent 均补充经典方法论引用 |
| 危机升级 | 危机公关角色增加强制升级路径 |
| 数据兜底 | 预算/受众/调性/KPI 缺失时引用 Benchmark 自动补全 |
