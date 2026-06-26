# 推特/X 页面 DOM 选择器脆弱性与调试流程

**日期**：2026-03-14
**影响版本**：scrape.js v7
**风险等级**：中（随时可能因推特前端发版而失效）

---

## 背景

Grok 页面（`x.com/i/grok`）属于推特/X 的 React 单页应用，使用 CSS-in-JS 方案生成原子化 class。
这些 class 名（如 `r-b88u0q`、`r-16lk18l`、`r-1blvdjr`）是构建时哈希，**没有语义含义**，推特每次发版都可能变化。

当前 scrape.js v7 依赖以下选择器来提取 Grok 回复内容：

| 用途 | 选择器 | 稳定性 |
|------|--------|--------|
| 定位回复完成 | `[aria-label="重新生成"]` | 较稳定（aria-label 属于无障碍标准） |
| 定位回复内容区 | `.r-16lk18l` | **脆弱**（构建时哈希 class） |
| 识别标题 span | `style="display: block" + margin-bottom` | 中等（依赖 inline style） |
| 识别粗体 span | `.r-b88u0q` | **脆弱**（构建时哈希 class） |
| 定位页面主区域 | `[data-testid="primaryColumn"]` | 较稳定（data-testid 通常保留） |
| emoji 图片识别 | `src` 含 `twimg.com/emoji` | 较稳定（CDN 域名稳定） |

---

## 失效时的典型表现

1. **`extractReplyHTML` 返回 `{ html: null, method: 'none' }`** → Markdown 长度为 0 → 脚本报 "Reply too short" 并退出
2. **提取到的 HTML 包含了不相关内容**（如整个页面侧边栏） → 输出 Markdown 中混入了 UI 文字
3. **turndown 转换后格式不对** → 标题没有 `##`、粗体没有 `**` → 可能是 Grok 改变了标题/粗体的渲染方式

---

## 调试流程

当 scrape.js 出现上述问题时，执行以下步骤：

### 第一步：运行 inspect 命令探查当前 DOM

```bash
cd scripts
npm run inspect
# 或带自定义 prompt
npm run inspect -- "你好"
```

`inspect-dom.js` 会：
1. 打开 Grok 页面、发送一条简短 prompt
2. 等待回复完成
3. 输出当前页面的关键 DOM 结构信息：
   - 所有 `data-testid` 属性值
   - 所有 `aria-label` 属性值
   - Grok 回复文字附近的祖先链（tag、class、testId、textLen）
   - 标题/粗体等格式元素的 HTML 结构
4. 将完整回复容器的 HTML 保存到 `output/inspect-reply.html`

### 第二步：分析输出，找到新的选择器

对照 inspect 输出，确认：

- **回复内容容器**：从"重新生成"按钮（`[aria-label="重新生成"]`）向上爬几层祖先，找到包含回复正文且不包含建议问题的 div。注意 `children[0]` 是正文内容、后面的 children 是 follow-up 建议
- **标题 span**：检查 `style` 属性是否仍用 `display: block` + `margin-bottom` 来渲染标题
- **粗体 span**：找当前用哪个 class 表示粗体（在 inspect 输出的 HTML 中搜索 `font-weight` 或 `bold`）

### 第三步：更新 scrape.js 中的选择器

需要更新的位置（在 `scrape.js` 中搜索以下关键词定位）：

1. **`SELECTORS` 常量**（文件顶部）：所有可变 class 都集中在此，修改对应值即可
2. **`createTurndown()` 中的 `grok-bold` 规则**：如果粗体 class 变了，更新 `SELECTORS.boldClass`
3. **`extractReplyHTML()` 中的容器定位逻辑**：如果"重新生成"按钮到容器的层级变了，调整 `for` 循环的层数

### 第四步：测试验证

```bash
npm run scrape -- "用标题和列表格式介绍 Python 的3个优点"
```

检查输出的 `.md` 文件是否有正确的 `##` 标题、`**粗体**`、`-` 列表。

---

## 降低风险的设计原则

1. **优先使用稳定属性**：`aria-label`、`data-testid`、`role` 比 CSS class 稳定得多
2. **可变 class 集中声明**：所有构建时哈希 class 放在 `SELECTORS` 常量中，不散落在各处
3. **多级回退策略**：主路径失败时有备用路径，最终回退到 innerText
4. **自动输出调试信息**：当提取失败时自动保存 `debug-dom.json` 和 `debug-reply.html`，无需手动运行 inspect
5. **inspect 脚本常备**：不需要每次从头写探查代码，直接 `npm run inspect` 即可
