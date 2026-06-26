# CSO 指南：Claude Search Optimization

> 你的 skill 写得再好，找不到就等于不存在。

CSO 解决的核心问题：**未来的 Claude 实例能否在正确时机找到并加载你的 skill？**

---

## 1. description 字段：最重要的一行

description 是 Claude 决定"要不要加载这个 skill"的唯一依据。

### 规则：只描述触发条件，绝不总结流程

```yaml
# ❌ 错误：总结了 skill 的工作流程
description: 帮你设计 skill，包括分型、L4规范填充、安全门控、评估打分和交付包整理

# ❌ 错误：太模糊，没有触发信号
description: 用于创建技能

# ✅ 正确：只说"什么时候用"
description: 设计并产出可发布的 Agent Skill（L4生产级）。用于从0到1创建技能、重构现有技能、做安全评审、建立评估与发布流程。
```

**为什么不能总结流程？**

测试发现：当 description 包含工作流摘要时，Claude 会按照 description 里的步骤执行，而不去读完整的 SKILL.md。描述里写了几步，它就做几步——哪怕 SKILL.md 里有更完整的流程。

description = 触发条件信号，不是 skill 的使用说明书。

### 格式要求

- 以"用于…"或"设计并…"开头，聚焦触发场景
- 第三人称，因为会被注入系统提示
- 总长 < 500 字符（含 frontmatter 共 < 1024 字符）
- 包含具体症状和场景，不要用抽象描述

---

## 2. 关键词覆盖策略

Claude 通过关键词匹配找 skill，覆盖这些类型：

| 类型 | 示例 |
|------|------|
| **错误信息** | "Hook timed out"、"permission denied"、"injection detected" |
| **用户症状** | "不知道怎么开始"、"skill 跑不稳"、"不知道发布标准" |
| **同义词** | "技能/skill/工具"、"发布/上线/部署" |
| **工具名** | 实际命令名、平台名、文件扩展名 |

在 SKILL.md 正文中自然使用这些词，不要只堆在 description 里。

---

## 3. Token 效率目标

频繁加载的 skill 每次对话都会消耗 token。SKILL.md 越精简，成本越低。

| skill 类型 | 目标字数 |
|-----------|---------|
| 高频加载（每次对话都可能触发） | < 200 词 |
| 普通 skill | < 500 词 |
| 带大量参考资料的 skill | 主文件 < 300 词，细节拆到 references/ |

**压缩技巧：**

```markdown
# ❌ 把所有参数写在主文件
score-skill.js 支持 --dir、--verbose、--threshold、--format 参数

# ✅ 引用 --help
运行 `node scripts/score-skill.js --help` 查看全部参数
```

```markdown
# ❌ 重复解释已在其他文档里的内容
当用户是新手时，先说明 skill 是什么，再解释为什么要有 L4 标准，
接下来介绍如何选择任务……

# ✅ 交叉引用
新手路径：见 [references/onboarding-zero-to-one.md](references/onboarding-zero-to-one.md)
```

---

## 4. 命名规范

用动词开头，描述你在**做什么**：

| ✅ 好的命名 | ❌ 避免 |
|-----------|--------|
| `l4-skill-forge` | `skill-creation-tool` |
| `behavioral-testing` | `test-helpers` |
| `release-checklist` | `checklist` |

用连字符分隔，只用字母、数字和连字符，不用括号和特殊字符。

---

## 5. 交叉引用规范

引用其他 skill 时，用 skill 名称，加明确的必要性标记：

```markdown
# ✅ 正确
**必读前置：** behavioral-testing（约束类 skill 必须先做基线测试）

# ✅ 正确
**推荐配合使用：** cso-guide（发布前检查 description 字段）

# ❌ 不要用 @ 语法强制加载
@references/behavioral-testing.md  ← 会立即消耗上下文
```

`@` 语法会在对话开始时立即加载文件内容，无论是否用到，浪费上下文。用名称引用，按需加载。

---

## 快速自检清单

发布前对照检查：

- [ ] description 只描述触发条件，没有工作流摘要
- [ ] SKILL.md 字数符合目标（频繁加载类 < 200 词）
- [ ] 包含用户可能搜索的关键词（症状、工具名、错误信息）
- [ ] 细节已拆到 references/，主文件做导航用
- [ ] 交叉引用用 skill 名，不用 @ 语法
