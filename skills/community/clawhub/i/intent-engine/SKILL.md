---
name: intent-engine
description: 意图引擎 - AI驱动的用户意图识别与智能路由。支持代码/知识/任务/闲聊四大分类，提供关键词+正则多策略匹配、置信度计算、动态意图管理，配备Web可视化管理界面。适用于AI助手任务调度、智能路由、对话理解等场景。
license: MIT-0
metadata:
  openclaw:
    requires: {}
    install: []
tags: [intent, classification, routing, nlp, understanding, dashboard]
version: 2.0.0
author: laosi & WB
source: original
---

# Intent Engine - 意图引擎 v2.0

> AI驱动的意图识别引擎 + Web管理面板 | 激活词: 识别意图 / 分类任务 / 智能路由

## 核心功能

1. **多策略分类** — 关键词匹配 + 正则模式 + 文本长度调整 + 优先级加权
2. **置信度计算** — 综合评分并归一化为0-1，含备选分类建议
3. **动态管理** — REST API CRUD 意图配置，热更新无需重启
4. **可视化面板** — Web UI 仪表盘、意图管理、分类测试三合一

## 架构

```
intent-engine/
├── intent_engine/
│   ├── engine.py      # 核心分类引擎
│   ├── storage.py     # JSON 持久化存储
│   ├── models.py      # 数据模型
│   └── api.py         # Flask REST API
├── static/
│   └── index.html     # Web 管理界面
├── data/
│   └── intents.json   # 意图配置（自动生成）
├── run.py             # 入口
└── requirements.txt
```

## 启动方式

```bash
cd intent-engine
pip install -r requirements.txt
python run.py
# 访问 http://localhost:5700 打开管理界面
```

## API 接口

| Method | Path | 说明 |
|--------|------|------|
| POST | `/api/classify` | 单文本分类 `{"text":"..."}` |
| POST | `/api/classify/batch` | 批量分类 `{"texts":[...]}` |
| POST | `/api/evaluate` | 测试集评估 |
| GET | `/api/intents` | 获取所有意图 |
| POST | `/api/intents` | 创建意图 |
| GET/PUT/DELETE | `/api/intents/:id` | 单意图CRUD |
| GET | `/api/stats` | 统计数据 |
| GET | `/api/categories` | 分类定义 |

## 意图分类体系

### 一级分类 (4类)

| 类型 | 标识 | 颜色 | 说明 |
|------|------|------|------|
| 代码类 | CODE | 蓝 #3b82f6 | 编写、修复、审查、测试、重构 |
| 知识类 | KNOW | 紫 #8b5cf6 | 定义、教程、对比、建议 |
| 任务类 | TASK | 黄 #f59e0b | 文件操作、命令执行、搜索、编排 |
| 闲聊类 | CHAT | 绿 #10b981 | 问候、反馈、澄清、结束 |

### 分类算法

```python
score = (
    pattern_matches * 4.0 +      # 正则命中 (高精度)
    keyword_matches * 2.0 * w +  # 关键词命中 (带权重)
    priority * 0.05              # 意图优先级加成
)
score *= 0.8 if len(text) < 10 else 1.0    # 短文本惩罚
score *= 1.1 if len(text) > 50 else 1.0    # 长文本加成
```

### 置信度计算

- 原始分数归一化: `confidence = score / max(10, score + 2)`
- 范围: 0-1，保留4位小数
- 备选分类: Top-K 意图中 confidence > 0.05 的

## 可视化界面功能

### 仪表盘
- 总意图数/启用数/禁用数 统计卡片
- 分类分布条形图
- 分类图例

### 意图管理
- 搜索/新建/编辑/删除 意图
- 关键词权重调优 (0.1-5.0)
- 正则模式批量编辑
- 启用/禁用开关
- JSON 导入/导出

### 分类测试
- 单文本实时分类
- 多标签分类模式
- 置信度环形图
- 命中关键词/模式展示
- 技能路由推荐

### 快速测试条
- 底部固定快速测试栏
- 回车即触发分类
- 实时显示分类结果

## 集成建议

将本技能与以下技能配合使用：

```markdown
- skill-creator: 代码生成路由
- workflow-verifier: Bug修复路由
- mempalace-assistant: 知识查询路由
- karpathy-principles: 编码最佳实践
- general-chat: 通用对话处理
```

## 更新记录

### v2.0.0 (2026-06-09)
- 重构为可运行的Python引擎
- 新增Web管理界面
- 支持意图动态CRUD
- 多策略加权分类算法
- 置信度计算与备选方案
- JSON持久化存储
- REST API 完整接口
- 导入/导出功能

### v1.0.0 (2026-04-28)
- 初始版本（伪代码原型）

---
**作者**: laosi & WB
**许可**: MIT-0
