# low-altitude-guardian

> 低空设备危机应急响应技能包 — OpenClaw / ClawHub Skill

[![ClawHub](https://img.shields.io/badge/ClawHub-low--altitude--guardian-blue)](https://clawhub.com/skills/low-altitude-guardian)
[![Version](https://img.shields.io/badge/version-0.2.0-brightgreen)]()
[![Stage](https://img.shields.io/badge/stage-alpha-red)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()

面向低空经济场景的无人设备（无人机、eVTOL、无人配送车等）突发危机应急响应技能包。通过 **感知 → 记录 → 分析 → 匹配 → 决策 → 执行 → 复盘** 的完整闭环，帮助设备在遇到突发情况时自主选择**最优最小损失**规避方案，并持续迭代自身的危机处理能力。

**v0.2.0 新增**：支持企业级应用 — 帮助企业收集运营数据、构建专属知识库、自动生成定制化应急预案、进行机队数据分析与运营优化。

---

## 核心设计

### 损失优先级金字塔

所有决策严格遵守不可逆转的优先级排序：

```
┌─────────────────┐
│  P0: 人员安全    │  ← 绝对最高，不可妥协
├─────────────────┤
│  P1: 公共安全    │  ← 公共设施、交通
├─────────────────┤
│  P2: 第三方财产  │  ← 他人车辆、农作物
├─────────────────┤
│  P3: 本机安全    │  ← 设备自身
├─────────────────┤
│  P4: 任务完成    │  ← 原定任务
└─────────────────┘
```

**硬性否决规则**：人员安全评分 < 80 的方案**无条件淘汰**，无论总分多高。

### 双层架构（v0.2.0）

```
┌─────────── 企业管理层 (v0.2.0) ──────────┐
│  知识库管理 → 预案生成 → 机队分析         │
│       ↑ 数据上传          ↓ 方案下发      │
├──────────── 设备执行层 ─────────────────┤
│  态势感知 → 危机分级 → 方案匹配 →        │
│  执行监控 → 事件上报 → 自迭代学习        │
└──────────────────────────────────────────┘
```

### 10 阶段闭环

**设备端（Phase 1-7）**

| 阶段 | 说明 | 脚本 |
|------|------|------|
| Phase 1 | 态势感知与情况记录 | `situation_awareness.py` |
| Phase 2 | 危机分级(L1~L5)与分类 | `crisis_engine.py --classify` |
| Phase 3 | 方案匹配 + 最优评分 | `decision_manager.py --match` |
| Phase 4 | 执行监控与动态调整 | `crisis_engine.py --monitor` |
| Phase 5 | 事件记录与分级上报 | `incident_reporter.py` |
| Phase 6 | 知识库自迭代学习 | `crisis_engine.py --learn` |
| Phase 7 | 特殊场景处理 | 完全失控 / 多机协同 / 法规合规 |

**企业端（Phase 8-10，v0.2.0 新增）**

| 阶段 | 说明 | 脚本 |
|------|------|------|
| Phase 8 | 企业知识库管理 | `enterprise_kb_manager.py` |
| Phase 9 | 应急预案生成 | `emergency_plan_generator.py` |
| Phase 10 | 机队数据分析 | `fleet_analytics.py` |

### 危机等级体系

| 等级 | 名称 | 响应时限 | 人工介入 |
|------|------|---------|---------|
| **L5** | 灾难性 | < 3秒 | 自主执行，事后通知 |
| **L4** | 严重 | < 10秒 | 自主执行，同步通知 |
| **L3** | 重大 | < 30秒 | 推荐方案，5秒超时自动执行 |
| **L2** | 一般 | < 2分钟 | 等待操作员确认 |
| **L1** | 注意 | < 5分钟 | 仅提醒，操作员决策 |

### 决策评分公式

```
Score = 0.40×S0(人员) + 0.25×S1(公共) + 0.15×S2(财产) + 0.12×S3(本机) + 0.08×S4(任务)
```

---

## 快速开始

### 安装

```bash
# 通过 ClawHub 安装
clawhub install low-altitude-guardian

# 或 clone 本仓库
git clone https://github.com/AAAlenwow/low-altitude-guardian.git
```

### 设备端演示

```bash
# 完整危机响应演示（单电机失效场景）
python3 scripts/crisis_engine.py --demo

# 事件报告演示
python3 scripts/incident_reporter.py --demo

# 查看所有解决方案模板
python3 scripts/decision_manager.py --list-templates
```

### 企业端演示（v0.2.0 新增）

```bash
# 企业知识库管理
python3 scripts/enterprise_kb_manager.py --demo          # 完整演示
python3 scripts/enterprise_kb_manager.py --status         # 查看知识库状态
python3 scripts/enterprise_kb_manager.py --health-check   # 健康度检查
python3 scripts/enterprise_kb_manager.py --search "电机故障"  # 搜索知识库

# 应急预案生成
python3 scripts/emergency_plan_generator.py --demo        # 生成示例预案
python3 scripts/emergency_plan_generator.py --generate \
  --company "顺丰低空物流运营部" \
  --scope "城市无人机配送" \
  --device-type multirotor                                # 自定义预案

# 机队数据分析
python3 scripts/fleet_analytics.py --demo                 # 完整分析演示
python3 scripts/fleet_analytics.py --report               # 生成分析报告
python3 scripts/fleet_analytics.py --device-health        # 设备健康评分
python3 scripts/fleet_analytics.py --compliance-report    # 生成合规报告
```

### 企业数据导入

```bash
# 从 CSV 批量导入历史事件（模板见 assets/enterprise_templates/）
python3 scripts/enterprise_kb_manager.py --ingest \
  --source incident_log \
  --file data/history.csv

# 导入行业案例
python3 scripts/enterprise_kb_manager.py --ingest \
  --source industry_case \
  --file cases/case_001.json

# 导入厂商通告
python3 scripts/enterprise_kb_manager.py --ingest \
  --source vendor_bulletin \
  --file bulletins/dji_safety_notice.json
```

---

## 预置解决方案

| 模板 | 危机类型 | 适用等级 | 历史成功率 |
|------|---------|---------|-----------|
| 单电机失效 | `power_failure.single_motor_loss` | L3 | 92% |
| 全动力丧失 | `power_failure.total_power_loss` | L4-L5 | 65% |
| GPS 信号丢失 | `navigation_failure.gps_loss` | L2-L3 | 88% |
| 通信链路断开 | `communication_failure.link_lost` | L2-L3 | 95% |
| 极端天气 | `environment_threat.severe_weather` | L2-L4 | 90% |

知识库无匹配时自动启动**应急推理**（分解子问题 + 组合策略 + 第一性原理），新方案验证有效后自动入库。

---

## 项目结构

```
low-altitude-guardian/
├── SKILL.md                                  # 技能定义（ClawHub 入口）
├── scripts/
│   ├── crisis_engine.py                      # 核心引擎（分级/匹配/监控/学习）
│   ├── situation_awareness.py                # 态势感知
│   ├── decision_manager.py                   # 决策管理
│   ├── incident_reporter.py                  # 事件记录与上报
│   ├── enterprise_kb_manager.py              # [v0.2.0] 企业知识库管理
│   ├── emergency_plan_generator.py           # [v0.2.0] 应急预案生成器
│   └── fleet_analytics.py                    # [v0.2.0] 机队数据分析
├── assets/
│   ├── solution_templates/                   # 解决方案知识库（5个预置模板）
│   ├── device_profiles/                      # 设备类型配置
│   └── enterprise_templates/                 # [v0.2.0] 企业导入模板
│       ├── data_ingestion_csv_template.csv   #   CSV 数据导入模板
│       ├── plan_config_template.json         #   预案配置模板
│       └── kb_health_check_template.json     #   知识库健康检查配置
├── references/
│   ├── crisis_taxonomy.md                    # 危机分类学（6大类 30+ 子类）
│   └── decision_priority_matrix.md           # 决策优先级矩阵
└── .guardian/                                # 运行时数据（自动生成，已 gitignore）
    ├── enterprise_kb/                        #   企业知识库
    ├── emergency_plans/                      #   生成的应急预案
    ├── analytics_reports/                    #   分析报告
    └── incidents/                            #   事件记录
```

---

## 支持的设备类型

| 设备 | 特有场景 | 特殊考虑 |
|------|---------|---------|
| 多旋翼无人机 | 电机失效、螺旋桨折断 | 可悬停，降落选项多 |
| 固定翼无人机 | 失速、发动机停车 | 不可悬停，需滑翔降落 |
| eVTOL | 过渡飞行段故障 | 载人，P0 最高优先 |
| 无人配送车 | 路障、行人冲突 | 低速，停车为首选 |
| 无人船 | 碰撞、进水 | 水域环境 |
| 巡检机器人 | 高空坠落、卡死 | 封闭环境 |

---

## 依赖

- Python 3.8+
- 无外部依赖（纯标准库实现）

---

## 安全原则

- **宁可误报不可漏报** — 过度反应优于低估风险
- **保守决策** — 信息不完整时假设最坏情况
- **可解释性** — 每个决策有清晰推理链路
- **人命无价** — 涉及人员安全的场景零容忍风险

---

## 更新日志

### v0.2.0 — 企业级功能

- 新增 `enterprise_kb_manager.py`：多源数据采集、知识库构建与管理
- 新增 `emergency_plan_generator.py`：基于知识库自动生成定制化应急预案
- 新增 `fleet_analytics.py`：机队数据统计分析、设备健康评分、合规报告
- 新增企业导入模板 `assets/enterprise_templates/`
- 支持 6 种数据源导入（Guardian 事件、CSV 日志、行业案例、厂商通告、法规、人工经验）
- 知识库健康度检查与优化建议
- CAAC/EASA/FAA 多标准合规报告

### v0.1.0 — 初始版本

- 7 阶段设备端危机响应闭环
- 5 个预置解决方案模板
- 损失优先级加权决策引擎
- L1-L5 危机分级与自适应人机协作

---

## 阶段

**Alpha** — 概念验证阶段，不可用于真实飞行控制。仅作为危机决策辅助分析工具。
