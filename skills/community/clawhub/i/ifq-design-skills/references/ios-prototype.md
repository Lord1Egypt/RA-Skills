# App / iOS 原型专属守则

> **触发**：「app 原型」「iOS mockup」「移动应用」「做个 app」。下面四条覆盖 [`content-guidelines.md`](content-guidelines.md) 的通用 placeholder 原则——app 原型是 demo 现场，静态摆拍和米白占位卡没有说服力。

## 0. 架构选型（必先决定）

**默认单文件 inline React** — 所有 JSX / data / styles 直接写进主 HTML 的 `<script type="text/babel">`，**不要** `<script src="components.jsx">`。`file://` 协议下浏览器把外部 JS 当跨 origin 拦截，强制起 HTTP server 违反「双击就能开」直觉。引用本地图片必须 base64 内嵌 data URL。

**拆外部文件只在两种情况**：
- (a) 单文件 >1000 行难维护 → 拆 `components.jsx` + `data.js`，附启动命令（`python3 -m http.server`）
- (b) 多 subagent 并行写不同屏 → `index.html` + 每屏独立 HTML（`today.html` / `graph.html`...），iframe 聚合

| 场景 | 架构 | 交付方式 |
|---|---|---|
| 单人 4-6 屏（主流） | 单文件 inline | 一个 `.html` 双击开 |
| 单人 >10 屏 | 多 jsx + server | 附启动命令 |
| 多 agent 并行 | 多 HTML + iframe | `index.html` 聚合 |

## 1. 先找真图，不是 placeholder 摆着

默认主动取真实图片填充，不画 SVG、不拿米白卡摆着、不等用户要求。

| 场景 | 首选渠道 |
|---|---|
| 美术 / 博物馆 / 历史 | Wikimedia Commons、Met Museum Open Access、Art Institute of Chicago API |
| 通用生活 / 摄影 | Unsplash、Pexels |
| 用户本地素材 | `~/Downloads`、项目 `_archive/` |

Wikimedia 下载避坑（本机 curl 走代理 TLS 会炸，Python urllib 直接走得通）：

```python
UA = 'ProjectName/0.1 (https://github.com/you; you@example.com)'
api = 'https://commons.wikimedia.org/w/api.php'
# action=query&list=categorymembers + prop=imageinfo&iiurlwidth
```

**真图诚实性测试**（关键）：取图前先问——**「如果去掉这张图，信息是否有损？」**

| 场景 | 判断 | 动作 |
|---|---|---|
| Essay 列表封面、Profile 风景头图、设置页装饰 banner | 装饰，与内容无内在关联 | **不要加**。加了就是 AI slop |
| 博物馆 / 人物肖像、产品详情实物、地图卡片地点 | 内容本身，有内在关联 | **必须加** |
| 图谱 / 可视化背景的极淡纹理 | 氛围 | 加，但 opacity ≤ 0.08 |

**反例**：给文字 Essay 配 Unsplash「灵感图」、给笔记 App 配 stock photo 模特——都是 AI slop。

## 2. 交付形态：overview / flow demo —— 先问用户

| 形态 | 何时用 | 做法 |
|---|---|---|
| **Overview 平铺**（默认） | 看全貌 / 比布局 / 走查一致性 | 所有屏并排静态展示，每屏一台独立 iPhone，内容完整，不需可点击 |
| **Flow demo 单机** | 演示特定用户流程（onboarding、购买） | 单台 iPhone，内嵌 `AppPhone` 状态管理器，tab bar / 按钮全可点 |

**路由关键词**：
- 「平铺 / 展示所有页面 / overview / 看一眼 / 比较」→ overview
- 「演示流程 / 用户路径 / 走一遍 / clickable / 可交互 demo」→ flow demo
- 不确定就问。不要默认选 flow demo（更费工）

**Overview 骨架**：

```jsx
<div style={{display: 'flex', gap: 32, flexWrap: 'wrap', padding: 48, alignItems: 'flex-start'}}>
  {screens.map(s => (
    <div key={s.id}>
      <div style={{fontSize: 13, color: '#666', marginBottom: 8, fontStyle: 'italic'}}>{s.label}</div>
      <IosFrame><ScreenComponent data={s} /></IosFrame>
    </div>
  ))}
</div>
```

**Flow demo 骨架**：

```jsx
function AppPhone({ initial = 'today' }) {
  const [screen, setScreen] = React.useState(initial);
  const [modal, setModal] = React.useState(null);
  // 根据 screen 渲染不同 ScreenComponent，传入 onEnter/onClose/onTabChange/onOpen
}
```

Screen 组件接 callback props（`onEnter`、`onClose`、`onTabChange`、`onOpen`、`onAnnotation`）。TabBar、按钮、作品卡加 `cursor: pointer` + hover。

## 3. 交付前跑真实点击测试

静态截图只能看 layout，交互 bug 要点过才发现。Playwright 跑 3 项最小点击测试：进入详情 / 关键标注点 / tab 切换。检查 `pageerror` 为 0 再交付。

## 4. 品位锚点（fallback 首选）

| 维度 | 首选 | 避免 |
|---|---|---|
| 字体 | 衬线 display（Newsreader / Source Serif / EB Garamond）+ `-apple-system` body | 全场 SF Pro 或 Inter |
| 色彩 | 一个有温度底色 + **单个** accent 贯穿（rust 橙 / 墨绿 / 深红） | 多色聚类（除非数据真有 ≥3 个分类维度） |
| 信息密度·克制（默认） | 少一层容器、少一个 border、少一个**装饰**性 icon | 每条卡片配无意义 icon + tag + status dot |
| 信息密度·高密度（例外） | 产品核心卖点是「智能 / 数据 / 上下文感知」时（AI 工具、Dashboard、Tracker、Copilot、番茄钟、健康监测、记账），每屏 ≥ 3 处差异化信息 | 只放一个按钮一个时钟——AI 智能感没表达，跟普通 App 没区别 |
| 细节签名 | 留一处「值得截图」的质感：极淡油画底纹 / serif 斜体引语 / 全屏黑底录音波形 | 到处平均用力，处处平淡 |

**两条原则同时生效**：
1. 品味 = 一个细节做到 120%，其它 80%
2. 减法是 fallback，不是普适律——AI / 数据 / 上下文感知类，加法优先

## 5. iOS 设备框必须用 `assets/ios_frame.jsx`

**硬性绑定**。已对齐 iPhone 15 Pro 精确规格：bezel、Dynamic Island（124×36、top:12、居中）、status bar（避让岛、vertical center 对齐岛中线）、Home Indicator、content top padding 都处理好了。

**禁止在你的 HTML 里自己写**：
- `.dynamic-island` / 手写黑圆角矩形
- `.status-bar` 手写时间 / 信号 / 电池
- `.home-indicator` / 底部 home bar
- iPhone bezel 圆角外框 + 黑描边 + shadow

99% 会撞位置 bug——status bar 时间 / 电池被岛挤压、或 content top padding 算错导致内容盖在岛下。刘海**固定 124×36 像素**，留给 status bar 两侧的可用宽度很窄。

**用法（严格三步）**：

```jsx
// 1. 读取本 skill 的 assets/ios_frame.jsx
// 2. 把整个 iosFrameStyles 常量 + IosFrame 组件贴进你的 <script type="text/babel">
// 3. 你的屏组件包在 <IosFrame> 里，不碰 island/status bar/home indicator
<IosFrame time="9:41" battery={85}>
  <YourScreen />
</IosFrame>
```

**例外**：用户明确要「假装是 iPhone 14 非 Pro 刘海」「做 Android 不是 iOS」「自定义设备形态」时，读对应 `android_frame.jsx` 或修改 `ios_frame.jsx` 常量，**不要**在项目 HTML 里另起一套。
