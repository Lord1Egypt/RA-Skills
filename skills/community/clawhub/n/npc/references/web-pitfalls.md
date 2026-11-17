# 前端陷阱备忘（血泪账）

> 本 skill 的单文件点选页曾因一个函数名整页全黑。这里是踩过的和躲过的。

## P0：全局标识符撞 window 不可配置属性

**现象**：页面全黑，`#app` 为空，控制台报
`SyntaxError: Identifier 'top' has already been declared`。

**原因**：渲染函数起名 `function top(right){...}`。`top` 是浏览器 `window` 的
不可配置（[LegacyUnforgeable]）内置属性，全局作用域的函数声明与它冲突时，
**解析期**直接抛 SyntaxError——整个 `<script>` 一行都不执行，不是运行到一半挂。
所以 `#app` 永远是空的，body 只剩深色背景，看起来像「页面坏了/没加载」。

**高危名单**（与 window 属性同名，全局声明前先查一遍）：
`top` `parent` `self` `window` `document` `name` `location` `origin` `closed`
`length` `status` `frames` `frameElement` `opener` `screen` `history`
`navigator` `crypto` `localStorage` `sessionStorage` `external`

`function` 声明和 `var` 最危险；`const`/`let` 遮蔽属性一般不报错，但别依赖这个行为。

**修法**：改名（本例 `top` → `topBar`）。本 skill 的构建脚本里有
「全局函数清单 vs 高危名单」的自动扫描，新增函数时看一眼构建输出。

## P0：mock DOM 会给假绿灯

Node 里模拟 `document`/`window` 测渲染代码，**测不出浏览器才有的约束**：
window 属性冲突、CSS 解析、`prefers-color-scheme`、`localStorage` 可用性、
事件循环差异。这次的 `function top` bug，mock 里跑一万次都是绿的。

**结论**：mock 只配测纯计算逻辑（引擎对拍就是这么用的）；「页面能不能显示」
必须真机说了算。本 skill 的门禁链是：

1. `--verify` 引擎对拍（Node，纯计算）
2. `--smoke` 真机冒烟（真实 Chromium：零 pageerror + #app 非空 + 双主题背景
   亮度断言 + 完整出卡 + 主题切换）

生成命令**默认自动跑冒烟**，环境缺 playwright/浏览器时显式打 `[SKIP]`。

## P1：深色设计撞上浅色环境

终端风深色（#0b0f14）是调性的一部分，但两张现实约束：

- 预览宿主（IDE/浏览器）是浅色主题时，大面积深色第一眼像「加载失败」；
- 卡片的传播方式是**截图发聊天**，深色截图贴在白色聊天背景里非常突兀。

**解法**：双主题。浅色纸感为默认（`prefers-color-scheme` 跟随系统 + 手动切换按钮），
深色保留为可选。所有颜色进 CSS 变量、变量值在 Python 侧定义为单一来源，
改色不出现两处漂移。**JS 内联样式一律走 `var(--x)`，禁止写死色值**——
否则切主题时内联部分会留下一块错色。

## P1：只改阈值不重新生成

页面里的锚点/stats 是构建时写死的。改 `meta.json` 后必须重新
`--out` 生成，否则页面与命令行给出不同结果（工程上这是「双源」坏味道，
当前用「改完必跑生成」的纪律兜住）。

## 排查「页面黑/白屏」的固定动作

1. 打开控制台看第一条错误——解析期 SyntaxError 会让整个 script 失效；
2. `document.getElementById('app').innerHTML.length` 是否 > 0；
3. 全局函数名与 window 不可配置属性对照（P0 名单）；
4. 真机跑 `--smoke`，别信 mock。
