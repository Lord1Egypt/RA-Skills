# 预设快捷方式

`--preset X` 展开为卡片类型 + 风格的推荐组合。用户可以覆盖其中任一维度。

## 按场景分类

### 学习与教育

| 预设 | 主要卡片类型 | 风格 | 适用场景 |
|------|-------------|------|----------|
| `study-guide`（学习指南） | tips + definition | study-notes | 考试重点、知识梳理 |
| `classroom`（课堂笔记） | tips + definition | chalkboard | 课堂内容、教学讲解 |
| `concept-map`（概念图） | mindmap + definition | notion | 概念脉络、知识体系 |
| `flashcard`（闪卡） | definition + qa | minimal | 术语记忆、快速复习 |

### 技术与干货

| 预设 | 主要卡片类型 | 风格 | 适用场景 |
|------|-------------|------|----------|
| `cheatsheet`（速查表） | tips | notion | 命令速查、API 参考 |
| `tutorial-cards`（教程卡） | steps | vector-illustration | 步骤教程、操作指南 |
| `tech-compare`（技术对比） | comparison | notion | 框架对比、方案选择 |
| `architecture`（架构卡） | mindmap + matrix | vector-illustration | 架构说明、系统设计 |

### 生活与分享

| 预设 | 主要卡片类型 | 风格 | 适用场景 |
|------|-------------|------|----------|
| `life-tips`（生活妙招） | tips | cute | 生活技巧、好物分享 |
| `product-review`（测评卡） | comparison + tips | warm | 产品对比、使用体验 |
| `daily-quote`（每日金句） | quote | minimal | 名言、启发、鸡汤 |

### 职场与商业

| 预设 | 主要卡片类型 | 风格 | 适用场景 |
|------|-------------|------|----------|
| `swot`（SWOT分析） | matrix | notion | SWOT、四象限分类 |
| `faq`（常见问答） | qa | warm | FAQ、面试准备 |
| `warning`（避坑指南） | tips | bold | 踩坑经验、注意事项 |
| `methodology`（方法论） | steps + mindmap | notion | 方法论、框架思维 |

### 观点与创意

| 预设 | 主要卡片类型 | 风格 | 适用场景 |
|------|-------------|------|----------|
| `opinion`（观点卡） | quote + tips | screen-print | 观点表达、深度思考 |
| `inspiration`（灵感卡） | quote | warm | 启发、创意收集 |

---

## 内容类型 → 预设推荐

在步骤 2 确认设置时，根据步骤 1 的内容分析推荐预设：

| 内容特征 | 主要推荐 | 备选 |
|----------|----------|------|
| 技术知识点列举 | `cheatsheet` | `study-guide` |
| 步骤/教程 | `tutorial-cards` | `classroom` |
| 概念解释 | `concept-map` | `flashcard` |
| 技术对比 | `tech-compare` | `architecture` |
| 学习笔记 | `study-guide` | `classroom` |
| 生活技巧 | `life-tips` | `product-review` |
| 避坑/踩雷 | `warning` | `faq` |
| 面试/问答 | `faq` | `flashcard` |
| 观点/评论 | `opinion` | `inspiration` |
| 分类/分析 | `swot` | `methodology` |
| 方法论/框架 | `methodology` | `architecture` |
| 名言/金句 | `daily-quote` | `inspiration` |

## 覆盖示例

```bash
# 使用预设
/panda-knowledge-card article.md --preset cheatsheet

# 预设 + 覆盖风格
/panda-knowledge-card article.md --preset cheatsheet --style chalkboard

# 预设 + 覆盖卡片类型
/panda-knowledge-card article.md --preset study-guide --layout qa
```

显式 `--layout`/`--style` 参数始终优先于预设值。
