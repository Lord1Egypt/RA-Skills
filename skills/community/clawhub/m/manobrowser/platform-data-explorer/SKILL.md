---
name: platform-data-explorer
description: 通用平台探索 Skill。使用 DataSaver Chrome MCP 工具对目标平台（URL/页面/模块）进行系统性探索，发现该平台可以做哪些用户操作类和数据提取类 Skill，输出 Skill 提案清单供用户确认，确认后按类型分流创建：API取数类调用 api-skill-builder，浏览器操作类调用 chrome-workflow-build。
version: 3.0.0
tags: [平台探索, Skill发现, DataSaver, 浏览器自动化, 数据提取]
mcp_tools_required: [chrome_navigate, chrome_execute_script, chrome_get_document, chrome_click_element, fetch_api]
---

# 平台探索与 Skill 发现

## 概述

这是一个**探索型 Meta-skill**：给定任意平台 URL 或功能模块，使用 DataSaver 工具系统性探索该平台，分析出可以做哪些 Skill（操作类 + 取数类），生成 Skill 提案清单供用户选择，用户确认后按类型分流调用对应的创建 skill：

- **API 取数类** → 调用 `api-skill-builder`（逆向 API → 生成取数 Skill）
- **浏览器操作类** → 调用 `chrome-workflow-build`（执行并记录 → 生成操作 Skill）

**输入**：平台 URL / 模块名称 / 功能描述
**输出**：Skill 提案清单（含优先级、可行性评估、实现方案）

## 执行流程

```
Phase 1: 平台侦察（了解平台全貌）
    ↓
Phase 2: 功能模块发现（逐个模块探索）
    ↓
Phase 3: Skill 可行性评估（每个潜在 Skill 的技术方案）
    ↓
Phase 4: 输出提案清单（供用户确认）
    ↓
Phase 5: 用户确认后，按类型分流创建 Skill
```

---

## Phase 1: 平台侦察

**目标**：了解平台整体结构、技术栈、主要功能模块。

### Step 1.1: 打开目标页面

```
工具: chrome_navigate
参数:
  url: {target_url}
  active: true
```

> ⚠️ `active: true` 很重要，某些 SPA 平台（如灵犀）在后台标签页不加载数据。

### Step 1.2: 页面结构分析

```
工具: chrome_get_document
```

**观察并记录**：
- 平台名称和类型（数据平台 / 内容平台 / 电商 / 工具类）
- 技术栈（React / Vue / Angular / jQuery）
- 导航结构（侧边栏菜单 / 顶部Tab / 面包屑）
- 是否需要登录
- 主要功能入口有哪些

### Step 1.3: 导航菜单提取

```javascript
// 提取平台的导航菜单结构
(() => {
  // 尝试多种常见导航结构
  const navSelectors = [
    'nav a', '.sidebar a', '.menu a', '.nav-item a',
    '[class*="menu"] a', '[class*="nav"] a', '[class*="sidebar"] a',
    '.ant-menu a', '.el-menu a', // Ant Design / Element UI
  ];
  const links = new Set();
  const menuItems = [];

  navSelectors.forEach(sel => {
    document.querySelectorAll(sel).forEach(a => {
      const text = a.textContent.trim();
      const href = a.getAttribute('href') || '';
      const key = text + '|' + href;
      if (text && text.length < 30 && !links.has(key)) {
        links.add(key);
        menuItems.push({ text, href, visible: a.offsetParent !== null });
      }
    });
  });

  return JSON.stringify({
    totalMenuItems: menuItems.length,
    items: menuItems.slice(0, 50)
  }, null, 2);
})()
```

### Step 1.4: API 与资源分析

```javascript
// 发现平台加载了哪些 API 和资源
(() => {
  const resources = performance.getEntriesByType('resource');
  const apis = resources
    .filter(r => r.initiatorType === 'xmlhttprequest' || r.initiatorType === 'fetch')
    .map(a => {
      const url = new URL(a.name);
      return { path: url.pathname, params: url.search.substring(0, 80) };
    });

  // 去重，按路径分组
  const apiGroups = {};
  apis.forEach(a => {
    const base = a.path.replace(/\/\d+/g, '/{id}'); // 归一化数字ID
    if (!apiGroups[base]) apiGroups[base] = { path: a.path, count: 0 };
    apiGroups[base].count++;
  });

  return JSON.stringify({
    totalAPIs: apis.length,
    uniqueAPIs: Object.keys(apiGroups).length,
    apiList: Object.values(apiGroups).slice(0, 30)
  }, null, 2);
})()
```

---

## Phase 2: 功能模块探索

**目标**：逐个进入主要功能模块，了解每个模块有什么数据和操作。

对 Phase 1 发现的每个主要模块：

### Step 2.1: 导航到该模块

```
工具: chrome_navigate 或 chrome_click_element
进入对应模块页面
```

### Step 2.2: 分析模块内容

```
工具: chrome_get_document
观察模块页面结构
```

**对每个模块记录**：

```markdown
### 模块: {模块名}
- **URL**: {url}
- **页面类型**: 列表页 / 详情页 / 图表页 / 表单页 / 仪表盘
- **主要内容**:
  - 数据展示: {描述看到了什么数据，表格/图表/卡片/数字}
  - 用户操作: {描述有哪些可操作的元素，按钮/筛选/输入框/导出}
  - 筛选条件: {时间/类目/关键词/地域等}
- **数据来源判断**:
  - 图表类 → 大概率有 API
  - 表格类 → 可能 DOM 提取或 API
  - 纯展示类 → DOM 提取
```

### Step 2.3: 探索数据源（对每个模块快速验证）

```javascript
// 在该模块页面下检查有哪些新的 API 请求
(() => {
  const resources = performance.getEntriesByType('resource');
  const apis = resources
    .filter(r =>
      (r.initiatorType === 'xmlhttprequest' || r.initiatorType === 'fetch') &&
      r.name.includes('/api/')
    )
    .map(a => new URL(a.name).pathname);
  return JSON.stringify([...new Set(apis)], null, 2);
})()
```

**快速验证 API 是否可用**（可选，针对重点模块）：

```
工具: fetch_api
参数:
  url: {discovered_api}
  method: GET
  cookieDomain: .{domain}
  includeCookies: true
```

---

## Phase 3: Skill 可行性评估

对 Phase 2 发现的每个潜在 Skill，评估技术可行性：

### 评估维度

| 维度 | 评分标准 |
|------|----------|
| **数据可获取性** | API 直接可调(⭐⭐⭐) / DOM 结构清晰(⭐⭐) / 需要复杂操作(⭐) |
| **稳定性** | API 稳定(⭐⭐⭐) / DOM 选择器稳定(⭐⭐) / 结构可能变化(⭐) |
| **反爬风险** | 无限制(⭐⭐⭐) / 有频率限制(⭐⭐) / 严格反爬(⭐) |
| **实用价值** | 高频需求(P0) / 有价值(P1) / 锦上添花(P2) |

### Skill 分类

**操作类 Skill**（自动化用户操作）：
- 发布内容、提交表单、批量操作、导出报表…

**取数类 Skill**（提取数据）：
- 搜索采集、详情提取、报表数据、图表数据、监控数据…

---

## Phase 4: 输出 Skill 提案清单

将探索结果整理为结构化提案，供用户确认：

```markdown
# {平台名} Skill 提案清单

## 平台概况
- **URL**: {url}
- **类型**: {平台类型}
- **技术栈**: {React/Vue/...}
- **需要登录**: 是/否

## 发现的模块
{Phase 2 中探索的模块列表}

## Skill 提案

### P0（高优先级）

#### 1. {skill-name-1}
- **类型**: 取数(API) / 取数(DOM) / 操作
- **功能**: {一句话描述}
- **数据/操作**: {具体能获取什么数据 或 完成什么操作}
- **技术方案**: API 逆向 / DOM 提取 / 混合
- **创建方式**: `api-skill-builder` / `chrome-workflow-build`
- **可行性**: ⭐⭐⭐
- **备注**: {特殊注意事项}

#### 2. {skill-name-2}
...

### P1（中优先级）
...

### P2（低优先级）
...

---
请确认想要创建哪些 Skill，我会根据类型调用对应的创建流程：
- API 取数类 → `api-skill-builder`
- 浏览器操作类 → `chrome-workflow-build`
```

---

## Phase 5: 按类型分流创建 Skill

用户确认后，根据 Skill 类型选择对应的创建流程，**逐个**创建：

### 分流规则

| Skill 类型 | 判断依据 | 创建流程 |
|------------|----------|----------|
| **API 取数类** | 数据来自 API 接口（图表、动态数据、需要参数的查询） | 调用 `api-skill-builder`（4阶段：侦察→逆向→验证→生成） |
| **浏览器操作类** | 需要模拟用户操作（点击、输入、导航、DOM提取） | 调用 `chrome-workflow-build` 模式1（3阶段：LOG→WORKFLOW→CREATOR） |

### API 取数类 → `api-skill-builder`

执行 `api-skill-builder` 的标准流程：
1. **阶段1 (侦察)**: 找到 API endpoint
2. **阶段2 (逆向)**: 破解请求参数
3. **阶段3 (验证)**: 确认数据完整性
4. **阶段4 (生成)**: 产出 workflow.json + SKILL.md

### 浏览器操作类 → `chrome-workflow-build`

执行 `chrome-workflow-build` 模式1 的标准流程：
1. **阶段1 (LOG)**: 使用 DS 工具实际执行一遍操作，记录执行日志
2. **阶段2 (WORKFLOW)**: 从日志提取可复用工作流
3. **阶段3 (CREATOR)**: 生成 SKILL.md

### 创建顺序

1. 每个 Skill 创建完成后向用户确认结果，再开始下一个
2. 优先创建 P0，再 P1、P2

<important_note>
本 Skill 负责的是**探索和发现**环节。
Skill 的实际创建交给对应的创建 skill，不要在本 Skill 中直接编写最终的 SKILL.md。
</important_note>

---

## 探索经验库

以下经验来自实际平台探索，供探索新平台时参考：

### 技术经验

<experience_api>
**API 逆向经验**：
- 图表数据（折线/柱状/气泡/饼图）一定来自 API，Canvas 渲染后 DOM 里没有数据
- 找 API 路径：`performance.getEntriesByType('resource')` → webpack chunk 搜索 → JS bundle 搜索
- 配置接口先行：`/config`、`/constants`、`/meta` 类接口返回字段定义、枚举值、类目树
- 参数名大小写敏感：同一 API 可能混用大小写（如 `xindex` 小写 vs `sizeIndex` 大写I）
- 参数名单复数：`taxonomyCodes`(复数) vs `taxonomyCode`(单数) 可能导致系统错误
- 某些 API 每次只返回部分指标，需要多次请求拼合
- `fetch_api` 自动带 cookie，是最可靠的 API 调用方式
</experience_api>

<experience_dom>
**DOM 提取经验**：
- 选择器优先级：ID > data-* 属性 > 语义化 class > 位置选择器
- 瀑布流/无限滚动需要先滚动触发加载，再提取
- 虚拟滚动平台（如小红书）DOM 中只保留可视区域元素
- 轮播图/推荐列表可能有重复元素，需要去重
- 某些字段延迟加载，提取前需要足够的等待时间
</experience_dom>

<experience_pitfalls>
**已知的坑（不要踩）**：
- ❌ `chrome_network_debugger_start` — DS 扩展 bug，附加到错误的标签
- ❌ `chrome_network_capture_start` — 不捕获 response body
- ❌ XHR/fetch Proxy 注入 — 页面 JS 在注入前已缓存原始引用
- ❌ 从 Canvas/SVG 提取图表数据 — 渲染后的像素无法还原数据
- ❌ 生产环境访问 ECharts/G2 全局实例 — 不暴露
- ❌ `active: false` 打开 SPA 平台 — 数据可能不加载
</experience_pitfalls>

### 平台类型速查

| 平台类型 | 探索重点 | 典型 Skill |
|----------|----------|-----------|
| **SPA 数据平台**（灵犀等后台） | API 端点 + 配置接口 | 各模块数据提取 |
| **内容/社交平台**（小红书/微博） | DOM 结构 + 搜索/列表/详情页 | 搜索采集、详情提取、发布 |
| **电商平台**（淘宝/京东） | 商品 API + 反爬机制 | 商品采集、价格监控 |
| **BI/报表平台** | iframe + 导出功能 | 报表数据提取 |
| **工具类平台**（文档/设计） | 操作流程 + 导出 | 批量操作、格式转换 |

## 错误处理

| 问题 | 原因 | 解决 |
|------|------|------|
| 页面空白 / 未加载 | `active: false` 或未登录 | 设 `active: true`，确认登录态 |
| 导航菜单提取为空 | 菜单是动态渲染或 iframe | 等待加载 / 检查 iframe |
| API 列表为空 | 数据在首屏加载前已请求 | 刷新页面后再检查 / 搜索 JS bundle |
| 探索中遇到验证码 | 操作太频繁 | 暂停，等待 30-60 秒 |

## 版本信息

- **当前版本**：3.0.0
- **创建日期**：2026-03-10
- **更新日期**：2026-03-10
- **基于经验**：小红书（DOM提取）、灵犀平台（API逆向）、千瓜数据（API探索）
- **依赖 Skill**：`api-skill-builder`（API取数类）、`chrome-workflow-build`（浏览器操作类）
