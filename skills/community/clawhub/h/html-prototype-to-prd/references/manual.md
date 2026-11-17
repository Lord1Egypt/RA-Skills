# 单文件 HTML 原型 → 产品需求文档（PRD）完整操作手册

> 目的：把一个已有的单文件 HTML 交互原型，做成一份「截图 + 文字说明」的产品需求文档，单文件自包含，可直接发人。
> 使用方式：按第 2 到第 7 节顺序执行，脚本在 `_tools/prd_pipeline/`，改配置区即可复用。
> 参照成品：`亚马逊运营工作课表_产品需求文档PRD_2026-09-28.html`（9 章、17 张表、8 张真实运行截图、1.78MB 单文件）。

---

## 1. 最终产出长什么样（先把目标定清楚）

一份**单文件 HTML**，特征是：

| 项 | 要求 |
|---|---|
| 图片 | 全部来自原型**真实运行截图**，不是手绘示意图；以 base64 内嵌，文件自带，不依赖外部目录 |
| 结构 | 封面 → 文档说明 → 信息架构 → 页面详情 → 全局规则 → 待确认事项 → 附数据规模 |
| 每个页面 | 固定四段：一句话描述 → 截图 → 功能点表 → 交互规则列表 |
| 导航 | 左侧 sticky 目录，点标题跳转；窄屏自动隐藏 |
| 视觉 | 白底、宝蓝 `#1457A6` 主色、圆角卡片、浅灰表头；无 emoji、无中文破折号 |
| 体积 | 8 张图约 1.3MB，成品约 1.8MB，可接受 |

「效果一样」的关键不在排版，在两条：
1. **截图是真实交互态**（抽屉真的点开了、身份真的切了、搜索真的过滤了）；
2. **规则写的是代码里的事实**，不是从界面猜的。

---

## 2. 环境事实（本机实测，别重复踩）

| 项 | 值 |
|---|---|
| Node | `C:/Users/17551/.workbuddy/binaries/node/versions/22.22.2-3/node.exe` |
| Python | `C:/Users/17551/.workbuddy/binaries/python/versions/3.13.12/python.exe` |
| Chrome | `C:/Program Files/Google/Chrome/Application/chrome.exe` |
| CDP 客户端 | `_tools/prd_pipeline/cdp.mjs`（零依赖，Node 22 自带全局 `WebSocket`） |

**不要装 playwright / puppeteer。** Chrome 自带 headless + CDP，够用，装了反而引入版本问题。

**bash coreutils 在本机残缺**：`ls / head / tail / wc / grep` 常报 `command not found`。所有编排写成 `.mjs` 用 Node 跑，不要写成 shell 脚本。

**脚本输出必须落盘再读**：终端回显经常被吞（只看到 `Command completed with exit code 0`）。统一 `fs.writeFileSync` 到文件，再用 Read 判读。

---

## 3. 阶段一：读懂原型（这一步不能跳）

**先读完原型的 `<script>` 段再动手。** 这是整份 PRD 质量的分水岭。

界面截图只能告诉你"长什么样"。下面这些东西**只存在于 JS 里**，看图永远看不到：

- 任务的**生成条件**（哪些任务每天生成、哪些满足条件才生成）
- **校验规则**（比如"状态选已完成时，结论必填"）
- **状态枚举**（有哪些状态、各自什么含义）
- **数据唯一性规则**（同一任务会不会重复生成）
- **权限判定逻辑**（谁能看谁的数据）

以课表原型为例，从 JS 里挖出来的、界面完全看不出的三条：

```
日度任务仅工作日生成；月度任务到期日遇周末自动前移到上一个工作日；
「下班收尾」任务只在当天存在临时事项、或有待跟进／待核验任务时才生成。
```

这三条写进了 PRD 第四章「全局规则」，是整个文档最值钱的部分。

同时要读出来的还有**数据规模**（多少条任务、按什么维度分组），放文档最后一节。

---

## 4. 阶段二：起环境（两个后台进程）

### 4.1 准备 staging

原型文件**复制到 ASCII 路径**再服务，规避中文和空格带来的 URL 转义问题：

```bash
mkdir -p "<staging>"
cp "<原型.html>" "<staging>/demo.html"
cp "_tools/prd_pipeline/cdp.mjs" "<staging>/cdp.mjs"
```

### 4.2 起静态服务（后台）

```bash
"<Python>" -m http.server 8766 --directory "<staging>" --bind 127.0.0.1
```

**不要用 `file://`**：中文路径要转义，而且 `localStorage` 会抛 `SecurityError`，页面上依赖本地存储的交互会直接崩。

### 4.3 起 Chrome（后台）

```bash
"<Chrome>" --headless=new --remote-debugging-port=9222 \
  --user-data-dir="<staging>/chrome-profile" \
  --window-size=1440,1000 --no-first-run --no-default-browser-check \
  --hide-scrollbars --disable-gpu
```

两个进程都放后台跑，结束后**记得关掉**。

---

## 5. 阶段三：探测各视图高度

**为什么必须先探测**：不同视图的内容量差很多。实测同一个原型：

| 视图 | 高度 |
|---|---|
| 我的本周 | 1372px |
| 单日工作 | 1549px |
| 月度总览 | 1733px |
| 任务库 | 7221px |

统一按 1000px 截会把内容切掉；统一按 7221px 截，短视图会留一大片空白。

执行：

```bash
cd "<staging>" && "<Node>" 01_probe_views.mjs
```

改 `01_probe_views.mjs` 的配置区：

```js
const CONFIG = {
  url: 'http://127.0.0.1:8766/demo.html',
  width: 1440,
  views: [
    { name: 'week', click: `<点开该视图的 JS>` },
    ...
  ],
};
```

把 `probe.txt` 里的 `h` 值抄到下一步。

---

## 6. 阶段四：批量截图

```bash
"<Node>" 02_capture.mjs
```

配置区是「步骤数组」，每步截图前可以执行一串 JS：

```js
const goView = v => `Array.from(document.querySelectorAll('[data-view]')).find(b=>b.dataset.view==='${v}').click()`;

steps: [
  { file: '01_week.png',  height: 1400, before: [goView('week'), `window.scrollTo(0,0)`] },
  // 交互态：点开抽屉再截
  { file: '05_detail.png', height: 1020, before: [goView('day'), `document.querySelector('.task-row').click()`], wait: 600 },
  // 切换身份 + 范围
  { file: '07_head.png',   height: 1400, before: [
      `(function(){const el=document.querySelector('#identity');el.value='boss';el.dispatchEvent(new Event('change',{bubbles:true}))})()`,
      `(function(){const el=document.querySelector('#scope');el.value='all';el.dispatchEvent(new Event('change',{bubbles:true}))})()`,
      goView('week') ] },
]
```

要点：

- **下拉框切换要用 `dispatchEvent(new Event('change'))`**，直接改 `value` 不会触发页面里的监听。
- 卡片点击一律**模拟真实 click**，不要去调页面内部函数（拿不到闭包里的 state）。
- `wait` 给足（抽屉动画、重绘需要时间），一般 500ms 起步。
- 超长页（任务库 7000px+）**只截首屏**，别整页截。
- 脚本会打印每步的 `mainLen`，如果某张图 `mainLen` 明显偏小，说明选择器没命中，截到空白了。

---

## 7. 阶段五：写 PRD 模板

复制 `prd_template_example.html` 改。图片位置留占位符：

```html
<img src="__IMG_01__" alt="我的本周视图">
```

### 7.1 章节骨架（可复用）

```
封面（标签 + 标题 + 版本/日期/形态/状态）
1 文档说明    产品目标（3 到 5 条，写业务价值不写功能）+ 阅读约定表（术语表）
2 信息架构    层级表（全局导航 / 视图级 / 抽屉）+ 页面关系说明
3 页面详情    每个页面固定四段：一句话描述 → 截图 → 功能点表 → 交互规则列表
4 全局规则    优先级体系 / 状态机 / 生成规则 / 唯一性 / 数据与权限边界
5 待确认事项  表格，两列：待确认项 + 影响
附 数据规模   数量、分组维度、枚举清单
```

### 7.2 每页四段的写法

- **一句话描述**：说清这个页面解决什么问题，不要复述界面。
- **功能点表**：两列「区域 / 说明」，逐块拆界面。截图里看得见的都要有对应行。
- **交互规则列表**：点击后发生什么、状态怎么变、边界怎么处理。
- **完成标准**：如果这一页有明确的目标状态，加一列写"验收口径"。

### 7.3 内容纪律（这部分决定 PRD 可信度）

- **事实与建议分开标注**。凡是自己补的、原型里没有的，必须显式写"建议值，最终以 XX 为准"。例：
  > 色值为建议值，最终以视觉规范为准。
- **不要写排期**。需求文档里塞具体日期，评审时会被当成承诺；排期放单独的交付节奏章节或干脆不放。
- **「待确认事项」这一节要真的写**。列出信息缺口和它的影响，这是评审会上最有用的部分。
- 配色：白底 + 主色 `#1457A6` + 暖白 `#F5F3ED` + 点缀 `#C56A31`；状态色（已完成绿、延期橙）属于**语义色**，不要被主色替换掉。
- 禁用：emoji、中文破折号 `——`。

---

## 8. 阶段六：base64 注入

```bash
"<Node>" 03_build_prd.mjs
```

配置区把占位符映射到 PNG：

```js
images: {
  '__IMG_01__': 'shots/01_week.png',
  ...
}
```

**必须用 `split().join()` 而不是 `replace()`**：base64 里会出现 `$&`、`$1` 这类序列，用 `replace` 时会被当成替换模式，注入结果直接烂掉。

脚本会打印**未替换占位符数量**，必须是 `0`，否则说明模板里的图片位没配全。

---

## 9. 阶段七：验收（跳过这步必翻车）

```bash
cp "<产物.html>" "<staging>/prd_view.html"
"<Node>" 04_verify.mjs
```

必查两项：

1. **坏图**：`document.images` 里 `!complete || naturalWidth === 0` 的张数必须为 `0`。这一条能揪出 base64 没接上、路径写错、图没生成三类问题。
2. **结构数字**：章节数、页面块数、表格数要和模板对得上（期望值从模板里数出来，别猜）。

再抽查一张截图看排版（有没有图爆出容器、表格挤成一团）。

---

## 10. 坑清单（每条都真实付过代价）

| # | 坑 | 后果 | 对策 |
|---|---|---|---|
| 1 | 没读完 `<script>` 段就写 PRD | 漏掉生成条件、校验规则、状态枚举，PRD 只能描述界面，开发照着做会做错 | 写文档前先把 JS 读完，这些规则单独成章 |
| 2 | 所有截图统一视口高度 | 长视图被截断，或短视图大片空白 | 先跑 `01_probe_views.mjs` 逐个测高 |
| 3 | 超长页整页截 | 长宽比崩坏，放进文档没法看 | 只截首屏 |
| 4 | 用 `replace()` 注入 base64 | 图片数据被 `$&` 吃掉，图烂掉 | 用 `split().join()` |
| 5 | 用 `file://` 打开原型 | 中文路径转义出错，`localStorage` 抛 `SecurityError` | 起本地 http 服务 |
| 6 | 改下拉框只设 `value` | 页面监听不触发，截到的是旧状态 | 补 `dispatchEvent(new Event('change',{bubbles:true}))` |
| 7 | 没查坏图就交付 | 文档里混进白图 | 验收脚本查 `naturalWidth === 0` |
| 8 | 把推测写成需求 | 评审时被当成已确认内容 | 建议值显式标注来源；待确认项单独成章 |
| 9 | 忘了关后台进程 | Chrome 和 http server 一直挂着 | 收尾关掉 |
| 10 | 脚本结果只看终端 | 回显被吞，误判成功 | 一律落盘再 Read |

---

## 11. 交付前自检清单

- [ ] 所有截图来自原型真实运行状态，含至少一个交互态（抽屉／弹层／切换）
- [ ] 每个页面的功能点表覆盖了截图里看得见的每个区域
- [ ] 全局规则章节的事实来自 JS 源码，不是从界面猜的
- [ ] 自己补的建议值都有「建议值」「待确认」标注
- [ ] 未替换占位符 = 0，坏图 = 0
- [ ] 文档里没有 emoji、没有中文破折号
- [ ] 成品是单文件，拷到别的电脑能独立打开
- [ ] 后台的 http server 与 Chrome 已关闭

---

## 12. 脚本清单

| 脚本 | 作用 | 关键产出 |
|---|---|---|
| `cdp.mjs` | 零依赖 CDP 客户端，导出 `openSession()` 得到 `{go, evalJs, shot, send}` | 被下面四个引用 |
| `01_probe_views.mjs` | 探测各视图真实像素高度 | `probe.txt` |
| `02_capture.mjs` | 按步骤批量截图（支持交互态） | `shots/*.png`、`capture.log` |
| `03_build_prd.mjs` | base64 内嵌，产出单文件 HTML | 成品 HTML、`build.log` |
| `04_verify.mjs` | 验收：坏图检查 + 结构数字 | `verify.log`、抽查截图 |
| `prd_template_example.html` | 可直接改的 PRD 模板（8 个图片占位符） | 模板 |

---

*手册版本 v1.0 ｜ 2026-09-29 ｜ 基于「亚马逊运营工作课表」原型 PRD 的实际制作过程整理*
