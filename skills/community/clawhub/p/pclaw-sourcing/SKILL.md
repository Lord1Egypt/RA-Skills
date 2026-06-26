---
name: pclaw-sourcing
description: "Pclaw工程寻源技能 - 知识变现平台的核心技能。当用户需要发布工程需求、匹配资源、查询技能、管理分润、创建展会等Pclaw平台操作时使用。触发词：发布需求、寻源、查技能、上架、创建展会、展会、需求广场、知识商店。"
---

# Pclaw 工程寻源技能

## 平台概述

**Pclaw = 知识变现平台 / 寻源引擎**

核心理念：寻源 = 经验分享 = 知识变现。任何资源交易，都是一次知识的交换：需求方分享需求经验，资源方分享专业能力，平台分享匹配知识。

**匹配成功 = 知识被验证 + 价值被量化**

## 核心理念

### 寻源六步法

```
1. 需求描述    ──→    2. 寻源匹配
3. 询价议价    ──→    4. 成交确认
5. 履约执行    ──→    6. 验收结算
```

平台只做：寻源匹配 + 成交托管
平台不做：履约执行 + 验收（资源方自行负责）

### 分润机制

匹配成功自动分润：
- **30%** → 需求提出者（躺赚）
- **40%** → 资源提供方
- **20%** → 平台（匹配知识费）
- **10%** → 运营基金

### 六大资源类型

| 类型 | 示例 | 定价参考 |
|------|------|---------|
| Skill/DNA | 标书写作、配筋计算、规范检索 | ¥0.05~50/次 |
| Service | 工程咨询、造价审核、方案评审 | ¥500~5000/人天 |
| Material | 钢材、管件、混凝土 | ¥100~10000/单 |
| Equipment | 发电机、机床租赁 | ¥1000~100000/台天 |
| Human | 工程师、造价师、施工队 | ¥500~5000/人天 |
| Digital | AI代理、自动化流程 | ¥0.01~1/调用 |

## 平台地址

- 网站：https://www.pclawai.com
- API基础URL：https://www.pclawai.com/api

## 功能路由

### QUERY - 查询技能/资源列表

查询平台上架的技能和资源。

```
触发词：查技能、看技能列表、有什么资源
```

**路由参数：**
```json
{
  "route": "QUERY",
  "params": {
    "type": "skill|service|material|equipment|human|digital",
    "category": "管道工程|法律|翻译|金融|建筑|代码",
    "keyword": "配筋",
    "limit": 10
  }
}
```

**API调用：**
```
GET /api/dna?type=skill&category=管道工程&limit=10
```

**返回示例：**
```json
{
  "success": true,
  "dnas": [
    {
      "id": "pipe",
      "name": "管道取量技能",
      "category": "管道工程",
      "price": 99,
      "unit": "次",
      "sales_count": 1234,
      "rating": 4.8
    }
  ]
}
```

### PUBLISH - 发布资源/技能

将技能或资源上架到平台。

```
触发词：发布技能、上架、技能入驻
```

**路由参数：**
```json
{
  "route": "PUBLISH",
  "params": {
    "type": "skill",
    "name": "管道取量技能",
    "category": "管道工程",
    "price": 99,
    "unit": "次",
    "description": "上传管道等轴测图PDF，自动提取BOM清单",
    "spec": {
      "input": "PDF文件",
      "output": "BOM清单",
      "format": "Excel"
    },
    "tags": ["BIM", "PDF解析", "BOM"]
  }
}
```

**API调用：**
```
POST /api/dna
Content-Type: application/json
{
  "name": "...",
  "type": "skill",
  ...
}
```

### DEMAND - 发布需求

在需求广场发布需求，等待资源方响应。

```
触发词：发布需求、我要需求、找资源
```

**路由参数：**
```json
{
  "route": "DEMAND",
  "params": {
    "title": "需要管道等轴测图BOM提取",
    "type": "skill",
    "category": "管道工程",
    "budget_min": 50,
    "budget_max": 200,
    "deadline": "2026-04-01",
    "description": "上传管道等轴测图PDF，需要提取BOM清单"
  }
}
```

**API调用：**
```
POST /api/demand
```

### MATCH - 发起匹配

将需求与资源进行匹配。

```
触发词：匹配、接单、响应需求
```

**路由参数：**
```json
{
  "route": "MATCH",
  "params": {
    "demand_id": "DEM-xxx",
    "resource_id": "RES-xxx"
  }
}
```

**API调用：**
```
POST /api/match
```

### EARNINGS - 查看收益

查看分润收益。

```
触发词：看收益、收益多少、收入
```

**API调用：**
```
GET /api/earnings
```

### EXPO - 展会操作

查询展会信息或参展。

```
触发词：展会、数字展会、参展
```

**路由参数：**
```json
{
  "route": "EXPO",
  "params": {
    "action": "list|info|create|join",
    "expo_id": "EXPO-xxx",
    "booth_type": "普通|黄金|冠名"
  }
}
```

**展会定价：**
| 展位类型 | 价格 | 说明 |
|---------|------|------|
| 普通展位 | ¥99/天起步 | 基础展示，标准匹配 |
| 黄金展位 | ¥699/展期（3-7天） | 首页置顶，搜索优先 |
| 冠名展位 | ¥1999/展期 | 全站banner，专属专题 |

## 定价参考

### Skill/DNA 技能

| 技能 | 功能路由 | 价格 |
|------|---------|------|
| 标书写作 | ANALYZE | ¥0.5/次 |
| 标书写作 | WRITE | ¥0.5/次 |
| 标书写作 | EXPORT | ¥0.3/次 |
| 标书写作 | OUTLINE | ¥0.2/次 |
| 配筋计算 | CALCULATE | ¥0.1/次 |
| 规范检索 | QUERY | ¥0.05/次 |
| Python执行 | RUN | ¥0.2/次 |

### 资源类型定价原则

| 类型 | 定价原则 |
|------|---------|
| Skill | 按次计费（¥0.01~50） |
| Service | 按人天计费（¥500~5000） |
| Material | 按订单计费（¥100~10000） |
| Equipment | 按台天计费（¥1000~100000） |
| Human | 按人天/月薪计费 |
| Digital | 按API调用计费（¥0.01~1） |

## 匹配算法

匹配得分计算：
```
得分 = 需求匹配度 × 0.4 + 资源质量 × 0.3 + 历史评价 × 0.2 + 响应速度 × 0.1
```

## 执行流程示例

### 场景：用户想发布一个管道BOM提取需求

**Step 1 - 理解需求**
用户：「我需要提取管道等轴测图的BOM清单」

**Step 2 - 匹配资源**
调用 QUERY 查找相关技能，找到「管道取量技能」

**Step 3 - 发布需求**
调用 DEMAND 发布需求，设定预算 ¥50~200

**Step 4 - 等待匹配**
资源方响应 → 匹配成功 → 自动分润

### 场景：用户想上架一个配筋计算技能

**Step 1 - 理解技能**
用户：「我想把配筋计算上架到平台」

**Step 2 - 收集信息**
- 类型：skill
- 名称：配筋计算技能
- 分类：结构工程
- 价格：¥0.1/次

**Step 3 - 发布上架**
调用 PUBLISH 上架技能

**Step 4 - 等待被购买**
有人购买 → 自动分润（40%归技能方）

## 注意事项

- 所有金额单位为 CNY
- 分润自动结算，T+1到账
- 展会参展需提前申请
- 资源下架后不再产生新匹配
- 一个需求可对应多个资源方（N笔分润）

## 相关链接

- 知识商店：https://www.pclawai.com/dna-shop.html
- 需求广场：https://www.pclawai.com/demand-plaza.html
- 数字展会：https://www.pclawai.com/expo.html
- 我的分润：https://www.pclawai.com/my-dna.html
