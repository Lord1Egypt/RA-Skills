# Token Reference 规范

> 定义 Design System Token 的引用语法，确保策略师和执行器之间通过引用而非硬编码传递设计值。

---

## 1. 引用语法

使用 `{path.to.value}` 格式引用品牌 Token 中的任意值：

| 引用路径 | 示例值 | 说明 |
|---------|--------|------|
| `{colors.primary}` | `#0f1011` | 主文字颜色 |
| `{colors.accent}` | `#5e6ad2` | 品牌强调色 |
| `{colors.background}` | `#f7f8f8` | 页面底色 |
| `{colors.surface}` | `#FFFFFF` | 卡片面板色 |
| `{colors.secondary}` | `#d0d6e0` | 次要文字 |
| `{colors.muted}` | `#8A8F98` | 弱化文字 |
| `{colors.border}` | `#E6E6E6` | 边框色 |
| `{typography.display.fontFamily}` | `Inter Variable` | 标题字体 |
| `{typography.display.fontSize}` | `3rem` | 标题字号 |
| `{typography.display.fontWeight}` | `600` | 标题字重 |
| `{typography.display.letterSpacing}` | `-0.02em` | 标题字距 |
| `{typography.body.fontFamily}` | `Inter Variable` | 正文字体 |
| `{typography.body.fontSize}` | `1rem` | 正文字号 |
| `{typography.mono.fontFamily}` | `JetBrains Mono` | 代码字体 |
| `{rounded.sm}` | `4px` | 小圆角 |
| `{rounded.md}` | `8px` | 中圆角 |
| `{rounded.lg}` | `16px` | 大圆角 |
| `{spacing.sm}` | `8px` | 小间距 |
| `{spacing.md}` | `16px` | 中间距 |
| `{spacing.lg}` | `32px` | 大间距 |
| `{ppt.accentBudget}` | `2` | accent用量上限/页 |

---

## 2. 策略师使用方式

在 `design_spec.md` 中，**写引用而非写死值**。这样更换品牌时只需切换 token 文件，无需逐一修改设计稿。

### 示例：design_spec.md 片段

```markdown
## 配色方案

- 页面背景：{colors.background}
- 卡片底色：{colors.surface}
- 标题文字：{colors.primary}
- 正文文字：{colors.secondary}
- 强调/CTA：{colors.accent}（每页 ≤ {ppt.accentBudget} 处）
- 边框/分割：{colors.border}

## 字体方案

- 标题：{typography.display.fontFamily}，{typography.display.fontSize}，weight {typography.display.fontWeight}
- 正文：{typography.body.fontFamily}，{typography.body.fontSize}
- 代码块：{typography.mono.fontFamily}，{typography.mono.fontSize}

## 布局参数

- 元素间距：{spacing.md}（标准）/ {spacing.lg}（章节间）
- 卡片圆角：{rounded.md}
- 按钮圆角：{rounded.lg}
- 内边距：{spacing.md}
```

---

## 3. 执行器解引用流程

执行器在生成 SVG 前执行以下步骤：

1. **加载品牌 Token**：读取 `references/design-systems/<brand>.md` 的 YAML frontmatter
2. **解析 design_spec.md**：扫描所有 `{xxx.yyy.zzz}` 格式的引用
3. **替换**：将每个 `{path}` 替换为 token 中对应的实际值
4. **校验**：确认所有引用都已成功解析（无残留 `{xxx}`）
5. **生成 SVG**：使用解引用后的实际值

### 解引用伪代码

```
token = parse_yaml_frontmatter(brand_token_file)
for each {ref} in design_spec:
    value = resolve_path(token, ref)  # e.g. "colors.accent" → token["colors"]["accent"]
    if value is None:
        WARN("未解析引用: {ref}")
    else:
        replace({ref}, value)
```

---

## 4. 注意事项

- **禁止部分引用**：`{colors.primary}80` 这种在引用后拼接透明度的写法不允许，应直接写完整值
- **嵌套引用**：不支持 `{colors.{role}}`，路径必须是确定的
- **默认值**：如果 token 中缺少某个路径，执行器应使用 `default.md` 中的对应值作为 fallback
- **大小写敏感**：路径严格大小写匹配
