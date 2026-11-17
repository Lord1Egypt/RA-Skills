# 回顾报告模板

所有模式的完整模板。执行回顾时复制对应模板，填充内容后保存到指定路径。

## 目录结构

```
<workspace>/learning/reviews/
├── post-learning/     # 模式 A：学后复盘
│   └── YYYY-MM-DD.md
├── weekly/            # 模式 B：周内化报告
│   └── YYYY-Www.md
├── application/       # 模式 C：应用检查
│   └── YYYY-MM-DD.md
├── archive/           # 模式 D：压缩归档记录
│   └── YYYY-MM-DD.md
└── integration/       # 模式 E：知识落地报告
    └── YYYY-MM-DD.md
```

初始化（如不存在）：

```bash
mkdir -p <workspace>/learning/reviews/{post-learning,weekly,application,archive,integration}
```

---

## 模式 A：学后复盘模板

保存到 `learning/reviews/post-learning/YYYY-MM-DD.md`

```markdown
# 学后复盘 - YYYY-MM-DD

## 学习主题
<topic>

## 一句话总结
<费曼法：用最通俗的话概括核心>

## 和我工作的关系
- 直接能用：<列出可以马上应用的点，具体到"在什么场景下做什么">
- 未来有用：<需要积累或特定条件才用得上的>
- 无关：<学完发现跟自己领域不大的，简要说明为什么>

## 待内化项
- [ ] → AGENTS.md：<需要更新的具体内容>
- [ ] → TOOLS.md：<需要更新的具体内容>
- [ ] → SOUL.md：<需要更新的具体内容>
- [ ] → MEMORY.md：<需要记录的重要洞察>

## 遗留问题
<学完还搞不懂的，或需要进一步探索的>
```

规则：没有就写"暂无"，不硬凑。"直接能用"必须具体。

---

## 模式 B：周内化报告模板

保存到 `learning/reviews/weekly/YYYY-Www.md`（如 `2026-W20.md`）

```markdown
# 周内化报告 - YYYY 第 Www 周 (MM-DD ~ MM-DD)

## 本周学习概览
- 共学习 <N> 个主题
- 主题列表：<topic1>, <topic2>, ...

## 已内化
| 内容 | 内化到 | 改了什么 |
|------|--------|---------|
| <topic> | AGENTS.md | <具体改动> |
| <topic> | TOOLS.md | <具体改动> |

## 未内化（及原因）
- <topic>：<为什么还没内化，比如"需要更多实践验证">

## 本周最有价值的收获
<一条，最多两条，用费曼法写>

## 下周关注
<基于本周学习，下周应该重点什么>
```

### 内化动作对照表

| 学到的内容类型 | 内化到 | 怎么改 |
|---------------|--------|--------|
| 工作流程改进 | AGENTS.md | 添加/修改对应流程步骤 |
| 工具使用经验 | TOOLS.md | 添加工具配置、技巧 |
| 认知/态度/方法论 | SOUL.md | 调整原则、风格描述 |
| 重要事件/决策 | memory/YYYY-MM-DD.md | 记录当天的 memory |
| 通用知识洞察 | MEMORY.md | 添加到长期记忆 |

### 各角色内化侧重点

| Agent 角色 | 主要内化到 | 侧重点 |
|-----------|-----------|--------|
| CTO / 研发总监 | AGENTS.md, memory/ | 技术架构决策、项目进度管理 |
| skill-engineer | AGENTS.md, TOOLS.md | Skill 设计方法、开发工具链 |
| learning-expert | SOUL.md, AGENTS.md | 学习方法论、教学策略 |
| efficiency-agent | AGENTS.md, TOOLS.md | 效率工具使用、时间管理技巧 |
| blog-agent | SOUL.md, TOOLS.md | 写作技巧、内容策略 |
| soul-questioner | SOUL.md | 思辨框架、哲学视角 |

### 内化三问

1. **这个知识改变了我"怎么做事"吗？** → 改 AGENTS.md
2. **这个知识让我有了新工具/新方法吗？** → 改 TOOLS.md
3. **这个知识改变了我"怎么想问题"吗？** → 改 SOUL.md

如果三个都是"没有"，说明这条知识还不到内化的时候，记在笔记里就好。

---

## 模式 C：应用检查报告模板

保存到 `learning/reviews/application/YYYY-MM-DD.md`

```markdown
# 应用检查 - YYYY-MM-DD

## 回顾周期：MM-DD ~ MM-DD

## 学习了什么
- <topic1> (MM-DD)
- <topic2> (MM-DD)

## ✅ 已应用
- **<topic>** → 在 <场景> 中使用了，效果：<具体描述>

## ❌ 未能应用
- **<topic>** → 原因：<没遇到场景/忘了/不适用>

## 🔄 需要修正
- **<topic>** → 实践发现笔记中 <哪里不对>，应改为 <正确的理解>

## 应用率
<已应用数> / <学习总数> = XX%

## 行动项
- [ ] <基于检查结果的具体行动>
```

---

## 模式 E：知识落地报告模板

保存到 `learning/reviews/integration/YYYY-MM-DD.md`

```markdown
# 知识落地报告 - YYYY-MM-DD

## 本周学习 → 落地检查

| 学习内容 | 落地判断 | 具体行动 |
|---------|---------|---------|
| <topic> | ✅ AGENTS.md | <改了什么> |
| <topic> | ✅ Skill: <name> | <改了什么> |
| <topic> | ⏳ 待验证 | <原因> |
| <topic> | 📦 知识储备 | 不强制落地 |

## Skill 优化记录
- **Skill名称**：<name>
- **改动内容**：<具体描述>
- **预期效果**：<改完后应该有什么变化>

## 反思
- 本周有没有"学了但用不起来"的内容？为什么？
- 我的 Skill 设计有没有阻碍知识落地的地方？
```
