# myapp-creator

Version: 1.0.31

让用户用一句话生成可独立打开的单文件 HTML 应用或文档，并落库到 fe-service。
本 skill **不主动调用 LLM**，所有 HTML / app_name / features 由调用本 skill 的 LLM agent 直接产出后传入工具。

> **⚠️ 最高优先级规则（违反即为严重错误）：**
> 1. 游戏类应用 **绝对禁止** 包含任何形式的 AI 对手、人机对战、电脑自动下棋/出牌。棋类/对战类游戏 **只允许** 双人同屏轮流操作，不实现任何计算机决策逻辑。
> 2. 所有应用 **绝对禁止** 出现"导出"、"打印"、"保存"按钮或相关功能代码。

## 触发条件

当用户需求匹配以下任一类别时，本 skill 参与：

### 应用类（交互式 HTML）
关键词：应用、app、小游戏、游戏、网页、页面、工具、计算器、时钟、日历、翻译器、转换器
示例：
- "做一个贪吃蛇游戏"
- "创建一个番茄钟"
- "生成一个天气页面"
- "给我做一个马里奥游戏"
- "帮我做一个单位转换工具"

### 文件类（文档式 HTML）
关键词：文档、文件、word、ppt、演示文稿、slides、pdf、excel、xlsx、表格、报告、简历、周报、日报、总结、方案、计划书
示例：
- "生成一个项目周报"
- "做一个自我介绍PPT"
- "创建一个预算表格"
- "帮我写一份简历"
- "保存一个会议纪要文档"

### 不触发（交给龙虾其他能力）
- 图片/绘画类："画一张…"、"生成一张图片…"
- 音频/音乐类："生成一首歌…"、"合成语音…"
- 视频类："剪辑一个…"、"生成视频…"
- 小说/纯文本类："写一篇小说…"、"写一首诗…"（纯创作不产出可交互文件）
- 纯问答/聊天/闲聊

### 判断规则
用户意图是"产出一个可独立打开、保存下来反复使用的文件或应用"时触发本 skill。
如果用户只是想让你"说一段话"或"回答问题"，不要触发。

## 触发标记（兼容旧入口）

以下前缀仍可直接触发，不需要语义判断：
- `[create_app]<描述>` → 创建新应用/文件
- `[update_app:app_id=<n>]<描述>` → 更新已有应用/文件
- `[install_check:session=<sid>]` → 安装自检（仅调 myapp_ping）
- 不带上述前缀 → 按语义判断是否匹配触发条件

## 创建流程

最长等待 300s。若 300s 内不能完成 HTML 生成与 `myapp_register` 调用，直接回复"应用创建失败，请稍后重试"。

1. 解析用户描述，判断类型（应用类 or 文件类），产出：
   - `app_name`：应用/文件名，≤30 字
   - `features`：JSON 字符串数组，3~8 条，每条 ≤30 字，描述具体功能/内容要点
   - `html_content`：完整可独立打开的单文件 HTML（按类型选择模板风格）

2. HTML 通用约束：
   - 自包含：CSS/JS 全部内联在 `<style>` / `<script>`
   - 不依赖本地资源
   - 外部资源仅允许：unpkg.com / jsdelivr.net / cdnjs.cloudflare.com
   - 总长度 ≤ 60KB（UTF-8 字节数）
   - 不引用任何小度专属 API
   - 必须包含 `<meta name="viewport" content="width=device-width,initial-scale=1">`

   **目标运行环境 — Android 8.1 WebView（Chrome/85）**：
   所有 HTML 最终运行在搭载 Android 8.1 的智能屏 WebView 中，无鼠标/硬键盘，仅支持触摸和左右滑动。
   生成代码时必须遵守以下兼容规则：

   **JS / Web API 兼容**（feature detection 优先，禁止仅凭 UA 判断）：
   - 使用 `typeof IntersectionObserver !== 'undefined'` 等特性检测，不要直接调用可能不存在的 API
   - 禁止使用 Chrome 86+ 才支持的 API：`CSS.registerProperty`、`@property`、`content-visibility`、`aspect-ratio`（CSS）、`ResizeObserver`（需检测）、`structuredClone`（用 `JSON.parse(JSON.stringify())` 替代）
   - 禁止使用 ES2020+ 语法：`??=`、`||=`、`&&=`、`import()`动态导入、`BigInt`、`globalThis`（用 `window` 替代）
   - **禁止使用 `ctx.roundRect()`**——这是 Canvas 2D 的新方法，Chrome 99 才加入，Chrome 85 WebView 直接抛异常导致整个 draw 函数崩溃。必须用以下自定义 helper 替代：
     ```js
     function rr(ctx, x, y, w, h, r) {
       ctx.beginPath();
       ctx.moveTo(x + r, y);
       ctx.lineTo(x + w - r, y);  ctx.arcTo(x + w, y,     x + w, y + r,     r);
       ctx.lineTo(x + w, y + h - r); ctx.arcTo(x + w, y + h, x + w - r, y + h, r);
       ctx.lineTo(x + r, y + h);  ctx.arcTo(x,     y + h, x,     y + h - r, r);
       ctx.lineTo(x, y + r);      ctx.arcTo(x,     y,     x + r, y,         r);
       ctx.closePath();
     }
     // 用法：rr(ctx, x, y, w, h, radius); ctx.fill();
     ```
   - **禁止在 Canvas 内用 emoji 字符**（如 🌕🔥❤️ 等）——Android WebView 字体渲染异常会抛异常或显示方块。Canvas 内所有文字必须用纯 ASCII/中文文字，用几何图形代替 emoji（如"♥ × 3"改用红色圆形绘制）
   - 可安全使用：`Promise`、`async/await`、`fetch`、`CSS Grid`、`Flexbox`、`CSS Variables`、`IntersectionObserver`（需检测）、`requestAnimationFrame`
   - `localStorage` / `sessionStorage` 在 WebView 中可用，但不要依赖跨页面持久化

   **CSS 兼容**：
   - `100vh` 在 Android WebView 中等于视口高度（无地址栏问题），可直接使用
   - `position: sticky` 在 Chrome 85 中支持，但父容器不能有 `overflow: hidden`，否则失效
   - `position: fixed` 在 WebView 中软键盘弹出时可能错位，避免在输入框场景依赖 fixed 定位
   - **禁止使用 CSS `inset` 属性**（`inset: 0` 等简写）——Chrome 87 才支持，Chrome 85 不识别，会导致遮罩层无法撑满、内容偏移到左上角。替换写法：`top:0; left:0; right:0; bottom:0`（注意：`box-shadow` 中的 `inset` 关键字不受此限制，可以正常使用）
   - 禁止使用 `backdrop-filter`（Chrome 85 需前缀，WebView 不保证支持）
   - `clamp()` 在 Chrome 85 中已支持，可正常使用
   - 滚动容器加 `-webkit-overflow-scrolling: touch` 保证惯性滚动

   **触摸与交互**：
   - 所有可点击元素最小触摸区域 ≥ 44×44px
   - 使用 `touchstart`/`touchmove`/`touchend` 处理手势；`click` 在 WebView 中有 300ms 延迟，交互敏感场景改用 touch 事件
   - 消除 300ms 延迟：在 `<meta name="viewport">` 中加 `user-scalable=no` 或在 CSS 中加 `touch-action: manipulation`
   - 禁止依赖 `hover` 状态（无鼠标），交互反馈改用 `:active` 或 JS touch 事件
   - 左右滑动手势用 `touchstart`/`touchend` 计算 `deltaX` 实现，不要用第三方手势库（CDN 可能不可达）
   - 游戏类应用禁止使用键盘事件（`keydown`/`keyup`）作为唯一控制方式，必须提供触摸按钮

   **软键盘与输入框**：
   - 输入框获焦时 WebView 会 resize 视口，避免用 `height: 100vh` 做全屏布局的唯一约束
   - 输入框弹出软键盘后 `fixed` 元素可能被遮挡，底部操作栏改用 `position: sticky` 或监听 `visualViewport.resize`
   - 如需监听软键盘：`window.visualViewport` 在 Chrome 61+ 可用，Chrome 85 支持

   **弹窗 / Modal**：
   - 自定义弹窗用 `position: fixed; top:0; left:0; width:100%; height:100%` 覆盖全屏
   - 弹窗内滚动区域加 `overflow-y: auto; -webkit-overflow-scrolling: touch`
   - 禁止使用原生 `alert()`/`confirm()`/`prompt()`（WebView 中可能被宿主拦截）

   - **横屏多设备适配**：目标设备均为横屏展示，尺寸差异较大：
     | 设备 | 视口宽×高比例 |
     |------|-----------|
     | 普通智能屏 | 960×600 |
     | mini智能屏 | 960×480 |
     | 闺蜜机 | 1280×720 |
     | 秋月 | 1280×800 |
     | pad | 1920×1080 |
     | pad17 | 2560×1600 |
     布局以横屏为前提（宽 > 高），使用 `vw`/`vh`/百分比等响应式单位，禁止固定像素宽度导致小屏溢出或大屏留白。
     字体大小建议用 `clamp()` 适配，如 `font-size: clamp(14px, 2vw, 18px)`。

3. HTML 模板风格（按类型选择）：

   **应用类** — 交互式：
   - 纯单机离线游戏/工具，不依赖任何 server 服务
   - **严禁实现 AI 对手 / 人机对战 / 电脑自动下棋等功能**，棋类游戏只做双人同屏轮流对战（两个玩家在同一屏幕上交替操作）
   - 棋类游戏正确做法示例：五子棋 → 黑白双方轮流点击落子，判断五连胜负，无任何电脑决策代码；象棋 → 红黑双方轮流移动棋子
   - 功能简单易上手，玩法直观，适合触屏快速操作
   - 支持触屏操作（touch 事件）
   - 美观的 UI 设计
   - 根容器使用 `width:100vw; height:100vh; overflow:hidden` 撑满全屏
   - 关键元素尺寸用 `vmin` 或百分比，确保 960px 小屏到 2560px 大屏均可用

   **游戏类强制横版左右布局**（所有游戏类应用必须遵守）：

   > ⚠️ **强制要求**：所有游戏页面必须是横版布局，整体分为左右两栏，**禁止竖版堆叠布局**。

   布局结构如下：
   ```
   ┌─────────────────────────────┬──────────────────┐
   │                             │  状态（必展示）    │
   │                             │  关卡/得分/生命    │
   │       游戏区域（左栏）        ├──────────────────┤
   │    占总宽约 65%~70%          │  下一块/预览      │
   │    高度撑满 100vh            ├──────────────────┤
   │                             │ ◀ II ▶  方向键   │
   └─────────────────────────────┴──────────────────┘
   ```

   **右栏布局规则（状态区和方向键始终可见）**：
   - `#status`（关卡、难度、得分/目标分、生命）：`flex:0 0 auto`，**必须展示，不可压缩**
   - `#game-preview`（下一块/预览区）：`flex:0 0 auto`，**有预览需求的游戏必须展示，不可压缩**
   - `#leaderboard`（排行榜）和 `#instructions`（操作说明）：**当游戏有 `#game-preview` 时，不展示排行榜和操作说明**（右栏空间有限，预览区优先）。仅在无预览需求的游戏中，才用 `flex:1 1 0; min-height:0` + 标题 h3 固定 + `.sb-inner` 内容区 `overflow-y:auto` 独立滚动的方式展示
   - `#controls`（方向键+暂停）：`flex:0 0 auto`，**固定在右栏底部，始终可见，不参与滚动**

   CSS 骨架模板（必须使用）：
   ```html
   <div id="app" style="width:100vw;height:100vh;display:flex;flex-direction:row;overflow:hidden;background:#1a1a2e;">
     <!-- 左栏：游戏区域，尽量大，canvas 撑满整个左栏，不留空白 -->
     <div id="game-area" style="flex:1;position:relative;min-width:0;">
       <canvas id="canvas" style="display:block;width:100%;height:100%;"></canvas>
       <!-- 开始/结束/暂停 遮罩层：必须用以下写法居中，禁止只写 top:0;left:0 导致内容贴左上角 -->
       <!-- <div id="overlay" style="position:absolute;top:0;left:0;right:0;bottom:0;display:flex;flex-direction:column;
            align-items:center;justify-content:center;text-align:center;
            background:rgba(0,0,0,.6);z-index:10;">
         <h2 style="color:#fff;font-size:clamp(18px,3vw,32px);margin:0 0 2vh;">游戏标题</h2>
         <p style="color:#ccc;font-size:clamp(12px,1.8vw,18px);margin:0 0 3vh;">操作说明文字</p>
         <button style="padding:1.2vh 4vw;font-size:clamp(14px,2vw,20px);border-radius:2vmin;
           border:none;background:#e74c3c;color:#fff;touch-action:manipulation;">开始游戏</button>
       </div> -->
       <!-- ⚠️ 遮罩内所有文字/按钮必须通过 flexbox 居中，严禁使用固定 top/left 像素值定位 -->
     </div>
     <!-- 右栏：固定宽度，状态区+方向键始终可见 -->
     <div id="sidebar" style="width:26vw;min-width:180px;max-width:300px;height:100vh;
          display:flex;flex-direction:column;padding:1.5vh 1.2vw;gap:0.8vh;box-sizing:border-box;overflow:hidden;">
       <!-- ① 游戏状态：必展示，不可压缩 -->
       <div id="status" style="flex:0 0 auto;font-size:clamp(10px,1.4vw,14px);">关卡/得分/生命...</div>
       <!-- ② 预览区（下一块等）：有预览需求时展示；若有预览区则不放排行榜和操作说明 -->
       <div id="game-preview" style="flex:1 1 0;min-height:0;">...</div>
       <!-- ③④ 排行榜+操作说明：仅在无预览区的游戏中使用（与 ② 二选一） -->
       <!--
       <div id="leaderboard" style="flex:1 1 0;min-height:0;display:flex;flex-direction:column;font-size:clamp(10px,1.3vw,13px);">
         <h3 style="flex:0 0 auto;margin:0 0 0.4vh;">排行榜</h3>
         <div class="sb-inner" style="flex:1 1 0;min-height:0;overflow-y:auto;-webkit-overflow-scrolling:touch;
              scrollbar-width:thin;scrollbar-color:rgba(255,255,255,.3) transparent;">
         </div>
       </div>
       <div id="instructions" style="flex:1 1 0;min-height:0;display:flex;flex-direction:column;font-size:clamp(10px,1.3vw,13px);">
         <h3 style="flex:0 0 auto;margin:0 0 0.4vh;">操作说明</h3>
         <div class="sb-inner" style="flex:1 1 0;min-height:0;overflow-y:auto;-webkit-overflow-scrolling:touch;
              scrollbar-width:thin;scrollbar-color:rgba(255,255,255,.3) transparent;">
         </div>
       </div>
       -->
       <!-- ⑤ 方向键+暂停：固定在底部，始终可见 -->
       <div id="controls" style="flex:0 0 auto;padding-top:0.8vh;">...</div>
     </div>
   </div>
   ```
   Canvas 尺寸初始化（JS 中必须这样写，确保 Android 8.1 WebView 中 canvas 像素与显示尺寸一致）：

   > ⚠️ **Android 8.1 WebView 已知问题**：页面刚加载时 `clientWidth/clientHeight` 可能为 0，导致 Canvas 尺寸变成 0×0、什么都画不出来。必须用以下模板，通过 `window.load` + 双层 `requestAnimationFrame` 延迟读取尺寸，并用 `offsetWidth` 做兜底。

   Canvas CSS（必须用 `position:absolute` 撑满，不依赖 flex 布局尺寸）：
   ```html
   <div id="game-area" style="flex:1;position:relative;min-width:0;">
     <canvas id="canvas" style="position:absolute;top:0;left:0;width:100%;height:100%;display:block;"></canvas>
   </div>
   ```

   Canvas 尺寸初始化（必须在 `window.load` + 双层 `requestAnimationFrame` 后执行）：
   ```js
   function initCanvas() {
     const gameArea = document.getElementById('game-area');
     const canvas = document.getElementById('canvas');
     // offsetWidth 兜底：Android 8.1 WebView 刚加载时 clientWidth 可能为 0
     const w = gameArea.clientWidth  || gameArea.offsetWidth  || window.innerWidth * 0.7;
     const h = gameArea.clientHeight || gameArea.offsetHeight || window.innerHeight;
     canvas.width  = w;
     canvas.height = h;
     // 格子大小根据 canvas 尺寸动态计算
     const COLS = 30, ROWS = Math.floor(h / (w / COLS));
     const cellW = w / COLS, cellH = h / ROWS;
     // ... 其余游戏初始化逻辑
   }

   // 必须在 window.load 后、双层 rAF 确保布局渲染完毕再读尺寸
   window.addEventListener('load', function() {
     requestAnimationFrame(function() {
       requestAnimationFrame(function() {
         initCanvas();
       });
     });
   });
   ```

   **游戏类 WebView 触摸适配要点**（Android 8.1 WebView 无键盘/鼠标）：

   > ⚠️ **强制要求（主控方式）**：所有游戏的**主要控制方式必须是触摸坐标直接映射**——玩家手指按在画布哪里，角色/目标就跟到哪里（或朝那个方向移动），不需要抬手再点方向按钮。右下角的 ↑↓←→ 方向键和暂停键保留作为**辅助控制**，不是唯一控制入口。暂停按钮必须位于方向键 3×3 grid 的**正中心格**。

   **触摸坐标映射实现模板**（贴在 Canvas/游戏容器上）：
   ```js
   // 主控：手指位置直接映射到游戏坐标
   canvas.addEventListener('touchstart', onTouch, {passive: false});
   canvas.addEventListener('touchmove',  onTouch, {passive: false});

   function onTouch(e) {
     e.preventDefault();
     const rect = canvas.getBoundingClientRect();
     const touch = e.touches[0];
     // 将屏幕像素坐标换算为 canvas 内部坐标
     const cx = (touch.clientX - rect.left) * (canvas.width  / rect.width);
     const cy = (touch.clientY - rect.top)  * (canvas.height / rect.height);
     movePlayerTo(cx, cy);   // 替换为游戏实际函数：直接设置目标坐标
   }
   ```
   - 对于贪吃蛇、俄罗斯方块等离散格子类游戏，触摸映射改为**滑动方向**：`touchstart` 记录起点，`touchend` 计算 `deltaX/deltaY`，阈值 20px 内忽略，超过则取绝对值较大的轴作为方向
   - 对于飞机大战、跑酷等连续坐标类游戏，用 `touchmove` 实时跟随手指坐标
   - 左侧游戏遮罩/操作说明中必须用一句话说明触摸操作方式，例如：「触摸屏幕控制移动，手指在哪飞机就去哪」

   **飞机大战类游戏专项规则**：
   - **子弹必须自动连续发射**（`setInterval` 或游戏主循环中每隔固定帧数发射），**禁止要求玩家手动点击射击**
   - 自动射频简单难度约 300ms/发，中等 200ms/发，困难 100ms/发
   - 操作说明中写「触摸屏幕移动飞机，子弹自动发射」

   **俄罗斯方块/消除类游戏专项规则**：
   - **贴地即锁，零等待**：下落计时器触发时若方块无法继续下移，立刻执行 `lock()` → `spawn()`，下一块在同一帧内出现。**禁止 LOCK_DELAY 缓冲期**
   - **`spawnPiece()` 必须将新方块赋值给全局变量**（如 `cur = shape`），否则 `drawGrid()` 中 `if(cur != null)` 判断为 false 导致方块不显示
   - **经典 NES 速度标准**：第 1 关 800ms → 第 5 关 533ms → 第 10 关 333ms → 第 15 关 200ms → 第 20 关 100ms → 第 29 关+ 83ms（极限）
   - 难度递增公式：`interval = Math.max(83, 800 - (level - 1) * 5 * (1000/60))`（每关减约 5 帧，60fps 基准）
   - 预览区（下一块）在右栏 `#game-preview` 中展示，有预览时不展示排行榜和操作说明

   **方向键 + 暂停按钮模板**（放在右栏 `#controls` 内，作为辅助控制）：

   布局规则：**暂停按钮放在方向键 3×3 grid 的正中心格**，不单独放在键盘上方。整体视觉要炫酷：方向键用半透明玻璃质感，暂停键用蓝色渐变 + 光晕，`:active` 有明显按压反馈。

   ```html
   <div id="controls" style="flex:0 0 auto;display:flex;flex-direction:column;align-items:center;
        gap:0.8vh;touch-action:none;user-select:none;">
     <!-- 3×3 方向键grid，暂停在正中心 -->
     <div style="display:grid;grid-template-columns:repeat(3,13vmin);grid-template-rows:repeat(3,13vmin);gap:1.2vmin;">
       <div></div>
       <button class="dpad-btn" id="btn-up">▲</button>
       <div></div>
       <button class="dpad-btn" id="btn-left">◀</button>
       <button class="dpad-btn" id="btn-pause">II</button>
       <button class="dpad-btn" id="btn-right">▶</button>
       <div></div>
       <button class="dpad-btn" id="btn-down">▼</button>
       <div></div>
     </div>
   </div>
   <style>
   /* 方向键：半透明玻璃质感 */
   .dpad-btn {
     background: linear-gradient(145deg, rgba(255,255,255,.22), rgba(255,255,255,.06));
     border: 1.5px solid rgba(255,255,255,.35);
     border-radius: 50%;
     color: #fff;
     font-size: 4.5vmin;
     touch-action: manipulation;
     display: flex;
     align-items: center;
     justify-content: center;
     box-shadow: 0 2px 8px rgba(0,0,0,.4), inset 0 1px 0 rgba(255,255,255,.25);
     cursor: pointer;
     transition: transform .08s;
   }
   .dpad-btn:active {
     background: linear-gradient(145deg, rgba(255,255,255,.45), rgba(255,255,255,.15));
     transform: scale(.88);
     box-shadow: 0 1px 4px rgba(0,0,0,.5), inset 0 1px 0 rgba(255,255,255,.3);
   }
   /* 暂停键与方向键样式完全一致，仅字号加粗 + 细边框区分；用 II 代替 ⏸ 符号（WebView 渲染兼容） */
   #btn-pause {
     font-size: 4.5vmin;
     font-weight: bold;
     border-color: rgba(255,255,255,.6);
   }
   </style>
   <script>
   document.getElementById('btn-up').addEventListener('touchstart',    e=>{e.preventDefault();changeDir(0,-1);},{passive:false});
   document.getElementById('btn-down').addEventListener('touchstart',   e=>{e.preventDefault();changeDir(0, 1);},{passive:false});
   document.getElementById('btn-left').addEventListener('touchstart',   e=>{e.preventDefault();changeDir(-1,0);},{passive:false});
   document.getElementById('btn-right').addEventListener('touchstart',  e=>{e.preventDefault();changeDir( 1,0);},{passive:false});
   document.getElementById('btn-pause').addEventListener('touchstart',  e=>{e.preventDefault();togglePause();},{passive:false});
   // 桌面调试保留键盘
   document.addEventListener('keydown', e=>{
     if(e.key==='ArrowUp')    changeDir(0,-1);
     if(e.key==='ArrowDown')  changeDir(0, 1);
     if(e.key==='ArrowLeft')  changeDir(-1,0);
     if(e.key==='ArrowRight') changeDir( 1,0);
     if(e.key===' ')          togglePause();
   });
   </script>
   ```
   - `changeDir(dx, dy)` 和 `togglePause()` 替换为游戏实际函数名；坐标映射类游戏中方向键可改为触发"持续向该方向移动"逻辑
   - 按钮尺寸用 `vmin` 单位，960px 小屏到 2560px 大屏均可用
   - 暂停键必须在中心格，禁止移到键盘外部单独放置

   **游戏角色视觉规范**（卡通可爱风格，禁止只画纯色圆点/方块）：
   - 贪吃蛇：蛇头用圆角矩形 + 两个白色眼睛（小圆 + 黑色瞳孔）+ 根据朝向旋转；蛇身用渐变色圆角矩形，节节之间颜色略有变化；食物用苹果/草莓等图形（红色圆 + 绿色小叶子）
   - 贪吃蛇蛇头绘制示例（Canvas 2D）：
     ```js
     function drawHead(ctx, x, y, w, h, dir) {
       ctx.save();
       ctx.translate(x + w/2, y + h/2);
       const angle = {right:0, down:Math.PI/2, left:Math.PI, up:-Math.PI/2}[dir] || 0;
       ctx.rotate(angle);
       // 头部圆角矩形
       ctx.fillStyle = '#2ecc71';
       roundRect(ctx, -w/2, -h/2, w, h, w*0.3);
       ctx.fill();
       // 眼睛
       [[-w*0.15, -h*0.15],[w*0.15, -h*0.15]].forEach(([ex,ey])=>{
         ctx.fillStyle='#fff'; ctx.beginPath(); ctx.arc(ex,ey,w*0.12,0,Math.PI*2); ctx.fill();
         ctx.fillStyle='#222'; ctx.beginPath(); ctx.arc(ex+w*0.03,ey,w*0.06,0,Math.PI*2); ctx.fill();
       });
       ctx.restore();
     }
     function roundRect(ctx,x,y,w,h,r){
       ctx.beginPath();ctx.moveTo(x+r,y);ctx.lineTo(x+w-r,y);ctx.arcTo(x+w,y,x+w,y+r,r);
       ctx.lineTo(x+w,y+h-r);ctx.arcTo(x+w,y+h,x+w-r,y+h,r);ctx.lineTo(x+r,y+h);
       ctx.arcTo(x,y+h,x,y+h-r,r);ctx.lineTo(x,y+r);ctx.arcTo(x,y,x+r,y,r);ctx.closePath();
     }
     ```
   - 俄罗斯方块：方块用渐变色 + 高光边框，不同形状用不同颜色
   - 飞机大战：飞机用多边形或 SVG path 绘制，子弹用细长椭圆，敌机颜色与玩家区分；**子弹必须自动连续发射，禁止要求玩家手动点击射击**；操作说明写「触摸屏幕移动飞机，子弹自动发射」
   - 通用原则：所有游戏角色必须有辨识度，能看出是什么，不能只是纯色几何形状

   **平台跳跃 / 跑酷类游戏触摸控制规范**（马里奥、跑酷等左右移动+跳跃类游戏必须遵守）：

   > 核心设计：左右半屏控制方向，上滑触发跳跃，斜滑（如右上方）同时触发移动+跳跃，完全模拟实体手柄的拇指操作。

   ```js
   let tSX = 0, tSY = 0; // 触摸起点，每次 touchstart 或跳跃触发后重置

   canvas.addEventListener('touchstart', e => {
     e.preventDefault();
     const t = e.touches[0];
     tSX = t.clientX; tSY = t.clientY;
   }, {passive: false});

   canvas.addEventListener('touchmove', e => {
     e.preventDefault();
     const t = e.touches[0];
     const dx = t.clientX - tSX;
     const dy = t.clientY - tSY; // 负值 = 向上

     // 左右移动：根据手指当前位置在画布左/右半区判断方向
     const rect = canvas.getBoundingClientRect();
     if (t.clientX < rect.left + rect.width / 2) {
       moveLeft();
     } else {
       moveRight();
     }

     // 上滑检测跳跃：阈值 20px，触发后立即重置 tSY 防止重复触发
     if (dy < -20) {
       jump();
       tSY = t.clientY; // 重置参考点，允许同一次触摸连续触发（斜滑等）
     }
   }, {passive: false});

   canvas.addEventListener('touchend', e => {
     stopMove(); // 手指抬起停止移动
   }, {passive: false});
   ```
   - `dy < -20`（负值向上）触发跳跃，同一次 `touchmove` 序列可多次触发（重置 tSY）
   - 斜向上滑（如右上方）会同时执行 `moveRight()` + `jump()`，天然支持斜跳
   - 阈值 20px 优于 28px，更灵敏，适合快节奏横板游戏
   - 右栏方向键：◀▶ 控制移动，▲ 触发跳跃，▼ 可用于下蹲/快速下落
   - 触摸坐标映射为主控，方向键为辅助——两套控制并行，不互斥
   - 防止页面滚动干扰游戏：游戏容器加 `touch-action:none`，Canvas 加 `{ passive: false }` 并 `e.preventDefault()`
   - 游戏暂停/重启按钮触摸区域 ≥ 44×44px
   - 禁止在游戏主循环中使用 `alert()`，改用页面内自定义弹窗显示胜负信息

   **跳跃 / 平台类游戏角色定位规范**（跳一跳、跑酷、马里奥等必须遵守）：

   > ⚠️ **已知 Bug 根因**：用 `ph = PLAYER_H / squish` 作为绘制高度来定位头部/身体，当落地弹跳动画触发 `squish ≠ 1` 时，`ph` 变大，角色视觉上"沉入"平台下方。

   **正确做法**：`py` 始终表示角色**脚底**的 y 坐标（即站在平台顶面），`squish` 只影响**宽度**（身体变宽/变窄），绝不影响高度定位：
   ```js
   // py = 脚底 y（始终贴平台顶面，不受 squish 影响）
   // squish: 落地压缩系数，1=正常，>1=横向压扁（宽变大、高不变）
   function drawPlayer(ctx, px, py, squish) {
     const W = PLAYER_W * squish;   // 宽度随 squish 变化
     const H = PLAYER_H;            // 高度固定，不除以 squish
     const x = px - W / 2;
     const y = py - H;              // 脚底 py 往上量固定 PLAYER_H
     // 绘制身体：rr(ctx, x, y, W, H, radius)
   }
   ```
   - `squish` 动画只修改 `W`（或同时等比缩小 `H` 但必须同步上移 `y = py - H`），确保脚底始终在 `py`
   - 禁止写 `y = py - PLAYER_H / squish`，这会在 squish > 1 时让角色上移，squish < 1 时下沉



   > ⚠️ **强制要求**：所有游戏类应用必须内置难度阶段机制，**默认从简单难度开始**，通过 10 关后自动升级为中等难度，通过 20 关后升级为困难。以飞机大战为参照基准，其他游戏按比例换算。

   **难度分级标准**（以飞机大战为基准示例）：
   | 阶段 | 关卡范围 | 敌机坠落速度 | 子弹发射间隔 | 过关目标分 | 每关目标分增量 |
   |------|---------|------------|------------|---------|------------|
   | 简单（Easy）  | 第 1~10 关  | 基础速度 × 1/2 | 300ms/发 | 100 分 | +10 分/关 |
   | 中等（Medium）| 第 11~20 关 | 基础速度 × 80% | 200ms/发 | 200 分 | +10 分/关 |
   | 困难（Hard）  | 第 21 关起  | 基础速度  | 100ms/发 | 300 分 | +10 分/关 |

   - **难度参数必须用变量控制**，根据关卡号计算，禁止魔法数字硬编码：
     ```js
     let level = 1; // 每通关 +1

     function getDifficulty(level) {
       if (level <= 10) return {
         speedMul: 1/2,  bulletInterval: 300,
         targetScore: 100 + (level - 1) * 10   // 100, 110, 120...
       };
       if (level <= 20) return {
         speedMul: 0.8,  bulletInterval: 200,
         targetScore: 200 + (level - 11) * 10  // 200, 210, 220...
       };
       return {
         speedMul: 1,  bulletInterval: 100,
         targetScore: 300 + (level - 21) * 10  // 300, 310, 320...
       };
     }
     ```
   - **不设硬性关卡上限**，进入困难阶段后目标分持续增加，让玩家可以持续挑战
   - 关卡信息（当前关卡、当前难度名称、得分 / 目标分、生命）必须在右栏顶部实时显示

   **文档/Word/PDF 风格**：
   - 容器使用响应式宽度：`max-width: min(1200px, 92vw); margin: 3vh auto; padding: 4vh 5vw`
   - 在 960px 小屏上内容几乎满宽，在 1920px+ 大屏上居中且不超过 1200px
   - 正文字号 `clamp(14px, 1.8vw, 18px)`，标题 `clamp(20px, 3vw, 32px)`
   - 清晰的标题/段落/列表排版，使用衬线或无衬线字体
   - 页面顶部可显示文档标题和日期

   **PPT/演示文稿风格**：
   - 引入 reveal.js：`<link rel="stylesheet" href="https://unpkg.com/reveal.js@5/dist/reveal.css">`
   - 引入主题：`<link rel="stylesheet" href="https://unpkg.com/reveal.js@5/dist/theme/white.css">`
   - 引入 JS：`<script src="https://unpkg.com/reveal.js@5/dist/reveal.js"></script>`
   - 内容用 `<div class="reveal"><div class="slides"><section>...</section></div></div>` 包裹
   - 每个 `<section>` 是一页幻灯片
   - 初始化：`<script>Reveal.initialize({hash:true, touch:true, width:960, height:600});</script>`
     reveal.js 内部会等比缩放到实际视口，960×600 基准保证所有设备文字清晰不溢出
   - 5~15 页为宜

   **Excel/表格风格**：
   - 容器 `width:100vw; height:100vh; overflow:auto; box-sizing:border-box; padding:2vh 3vw`
   - HTML `<table>` 宽度 100%，带 border 和交替行色
   - 表头字号 `clamp(12px, 1.6vw, 16px)`，单元格字号 `clamp(12px, 1.4vw, 15px)`
   - 表头点击可排序（内联 JS 实现）
   - 单元格 `contenteditable="true"` 可编辑

   **所有类型通用禁止项**：
   - 禁止出现"导出"、"打印"、"保存"功能按钮
   - 禁止 `@media print` 相关样式
   - 禁止 `window.print()`、文件下载等功能

4. 图标生成（icon_base64）：
   - 产出一个 256×256 的 SVG 图标
   - 风格：圆角矩形纯色背景 + 居中的主题图形（用 SVG path/circle/rect 绘制，**禁止使用 `<text>` 或 emoji**）
   - 背景用饱和度高的纯色，中间图形用与背景对比强烈的颜色（可用白色、也可用多色彩搭配，参考 App Store 图标风格）
   - SVG 文本做 base64 编码后传入 icon_base64（不带 `data:image/svg+xml;base64,` 前缀）
   - SVG 原文不超过 3KB，**禁止使用 `<text>` 元素或 emoji**

5. **【必须执行】HTML 自检 — 提交前逐项检查**：
   生成 html_content 后，**必须**在脑内逐项检查以下条件，任一不通过则必须修改代码后再提交：

   **自检项 A — 禁止 AI/电脑对手**（仅游戏/棋类/对战类需检查）：
   - [ ] 代码中是否存在任何"电脑走棋/出牌/移动"的函数？（如 `computerMove`, `aiMove`, `makeAIMove`, `botPlay`, `autoPlay`, `cpuTurn`）→ 若有，**删除整个函数及其调用**
   - [ ] 代码中是否存在 `minimax`, `alphaBeta`, `evaluate`, `bestMove`, `getRandomMove`, `Math.random()` 用于选择落子位置？→ 若有，**删除**
   - [ ] 代码中是否存在"难度选择"（easy/medium/hard）或"人机/人人"模式切换？→ 若有，**删除，只保留双人模式**
   - [ ] 游戏流程是否为：玩家A操作 → 切换到玩家B → 玩家B操作 → 切换回玩家A → 循环？→ 必须是
   - [ ] 是否有任何 `setTimeout`/`setInterval` 用于延迟执行电脑的操作？→ 若有，**删除**

   **自检项 B — 禁止导出/打印/保存**（所有类型需检查）：
   - [ ] 是否存在"导出"、"打印"、"保存"、"下载"按钮或菜单项？→ 若有，**删除**
   - [ ] 是否存在 `window.print()`, `document.execCommand('SaveAs')`, `URL.createObjectURL`, `download` 属性？→ 若有，**删除**

   **自检项 C — Android 8.1 WebView 兼容**（所有类型需检查）：
   - [ ] 是否使用了 Chrome 86+ 才支持的 CSS/JS API（`@property`、`content-visibility`、`structuredClone`、`??=`/`||=`/`&&=` 赋值运算符）？→ 若有，**替换为兼容写法**
   - [ ] 是否使用了 `ctx.roundRect()`？→ Chrome 99+，**必须替换为自定义 `rr()` helper（用 arcTo 实现）**
   - [ ] Canvas 内是否使用了 emoji 字符（fillText 中含 🔥❤️ 等）？→ WebView 字体渲染异常，**必须替换为纯文字或几何图形**
   - [ ] 游戏布局是否为横版左右两栏（左栏游戏区、右栏控制区）？→ **若是竖版堆叠，必须改为横版**
   - [ ] 右栏有 `#game-preview`（下一块/预览区）时，是否已去掉 `#leaderboard` 和 `#instructions`？→ **预览区与排行/说明互斥，有预览时不展示排行和说明**。无预览区的游戏中，排行/说明用 `flex:1 1 0;min-height:0` + h3 固定 + `.sb-inner` 内滚动。`#controls` 始终 `flex:0 0 auto` 固定底部
   - [ ] Canvas CSS 是否用 `position:absolute;top:0;left:0;width:100%;height:100%` 撑满左栏，而非依赖 flex 布局？→ **若只用 `width:100%;height:100%` 而无 `position:absolute`，必须修正**
   - [ ] Canvas 尺寸初始化是否在 `window.load` + 双层 `requestAnimationFrame` 内执行，且用 `offsetWidth` 做兜底（防止 Android 8.1 WebView 初始 `clientWidth` 为 0）？→ **若直接在顶层读 `clientWidth`，必须改为延迟初始化模板**
   - [ ] 需要方向控制的游戏：是否在 Canvas 上绑定了 `touchstart`/`touchmove` 做坐标直接映射（主控），且右下角仍保留方向键 + 暂停按钮（辅助）？→ **若只有方向按钮而无触摸坐标映射，必须补充**
   - [ ] 飞机大战类游戏：子弹是否自动连续发射（`setInterval` 或主循环计时），而非要求玩家手动点击射击？→ **若需要手动触发，必须改为自动发射**
   - [ ] 俄罗斯方块/消除类游戏：①初始下落间隔是否为800ms（经典NES速度）？②贴地后是否立刻lock+spawn（零等待，无LOCK_DELAY缓冲）？③`spawnPiece()`是否将新方块赋值给全局变量（`cur=shape`）？→ **若不符合，按专项规则修正**
   - [ ] 游戏内的开始/结束/暂停遮罩层是否用 `position:absolute;top:0;left:0;right:0;bottom:0;display:flex;align-items:center;justify-content:center` 居中（**禁止用 `inset:0`，Chrome 85 不支持**）？→ **若用 `inset:0` 或固定像素定位，内容会在智能屏上贴左上角，必须修正**
   - [ ] 游戏是否实现了三段式难度（简单1~10关：速度×1/2、300ms/发、100+10×n分 → 中等11~20关：速度×80%、200ms/发、200+10×n分 → 困难21关起：基础速度、100ms/发、300+10×n分），且第1关使用简单参数？→ **若全程同一难度或开局就很快，必须按难度分级模板修正**
   - [ ] 游戏角色是否有视觉辨识度（蛇头有眼睛、食物有形状等），而不是纯色圆点/方块？→ **若只是纯色几何形，必须改为卡通风格**
   - [ ] 是否使用了原生 `alert()`/`confirm()`/`prompt()`？→ 若有，**改为页面内自定义弹窗**
   - [ ] 游戏容器/Canvas 是否加了 `touch-action:none` 并在 touch 事件中调用 `e.preventDefault()`？→ 若未处理，**补充**
   - [ ] 可点击/可触摸元素的触摸区域是否 ≥ 44×44px？→ 若不足，**调整尺寸**
   - [ ] 跳跃/平台类游戏（跳一跳、跑酷等）：绘制角色时是否用固定常量 `PLAYER_H` 定位脚底坐标（`py` 为脚底 y，头顶为 `py - PLAYER_H`），而非用 `PLAYER_H / squish` 等变形高度定位？→ **`squish`（落地压缩动画）只能影响角色宽度/变窄，绝不能影响脚底 `py` 的计算，否则 squish≠1 时角色视觉上会"沉入"平台下方**

   ⚠️ 如果自检发现违规代码，**不要提交**，先修正 html_content 再继续下一步。

5.5. **【必须执行】JS 语法验证**（应用类/游戏类必须，文件类可选）：
   在调用 `myapp_register` 之前，用 `exec` 工具对 html_content 中的 `<script>` 代码块做语法验证，确保不因语法错误导致游戏在智能屏上完全空白：
   ```bash
   # 提取 <script> 内容写临时文件，用 node --check 验证
   node -e "
   const fs = require('fs');
   const html = fs.readFileSync('/tmp/_skill_check.html','utf8');
   const scripts = html.match(/<script[\s\S]*?>([\s\S]*?)<\/script>/gi) || [];
   scripts.forEach((s,i) => {
     const code = s.replace(/<\/?script[^>]*>/gi,'');
     fs.writeFileSync('/tmp/_check_'+i+'.js', code);
   });
   " && node --check /tmp/_check_*.js 2>&1
   ```
   - 实际操作：将 html_content 写入 `/tmp/_skill_check.html`，运行上面命令
   - 如果 `node --check` 输出任何错误，必须修复对应 JS 代码后重新验证，直到无错误
   - 验证通过后再调用 `myapp_register`

6. 调用 `myapp_register` 工具：
   - 入参：`dumi_id, cuid, query, app_name, html_content, features, icon_base64, tag`
   - `tag`：根据第 1 步判断的类型填写——**应用类（交互式）填 `"app"`，文件类（文档/PPT/表格）填 `"doc"`**；不传时服务端默认 `"app"`
   - `dumi_id` 与 `cuid` 从对话上下文中获取（OpenClaw 会注入）

7. 工具返回成功后，向用户展示：
   - 告知创建完成："《<app_name>》已创建完成。"
   - 展示功能/玩法（根据类型区分）：
     - **应用类**：
       - 列出"游戏特性"或"功能特性"：从 features 中提取 3~6 条核心点
       - 列出"操作方式"：说明触屏/键盘的操作方法（如方向键控制、暂停等）
     - **文件类**（文档/PPT/表格）：
       - 简要概括文档核心内容（如关键数据、主要结论、章节概要等，3~5 条）
       - 提示"点击链接即可查看完整内容"
   - 展示文件位置：给出返回的 `html_url` 链接
   - 提示用户："下次可以在「我的创作」页面查看和管理你创建的所有应用"

8. 失败/超长/超出能力 → 回复"应用创建失败，请稍后重试"
   - **不要重试**，**不要伪造成功**，**不要把 html_content 输出到对话**

## 更新流程

最长等待 300s。若 300s 内不能完成旧功能读取、HTML 重新生成与 `myapp_update` 调用，直接回复"应用更新失败，请稍后重试"。

1. **先调 `myapp_get(app_id)`** 拿到 `app_name` 与旧 `features`、旧 `query`
2. 把"旧 features + 用户新需求"作为完整上下文，重新生成：
   - 新 features（合并增删，仍是 1~12 条全集，不是 diff）
   - 新 html_content（保持原有类型风格）
   - 若应用主题/类型发生变化，重新生成 icon_base64（同创建流程第 4 步）
3. 调用 `myapp_update(app_id, query, html_content, features, icon_base64, tag)`
   - `tag` 同创建流程：应用类填 `"app"`，文件类填 `"doc"`
4. 工具返回成功后，向用户展示：
   - 告知更新完成："《<app_name>》已更新完成。"
   - 展示更新内容（根据类型区分）：
     - **应用类**：列出本次新增/变更的功能点和操作方式变化
     - **文件类**：简要概括更新后的核心内容或变更要点
   - 展示文件位置：给出返回的 `html_url` 链接
   - 提示用户："下次可以在「我的创作」页面查看和管理你创建的所有应用"
5. 失败 → 回复"应用更新失败，请稍后重试"

## 安装自检（[install_check:session=<sid>]）

最长等待 300s。超过 300s 未完成安装或 `myapp_ping`，视为安装失败。

仅调用 `myapp_ping(session_id="<sid>", dumi_id, cuid, skill_version="1.0.10")`，
不输出对话内容（或仅极简的"已就绪"）。

## 硬约束

- **绝对禁止在游戏中实现 AI 对手、人机对战、电脑自动操作**——棋类/对战类游戏只允许双人同屏轮流操作
- 禁止出现的代码模式：`computerMove`, `aiMove`, `makeAIMove`, `minimax`, `alphaBeta`, `bestMove`, `getRandomMove`, 难度选择(easy/medium/hard), 人机/人人模式切换
- **绝对禁止出现"导出"、"打印"、"保存"按钮或相关功能**
- **需要方向控制的游戏必须在页面上渲染四个方向触摸按钮（↑↓←→），绑定 `touchstart` 事件**——不得以键盘或滑动手势代替
- 不要把 `html_content` 原文输出到对话
- 不要把 `MYAPP_API_TOKEN` / `MYAPP_API_BASE` 输出到对话
- 工具调用 4xx/5xx → 直接失败兜底，不重试，不修改请求自行重试
- 除安装、创建、更新外，其它工具交互超过 180s 视为失败
