# Ops-PM Bridge - 运营产品协同加速套件

> 解决运营与产品之间的信息不对称、需求扯皮、效果归因等核心痛点

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Skill Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/openclaw/ops-pm-bridge)
[![OpenClaw Compatible](https://img.shields.io/badge/OpenClaw-Compatible-green.svg)](https://openclaw.ai)

## 🔥 核心痛点与解决方案

| 痛点 | 解决方案 | 命令 |
|------|----------|------|
| 信息不对称 | 需求双向翻译 | `/ops-translate` |
| 需求扯皮 | 优先级智能计算 | `/priority-calc` |
| 效果归因争议 | 统一归因框架 | `/attribution` |
| 验收标准模糊 | 自动生成验收标准 | `/acceptance` |
| 数据口径不一致 | 数据定义对齐 | `/data-align` |
| 协同文档分散 | 一键生成协同文档 | `/ops-doc` |

---

## 🚀 快速开始

### 安装

```bash
# OpenClaw
cp -r ops-pm-bridge ~/.openclaw/skills/

# Hermes Agent
cp -r ops-pm-bridge ~/.hermes/skills/
```

### 使用

```
# 运营需求翻译
/ops-translate --from ops --to pm
运营需求：我们要搞个大促活动

# 效果归因框架
/attribution
活动名称：双11大促

# 优先级计算
/priority-calc
[输入需求列表]
```

---

## 📖 功能详解

### 1. 需求翻译器 (`/ops-translate`)

**运营 → 产品翻译：**

```
输入：我们要搞个大促活动，用户参与度要高一点

输出：
- 功能需求：营销活动模块
- 核心指标：用户参与率提升 ≥ 30%
- 具体功能点：
  1. 活动落地页配置后台
  2. 用户任务系统
  3. 积分/优惠券奖励发放
  4. 实时数据看板
```

---

### 2. 效果归因框架 (`/attribution`)

**统一数据口径：**

```yaml
attribution:
  model: "time_decay"  # 时间衰减归因
  lookback_window: 7   # 回溯7天
  
  metrics:
    primary: "GMV"
    secondary:
      - "参与用户数"
      - "转化率"
      - "ROI"
```

---

### 3. 优先级计算器 (`/priority-calc`)

**多维度自动计算：**

```
综合得分 = 业务价值(0.35) + 紧急度(0.25) 
         - 开发成本(0.15) - 风险(0.10) + 干系人(0.15)
```

---

### 4. 验收标准生成器 (`/acceptance`)

**自动生成可量化验收标准：**

| 验收项 | 标准 | 验证方法 |
|--------|------|----------|
| 邀请率 | ≥ 15% | 埋点数据 |
| 邀请成功率 | ≥ 30% | 活动系统 |
| 新用户留存率 | ≥ 40% | 用户系统 |

---

### 5. 数据口径对齐 (`/data-align`)

**统一指标定义：**

| 指标 | 运营口径 | 产品口径 | 统一口径 |
|------|----------|----------|----------|
| DAU | 登录用户 | 有效行为用户 | ✅ 统一 |
| GMV | 订单金额 | 支付金额 | ✅ 统一 |
| 转化率 | 下单/访问 | 支付/访问 | ✅ 统一 |

---

### 6. 协同文档生成器 (`/ops-doc`)

**一键生成完整协同文档：**
- 需求清单
- 排期计划
- 验收标准
- 效果归因
- 数据口径
- 沟通机制

---

## 📁 项目结构

```
ops-pm-bridge/
├── SKILL.md                    # 主文档
├── README.md                   # 项目说明
├── LICENSE                     # MIT 许可证
├── references/                 # 参考文档
│   ├── ops_pm_dictionary.md    # 运营产品翻译词典
│   ├── priority_weights.md     # 优先级权重配置
│   └── attribution_models.md   # 归因模型说明
└── examples/                   # 示例文件
    ├── example-attribution.yaml
    ├── example-priority.json
    └── example-ops-doc.md
```

---

## 🎯 使用场景

### 场景一：运营提新需求

```
1. /ops-translate 需求翻译
2. /acceptance 生成验收标准
3. /priority-calc 计算优先级
4. /ops-doc 生成协同文档
```

### 场景二：活动效果评估

```
1. /data-align 对齐数据口径
2. /attribution 生成归因框架
3. /ops-doc 更新协同文档
```

### 场景三：需求优先级争议

```
1. /priority-calc 自动计算
2. 基于数据而非主观判断
3. 双方确认结果
```

---

## 📄 许可证

MIT License

---

## 🙏 致谢

解决运营与产品协同痛点，让协作更高效！
