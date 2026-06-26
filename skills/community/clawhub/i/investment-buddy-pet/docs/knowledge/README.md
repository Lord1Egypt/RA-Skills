# 📚 Investment Buddy 知识库

**版本**：V1.0  
**创建日期**：2026-04-11  
**最后更新**：2026-04-11

---

## 一、概述

本知识库是 Investment Buddy 项目的**核心资产**，包含宠物人格、投资性格体系、对话模板、任务规则和关系图谱的完整文档。

### 1.1 文档列表

| 文档 | 大小 | 说明 | 状态 |
|------|------|------|------|
| [PET_KNOWLEDGE_BASE.md](./PET_KNOWLEDGE_BASE.md) | 6.2KB | 12 只宠物完整人格设定 | ✅ 完成 |
| [INVESTMENT_PERSONALITY_ONTOLOGY.md](./INVESTMENT_PERSONALITY_ONTOLOGY.md) | 7.1KB | 五维投资性格分类体系 | ✅ 完成 |
| [CONVERSATION_TEMPLATES.md](./CONVERSATION_TEMPLATES.md) | 10.9KB | 3 类触发器 × 12 只宠物对话模板 | ✅ 完成 |
| [TASK_GENERATION_RULES.md](./TASK_GENERATION_RULES.md) | 17.4KB | 8 大触发规则 + 5 类任务生成系统 | ✅ 完成 |
| [PET_RELATION_GRAPH.md](./PET_RELATION_GRAPH.md) | 15.7KB | ECharts + Neo4j 关系图谱可视化 | ✅ 完成 |

**总计**：57.3KB

---

## 二、核心概念

### 2.1 12 只宠物

| 宠物 | 投资风格 | 风险偏好 | 沟通风格 | 专长 |
|------|---------|---------|---------|------|
| 🐿️ 松果 | 价值 | 保守 | 温暖 | 估值、定投 |
| 🐢 慢慢 | 长期 | 平衡 | 平静 | 心态、复利 |
| 🦉 博士 | 价值 + 量化 | 平衡 | 理性 | 财报、数据 |
| 🐺 猎手 | 趋势 | 激进 | 果断 | 趋势、技术 |
| 🐬 泡泡 | 灵活 | 平衡 | 幽默 | 情绪、逆向 |
| 🐻 阿守 | 防御 | 保守 | 严肃 | 配置、风控 |
| 🦅 天眼 | 宏观 | 激进 | 理性 | 宏观、周期 |
| 🐘 大山 | 均衡 | 平衡 | 平静 | 配置、再平衡 |
| 🦊 狐狸 | 灵活 | 平衡 | 机智 | 波段、切换 |
| 🐎 骏马 | 行业轮动 | 激进 | 热情 | 行业、景气 |
| 🐪 骆驼 | 逆向 | 激进 | 理性 | 逆向、估值 |
| 🦄 星星 | 成长 | 激进 | 幽默 | 成长、创新 |

### 2.2 五维投资性格

```
风险承受力 (Risk Tolerance)
知识水平 (Knowledge Level)
决策风格 (Decision Style)
情绪稳定性 (Emotional Stability)
时间偏好 (Time Preference)
```

### 2.3 触发器分类

| 类型 | 数量 | 说明 |
|------|------|------|
| 主动触发 | 3 类 | 风险提醒、机会提示、日常关怀 |
| 被动触发 | 5 类 | 用户提问、用户交易、用户查看等 |
| 定时触发 | 2 类 | 每日问候、每周复盘 |

### 2.4 任务类型

| 类型 | 说明 | 优先级 |
|------|------|--------|
| T-A | 信息推送 | P1-P2 |
| T-B | 风险提醒 | P0 |
| T-C | 机会提示 | P0-P1 |
| T-D | 互动任务 | P1-P2 |
| T-E | 执行建议 | P0-P1 |

---

## 三、技术架构

### 3.1 数据存储

- **Neo4j**：宠物关系图谱
- **MySQL**：用户数据、任务记录
- **Redis**：缓存、会话状态

### 3.2 可视化

- **ECharts**：关系图谱可视化
- **React**：前端交互组件

### 3.3 API 接口

- **RESTful**：图查询、宠物推荐
- **WebSocket**：实时推送

---

## 四、使用指南

### 4.1 开发者

```bash
# 克隆项目
git clone https://github.com/your-org/investment-buddy.git

# 安装依赖
cd investment-buddy
pip install -r requirements.txt

# 启动服务
python -m src.main
```

### 4.2 宠物匹配

```python
from investment_buddy import PetMatcher

matcher = PetMatcher()
pets = matcher.recommend_pets(user_id="user_12345", top_k=3)
```

### 4.3 任务生成

```python
from investment_buddy import TaskEngine

engine = TaskEngine()
tasks = engine.generate_tasks(trigger_type="market_volatility")
```

---

## 五、更新日志

### 2026-04-11 - Day 1/10

**完成度**：80%

**新增**：
- ✅ PET_KNOWLEDGE_BASE.md（12 只宠物完整人格）
- ✅ INVESTMENT_PERSONALITY_ONTOLOGY.md（五维分类体系）
- ✅ CONVERSATION_TEMPLATES.md（对话模板库）
- ✅ TASK_GENERATION_RULES.md（任务生成规则）
- ✅ PET_RELATION_GRAPH.md（关系图谱）

**待完成**：
- [ ] 宠物成长体系文档
- [ ] 广场互动规则
- [ ] 用户反馈系统

---

## 六、贡献指南

### 6.1 添加新宠物

1. 在 `PET_KNOWLEDGE_BASE.md` 中添加宠物档案
2. 在 `CONVERSATION_TEMPLATES.md` 中添加对话模板
3. 在 `PET_RELATION_GRAPH.md` 中添加关系定义

### 6.2 更新对话模板

1. 确保模板符合宠物人格
2. 添加变量占位符
3. 测试模板填充效果

### 6.3 修改任务规则

1. 更新 `TASK_GENERATION_RULES.md`
2. 同步更新代码实现
3. 添加单元测试

---

## 七、许可证

MIT License

---

*最后更新：2026-04-11 | Day 1/10 完成度 80%*
