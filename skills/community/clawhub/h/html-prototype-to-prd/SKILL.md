---
name: html-prototype-to-prd
description: 把单文件 HTML 交互原型做成「截图 + 文字说明」的产品需求文档（PRD，单文件自包含 HTML，可直接发人）。当用户要把 HTML 原型 / 网页 demo / 交互原型转成 PRD、需求文档、产品文档，或提到「原型截图写文档」「原型转 PRD」「把 demo 做成 PRD」「给原型出需求文档」时使用。覆盖全流程：读原型 JS 挖业务规则 → CDP headless Chrome 真实交互态截图 → 视图测高 → 写 PRD 模板 → base64 内嵌成单文件 → 坏图/结构验收。
---

# 单文件 HTML 原型 → PRD 完整流水线

把一个已有的单文件 HTML 交互原型，做成一份「截图 + 文字说明」的产品需求文档，单文件自包含，可直接发人。

参照成品：「亚马逊运营工作课表_产品需求文档PRD_2026-09-28.html」（9 章、17 张表、8 张真实运行截图、1.78MB 单文件）。

## 什么时候用

- 用户有单文件 HTML 交互原型（demo），要出正式 PRD
- 要把网页/原型截图放进需求文档，且文档要能单独发人、拷到任何电脑能打开
- 需要文档里的截图是**真实交互态**（抽屉真的点开了、身份真的切了、搜索真的过滤了），不是手绘示意图
- 需要文档规则写的是**代码里的事实**（任务生成条件、校验规则、状态枚举），不是从界面猜的

## 产出标准

| 项 | 要求 |
|---|---|
| 图片 | 全部来自原型真实运行截图，以 base64 内嵌，不依赖外部目录 |
| 结构 | 封面 → 文档说明 → 信息架构 → 页面详情 → 全局规则 → 待确认事项 → 附数据规模 |
| 每个页面 | 固定四段：一句话描述 → 截图 → 功能点表 → 交互规则列表 |
| 导航 | 左侧 sticky 目录，点标题跳转；窄屏自动隐藏 |
| 觐觉 | 白底、宝蓝 #1457A6 主色、圆角卡片、浅灰表头；无 emoji、无中文破折号 |
| 体积 | 8 张图约 1.3MB，成品约 1.8MB，可接受 |

「效果一样」的关键不在排版，在两条：①截图是真实交互态；②规则写的是代码里的事实。

## 流程总览（七阶段）

```
阶段一 读懂原型（读 <script> 挖规则，不能跳）
阶段二 起环境（http server + headless Chrome 两个后台进程）
阶段三 探测视图高度（01_probe_views.mjs → probe.txt）
阶段四 批量截图（02_capture.mjs → shots/*.png）
阶段五 写 PRD 模板（占位符 __IMG_01__，模板在 assets/）
阶段六 base64 注入（03_build_prd.mjs → 单文件 HTML）
阶段七 验收（04_verify.mjs：坏图=0 + 结构数字对）
```

详细操作手册（每个阶段的完整说明、坑清单、自检清单）在 `references/manual.md`，做之前先读它。

## 快速开始

1. 建 staging 目录，复制原型为 `demo.html`、复制本 skill 的 `scripts/` 全部文件进去（**ASCII 路径**，规避中文转义问题）
2. 起两个后台进程：
   ```bash
   <Python> -m http.server 8766 --directory <staging> --bind 127.0.0.1
   <Chrome> --headless=new --remote-debugging-port=9222 --user-data-dir=<staging>/chrome-profile --window-size=1440,1000 --no-first-run --no-default-browser-check --hide-scrollbars --disable-gpu
   ```
   不要用 file://，localStorage 会抛 SecurityError。
3. 改 `01_probe_views.mjs` 配置区（URL、视图点击 JS），跑出 `probe.txt`，把 h 值填进 02 的 height
4. 改 `02_capture.mjs` 配置区（截图步骤、交互态 before JS），批量截图
5. 复制 `assets/prd_template_example.html` 改内容，图片位留 `__IMG_01__` 占位符
6. 改 `03_build_prd.mjs` 配置区（占位符→PNG 映射），产出单文件 HTML
7. 复制成品到 staging 为 `prd_view.html`，改 `04_verify.mjs` 期望值，跑验收：坏图=0、结构数字对
8. **结束后关掉两个后台进程**

## 三个不能跳的铁律

1. **写文档前先把原型的 `<script>` 段读完。** 任务生成条件、校验规则、状态枚举、数据唯一性、权限判定只存在于 JS 里，看界面永远看不出来——这些才是 PRD 最值钱的部分（全局规则章节的事实来源）。
2. **截图不要统一视口高度。** 先跑 01 测高。实测同一原型四个视图 1372/1549/1733/7221px，统一高度要么截断要么大片空白；超长页只截首屏。
3. **base64 注入必须用 `split().join()` 而不是 `replace()`。** base64 里会出现 `$&`、`$1` 序列，`replace` 会当替换模式，图直接烂掉。

## 交互态截图要点

- 下拉框切换要用 `dispatchEvent(new Event('change',{bubbles:true}))`，直接改 `value` 不触发监听
- 卡片点击一律模拟真实 click，不要调页面内部函数（拿不到闭包里的 state）
- `wait` 给足（抽屉动画、重绘要时间），500ms 起步
- 每步打印 `mainLen`，明显偏小 = 选择器没命中截到空白

## 环境要求

- Node 22+（需要自带的全局 `WebSocket`，cdp.mjs 零依赖）
- Python 3（起本地 http server 用）
- Chrome（headless + CDP）
- **不要装 playwright / puppeteer**，Chrome 自带 headless + CDP 够用
- 路径中有中文/空格的，先把文件复制到 ASCII 路径的 staging 目录再操作
- bash coreutils 可能残缺（ls/head/grep 报 command not found），编排一律写 .mjs 用 Node 跑；脚本输出必须落盘再读，终端回显经常被吞

## PRD 内容纪律

- 事实与建议分开标注：凡自己补的、原型里没有的，显式写「建议值，最终以 XX 为准」
- 不写排期（评审时会被当承诺）
- 待确认事项要真的写：列信息缺口和影响，这是评审会上最有用的部分
- 配色：白底 + 宝蓝 #1457A6 + 暖白 #F5F3ED + 点缀 #C56A31；状态色（已完成绿、延期橙）是语义色，不被主色替换
- 禁用：emoji、中文破折号 ——

## 文件清单

| 文件 | 作用 |
|---|---|
| scripts/cdp.mjs | 零依赖 CDP 客户端，导出 openSession() 得 {go, evalJs, shot, send} |
| scripts/01_probe_views.mjs | 探测各视图真实像素高度 → probe.txt |
| scripts/02_capture.mjs | 按步骤批量截图（支持交互态）→ shots/*.png |
| scripts/03_build_prd.mjs | base64 内嵌 → 单文件 HTML |
| scripts/04_verify.mjs | 验收：坏图检查 + 结构数字 → verify.log |
| assets/prd_template_example.html | 可直接改的 PRD 模板（8 个图片占位符） |
| references/manual.md | 完整操作手册（七阶段详解 + 坑清单 + 自检清单） |
