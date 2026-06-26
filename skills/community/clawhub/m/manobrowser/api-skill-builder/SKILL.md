---
name: api-skill-builder
description: 根据用户需求，通过逆向网页API生成可复用的API取数Skill。适用于：图表数据（Canvas/ECharts/G2等前端渲染的图表）、需要登录态的平台数据、任何通过浏览器能看到但DOM中无法直接提取的数据。核心方法：鉴权探测决定架构 → 找到API endpoint → 逆向请求参数 → 验证数据 → 生成标准化Skill。
version: 2.0.0
tags: [API逆向, 数据提取, Skill生成, 元技能]
---

# API 取数 Skill 生成器

## 安全声明

本模块的 Cookie 提取和 API 测试功能遵循以下安全原则：

- **本地验证**：`document.cookie` 仅用于本地 `curl` 命令测试 API 鉴权机制，不会上传至任何外部服务
- **用户授权**：所有操作仅作用于用户已登录的平台，需用户明确触发
- **合法用途**：适用于开发调试、数据导出、自动化测试等场景，用户需确保符合目标平台的使用条款

---

## 概述

这是一个**元技能（Meta-skill）**，将"逆向网页API并生成可复用取数Skill"的方法论封装为标准流程。

**核心思路：页面上能看到的数据，一定来自某个 API 请求。找到 API → 逆向参数 → 生成可复用 Skill。**

**输入**：用户描述要从某个网页/平台获取什么数据
**输出**：一个完整的、可复用的 API 取数 Skill（SKILL.md + Python 脚本 + api_mapping.json）

## 前置条件

1. 浏览器已登录目标平台，登录态有效
2. DataSaver Chrome 扩展已安装并连接（提供 `fetch_api` 等工具）
3. MCP 端点已配置

## 设计原则

- **逻辑尽量收敛到 Python 脚本**：脚本可独立测试、可维护，SKILL.md 保持精简
- **SKILL.md 控制在 500 行以内**：超过后 Claude 执行步骤时遗漏/出错概率显著上升
- **Claude 只做调度员**：参数收集 + 执行脚本 + 转述输出，不参与数据处理
- **所有数据处理由脚本完成**：避免 LLM 截断数据或产生幻觉

## 执行流程（5个阶段）

```
阶段0: 鉴权探测（确定 Cookie 是否够用）
  ↓
阶段1: 侦察（找到 API endpoint）
  ↓
阶段2: 逆向（破解请求参数）
  ↓
阶段3: 验证（确认数据完整性 + 发现转换规则）
  ↓
阶段4: 生成（产出 Skill 三件套）
```

---

### 阶段0: 鉴权探测 — 确定 Cookie 可用性

**目标**：确认 `document.cookie` 能否独立完成 API 鉴权，这决定了脚本是否能直接调用 API。

#### Step 0.1: 提取 document.cookie

```javascript
// chrome_execute_script, world: MAIN, tabId: <目标页面>
() => document.cookie
```

记录 Cookie 内容，识别可能的鉴权 token（如 `sso.token`、`access-token`、`User`、`sessionid` 等）。

#### Step 0.2: 找到一个数据 API endpoint

通过 Performance API 快速找一个数据 API（详见阶段1 Step 1.2），用于鉴权测试。

#### Step 0.3: curl 鉴权测试

<critical>
⚠️ **必须使用 Bash 的 curl 命令测试，严禁使用 MCP 工具（fetch_api / chrome_background_network_request）！**

MCP 工具走 Chrome 网络栈，会在底层自动附加 httpOnly cookie，即使设置 `includeCookies: false` 或传入假 Cookie 也无效，导致鉴权测试结果**永远成功**，产生误判。

curl 是完全独立于浏览器的 HTTP 客户端，只发送你显式传入的 Cookie，是唯一可靠的验证方式。
</critical>

```bash
curl -s -X <METHOD> \
  -H "Cookie: <Step 0.1 提取的 document.cookie>" \
  -H "Content-Type: application/json" \
  -H "User-Agent: Mozilla/5.0" \
  "<API_URL>" [-d '<request_body>'] \
  | python3 -c "import json,sys; d=json.load(sys.stdin); print(json.dumps({
    'status': d.get('status', d.get('code', d.get('Code'))),
    'msg': d.get('msg', d.get('Msg', ''))
  }, ensure_ascii=False))"
```

> ⚠️ **必须测试数据接口**，不能只测配置接口。同一平台的不同 API 鉴权要求可能不同——配置接口可能无需 session，但数据接口需要。

#### Step 0.4: 确定 Cookie 可用性

- **curl 成功（返回正常数据）**→ `document.cookie` 包含全部鉴权信息。Python 脚本可通过 Cookie 文件独立发请求，完整包揽 API 调用 + 格式化 + 保存。
- **curl 失败（session 为空 / 401 / 签名错误）**→ 平台使用 httpOnly cookie 或请求签名。API 调用必须通过 MCP `fetch_api`（自动注入浏览器全部 cookie）完成，Python 脚本仅负责格式化和保存。

**阶段0产出**：明确 Cookie 是否够用，决定 Python 脚本的职责范围。

---

### 阶段1: 侦察 — 找到 API Endpoint

**目标**：确定目标数据来自哪个 API 请求。

#### Step 1.1: 页面截图 + 结构分析

用 `chrome_screenshot` 和 `chrome_accessibility_snapshot` 了解页面布局，确认：
- 数据展示方式（表格/图表/卡片等）
- 是 DOM 渲染还是 Canvas 渲染
- 有哪些筛选条件（类目、日期、维度等）
- 页面区块划分（一组筛选条件对应几个数据区块/API）

#### Step 1.2: Network Debugger 抓包（推荐首选）

**`chrome_network_debugger_start` 是最直接的 API 发现方式**，能同时捕获完整的请求 URL、请求体和响应体。

**使用流程**：

1. 启动 debugger：
```
chrome_network_debugger_start
```

2. 如果报错 `"Debugger is already attached to tab ... by another tool (e.g., DevTools)"`：

   **原因和解决方法（按可能性排序逐一尝试）**：

   1. **MCP 浏览器扩展自身占用**（最常见）：浏览器顶部会出现「"XXX"已开始调试此浏览器」的蓝色/黄色提示条。**提示用户点击提示条上的「取消」按钮**释放 debugger 连接，然后重试
   2. **Chrome DevTools 占用**：目标标签页打开了 DevTools（F12）。**提示用户关闭 DevTools**，然后重试
   3. **新开标签页重试**：用 `chrome_navigate` 打开同 URL 的新标签页，关闭旧标签页，再启动 debugger
   4. **以上都不行时**：明确告知用户「Network Debugger 被占用，请检查浏览器顶部是否有调试提示条并点击取消，或关闭 DevTools 后告诉我」，**等待用户确认后再重试**

   > ⚠️ **不要跳过 Network Debugger 直接用其他方法替代**。debugger 是唯一能同时获取完整请求体+响应体的工具，对 API 逆向至关重要。务必通过上述步骤排除占用问题后成功启动。

3. Debugger 启动后，通过**切换筛选条件**或**点击页面元素**触发数据 API 请求（不要刷新页面，刷新会断开 debugger 连接）

4. 等待几秒后停止捕获：
```
chrome_network_debugger_stop
```

5. 从结果中筛选数据 API（排除 `mcs.zijieapi.com`、`mon.zijieapi.com` 等埋点域名），提取 URL、请求体、响应体

<critical_warning>
⚠️ 注意事项：
- 启动 debugger 后**不要刷新页面**，刷新会断开连接导致抓到 0 条请求
- 页面数据已加载完毕时，需要通过交互（切换下拉框、点击按钮等）触发新的 API 请求
- 如果持续报 "Debugger is already attached" 且关闭 DevTools 无效，尝试新开标签页
</critical_warning>

#### Step 1.3: Performance API 探测（补充）

如果 Network Debugger 无法使用，或需要快速获取页面已加载的 API 列表：

```javascript
// chrome_execute_script, world: MAIN
() => JSON.stringify(
  performance.getEntriesByType('resource')
    .filter(e => e.initiatorType === 'xmlhttprequest' || e.initiatorType === 'fetch')
    .map(e => ({ url: e.name.split('?')[0], duration: Math.round(e.duration) }))
)
```

从结果中筛选出可能的数据 API（排除埋点、统计、静态资源等）。

> Performance API 只返回 URL（不含请求体和响应体），适合快速定位 API 端点后用 `fetch_api` 试探验证。

#### Step 1.4: XHR 拦截器注入（备选）

如果 Network Debugger 不可用且 Performance API 不够，可注入拦截器后**切换筛选条件**触发新请求：

```javascript
// chrome_inject_script, type: MAIN
(function() {
  window.__capturedAPIs = [];
  const origFetch = window.fetch;
  window.fetch = function(input, init) {
    const url = typeof input === 'string' ? input : input.url;
    if (url && url.includes('/api/')) {
      return origFetch.apply(this, arguments).then(resp => {
        const cloned = resp.clone();
        cloned.text().then(text => {
          window.__capturedAPIs.push({
            method: (init && init.method) || 'GET',
            url: url.split('?')[0],
            body: init && init.body ? String(init.body).substring(0, 2000) : null,
            status: resp.status,
            responsePreview: text.substring(0, 800)
          });
        });
        return resp;
      });
    }
    return origFetch.apply(this, arguments);
  };
})();
```

> 注入后通过**切换筛选条件**（而非刷新页面）触发 API，刷新会清除注入的脚本。
> ⚠️ 在使用微前端沙箱的平台上，拦截器可能对子应用请求无效。

#### Step 1.5: JS Bundle / Webpack Chunk 搜索（最后手段）

在 JS 源码中搜索 API 路径常量。适用于上述方法都无法捕获到目标 API 时：

```javascript
// chrome_execute_script, world: MAIN
() => {
  const chunks = window.webpackChunk_N_E || window.webpackChunkapp || [];
  let results = [];
  chunks.forEach((chunk, i) => {
    const modules = chunk[1];
    Object.entries(modules).forEach(([id, fn]) => {
      const src = fn.toString();
      if (src.includes('搜索关键词')) {
        results.push({ chunkIndex: i, moduleId: id,
          snippet: src.substring(src.indexOf('关键词') - 50, src.indexOf('关键词') + 100) });
      }
    });
  });
  return JSON.stringify(results);
}
```

> ⚠️ 在微前端架构下效率极低（子应用代码分散在多个异步 chunk 中，API 路径可能被动态拼接），优先使用 Network Debugger。

**阶段1产出**：确认目标 API 的完整 URL 和请求方法

---

### 阶段2: 逆向 — 破解请求参数

**目标**：搞清楚 API 需要什么参数、参数名是什么、值怎么来。

#### Step 2.1: 获取配置/常量接口

大多数平台有配置接口，返回可用字段、枚举值、类目树等。从中提取：
- 可用字段列表（指标名、字段名）
- 类目/分类树结构
- 枚举值映射

#### Step 2.2: JS 源码逆向参数构造

在 JS bundle 或 webpack chunks 中搜索 API 路径常量，关注：
- **参数名**（⚠️ 大小写敏感！）
- **参数类型**（string/array/number）
- **必填/可选**、**默认值**
- **参数值来源**（硬编码/用户选择/其他接口返回/页面组件状态）

#### Step 2.3: 动态参数发现

部分参数无法通过 API 获取（如下拉框选项的内部 ID），需从页面组件状态提取：

```javascript
// React 组件 fiber 提取
() => {
  const results = [], seen = new Set();
  document.querySelectorAll('*').forEach(el => {
    for (const key in el) {
      if (key.startsWith('__reactFiber$')) {
        let fiber = el[key];
        for (let i = 0; i < 10 && fiber; i++, fiber = fiber.return) {
          const p = fiber.memoizedProps || fiber.pendingProps;
          if (p && p.value && p.label && !seen.has(p.value)) {
            results.push({label: p.label, value: p.value});
            seen.add(p.value);
          }
        }
        break;
      }
    }
  });
  return JSON.stringify(results);
}
```

> Vue 项目改用 `el.__vue__` 或 `el.__vue_app__` 获取组件实例。

#### Step 2.4: 试探性请求

用 `fetch_api` 发送试探请求，逐步确认参数：
1. 先发最小参数集 → 看返回什么
2. 逐个加可选参数 → 观察返回变化
3. 测试参数名大小写变体 → 确认哪个版本有效
4. 确认返回数据是否完整覆盖页面展示的内容

<critical_warning>
⚠️ 参数名大小写陷阱！同一 API 中可能混用大小写参数名（如 `xindex` 和 `sizeIndex` 共存），用错大小写可能请求成功但数据不完整。必须逐一验证！
</critical_warning>

#### Step 2.5: 区分用户参数与固定参数

- **用户参数**：需要用户指定的（类目、日期、排序等）→ 写入参数确认流程
- **固定参数**：每次固定不变的（版本号、指标默认值等）→ 硬编码到脚本中

**阶段2产出**：完整的请求参数文档 + 用户参数 vs 固定参数清单

---

### 阶段3: 验证 — 确认数据完整性 + 发现转换规则

**目标**：确保 API 返回的数据与页面展示一致，并发现所有数据转换规则。

#### Step 3.1: 数据对比验证

1. 截图页面上显示的数据
2. 用 API 获取同样条件的数据
3. 逐一对比确认数值一致

#### Step 3.2: 数据转换规则发现

<critical>
API 返回的原始值往往与页面展示值不同。必须逐一对比发现转换规则并记录。
</critical>

常见转换模式：

| 检查项 | 示例 |
|--------|------|
| **数值缩放** | API 返回 4.2266，页面显示 422 → 需 ×100 取整 |
| **层级过滤** | API 返回一级+二级分类，页面只显示一级 → 按字段过滤 |
| **百分比格式不统一** | 同一 API 中字段 A 已是百分比，字段 B 需要 ×100 |
| **排序截断** | 页面只展示 TOP N |
| **字段重命名** | API 字段名与页面显示名不同 |
| **数值格式化** | API 返回字符串数字，需转数字后格式化 |

**将所有转换规则记录下来，写入 Python 脚本的格式化函数中。**

#### Step 3.3: 边界情况测试

- 不同参数组合是否都能正常返回
- 空数据情况的处理
- **分页陷阱**：`pagesize` 参数是否真实生效（有些平台声称支持 50 条/页但实际只返回 10 条）
- 多次请求覆盖所有指标组合

#### Step 3.4: 响应结构文档化

记录完整的响应 JSON 结构、各字段含义、数据类型、嵌套结构、分页信息。

**阶段3产出**：验证通过的 API 调用方案 + 响应结构文档 + 数据转换规则清单

---

### 阶段4: 生成 — 产出 Skill 三件套

**目标**：生成 SKILL.md + Python 脚本 + api_mapping.json。

#### Step 4.1: 生成目录结构

```
skill-name/
├── SKILL.md              # 流程编排（≤500行）
├── scripts/
│   └── fetch_xxx.py      # Python 脚本
└── references/
    └── api_mapping.json   # API 参考文档
```

#### Step 4.2: 生成 api_mapping.json

记录所有 API 端点、参数、响应结构，作为开发和维护的参考文档。

#### Step 4.3: 生成 Python 脚本

**脚本职责取决于阶段0的结论**：

- **Cookie 够用时**：脚本包揽全部逻辑——Cookie 文件读取、HTTP 请求（带重试/限流）、并发编排、结果格式化、JSON 保存。Claude 只执行一条 bash 命令调用脚本。
- **Cookie 不够时**：API 调用由 Claude 通过 MCP `fetch_api` 完成，脚本只负责读取 API 响应 JSON 文件、格式化展示、合并保存。

**无论哪种情况，脚本都应包含**：
- 阶段3发现的所有数据转换规则
- 格式化输出（终端友好的表格/列表）
- JSON 文件保存（含查询参数元信息）
- `argparse` 命令行参数支持
- `FileNotFoundError` / `JSONDecodeError` 标准异常处理

**脚本输入格式约定**：脚本接收的 JSON 文件应为 **API 完整响应**（含 `code`/`status`/`msg`/`data` 外层包装），脚本内部负责检查状态码并提取 `data` 字段。SKILL.md 中保存文件的步骤和脚本的解析逻辑必须对齐，避免一方保存完整响应、另一方只解析内层数据导致"找不到数据"。

**Cookie 够用时，脚本额外包含**：
- `load_cookies(file)` 从文件解析 Cookie
- `_make_request(method, url, cookies, body)` 带重试和限流
- `ThreadPoolExecutor` 并发请求，带 `STAGGER_DELAY` 错开间隔
- 退出码协议：`0`=成功，`2`=需用户确认，`3`=Cookie 过期
- `--list-xxx` 查看可选项的子命令

#### Step 4.4: 生成 SKILL.md

参考 [skill_template.md](references/skill_template.md) 模板。

**SKILL.md 通用结构**：

```
1. YAML 头部（name, description）
2. 执行流程概览
3. Step 0: Cookie/登录检查
4. Step 1: 参数确认（含路径分支）
5. Step 2: 执行查询
6. Step 3: 展示结果
7. Cookie 刷新流程
8. 错误处理表
9. 测试验证（≥3 个问答对）
```

**参数确认流程**应为每个用户参数提供路径分支：

- **路径 A：用户已明确指定** → 直接使用
- **路径 B：用户未指定，有列表 API** → 调用脚本或 MCP 获取列表，展示后等待选择
- **路径 C：无列表 API，需页面提取** → MCP 导航页面 + chrome_execute_script 提取组件状态
- **路径 D：需二次确认** → 脚本 exit code 2 触发，解析输出后询问用户

**Cookie 刷新流程**根据阶段0结论决定：
- Cookie 够用：MCP 提取 document.cookie → 写入文件 → 重跑脚本
- Cookie 不够：确认浏览器已登录 → MCP fetch_api 直接调 API（无需提取 cookie）

**展示结果规则**：
- 严禁幻觉：所有内容必须来自脚本实际终端输出
- 严禁截断：所有数据处理由脚本完成，Claude 只转述输出
- 必须列出 JSON 文件完整路径

#### Step 4.5: 展示摘要并等待确认

```
✅ API 取数 Skill 生成完成！

📊 生成统计：
- Skill名称：{skill-name}
- 目标平台：{platform}
- Cookie可独立鉴权：是/否
- API端点：{N} 个
- 用户参数：{M} 个
- 数据转换规则：{K} 条

📁 文件：
- {skill-name}/SKILL.md（{lines}行）
- {skill-name}/scripts/{script}.py（{lines}行）
- {skill-name}/references/api_mapping.json

请确认是否符合预期？
```

#### Step 4.6: 稳定性自检

- [ ] SKILL.md 行数 ≤ 500
- [ ] Python 脚本可独立运行测试
- [ ] 所有数据处理在脚本中完成，Claude 只转述输出
- [ ] 有 ≥ 3 个测试问答对
- [ ] Cookie 过期有检测和恢复流程
- [ ] 分页逻辑已验证（实际返回量 vs pagesize 参数）
- [ ] 阶段3发现的数据转换规则已全部写入脚本
- [ ] 鉴权方式经过 curl 验证

---

## 不靠谱的方法（踩过的坑，不要再试）

| 方法 | 为什么不行 |
|------|-----------|
| **MCP 工具做 cookie 鉴权测试** | `fetch_api` 和 `chrome_background_network_request` 都走 Chrome 网络栈，自动附加 httpOnly cookie，即使设 `includeCookies: false` 也无效。**必须用 curl 验证** |
| **cookieStore.getAll() 检测 httpOnly** | JavaScript API 设计上就无法看到 httpOnly cookie，返回空不代表没有 |
| **单一 API 测试代表全部** | 同一平台的配置接口和数据接口鉴权要求可能不同 |
| **SKILL.md 承载过程性代码** | 超过 500 行后稳定性急剧下降，逻辑应收敛到 Python 脚本 |
| **依赖 Claude 处理完整数据** | LLM 天然倾向截断长列表。数据处理必须由脚本完成 |
| `chrome_network_debugger_start` 报 "Debugger already attached" | 不是工具 bug，常见原因：MCP 浏览器扩展自身占用（看浏览器顶部调试提示条）或 DevTools 打开。**必须排除占用后成功启动，不要跳过**（见阶段1 Step 1.2） |
| **WebFetch 读取 OSS 响应 URL** | `fetch_api` 返回的 OSS URL（如 `deepmining.oss-cn-beijing.aliyuncs.com`）会被 WebFetch 的域名安全检查拦截。**必须用 `curl`（Bash 工具）下载 OSS 文件** |
| `chrome_network_capture_start` | webRequest API 不捕获 response body |
| XHR/fetch 注入后刷新 | 刷新后脚本丢失。应通过**切换筛选条件**触发新请求 |
| 从 DOM 提取 Canvas 图表数据 | 图表是 Canvas 渲染，数据不在 DOM 中 |
| `echarts.getInstanceByDom()` | 生产环境不暴露全局图表实例 |

**正确路径：curl 验证鉴权 → 找 API → 逆向参数 → 生成脚本**

---

## 关键技巧速查

| 技巧 | 说明 |
|------|------|
| **curl 鉴权验证** | 唯一可靠的 Cookie 鉴权测试方法 |
| **Network Debugger 抓包** | `chrome_network_debugger_start` → 交互触发 → `stop`，能抓完整请求体+响应体，是 API 发现的首选方法 |
| Performance API | `performance.getEntriesByType('resource')` 快速找 API 列表（只有 URL，无请求体/响应体） |
| XHR 拦截器 + 切换筛选 | 注入后切换条件（不刷新），捕获完整请求体和响应 |
| React fiber 提取 | `el.__reactFiber$` 遍历组件树获取下拉选项的 value/label |
| JS Bundle 搜索 | 下载 JS 文件搜索 API 路径关键词 |
| Webpack Chunk 遍历 | `window.webpackChunkXXX` 搜索已加载模块 |
| 配置接口先行 | 先调 constants/config 类接口获取字段定义 |
| 参数大小写验证 | 同一 API 可能混用大小写参数名 |
| fetch_api 自带 cookie | MCP fetch_api 自动注入浏览器全部 cookie（含 httpOnly） |
| 数据转换规则对比 | API 值 ≠ 页面值时记录缩放/过滤/格式化规则 |
| 退出码协议 | 脚本用 exit code 0/2/3 与 Claude 通信 |
