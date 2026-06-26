---
name: huo15-openclaw-desktop-control
displayName: 火一五桌控（macOS 自动化心法）
description: >-
  把 desktop-control MCP（火一五桌控，36 个 tool）用对的心法。
  AX 树优先而非像素点击；act tool 必带 expect_after；session 状态摘要 [state ...] 要读。
  触发：用户说"火一五桌控/桌控/帮我点/帮我截屏/控制电脑/自动化 macOS/打开 X 然后做 Y/在 X 应用里…"。
version: 1.0.0
user-invocable: true
homepage: https://cnb.cool/huo15/ai/huo15-skills
aliases:
  - 火一五桌控
  - 桌控
  - 控制电脑
  - 自动化 macOS
  - 自动化电脑
  - 帮我点
  - 帮我截屏
  - 帮我截图
  - 看下屏幕
  - desktop-control
  - desktop-use-mcp
metadata:
  openclaw:
    emoji: 🖥️
    requires:
      bins: []
      mcpServers:
        - desktop-control
---

# 火一五桌控 · macOS 自动化心法

> **绑定的 MCP server**：`desktop-control`（npm slug `desktop-use-mcp`，36 个 tool）。
> **激活时机**：用户说"控制电脑 / 操作 macOS / 帮我点 X / 截屏看 Y / 在 Safari 里做 Z" 等任何要 LLM 替他动鼠标键盘 / 看屏幕 / 控制 app 的请求。

## TL;DR — 三大心法（违反一条就大概率出幻觉）

1. **AX 优先于像素**：要点击 / 输入哪个元素，**先 `dump_ax_tree` 或 `find_element`，再用返回的 `eid` 调 `click_element_by_id`**。截图肉眼定坐标只在 AX 不可用时才用。
2. **act tool 必带 `expect_after`**：`click` / `click_element_by_id` / `type` / `key` / `launch_url` / `open_app` / `focus_window` / `drag` 都接 `expect_after`，操作后自动等元素出现 / 消失 / app 前置 / 等指定毫秒。**没验证 = 没发生**。
3. **每条返回末尾的 `[state ...]` 必看**：里面写明 `screenshot=Xs ago focus=… last=…@Ys actions=A/T`。截图过期超 60s 还在沿用旧坐标 = 幻觉源头。

---

## 工具速记（36 个分 8 类）

| 类别 | 关键工具 |
|---|---|
| 屏幕 | `screenshot` · `screenshot_region` · `display_info` · `list_displays` |
| 鼠标 | `click`(L/R/M/back/forward × 1-3次) · `mouse_move` · `mouse_down`/`up` · `drag`(单段或多点 path) · `scroll`(2D) · `get_cursor_position` |
| 键盘 | `type`(剪贴板粘贴) · `key`(组合键) · `hold_key`(按住 N 毫秒) |
| 剪贴板 | `clipboard_read` · `clipboard_write` |
| 系统 | `wait` · `launch_url` · `run_command`(shell) |
| 应用 / 窗口 | `list_apps` · `list_windows` · `focus_window` · `open_app` · `quit_app` · `hide_app` · `move_window` · `resize_window` |
| **辅助功能 (AX)** | `dump_ax_tree` · `find_element` · `wait_for_element` · `click_element` · **`click_element_by_id`** · `inspect_element` |
| **harness 元工具** | `get_state` · `reset_session` · `verify_state` |

---

## 标准 Pattern 库（直接套用）

### Pattern 1 — 在某 app 里点指定按钮

```
1. open_app  app_name="Safari"  expect_after={kind:"app_frontmost", app_name:"Safari"}
2. find_element  app_spec="Safari"  selector={role:"AXButton", titleContains:"登录"}
   → 拿到 eid_xxxxxx
3. click_element_by_id  eid="eid_xxxxxx"
   expect_after={kind:"element_appears", app_spec:"Safari",
                 selector:{titleContains:"欢迎"}, timeout_ms:8000}
```

### Pattern 2 — 填表 + 提交

```
1. click_element  app_spec="Safari"  selector={role:"AXTextField", titleContains:"邮箱"}
2. type  text="user@example.com"
3. key  key_sequence="tab"
4. type  text="my-password"
5. click_element  app_spec="Safari"  selector={role:"AXButton", title:"登录"}
   expect_after={kind:"element_disappears", app_spec:"Safari",
                 selector:{role:"AXTextField", titleContains:"邮箱"}, timeout_ms:10000}
```

### Pattern 3 — 等弹窗 / 等加载完

```
wait_for_element  app_spec="..."  selector={titleContains:"加载完成"}  timeout_ms=15000
# 或者
verify_state  expectation={kind:"element_appears", app_spec:"...", selector:{...}}
```

### Pattern 4 — 跨调用引用同一元素（防坐标飘移）

```
1. find_element  app_spec="Slack"  selector={role:"AXTextArea", titleContains:"消息"}
   → eid_abc123
2. （任意操作 / wait 几秒 / 滚动列表）
3. click_element_by_id  eid="eid_abc123"
   ↑ 桌控自动从最新 AX 树里重新解析此 eid，窗口移了 / 列表滚了都不影响。
```

### Pattern 5 — 像素截图兜底（仅 AX 不可用时）

```
1. screenshot  → 看清楚目标位置 (x_img, y_img)
2. click  x=x_img  y=y_img  expect_after={kind:"wait", ms:500}
   ↑ 如果坐标超界或截图 > 60s，桌控会直接拒绝并告诉你"先重新截图"
```

---

## 反模式（这样写一定崩）

| ❌ 反模式 | ✅ 改法 |
|---|---|
| 截图后想 30 秒再点已记下的坐标 | 重新截图（≤ 60s 鲜度），或一开始就用 `find_element` + `eid` |
| `click` 完接着 `type`，没验证按钮按下生效 | act tool 全部加 `expect_after` |
| 看到 `[state]` 里 `screenshot=120s ago` 还在用旧坐标 | 先调 `screenshot` 重置截图新鲜度 |
| 用 `screenshot` + 像素识别去找按钮位置 | 优先 `find_element` 按 role/title 直接拿到中心坐标 |
| `run_command` 跑 `rm -rf` / `curl \| sh` | 桌控 guardrail 直接拒；让用户自己跑 |
| 多步操作之间不调 `get_state` 检查健康 | 每 5-10 步调一次 `get_state` 确认会话状态 |

---

## 选 AX 还是截图：决策树

```
用户给的目标元素有名字 / 角色清晰（按钮、链接、输入框）？
  ├─ Yes → 用 AX：dump_ax_tree → find_element → click_element_by_id
  │
  └─ No（图标无标题 / 视觉化拖拽 / Canvas 内容 / 游戏画面）
       → 用截图：screenshot → 肉眼定位 → click(x,y)
```

OpenClaw / macOS 原生应用、第三方 macOS 应用绝大多数 AX 完整。**Web 内容**（Safari 里的网页）AX 完整度看网站；输入框 / 链接 / 按钮基本都有 AX 角色，可放心用 AX。

---

## 失败 → 自愈 SOP

桌控操作失败时按这个顺序：

1. 看 tool 返回的 `[guardrail XXX]` 错误码
   - `NO_SCREENSHOT` / `COORDS_OUT_OF_BOUNDS` → 先 `screenshot`
   - `DANGEROUS_COMMAND` → 命令本身有问题，重写或让用户跑
   - `TEXT_TOO_LONG` → 用 `clipboard_write` + `key cmd+v`
   - `UNKNOWN_EID` → eid 缓存被清；重新 `find_element`
   - `ELEMENT_GONE` → 元素已消失；重新 `find_element` 或 `screenshot` 看现状
2. 看 `expect_after` 的 `[verify ... FAILED]` 详情：通常是上一步操作没真正生效
3. 调 `get_state` 看会话健康
4. 必要时 `reset_session` 清状态后重来

---

## 系统权限提醒

第一次用必须 macOS System Settings → Privacy & Security 给 OpenClaw（或 spawn MCP 的 shell）：

- **Accessibility**（必须）— 否则所有 click / AX 全失败但不报错
- **Screen Recording**（必须）— 否则 `screenshot` 黑屏
- **Automation**（首次会弹窗）— `open_app` / `focus_window` 等

如果 LLM 调 `dump_ax_tree` 返回的全是 `AXUnknown` 节点 → 几乎一定是 Accessibility 没授权。

---

## 复杂任务模板（"在 X 里完成 Y"）

```
1. list_apps  → 确认 X 在不在跑
2. open_app  app_name="X"  expect_after={kind:"app_frontmost", app_name:"X"}
3. dump_ax_tree  app_spec="X"  depth=8  → 看一眼 UI 结构，记下关键 eid
4. 按 Pattern 1/2/3 逐步操作
5. 每 5 步调 get_state 确认健康
6. 失败按"失败 → 自愈 SOP"
7. 任务完成后 verify_state 做最终确认
8. （可选）reset_session 清状态后切下一任务
```
