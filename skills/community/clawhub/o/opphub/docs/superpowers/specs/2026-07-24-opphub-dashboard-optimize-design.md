# Dashboard 任务流首页优化设计

**Date**: 2026-07-24
**Status**: draft
**Author**: OpenClaw bot
**Scope**: `opphub-web/app/dashboard/page.tsx` (单文件,客户端组件)

---

## 0. 背景与问题

### 0.1 舟哥原话

> "优化一下工作台首页,规划一下看如何改动"
> 范围限定:`https://api.opphub.ruiplus.cn/dashboard` 单页

### 0.2 现实(对照 2026-07-24 fetch + 仓代码)

`app/dashboard/page.tsx` **不是空白**,已经有 5 个模块:

| 模块 | 当前状态 | 用到的 API |
|---|---|---|
| 账号引导卡 | ✅ 渲染 (onboarding 未完成时) | `GET /api/onboarding/status` |
| 4 个统计卡 (信任分/余额/今日撮合/待处理订单) | ⚠️ 渲染但**字段错配** (stats 返 `todayDemands` 不返 `todayMatches`,所以"今日撮合"和"待处理订单"**永远显 0**) | `GET /api/onboarding/status` + `GET /api/opc/stats` |
| 🕊 实时消息 | ✅ 列表 + ack | `GET /api/opc/messages/pending` |
| 🚀 快速入口 | ⚠️ 6 个 nav 链接,**跟顶部 nav 重复** | - |

舟哥 fetch 看到的 `⏳ 加载中...` 是 SSR 阶段 `useEffect` 不跑的骨架 (`mounted=false` 兜底),**不是空白**。客户端接管后内容是渲染的,但 4 个统计卡因字段错配看起来像空。

### 0.3 优化目标 (5 个问题点)

| # | 问题 | 优化方向 |
|---|---|---|
| 1 | 4 个统计卡字段错配 → 今日撮合/待处理订单永远 0 | 改成真实字段 (todayDemands/trustPoints),或换字段语义 |
| 2 | 缺"今日撮合"模块 — task-flow 核心 | 新增"今日撮合"卡片,用 `/api/opc/match/today` (已有) |
| 3 | 快速入口 6 链接与 nav 重复 | 砍掉或缩到 3 个 (任务流相关) |
| 4 | 视觉扁平 — 5 个模块堆叠无层级 | 任务流 (消息 + 撮合) 置顶,统计/入口下移或合并 |
| 5 | SSR 骨架体验差 (⏳ 占位太显眼) | 改 SSR 占位为更柔性的"加载中"提示 |

---

## 1. 范围

### 1.1 改什么

| 文件 | 动作 |
|---|---|
| `opphub-web/app/dashboard/page.tsx` | **改** — 重构模块顺序 + 修字段错配 + 加今日撮合 + 删冗余入口 |
| `opphub-web/app/dashboard/components/MessageCard.tsx` | **新** — 消息卡片 (从 page.tsx 抽出) |
| `opphub-web/app/dashboard/components/MatchCard.tsx` | **新** — 撮合卡片 (新模块) |
| `opphub-web/app/dashboard/components/EmptyState.tsx` | **新** — 空状态 (复用 3 处) |

### 1.2 不改什么 (舟哥红线)

- ❌ 顶部 `TopBar` / `nav` — 不动 IA
- ❌ `/messages` / `/match` / `/discover` 等其他页面
- ❌ 后端 API — 全用已有 (`/api/onboarding/status` + `/api/opc/stats` + `/api/opc/messages/pending` + `/api/opc/match/today`)
- ❌ 引导卡 / 余额 / 信任分 — 模块逻辑保留,只动展示
- ❌ SSR 骨架 (`mounted=false` 兜底) — 保留防 hydration mismatch,只优化视觉

---

## 2. 新布局 (desktop ≥ md)

```
┌─────────────────────────────────────────────────────────────┐
│ TopBar (现有不动)                                             │
├─────────────────────────────────────────────────────────────┤
│ max-w-[960px] mx-auto px-4 md:px-6 py-4 md:py-6             │
│                                                             │
│  下午好,[名字] · 今天有 N 条待办  (顶栏一句话总结)              │
│  ┌─────────────── 账号引导 (onboarding 未完成时) ──────────┐  │
│  │ 进度条 + 继续完善 →                                       │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌──────── 📨 新消息 N ──────┐ ┌── 🎯 今日撮合 M ──┐         │
│  │ [icon] 标题 / 摘要        │ │ 需求标题            │        │
│  │         [时间]    [处理→] │ │ ¥预算 / 城市         │        │
│  │ ...                      │ │ 行业标签  [→]       │        │
│  │ (空状态引导)               │ │ ...                 │        │
│  └──────────────────────────┘ │ (空状态引导)         │        │
│                              └─────────────────────┘         │
│                                                             │
│  ┌─────────── 信任分 / 今日撮合 ──────────┐ ┌── 快速入口 ──┐  │
│  │ 信任分: 88  ·  今日撮合: 3 单           │ │ 需求广场      │  │
│  │ (单一窄条 · 一行两个数)                  │ │ 智能撮合      │  │
│  │                                        │ │ 我的订单      │  │
│  └────────────────────────────────────────┘ └──────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### 2.1 移动端 (< md)

- 单列堆叠,模块顺序不变
- 双列卡片 (消息/撮合) 退化为单列,各自占满宽度
- 统计 + 入口退化为单列

---

## 3. 单条卡片规格

### 3.1 MessageCard (从 page.tsx 抽出)

- 32px 圆形 icon (🎯 opportunity / ⚙️ system / ⭐ 默认)
- 主标题 (14px, fontWeight 500, #1f2937)
- 摘要 (12px, #6b7280, truncate 1 行, line-clamp CSS)
- 时间 (11px, #9ca3af, 相对时间 "5 分钟前" — 不再用 toLocaleString 绝对时间)
- `[处理 →]` 按钮 (right-aligned, 12px, #4f46e5 → 跳 `/messages?focus=id`)
- 已 ack: opacity 0.5 + 划线 (保留现有逻辑)
- 卡片整体: `bg-gray-50 rounded-lg p-3 cursor-pointer hover:bg-gray-100 transition`

### 3.2 MatchCard (新增)

- 32px 圆形 icon (📋)
- 需求标题 (14px, fontWeight 500, truncate 1 行)
- 预算 (¥X,XXX 16px, #10b981 绿色, 高亮)
- 城市 + 截止日期 (12px, #6b7280, "上海 · 7 天内")
- 行业标签 (最多 2 个, 11px badge 风格)
- `[→]` 按钮 (right-aligned, 跳 `/match?focus=matchingId`)
- 卡片整体: 同 message 风格

### 3.3 EmptyState (抽出复用)

```
┌────────────────────────────────────────┐
│  ⓘ 暂无 X — [引导文案] [CTA 按钮 →]   │
└────────────────────────────────────────┘
```

- 居中, padding 24px, 字号 13px, 颜色 #9ca3af
- 3 处复用:消息空 / 撮合空 / (可选统计空)
- 文案:
  - 消息 0: "暂无新消息 — 完善画像让对方精准找到你 [去完善 →] `/knowledge`"
  - 撮合 0: "今日无匹配 — 去发现页看看热门需求 [去看看 →] `/discover`"
  - 统计空: 直接 "暂无数据" 不加 CTA

### 3.4 统计卡 (修复字段错配)

| 卡 | 当前显示 | stats API 实际 | 改后显示 |
|---|---|---|---|
| 信任分 | `stats.trustScore` (永远 null) | `trustPoints` (余额) | 改用 `trustPoints` 字段名 |
| 余额 | `stats.balance` (永远 null) | `trustPoints` 同字段 | **删**这个卡 (重复) |
| 今日撮合 | `stats.todayMatches` (永远 0) | `todayDemands` | **改**用 `todayDemands` |
| 待处理订单 | `stats.pendingOrders` (永远 0) | 无 | **删**这个卡 (API 缺,违反 A · 严格依赖) |

最终统计区:**信任分 (余额) + 今日撮合 (发的需求)** 2 个卡,合并显示在右下快速入口上方。

---

## 4. 数据获取

### 4.1 并行拉 4 个 API (现有 3 + 新增 1)

```ts
const [r1, r2, r3, r4] = await Promise.all([
  fetch("/api/onboarding/status"),     // 已有
  fetch("/api/opc/messages/pending?limit=10"),  // 已有
  fetch("/api/opc/stats"),             // 已有 (修字段)
  fetch("/api/opc/match/today"),       // 新增
]);
```

### 4.2 错误处理

- 任一 API 失败:对应卡片内联 `[重试]` 按钮,**不阻塞其他卡片**
- 401 (token 失效):统一跳 `/login` (保留现有行为)
- 网络错:console.warn + 卡片内联 "加载失败" 文字

### 4.3 防 hydration mismatch

- SSR 阶段只渲染骨架 (保留现有 `mounted=false` 兜底)
- 骨架视觉优化:从单卡 ⏳ 占位 → 4 个骨架卡 (消息/撮合/统计/入口 各 1 个) + "加载中..." 顶栏
- `useEffect` 触发后 `setMounted(true)` 才渲染真内容

---

## 5. 视觉规范

### 5.1 复用现有 token

- 颜色: `#4f46e5` (蓝) / `#06b6d4` (青) / `#10b981` (绿) / `#6b7280` (灰) / `#9ca3af` (浅灰)
- 卡片: `bg-white rounded-2xl shadow p-4 md:p-6`
- 字号: 标题 16px / 模块内文字 14px / 元数据 12px
- 字体: `-apple-system, BlinkMacSystemFont, "Helvetica Neue", "PingFang SC", sans-serif` (保留)

### 5.2 不引入新依赖

- 继续用 inline `style={}` (现有风格) — 不引入 CSS module / Tailwind 重写
- 移动端用 `<style jsx>` 块写 CSS media query (`@media (max-width: 767px) { ... }`) — **不要**用 `window.innerWidth` (SSR 时 undefined 会 hydration mismatch)

### 5.3 SSR 骨架优化

```tsx
if (!mounted || authed === null) {
  return (
    <main style={wrap}>
      <TopBar current="dashboard" rightSlot={<span style={...}>加载中...</span>} />
      <div className="max-w-[960px] mx-auto px-4 md:px-6 py-4">
        {/* 4 个骨架卡: 消息 / 撮合 / 统计 / 入口 */}
        <div style={skeletonCard}>...</div>
        <div style={{...grid, opacity: 0.5}}>{/* 4 个 stat 占位 */}</div>
      </div>
    </main>
  );
}
```

骨架视觉比单 ⏳ 更"产品在加载",降低"空白感"。

---

## 6. 文件改动清单

| 文件 | 行数变化 | 说明 |
|---|---|---|
| `app/dashboard/page.tsx` | 318 → ~280 | 重构,字段修复,抽组件 |
| `app/dashboard/components/MessageCard.tsx` | 新增 ~50 行 | 从 page.tsx 抽出 |
| `app/dashboard/components/MatchCard.tsx` | 新增 ~60 行 | 新增撮合卡 |
| `app/dashboard/components/EmptyState.tsx` | 新增 ~30 行 | 抽出空状态 |

**净增**: ~150 行 → ~220 行 (+70 行)

---

## 7. 测试

### 7.1 单元 (3 个组件)

- `MessageCard.test.tsx` — 渲染 3 种 type (opportunity/system/默认) / ack 状态 / 点击
- `MatchCard.test.tsx` — 渲染字段 / 截断 / 跳转链接
- `EmptyState.test.tsx` — CTA 文案 / 链接 / 显隐

### 7.2 集成 (page.tsx)

- 4 个 API mock → 断言 DOM 顺序 (引导 → 消息+撮合 → 统计+入口)
- 任一 API 失败 → 对应卡片内联 [重试]
- token 缺失 → 跳 /login

### 7.3 E2E (ECS)

- 手动 curl `/api/opc/match/today` 确认数据格式
- 本地 `pnpm build` 通过 + `pnpm start` 起服务 + 浏览器访问 dashboard
- 验收点:消息/撮合卡正常显示 / 空状态显引导 / 统计卡显真实字段 / 跳转链接对

---

## 8. 风险与回滚

| 风险 | 缓解 |
|---|---|
| 字段错配修复后,旧 dashboard 视觉变化大 | 截图对比 (改动前/后) 给舟哥看再 deploy |
| `use client` + `Promise.all` 在慢网下体验差 | 骨架卡 + 错位加载 (最快先显) |
| ECS 无 seed 数据 → 全空状态 | 空状态文案已经设计好,体验闭环 |
| 改动 page.tsx 影响 dashboard 其他用法 | dashboard 是 OPC 用户唯一入口,无其他引用方 |

**回滚**:`git revert <commit>` (单文件,单 commit)

---

## 9. 不做的事 (反复钉的纪律)

- ❌ 不动 nav / IA / 其他页面
- ❌ 不补后端 API
- ❌ 不引入新依赖 (CSS module / Tailwind 重写)
- ❌ 不做 IA 重构 (舟哥"为什么要动,现在不是挺好的么")
- ❌ 不动 SSR 兜底逻辑 (防 hydration mismatch,只优化视觉)
- ❌ 不加 mock 数据 (违反 7/24 教训"不显示层过滤数据")

---

## 10. 验收标准 (舟哥点头用)

- [ ] dashboard 加载后,消息 + 撮合 2 个卡片模块可见
- [ ] 4 个统计卡字段名修复,`todayDemands` / `trustPoints` 真实值
- [ ] 快速入口从 6 个砍到 3 个 (任务流相关)
- [ ] SSR 骨架从单 ⏳ 占位 → 4 个骨架卡
- [ ] 空状态 3 处引导文案 + CTA 按钮可见
- [ ] 任一 API 失败不阻塞其他卡片
- [ ] `pnpm build` 通过,无 hydration mismatch 警告
- [ ] 移动端 (< 768px) 单列堆叠正常

---

## 11. 关联文档

- 舟哥 USER.md — 产品定位严苛,不啰嗦
- MEMORY.md §1.2 — opphub-web 部署规范 (改 ECS 代码 4 步走)
- `memory/2026-07-21-opphub-web-flow-test.md` — API 实装状态盘点
- `memory/2026-07-24.md` — 7/24 教训"不显示层过滤数据"