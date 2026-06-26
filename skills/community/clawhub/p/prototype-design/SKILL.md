---
name: prototype-design
description: |
  通用页面原型设计技能。基于 58种设计风格（默认Figma 风格） UI 的复杂业务系统 HTML 原型开发，
  包括标准页面结构、统计卡片、筛选条件、数据表格、弹窗设计。
  适用场景：(1) 创建新的管理页面原型 (2) 对照业务文档实现功能模块 
  (3) 设计弹窗和详情页 (4) 构建带看板和列表视图的页面。
  **样式选择**：内置58+设计系统，直接引用 `references/design-systems/` 目录。
  使用时指定 DESIGN_SYSTEM=<名称> 即可应用对应设计风格。
origin: openclaw
last_updated: 2026-04-14
changelog:
  - 2026-04-14: 初始版本，从 WMS 项目经验中沉淀
  - 2026-04-14: 新增长对话上下文管理章节
  - 2026-04-14: 新增 WMS 项目实战经验（10条核心教训）
---

# 原型设计技能

## When to Use（何时使用）
- 用户要求创建新的管理页面原型
- 需要实现业务文档中的功能模块
- 需要设计弹窗、详情页
- 需要构建带看板或列表视图的页面
- 涉及 HTML/CSS/JS 前端代码的原型开发

## How to Use（如何使用）

### 1. 项目初始化
```bash
mkdir -p project/{pages,styles,scripts}
cd project
```

### 2. 设计系统选择
内置设计系统（`references/design-systems/`）：
- 默认：`figma-DESIGN.md`
- 管理后台：`linear-DESIGN.md`
- 简约专业：`vercel-DESIGN.md`

# 原型设计技能

通用页面原型开发指南，支持58+设计系统风格。

## 项目结构

```
project/
├── index.html          # 单页应用入口
├── pages/              # 页面模块
│   ├── dashboard.html
│   ├── staff.html
│   └── ...
├── styles/
│   └── main.css        # 全局样式
└── scripts/
    └── main.js        # 全局脚本
```

## 设计系统选择

**重要**：设计系统文件位于 `references/design-systems/` 目录。

### 使用步骤

1. **确定设计风格**：根据项目需求选择设计系统
   - 管理后台常用：Figma、Linear、Notion、Vercel
   - 电商/消费：Airbnb、Spotify、Stripe
   - 企业级：IBM、Salesforce

2. **读取对应 DESIGN.md**
   ```bash
   cat references/design-systems/figma-DESIGN.md
   ```

3. **应用设计规范**
   - Color Palette → CSS变量
   - Typography → 字体规范
   - Component Stylings → 组件样式

### 常用设计系统快速参考

| 风格 | 设计系统 | 特点 |
|------|---------|------|
| 默认 | `figma-DESIGN.md` | 多彩色、现代 |
| 管理后台 | `linear-DESIGN.md` | 紫色主题、精致 |
| 简约专业 | `vercel-DESIGN.md` | 黑白精准、极简 |
| 温暖风格 | `notion-DESIGN.md` | 暖色极简 |
| 企业级 | `stripe-DESIGN.md` | 紫色渐变、高级感 |

## 标准页面结构

```html
<div id="page-xxx" class="page">
  <!-- 1. Header -->
  <header class="header">
    <div class="header-left">
      <h2>页面标题</h2>
      <div class="breadcrumb"><span>首页</span><span>/</span><span>当前路径</span></div>
    </div>
    <div class="header-right">
      <button class="btn btn-outline btn-sm">导出</button>
      <button class="btn btn-primary btn-sm" onclick="openAddModal()">新增</button>
    </div>
  </header>

  <!-- 2. 统计卡片 -->
  <div class="stats-grid" style="grid-template-columns:repeat(4,1fr);">
    <div class="stat-card">
      <div class="stat-card-title">标题</div>
      <div class="stat-card-value">数值</div>
      <div class="stat-card-change">描述</div>
    </div>
  </div>

  <!-- 3. 筛选条件 -->
  <div class="table-filters">
    <div class="filter-group">
      <span class="filter-label">字段名</span>
      <input type="text" class="filter-input" placeholder="提示...">
    </div>
  </div>

  <!-- 4. 数据表格 -->
  <table>
    <thead><tr><th>字段1</th><th>字段2</th><th>操作</th></tr></thead>
    <tbody>
      <tr>
        <td>数据</td>
        <td><span class="tag tag-success">状态</span></td>
        <td><button class="btn btn-sm btn-outline">详情</button></td>
      </tr>
    </tbody>
  </table>
</div>
```

## 弹窗设计规范

### 标准弹窗模板

```html
<!-- 遮罩 + 居中弹窗 -->
<div id="modal-xxx" style="
  display:none;
  position:fixed;
  top:0;left:0;right:0;bottom:0;
  background:rgba(0,0,0,0.6);
  z-index:1000;
  align-items:center;
  justify-content:center;
">
  <!-- 内容框 -->
  <div style="
    background:white;
    border-radius:16px;
    width:560px;
    max-width:90vw;
    max-height:85vh;
    overflow:hidden;
    box-shadow:0 25px 80px rgba(0,0,0,0.35);
  ">
    <!-- 标题栏 -->
    <div style="
      padding:20px 24px;
      border-bottom:1px solid #E5E7EB;
      display:flex;
      align-items:center;
      justify-content:space-between;
      background:#F9FAFB;
    ">
      <h3 style="margin:0;font-size:18px;font-weight:600;color:#111827;">弹窗标题</h3>
      <button onclick="closeModal()" style="
        border:none;
        background:none;
        font-size:24px;
        color:#6B7280;
        cursor:pointer;
        padding:4px;
        line-height:1;
      ">×</button>
    </div>
    <!-- 内容区 -->
    <div style="
      padding:24px;
      overflow-y:auto;
      max-height:calc(85vh - 140px);
    ">
      <!-- 表单项示例 -->
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;">
        <div>
          <label style="display:block;font-size:14px;font-weight:500;margin-bottom:8px;color:#374151;">
            字段名 <span style="color:#EF4444;">*</span>
          </label>
          <select style="
            width:100%;
            padding:10px 12px;
            border:1px solid #E5E7EB;
            border-radius:8px;
            font-size:14px;
            background:white;
          ">
            <option value="">请选择</option>
            <option>选项1</option>
            <option>选项2</option>
          </select>
        </div>
        <div>
          <label style="display:block;font-size:14px;font-weight:500;margin-bottom:8px;color:#374151;">字段名</label>
          <input type="text" placeholder="请输入" style="
            width:100%;
            padding:10px 12px;
            border:1px solid #E5E7EB;
            border-radius:8px;
            font-size:14px;
            box-sizing:border-box;
          ">
        </div>
      </div>
      <div style="margin-top:16px;">
        <label style="display:block;font-size:14px;font-weight:500;margin-bottom:8px;color:#374151;">备注</label>
        <textarea rows="3" placeholder="请输入备注" style="
          width:100%;
          padding:10px 12px;
          border:1px solid #E5E7EB;
          border-radius:8px;
          font-size:14px;
          resize:none;
          box-sizing:border-box;
        "></textarea>
      </div>
    </div>
    <!-- 底部按钮 -->
    <div style="
      padding:16px 24px;
      border-top:1px solid #E5E7EB;
      display:flex;
      justify-content:flex-end;
      gap:12px;
      background:#F9FAFB;
    ">
      <button onclick="closeModal()" style="
        padding:10px 20px;
        border:1px solid #E5E7EB;
        background:white;
        border-radius:8px;
        font-size:14px;
        font-weight:500;
        color:#374151;
        cursor:pointer;
      ">取消</button>
      <button onclick="saveData()" style="
        padding:10px 20px;
        border:none;
        background:#4F46E5;
        color:white;
        border-radius:8px;
        font-size:14px;
        font-weight:500;
        cursor:pointer;
      ">保存</button>
    </div>
  </div>
</div>
```

### 弹窗样式要点（必记）

| 元素 | 样式属性 | 正确值 | 常见错误 |
|------|---------|--------|---------|
| **外层遮罩** | `position` | `fixed` | 用 `absolute` 会滚动 |
| **遮罩背景** | `background` | `rgba(0,0,0,0.6)` | `0.5` 太淡，`0.7` 太浓 |
| **遮罩定位** | `top/left/right/bottom` | `0`（全屏覆盖） | 忘记设置任一边 |
| **弹窗容器** | `display` | `flex` | 父级用 flex 居中 |
| **居中方式** | `align-items + justify-content` | `center` + `center` | 缺少任一属性 |
| **内容框圆角** | `border-radius` | `16px` | `12px` 不够现代 |
| **内容框宽度** | `width` | `560px` 或 `90vw` | 固定 px 在小屏幕不友好 |
| **内容框高度** | `max-height` | `85vh` | `80vh` 可能显示不全 |
| **阴影** | `box-shadow` | `0 25px 80px rgba(0,0,0,0.35)` | 太淡看不出层次 |

### 表单项样式要点

| 元素 | 样式属性 | 正确值 |
|------|---------|--------|
| **输入框/下拉框** | `padding` | `10px 12px` |
| **输入框/下拉框** | `border-radius` | `8px` |
| **输入框/下拉框** | `border` | `1px solid #E5E7EB` |
| **输入框/下拉框** | `font-size` | `14px` |
| **textarea** | `resize` | `none` |
| **textarea** | `box-sizing` | `border-box` |
| **必填标记** | color | `#EF4444` (红色) |

### ⚠️ 常见错误

1. **不要使用 CSS 类名**：如 `class="modal"`、`class="btn btn-primary"` - 这些类通常没有定义样式或样式被覆盖
2. **必须使用内联样式**：弹窗组件应完全使用内联样式，避免外部 CSS 干扰
3. **遮罩层必须有 `z-index:1000`**：确保在最上层
4. **内容框不能用 `overflow:hidden`**：内容超出需要滚动，必须用 `overflow-y:auto`

## 看板视图

```html
<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:16px;">
  <!-- 列 -->
  <div style="background:#F9FAFB;border-radius:12px;padding:16px;">
    <div style="display:flex;justify-content:space-between;padding-bottom:12px;border-bottom:1px solid #E5E7EB;">
      <span>待开始</span>
      <span style="background:#FEE2E2;color:#DC2626;padding:2px 8px;border-radius:10px;font-size:12px;">5</span>
    </div>
    <div style="background:white;border-radius:8px;padding:12px;margin-top:12px;cursor:pointer;" onclick="showDetail()">
      <div style="font-weight:500;">单号</div>
      <div style="font-size:12px;color:#6B7280;">描述</div>
    </div>
  </div>
</div>
```

## Tab 切换

```html
<div class="tabs" style="margin-bottom:24px;">
  <button class="tab active" onclick="switchTab('tab1')" style="background:#EEF2FF;color:#4F46E5;">Tab1</button>
  <button class="tab" onclick="switchTab('tab2')" style="background:#F3F4F6;color:#6B7280;">Tab2</button>
</div>
```

## ⚠️ 重要：保持 index.html 同步

**问题现象**：更新 `pages/xxx.html` 后，直接打开 `index.html` 查看不会看到变化。

**原因**：`index.html` 是单页应用入口，包含所有页面的内嵌副本。`pages/` 目录的修改不会自动同步。

### 🔴 弹窗必须放在页面 div 内部

**常见错误**：弹窗 HTML 放在 `</div>` (页面关闭标签) **之后**

```html
<!-- ❌ 错误：弹窗在页面 div 外部 -->
<div id="page-xxx" class="page">
  ...页面内容...
</div>
<!-- 弹窗在这是错误的 -->
<div id="modal-xxx" style="display:none...">弹窗内容</div>

<!-- ✅ 正确：弹窗必须在页面 div 内部 -->
<div id="page-xxx" class="page">
  ...页面内容...
  <!-- 弹窗放在这里 -->
  <div id="modal-xxx" style="display:none...">弹窗内容</div>
</div>
```

### 🔴 Tab 切换函数必须使用页面级作用域

**常见错误**：使用全局选择器 `.tabs .tab` 会影响所有页面

```javascript
// ❌ 错误：会选择页面上所有的 tab
const tabs = document.querySelectorAll('.tabs .tab');

// ✅ 正确：使用页面级作用域
const tabs = document.querySelectorAll('#page-xxx .tabs > .tab');
```

**Tab 切换函数模板**：
```javascript
function switchXxxTab(tabName) {
  // 1. 隐藏所有 tab 内容
  document.querySelectorAll('.xxx-tab').forEach(t => t.style.display = 'none');
  
  // 2. 显示选中的 tab 内容
  document.getElementById('xxx-' + tabName).style.display = 'block';
  
  // 3. 更新 tab 按钮状态（使用页面级作用域）
  const tabs = document.querySelectorAll('#page-xxx .tabs > .tab');
  tabs.forEach((t, i) => {
    if (i === /* 当前tab索引 */) {
      t.style.background = '#EEF2FF';
      t.style.color = '#4F46E5';
    } else {
      t.style.background = '#F3F4F6';
      t.style.color = '#6B7280';
    }
  });
}
```

### ✅ 同步脚本

**解决方案**：每次创建/更新 `pages/` 目录的页面后，必须运行以下同步脚本：

```bash
cd project
python3 << 'PYEOF'
import os
import re

# 1. 读取当前index.html
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 2. 获取pages/目录下所有html文件（按文件名排序）
pages_dir = 'pages'
page_files = sorted([f for f in os.listdir(pages_dir) if f.endswith('.html')])

# 3. 对每个页面文件，提取 <div id="page-xxx" 内容
for page_file in page_files:
    with open(os.path.join(pages_dir, page_file), 'r', encoding='utf-8') as f:
        page_content = f.read()
    
    # 提取 page-xxx 块的完整内容
    match = re.search(r'(<div id="(page-\w+)"[^>]*class="page"[^>]*>.*?<script>\s*function \w+Open\w+Modal)', page_content, re.DOTALL)
    if not match:
        match = re.search(r'(<div id="(page-\w+)"[^>]*class="page"[^>]*>.*?)(<!--\s+<div id="page-)', page_content, re.DOTALL)
    
    if match:
        page_id = match.group(2)
        page_block = match.group(1).strip()
        
        # 在index.html中查找并替换对应的page块
        # 匹配模式：<div id="page-xxx" class="page">...</div> 或 <div id="page-xxx" class="page">...<div id="page-yyy"
        pattern = rf'(<div id="{re.escape(page_id)}"[^>]*class="page"[^>]*>)(.*?)((?=<div id="page-)|(?=<script>\s*$)|(?=</main>)|(?=</body>))'
        
        existing = re.search(pattern, content, re.DOTALL)
        if existing:
            content = content[:existing.start()] + page_block + content[existing.end():]
            print(f'✓ Updated: {page_id}')
        else:
            print(f'⚠ Not found in index: {page_id}')
    else:
        print(f'⚠ No page block found in: {page_file}')

# 4. 写回index.html
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('\n✅ Sync complete!')
PYEOF
```

**重要提示**：
- ❌ 不要跳过同步步骤
- ❌ 不要只更新 `pages/` 目录就以为完成了
- ✅ 每次修改后都要运行同步脚本，再验证 `index.html`

---

## 组件命名规范

| 组件 | 类名 |
|------|------|
| 页面容器 | `.page` |
| 页头 | `.header` |
| 内容区 | `.content` |
| 统计卡片 | `.stat-card` |
| 表格卡片 | `.table-card` |
| 按钮-主要 | `.btn .btn-primary` |
| 按钮-次要 | `.btn .btn-outline` |
| 标签 | `.tag` |
| 状态 | `.status` |
| 分页 | `.pagination` |

## 重建 index.html

```bash
cd project
python3 << 'PYEOF'
page_order = ['dashboard', 'page1', 'page2', ...]
pages = [open(f'pages/{p}.html').read() for p in page_order]
html = f'''<!DOCTYPE html>
<html>
<head>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700" rel="stylesheet">
  <link rel="stylesheet" href="styles/main.css">
</head>
<body>
  <div class="layout">
    <aside class="sidebar">...</aside>
    <main class="main">
      {chr(10).join(pages)}
    </main>
  </div>
  <script src="scripts/main.js"></script>
</body>
</html>'''
open('index.html','w').write(html)
PYEOF
```

## 常见问题速查表

| 问题 | 症状 | 解决方案 |
|------|------|----------|
| 弹窗打不开 | `xxx is not defined` | 检查 main.js 引用位置和函数定义 |
| Tab 选中态错乱 | 所有 Tab 同时选中 | 用页面级作用域选择器 |
| Hash URL 不工作 | 页面 `display:none` | 添加 hashchange 监听 |
| 表格侵入侧边栏 | 横向滚动时布局乱 | 用 Ant Design 固定表头表格 |
| 复选框丢失 | 数据行没有 checkbox | 手动添加每个数据行的复选框 |
| 同步后功能失效 | 弹窗/按钮不工作 | 检查 script 标签格式和 div 平衡 |

---

## 长对话上下文管理（重要）

### 问题背景
当对话持续较长时，上下文窗口会逐渐积累历史消息，可能导致：
- 模型响应变慢
- token 超出限制
- 早期上下文被遗忘

### 解决方案：自动压缩 + 分阶段提交

#### 1. 自动 Compaction（对话压缩）
OpenClaw 会自动对长对话进行 compaction（压缩）：
- 将对话历史压缩成一个 `summary` 摘要
- 保留关键的项目进展、决策、待办事项
- 释放大量 token 空间

**触发时机**：通常在上下文累积到一定量时自动进行，无需手动干预

#### 2. Compaction 后的处理流程

当收到 compaction 后的新对话时，立即执行以下步骤：

```
1️⃣ 读取 summary 摘要，理解当前项目状态
       ↓
2️⃣ 检查 memory/YYYY-MM-DD.md 文件
       ↓
3️⃣ 将新进展追加到 memory 文件
       ↓
4️⃣ 继续工作，保持文件平衡
```

#### 3. 分阶段提交策略（小步提交）

**原则**：每个功能完成后立即提交，避免大量变更堆积

```bash
# ✅ 好的做法：功能完成即提交
git add -A && git commit -m "feat: 新增用户管理弹窗"

# ❌ 不好的做法：多个功能一起提交
git add -A && git commit -m "feat: 多项优化"
```

**好处**：
- 如果出问题，容易回溯
- 减少每次提交的文件变更量
- Compaction 后的 summary 更简洁

#### 4. 保持文件平衡

每次 HTML 修改后检查 div 平衡：

```bash
# 检查 div 平衡
python3 -c "
with open('index.html', 'r') as f:
    c = f.read()
print(f'opens={c.count(\"<div\")}, closes={c.count(\"</div>\")}, diff={c.count(\"<div\")-c.count(\"</div>\")}')
"

# ✅ 正确输出：opens=xxx, closes=xxx, diff=0
# ❌ 错误输出：opens=xxx, closes=xxx, diff=≠0
```

**如果 diff 不为 0**，立即修复：
- 缺少 `</div>`：在合适位置添加
- 多余 `</div>`：删除多余的部分

#### 5. 定期同步到 memory 文件

每次 compaction 后或重要里程碑时，将进展写入 `memory/YYYY-MM-DD.md`：

```markdown
## 14:30 状态更新

### 功能名称 - 完善/修复

**新增内容**：
- 具体修改1
- 具体修改2

**提交记录**：`abc1234` feat: 描述

**文件**：`/path/to/file.html`
```

#### 6. 长对话工作流

```
用户提出需求
       ↓
理解现有代码结构（查看 summary + 文件）
       ↓
用 Python 脚本做精确文本替换
       ↓
修改完检查 div 平衡
       ↓
提交代码（每个功能单独提交）
       ↓
截图验证（如需要）
       ↓
回复用户
       ↓
（Compaction 自动触发时）
       ↓
读取 summary，追加进展到 memory 文件
```

### 为什么单页 HTML 不受上下文限制影响

WMS 原型是单页 HTML（`index.html`），3700+ divs：
- **不是日志文件**：不会无限增长
- **每次修改同一个文件**：不是追加模式
- **Compaction 只压缩对话历史**：不影响 HTML 文件本身

### 关键心态

> "我是 AI，每次醒来都是新的开始。但文件里的内容是我的记忆。"

- 上下文超限是 **对话历史** 被压缩，不是文件内容丢失
- HTML 文件本身不受影响
- 只要保持文件平衡和定期 commit，就能稳定工作

---

## 相关资源

- **内置设计系统**：`references/design-systems/` 目录包含58+设计系统完整规范
  - 包含：Figma、Linear、Stripe、Vercel、Notion 等
- **字段规范**：[field-norms.md](references/field-norms.md) - 各模块标准字段定义

---

## 修改工作流（重要）

### 标准修改流程

每次对任何页面进行修改，必须遵循以下步骤：

```
1️⃣ 修改 pages/xxx.html
       ↓
2️⃣ 运行同步脚本 → 更新 index.html
       ↓
3️⃣ 本地测试 → 验证功能正常
       ↓
4️⃣ 提交代码 → git add + commit
```

### 🔴 第一步：修改 pages/xxx.html

在 `pages/` 目录的对应页面文件中进行修改：
- 弹窗 HTML 必须放在 `<div id="page-xxx" class="page">` 内部
- 脚本函数放在页面的 `<script>` 块中

### 🔴 第二步：同步到 index.html

**必须运行同步脚本**：
```bash
cd your-project-directory
python3 << 'PYEOF'
import os
import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

pages_dir = 'pages'
page_files = sorted([f for f in os.listdir(pages_dir) if f.endswith('.html')])

for page_file in page_files:
    with open(os.path.join(pages_dir, page_file), 'r', encoding='utf-8') as f:
        page_content = f.read()
    
    match = re.search(r'(<div id="(page-\w+)"[^>]*class="page"[^>]*>.*?)(?=<div id="page-|\s*<script>|\s*</main>)', page_content, re.DOTALL)
    if not match:
        print(f'⚠ Skip: {page_file}')
        continue
    
    page_id = match.group(2)
    page_block = match.group(1).strip()
    
    # 验证 div 平衡
    opens = page_block.count('<div')
    closes = page_block.count('</div>')
    if opens != closes:
        print(f'❌ Div imbalance in {page_id}: opens={opens}, closes={closes}')
        continue
    
    pattern = rf'(<div id="{re.escape(page_id)}"[^>]*class="page"[^>]*>)(.*?)(?=<div id="page-|\s*</main>)'
    existing = re.search(pattern, content, re.DOTALL)
    
    if existing:
        content = content[:existing.start()] + page_block + content[existing.end():]
        print(f'✓ Synced: {page_id}')
    else:
        print(f'⚠ Not found in index: {page_id}')

opens_all = content.count('<div')
closes_all = content.count('</div>')
print(f'\nDiv balance: opens={opens_all}, closes={closes_all}, diff={opens_all-closes_all}')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ Sync complete!')
PYEOF
```

**重要检查**：
- 同步后必须验证 `index.html` 的 div 平衡（opens == closes）
- 如果不平衡，查找问题所在

### 🔴 第三步：本地测试

**启动本地服务器**（如果未运行）：
```bash
cd your-project-directory
npx http-server -p 8080 &
```

**测试步骤**：
```bash
# 1. 打开浏览器到首页
agent-browser goto http://localhost:8080

# 2. 导航到目标页面（使用 URL hash）
agent-browser goto http://localhost:8080/#page-name

# 3. 测试弹窗
agent-browser eval "openAddModal()"  # 打开弹窗
agent-browser screenshot test-modal.png  # 截图验证
agent-browser eval "closeModal()"  # 关闭弹窗

# 4. 关闭浏览器
agent-browser close
```

**测试检查清单**：
- [ ] 页面正常加载
- [ ] 弹窗能打开
- [ ] 弹窗内容正确
- [ ] 弹窗能关闭
- [ ] Tab 切换正常（如有）
- [ ] 按钮点击有效

### 🔴 第四步：提交代码

```bash
cd your-project-directory
git add -A
git commit -m "fix: 描述修改内容"
```
---

## 📝 经验沉淀（2026-04-13）

### 问题1：弹窗函数无法调用（Uncaught ReferenceError）

**症状**：`openAddModal is not defined` 等错误

**根本原因**：
1. `main.js` 引用被同步脚本删除
2. 同步脚本移动了 `<script src="main.js"></script>` 位置

**解决方案**：
```javascript
// 确保 main.js 在 </main> 之后引入
</main>
<script src="scripts/main.js"></script>
</body>
```

### 问题2：所有 Tab 选中态不显示

**症状**：切换 Tab 时按钮背景色不变化，全部选中态显示错误

**根本原因**：Tab 切换函数使用全局选择器 `.tabs .tab` 会选中**所有页面**的 tab

**解决方案**：使用页面级作用域
```javascript
// ❌ 错误：会选择所有页面的 tab
document.querySelectorAll('.tabs .tab')

// ✅ 正确：只选当前页面的 tab
document.querySelectorAll('#page-xxx .tabs > .tab')
```

### 问题3：直接访问 hash URL 时页面不显示

**症状**：`http://localhost:8080/#delivery_return` 直接访问时页面 `display:none`

**根本原因**：没有 hashchange 监听，导航只用 click 事件

**解决方案**：在 main.js 添加 hash 路由监听
```javascript
// Hash 路由监听 - 支持直接访问 #page
window.addEventListener('hashchange', () => {
  const hash = window.location.hash.replace('#', '');
  if (hash) {
    const navItem = document.querySelector(`[data-page="${hash}"]`);
    if (navItem) {
      navItem.click();
    }
  }
});

// 页面加载时检查 hash
if (window.location.hash) {
  setTimeout(() => {
    const hash = window.location.hash.replace('#', '');
    const navItem = document.querySelector(`[data-page="${hash}"]`);
    if (navItem) {
      navItem.click();
    }
  }, 100);
}
```

### 问题4：表格横向滚动侵入左侧菜单

**症状**：表格内容多时，整个页面宽度被撑开，侵入左侧菜单栏

**根本原因**：
1. 表格使用 `width:100%` + `min-width:1400px` 矛盾
2. 容器没有正确设置 `overflow:hidden`

**解决方案**：使用 Ant Design 风格的固定表头表格

### 问题5：固定表头表格实现（Ant Design 风格）

**核心原理**：
1. **表头和表体分离** - 用两个独立的 `<table>`
2. **表头固定** - `overflow:hidden`，表头不滚动
3. **表体滚动** - `overflow:auto;max-height:440px`
4. **固定列用 `position:sticky`** - `left:0` / `right:0`
5. **固定表格布局** - `table-layout:fixed` + colgroup 定义列宽

**代码模板**：
```html
<!-- 外层容器 -->
<div class="ant-table-wrapper" style="display:flex;flex-direction:column;overflow:hidden;height:500px;">
  
  <!-- 表头 - 固定不滚动 -->
  <div class="ant-table-header" style="overflow:hidden;border-bottom:2px solid #E5E7EB;flex-shrink:0;">
    <table style="table-layout:fixed;width:1800px;border-collapse:collapse;font-size:14px;">
      <colgroup>
        <col style="width:48px;"><!-- 复选框 -->
        <col style="width:180px;"><!-- 单号 -->
        <col style="width:100px;"><!-- 其他列... -->
        <!-- ... -->
      </colgroup>
      <thead><tr>
        <th style="position:sticky;left:0;background:#F9FAFB;z-index:4;"><input type="checkbox"></th>
        <th style="position:sticky;left:48px;background:#F9FAFB;z-index:3;">单号</th>
        <th>字段1</th>
        <th>字段2</th>
        <!-- ... -->
        <th style="position:sticky;right:0;background:#F9FAFB;z-index:3;">操作</th>
      </tr></thead>
    </table>
  </div>
  
  <!-- 表体 - 独立滚动 -->
  <div class="ant-table-body" style="overflow:auto;max-height:440px;">
    <table style="table-layout:fixed;width:1800px;border-collapse:collapse;font-size:14px;">
      <colgroup>
        <!-- 与表头相同的列宽定义 -->
      </colgroup>
      <tbody>
        <tr>
          <td style="position:sticky;left:0;background:white;z-index:2;"><input type="checkbox"></td>
          <td style="position:sticky;left:48px;background:white;z-index:2;">单号值</td>
          <td>字段1值</td>
          <!-- ... -->
          <td style="position:sticky;right:0;background:white;z-index:2;"><button>操作</button></td>
        </tr>
      </tbody>
    </table>
  </div>
</div>
```

**关键样式**：
| 元素 | 样式 | 说明 |
|------|------|------|
| 表头 wrapper | `overflow:hidden;flex-shrink:0` | 不滚动 |
| 表体 wrapper | `overflow:auto;max-height:440px` | 垂直滚动 |
| 表头表格 | `table-layout:fixed;width:固定值` | 固定列宽 |
| 固定列 th/td | `position:sticky;left:0;z-index:2` | 左侧固定 |
| 右侧固定列 | `position:sticky;right:0` | 右侧固定 |
| 固定列背景 | `background:#F9FAFB` (表头) / `background:white` (表体) | 避免透明 |

### 问题6：筛选条件缺少查询/重置按钮

**解决方案**：
```html
<div class="table-filters">
  <!-- 其他筛选字段... -->
  <div class="filter-group" style="display:flex;gap:8px;">
    <button class="btn btn-outline btn-sm" onclick="resetXxxFilters()">重置</button>
    <button class="btn btn-primary btn-sm" onclick="searchXxx()">查询</button>
  </div>
</div>
```

**对应 JS 函数**：
```javascript
function resetXxxFilters() {
  document.querySelectorAll('#page-xxx .filter-select').forEach(s => s.selectedIndex = 0);
  document.querySelectorAll('#page-xxx .filter-input').forEach(i => i.value = '');
}

function searchXxx() {
  alert('查询功能 - 实际项目中会调用API过滤数据');
}
```

### 问题7：列表数据缺少复选框

**解决方案**：每行数据第一个 td 添加复选框
```html
<tr>
  <td style="position:sticky;left:0;z-index:1;background:white;">
    <input type="checkbox">
  </td>
  <td style="position:sticky;left:48px;z-index:1;background:white;">
    <span style="font-family:monospace;font-weight:500;">FC-2026-0410-001</span>
  </td>
  <!-- 其他字段... -->
</tr>
```

### 问题8：script 标签格式导致同步失败

**症状**：同步后弹窗函数丢失

**原因**：`</script>` 后面没有正确换行，导致被当作 HTML 标签解析

**解决方案**：
```html
<!-- ❌ 错误 -->
<script>function foo(){}</script><div>

<!-- ✅ 正确 -->
<script>
function foo(){}
</script>
<div>
```

---

## 常见问题速查表

| 问题 | 症状 | 解决方案 |
|------|------|----------|
| 弹窗打不开 | `xxx is not defined` | 检查 main.js 引用位置和函数定义 |
| Tab 选中态错乱 | 所有 Tab 同时选中 | 用页面级作用域选择器 |
| Hash URL 不工作 | 页面 `display:none` | 添加 hashchange 监听 |
| 表格侵入侧边栏 | 横向滚动时布局乱 | 用 Ant Design 固定表头表格 |
| 复选框丢失 | 数据行没有 checkbox | 手动添加每个数据行的复选框 |
| 同步后功能失效 | 弹窗/按钮不工作 | 检查 script 标签格式和 div 平衡 |

---

## 📝 WMS 项目实战经验（2026-04-14）

### 经验1：弹窗 HTML 必须在页面 div 内部

**问题现象**："新增组织"按钮点击无反应，弹窗无法打开

**排查过程**：
1. 检查按钮 onclick 处理函数 → 存在
2. 检查 JavaScript 函数 → 存在
3. 检查弹窗 HTML 位置 → **发现弹窗放在了页面 div 外部**

**根本原因**：
```html
<!-- ❌ 错误：弹窗在页面 div 外部 -->
<div id="page-system_org" class="page">
  ...页面内容...
</div>
<!-- 弹窗在这里，页面关闭后的位置 -->
<div id="modal-add-org" style="display:none...">...</div>

<!-- ✅ 正确：弹窗必须在页面 div 内部 -->
<div id="page-system_org" class="page">
  ...页面内容...
  <!-- 弹窗必须放在这里 -->
  <div id="modal-add-org" style="display:none...">...</div>
</div>
```

**教训**：弹窗 HTML 放在 `</div>` (页面关闭标签) **之后**导致弹窗不显示。必须在页面 div 内部。

---

### 经验2：JavaScript 语法错误会导致整个脚本块失效

**问题现象**：修复弹窗位置后，按钮仍然无法点击

**排查过程**：
1. 使用 prototype-design 技能的调试方法
2. 检查 div 平衡 → 发现页面 div 缺少闭合标签
3. 修复 div 后检查脚本块 → 发现多余的 `}`

**根本原因**：`submitNewException()` 函数后有一个**多余的闭合括号 `}`**，导致 JavaScript 语法错误，整个脚本块无法执行

```javascript
// ❌ 错误：函数后有多余的 }
function submitNewException() {
  // ...表单提交逻辑
}
//}  <-- 多余的括号导致语法错误

// ✅ 正确：括号匹配
function submitNewException() {
  // ...表单提交逻辑
}
```

**教训**：修改 HTML 时要确保 div 平衡；修改 JS 时要确保括号匹配。使用 Python 脚本做精确替换比手动编辑更安全。

---

### 经验3：按钮必须手动绑定 onclick

**问题现象**：新增弹窗后，弹窗中的按钮点击无反应

**根本原因**：新增的弹窗按钮**没有 onclick 属性**

**解决方案**：每个按钮都要显式绑定 onclick
```html
<!-- ❌ 错误：按钮没有 onclick -->
<button class="btn btn-primary">确定</button>

<!-- ✅ 正确：显式绑定 onclick -->
<button onclick="submitAddOrg()" class="btn btn-primary">确定</button>
```

**教训**：复制弹窗模板时，别忘了修改按钮的 onclick 属性。

---

### 经验4：按钮样式统一使用 CSS 类

**问题现象**：各页面按钮样式不统一，有内联样式如 `style="padding:10px 24px;"`

**解决方案**：统一使用 CSS 类
```html
<!-- ✅ 主按钮：黑色背景，胶囊形状 -->
<button class="btn btn-primary btn-sm">新增</button>

<!-- ✅ 次按钮：白色背景，灰色边框 -->
<button class="btn btn-outline btn-sm">取消</button>
```

**按钮样式规范**：
| 元素 | 类名 | 样式 |
|------|------|------|
| 主按钮 | `.btn .btn-primary` | 黑色背景 `#111827`，胶囊形 |
| 次按钮 | `.btn .btn-outline` | 白色背景，`#E5E7EB` 边框 |
| 按钮尺寸 | `.btn-sm` | `padding: 6px 12px; font-size: 12px` |
| 胶囊形状 | `border-radius: 50px` | 用于主、次按钮 |

---

### 经验5：Python 脚本精确替换避免手动错误

**问题现象**：手动编辑 HTML 时容易出现 div 不平衡、括号遗漏等问题

**解决方案**：使用 Python 脚本做精确文本替换

```python
with open('index.html', 'r') as f:
    content = f.read()

# 替换前先备份
# ...

# 精确替换一段 HTML
old_text = '''<button class="btn btn-primary btn-sm">
              新增模块
            </button>'''

new_text = '''<button class="btn btn-primary btn-sm" onclick="openAddModuleModal()">
              新增模块
            </button>'''

content = content.replace(old_text, new_text)

with open('index.html', 'w') as f:
    f.write(content)

# 验证 div 平衡
print(f'opens={content.count("<div")}, closes={content.count("</div>")}, diff={content.count("<div")-content.count("</div>")}')
```

**教训**：用 Python 脚本做精确替换，比手动编辑更可靠，尤其是涉及多行 HTML 时。

---

### 经验6：系统管理模块弹窗字段设计

**新增模块弹窗字段**：
| 字段 | 类型 | 说明 |
|------|------|------|
| 模块编码 | text | 必填，如 SYS_010 |
| 模块名称 | text | 必填 |
| 上级模块 | select | 无（顶级模块）/系统管理/基础档案... |
| 模块分类 | select | 系统管理/基础档案/作业配置... |
| 菜单层级 | select | 一级/二级/三级菜单 |
| 菜单图标 | text | emoji 格式 |
| 路由路径 | text | 如 /system/module |
| 排序 | number | 数字越小越靠前 |
| 状态 | select | 启用/禁用 |
| 备注 | textarea | 可选 |

**新增组织弹窗字段**：
| 字段 | 类型 | 说明 |
|------|------|------|
| 组织编码 | text | 必填，如 ORG_010 |
| 组织名称 | text | 必填 |
| 上级组织 | select | 母公司/北京仓/上海仓... |
| 组织类型 | select | 公司/仓库/部门/作业组 |
| 负责人 | text | 可选 |
| 联系电话 | tel | 可选 |
| 所在地区 | text | 如 北京市/朝阳区 |
| 状态 | select | 启用/禁用 |
| 组织地址 | textarea | 可选 |

**新增用户弹窗字段**：
| 字段 | 类型 | 说明 |
|------|------|------|
| 用户名 | text | 必填 |
| 登录密码 | password | 必填，6位以上 |
| 姓名 | text | 必填 |
| 手机号 | tel | 必填 |
| 邮箱 | email | 可选 |
| 所属组织 | select | 必填，北京仓-收货组/上海仓... |
| 用户角色 | select | 超级管理员/仓库管理员/作业员... |
| 岗位 | text | 可选 |
| 入职日期 | date | 可选 |
| 状态 | select | 正常/禁用/待审核 |

---

### 经验7：数据统计报表页面丰富度提升

**质量与异常报表增强**：
- 异常趋势图（近7天柱状图）
- 异常类型分布（货损42%/配送延误28%等）
- 闭环率分析（96.8%闭环率、2.5h平均处理时长）

**对账准确率监察增强**：
- KPI 从 4 个扩展到 6 个
- 新增已核销/核对中指标

**作业报表增强**：
- 新增时效达标率分析（拣货98.5%/上架97.8%等）

**库存报表增强**：
- 新增滞销库存预警（30天以上）
- 新增安全库存预警

---

### 经验8：复合条件定位按钮

**问题现象**：页面有多个相似按钮（如"新增"），用 `document.querySelector` 定位困难

**解决方案**：使用复合条件或更精确的选择器

```javascript
// ❌ 困难：页面有多个 btn-primary
document.querySelector('.btn.btn-primary')

// ✅ 更好：使用 onclick 属性定位
document.querySelector('button[onclick="openAddModuleModal()"]')

// ✅ 更好：在页面内部查找
document.querySelector('#page-system_module button[onclick="openAddModuleModal()"]')
```

---

### 经验9：修改后立即验证

**原则**：每次修改后立即验证，不要积累多个问题

**验证清单**：
```bash
# 1. 检查 div 平衡
python3 -c "with open('index.html') as f: c=f.read(); print(f'opens={c.count(\"<div\")}, closes={c.count(\"</div>\")}, diff={c.count(\"<div\")-c.count(\"</div>\")}')"

# 2. 截图验证
agent-browser goto http://localhost:8080/#page-name
agent-browser eval "openAddModal()"
agent-browser screenshot test-modal.png
agent-browser close

# 3. 提交代码
git add -A && git commit -m "feat: 描述"
```

---

### 经验10：单页 HTML 项目的好处

**为什么 WMS 原型用单页 HTML 没有问题**：
1. **Compaction 只压缩对话历史**：不影响 HTML 文件本身
2. **不是日志文件**：不会无限增长
3. **每次修改同一个文件**：不是追加模式
4. **3700+ divs 仍然高效**：文件体积适中，渲染快

**什么时候该拆分成多文件**：
- 单个文件超过 2MB
- 需要多人协作（git merge 冲突）
- 模块之间完全独立

