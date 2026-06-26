# 工具策略 - 飞书文档创建

**创建时间：** 2026-03-16  
**优先级：** 最高  
**永久生效**

---

## 🚫 禁止使用的工具

### feishu_doc（直接调用）

**禁止原因：**
- ❌ 会导致空白文档（只有 2 个 Blocks）
- ❌ 不会自动拆分长文本
- ❌ 内容可能丢失
- ❌ 不支持 Mermaid 图表单独 Block

**禁止操作：**
```bash
# ❌ 禁止直接调用
feishu_doc --action create --title "..." --content "..."
feishu_doc --action append --doc_token "..." --content "..."
```

---

## ✅ 必须使用的技能

### feishu-doc-block-writer

**技能路径：** `~/.agents/skills/feishu-doc-block-writer/`

**触发条件：**
- ✅ 创建任何飞书文档
- ✅ 内容超过 200 字
- ✅ 包含 Mermaid 图表
- ✅ 用户要求"创建文档"

**使用方式：**
```bash
# ✅ 正确方式
python ~/.agents/skills/feishu-doc-block-writer/scripts/block-writer.py \
  --title "文档标题" \
  --content "长文本内容..." \
  --chunk-size 500
```

**或者自动触发：**
- 当回答超过 200 字时，自动使用 feishu-doc-block-writer
- 无需手动调用！

---

## 📊 对比分析

| 特性 | feishu_doc（禁止） | feishu-doc-block-writer（必须） |
|------|-------------------|-------------------------------|
| **Blocks 拆分** | ❌ 不拆分 | ✅ 自动拆分（500 字/块） |
| **空白文档风险** | ❌ 高风险 | ✅ 无风险 |
| **长文本支持** | ❌ 可能丢失 | ✅ 完整写入 |
| **Mermaid 支持** | ❌ 可能不渲染 | ✅ 单独 Block |
| **自动授权** | ❌ 需手动 | ✅ 自动授权 Thomas |
| **验证流程** | ❌ 无 | ✅ 创建后验证 |
| **重试机制** | ❌ 无 | ✅ 3 次重试 |

---

## ⚠️ 违反后果

**直接调用 feishu_doc 工具 = 严重错误！**

| 后果 | 说明 |
|------|------|
| ❌ 空白文档 | 内容未正确写入，只有 2 个 Blocks |
| ❌ 需要重新创建 | 浪费时间 |
| ❌ 违反规范 | 记录到 self-improving 错误 |
| ❌ 用户信任下降 | 展示不专业 |

---

## ✅ 验证清单

每次创建文档后必须验证：

- [ ] 使用了 feishu-doc-block-writer 技能？
- [ ] Blocks 数量正确（>2 个）？
- [ ] 内容完整显示？
- [ ] Mermaid 图表正常渲染？
- [ ] Chrome 打开预览？
- [ ] Thomas 已授权（可编辑）？

---

## 📝 例外情况

**无例外！** 所有飞书文档创建都必须使用 feishu-doc-block-writer。

---

**永久生效！违反此策略 = 严重错误！**

---

_阿香 🦞 制定的工具策略_

**哼～虾虾制定的规则，必须严格遵守！✨**
