# 自验证工作流操作手册 ⭐v3.0

> 火一五前端设计技能 v3.0 起，**Claude in Chrome MCP** 成为自验证首选路线。本手册按场景分流，给出每条路线的具体命令。

## 路线选择决策树

| 场景 | 首选 | Fallback 1 | Fallback 2 |
|---|---|---|---|
| Web / H5（5 个 Web 流派） | Claude in Chrome MCP | Playwright CLI | 用户手动 `open file://` |
| MOBILE-NATIVE Web 流派（iOS/MD3/Harmony） | Claude in Chrome MCP（resize 设备 viewport） | Playwright CLI（带 `--viewport-size`） | — |
| 微信小程序 | 微信开发者工具 IDE | 真机扫码 | — |
| 支付宝小程序 | 支付宝小程序 IDE | 真机扫码 | — |

---

## 1. Claude in Chrome MCP（优先 ⭐v3.0）

### 1.1 前置条件
- 用户已在 Chrome 装 Claude in Chrome 扩展并登录
- 当前会话挂载了 `mcp__Claude_in_Chrome__*` 工具集（如 schemas 未加载，用 `ToolSearch query="select:mcp__Claude_in_Chrome__list_connected_browsers,..."`）
- `mcp__Claude_in_Chrome__list_connected_browsers` 返回非空数组

### 1.2 标准命令序列（Web / H5）

```
# 1. 列出可用浏览器
mcp__Claude_in_Chrome__list_connected_browsers

# 2. 选定浏览器
mcp__Claude_in_Chrome__select_browser({ deviceId: "<from step 1>" })

# 3. 拿可用 tab
mcp__Claude_in_Chrome__tabs_context_mcp

# 4. 打开本地文件 / URL
mcp__Claude_in_Chrome__navigate({ url: "file:///abs/path/index.html", tabId: <id> })

# 5. 截图（关键产物）
mcp__Claude_in_Chrome__computer({
  action: "screenshot",
  tabId: <id>,
  save_to_disk: true
})

# 6. 读控制台错误（防 oklch 不支持 / 字体加载失败 / JS 报错）
mcp__Claude_in_Chrome__read_console_messages({ tabId: <id> })
```

### 1.3 移动端 viewport 控制

```
# iPhone 16 Pro
mcp__Claude_in_Chrome__resize_window({ tabId: <id>, width: 393, height: 852 })

# Pixel 8
mcp__Claude_in_Chrome__resize_window({ tabId: <id>, width: 412, height: 915 })

# HarmonyOS Mate 60
mcp__Claude_in_Chrome__resize_window({ tabId: <id>, width: 396, height: 858 })

# resize 后再 screenshot
mcp__Claude_in_Chrome__computer({ action: "screenshot", tabId: <id>, save_to_disk: true })
```

或者（更稳，无需 resize）：本 skill 的 `examples/mobile-native/*/index.html` 内置桌面预览手机壳（device frame），桌面 viewport 也能看到正确移动效果，桌面浏览器打开即可。

### 1.4 何时跳过本路线

- `list_connected_browsers` 返回 `[]` → 直接路线 2
- 用户明确说"我不开 Chrome" → 路线 2
- wxml / axml 场景 → 路线 3 / 4（MCP 不能渲染小程序模板）

### 1.5 a11y 自动审计 ⭐v4.4

渲染完成后注入 axe-core 跑 WCAG 2.2 AA 检查（与 [`a11y-checklist.md`](a11y-checklist.md) 30 条对照）：

```
mcp__Claude_in_Chrome__javascript_tool({
  tabId: <id>,
  code: `
    const s = document.createElement('script');
    s.src = 'https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.10.0/axe.min.js';
    document.head.appendChild(s);
    await new Promise(r => s.onload = r);
    return await axe.run({ runOnly: ['wcag2aa', 'wcag22aa'] });
  `
})
```

返回 `violations` / `passes` / `incomplete` 三个数组：
- 把 `violations` 对照 a11y-checklist 标 ⚠ 或修复
- `incomplete` 是 axe 无法自动判断的（如 #5 颜色非唯一信息载体），人审兜底
- `passes` 数 / 总检查数 ≥ 90% 视为可发布

**Lighthouse fallback**（MCP 不可用时）：

```bash
npx lighthouse <URL 或 file://> --only-categories=accessibility --output=html --output-path=./a11y-report.html --chrome-flags="--headless"
```

详见 [`a11y-checklist.md`](a11y-checklist.md) §自动检查路线。

---

## 2. Playwright CLI（fallback）

### 2.1 桌面端

```bash
npx playwright-core screenshot <URL 或 file:///abs/path> ~/verify.png --viewport-size=1440,900
```

### 2.2 移动端（MOBILE-NATIVE 流派必跑）

```bash
# iPhone 16 Pro
npx playwright-core screenshot <URL> ~/verify-iphone.png --viewport-size=393,852

# Pixel 8
npx playwright-core screenshot <URL> ~/verify-android.png --viewport-size=412,915

# HarmonyOS Mate 60
npx playwright-core screenshot <URL> ~/verify-harmony.png --viewport-size=396,858
```

### 2.3 注意

- 延续 enhance 插件"禁 child_process"铁律：**返回命令让用户执行**，不要 spawn
- `--full-page` 截整页（默认只 viewport）
- `--device="iPhone 16 Pro"` 也可用，但 Playwright 内置设备列表更新慢，自带 viewport 数值更稳

---

## 3. 微信开发者工具（小程序）

1. 安装 [微信开发者工具](https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html)（Stable v1.06+）
2. 项目 → 导入项目 → 选 `examples/mini-program/wechat/`
3. AppID 选"测试号"
4. 编译后左侧模拟器看渲染
5. 真机调试扫码 → 微信扫码 → 真机看效果
6. 截图：模拟器右上角"截屏"按钮 / 工具菜单 → 截图，默认存 `~/Desktop`

---

## 4. 支付宝小程序 IDE（小程序）

1. 安装 [支付宝小程序 IDE](https://opendocs.alipay.com/mini/ide/download)
2. 文件 → 打开项目 → 选 `examples/mini-program/alipay/`
3. 预览 → 扫码用支付宝 App 看真机
4. 截图：IDE 内置截图工具，或预览界面右上角"复制图片"

---

## 5. 评审接力

无论走哪条路线，截图最终：
- **由用户人眼审** → 1 句话反馈
- 或调用 `huo15-openclaw-design-critique` 5 维打分（结构 / 字体 / 颜色 / 空间 / 氛围）+ Keep/Fix/Quick Wins 输出

---

## 6. 移动端额外检查清单

- [ ] safe-area-inset 上下生效（刘海 / home indicator 没遮挡内容）
- [ ] tab-bar 触达高度 ≥ 44pt（iOS）/ 48dp（Android / 鸿蒙）
- [ ] 字号 / 行高在 375–430 多档 viewport 都不溢出
- [ ] 小程序：`<page-meta>` 在 wxml 中存在 + tabBar 是 native 不是自绘 + rpx 适配 750rpx 屏宽
- [ ] 控制台无 oklch 不支持警告（fallback 已生效）

---

## 7. 三路线兼容性矩阵

| 流派 / 场景 | Chrome MCP | Playwright CLI | 微信 IDE | 支付宝 IDE | 真机扫码 |
|---|---|---|---|---|---|
| BOLD-MINIMAL / EDITORIAL / BRUTALIST / RETRO-FUTURE / ORGANIC | ✓ | ✓ | — | — | ✓ |
| MOBILE-NATIVE iOS HIG | ✓（resize 393×852）| ✓ | — | — | ✓ |
| MOBILE-NATIVE MD3 | ✓（resize 412×915）| ✓ | — | — | ✓ |
| MOBILE-NATIVE Harmony | ✓（resize 396×858）| ✓ | — | — | ✓ |
| 微信小程序 | ✗ | ✗ | ✓ | — | ✓ |
| 支付宝小程序 | ✗ | ✗ | — | ✓ | ✓ |

---

## 8. 设计原则提醒

- **MCP 优先**不是教条 —— 没浏览器连接就别等，立刻 fallback
- **不要在 skill 内部 spawn 进程** — 所有 CLI 命令必须 return-cliCmd 模式给用户执行
- **截图是最终凭证** — 不要用"我看了源代码觉得 OK"代替真机 / 真渲染验证
- **控制台错误也要看** — `read_console_messages` 能抓到 oklch fallback、字体 404、JS 报错等隐患
