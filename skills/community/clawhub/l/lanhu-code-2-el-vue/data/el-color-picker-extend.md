# el-color-picker-extend 组件说明

面向 **Vue 2 + Element UI 2.x** 的自定义填充色面板（`src/components/el-color-picker-extend.vue`），视觉与交互对齐设计稿：预设网格 / 调色板双模式、不透明度、Hex/RGB、最近使用、吸管（浏览器能力允许时）。

---

## 颜色选择：触发与下拉的共同结构（通用规则）

页面上每一处「颜色选择」交互，在交互模型上都是一致的：

| 部分 | 说明 |
|------|------|
| **触发区** | 用户点击后切换下拉显示/隐藏：常见为 **色块按钮**、**「填充」标题旁的入口**、**字体颜色行里的 A + 下划线 + 箭头** 等。触发区的视觉样式**不作为**选用 `el-color-picker` 与 `el-color-picker-extend` 的依据。 |
| **下拉层（弹层面板）** | 点击触发后展开的区域。**组件选型只看这一块的版式与控件组合**，与触发区是方块还是文字无关。 |

**选型原则（一句话）**：  
**若展开后的下拉内容符合「图1」特征 → 使用 `el-color-picker-extend`；若符合「图2」特征 → 使用 Element UI 官方的 `el-color-picker`。** 不得仅根据「有没有色块按钮」或「是不是小条工具栏」猜组件；必须在设计稿或产品中 **确认展开后的面板**。

---

## 图1 / 图2 对照与识别清单（问题排查用）

| 维度 | 图1（→ `el-color-picker-extend`） | 图2（→ `el-color-picker`） |
|------|-----------------------------------|-----------------------------|
| **主视觉区** | 大块 **预设色格矩阵**（如 10×5），首格常为无填充/透明 | 左侧大块 **SV（饱和度×明度）** 渐变方 |
| **色相** | 调色板模式下可能为 **横向色相条**（与 extend 内部实现一致），或预设格为主 | **右侧竖向彩虹色相条**（Element 2 默认布局） |
| **底部/中部输入** | 常见 **# + Hex**、**% 不透明度**、**R / G / B** 分栏、**吸管** | 底部 **Hex 单行** 为主，配 **「清空」「确定」**（文案以稿为准） |
| **其他特征** | **「最近使用」** 可折叠列表、标题 **「填充」**、模式切换图标等（设计稿专用面板） | **无** 与 extend 一致的「预设矩阵 + 最近使用」一体化稿面；为标准 Element 取色器皮肤 |

**识别操作顺序（推荐）**

1. 在稿面或交互稿中找到该取色点，确认 **点击后展开的是哪一块面板**（可让设计/产品标注「展开态」）。  
2. 用上表对照：有 **SV 大方块 + 右侧竖色相条 + 底栏清空/确定** → 图2；有 **色格矩阵 + 填充/最近使用/吸管/分栏 RGB** 等稿面定制组合 → 图1。  
3. 静态 HTML 改 `Custom.vue` 时：在 `index.vue` 中搜索「填充」、色格切图、`#`+hex、最近使用等 **整块** 结构，多为图1 页内模拟；「字体颜色」旁小框 + 展开为 Element 默认面板 → 图2。

---

## 两种取色弹层与组件选型（识别 → 修复 → 需求）

静态改动态或修复已有 `Custom.vue` 时，**先区分稿面/产品要求的取色弹层形态（图1 或 图2）**，再选用组件；替换完成后 **删除** 页面内原有的颜色选择静态结构或错误组件，**只保留**与选型一致的一套取色 UI。

### 图1 形态（→ `el-color-picker-extend`）

| 环节 | 内容 |
|------|------|
| **识别特征** | 弹层或页内区含 **标题「填充」**（或同类）；**多格预设色板**（如 5×10）；**横向渐变/透明度滑条**；**# + Hex**、**% 不透明度**、**R/G/B 数字**；**吸管**；**「最近使用」** 可折叠列表等。整体为 **设计稿专用「填充」面板**，**不是** Element 默认取色器布局。 |
| **修复** | 用 **`<el-color-picker-extend v-model="..." recent-storage-key="业务唯一键" />`**（在 `main.js` 全局注册）替换上述 **整块** DOM；`v-model` 使用 **`rgba(r,g,b,a)`** 字符串。 |
| **删除** | 移除原 **所有** 与填充相关的静态 `img` 色条/色格、独立 `el-input` 拼装的 hex/rgb/透明度、静态「最近使用」色块等，避免与扩展组件 **重复**。 |
| **父级样式** | 若 index.css 对容器写了 **固定 `height` / `min-height`**（如 354px）导致折叠或内容变化后留白异常，在包裹类上改为 **`height: auto`**，必要时 **`min-height: 0`**，见下文「实现中常见问题」表。 |

### 图2 形态（→ `el-color-picker`）

| 环节 | 内容 |
|------|------|
| **识别特征** | 打开后为 **Element UI 2 默认取色下拉**：大块 **饱和度/明度（SV）面**；**右侧竖向** 彩虹 **色相条**；底部 **Hex 输入**；操作 **「清空」**、**「确定」**（文案以稿面为准）。 |
| **修复** | 使用 **`el-color-picker`**（可 `show-alpha`）；**字体颜色工具条**（A + 下划色条 + 箭头）须 **透明叠层** 覆盖触发区，见下文 **「字体颜色触发器」**；**勿**对 `.el-color-picker` 根节点整体 `opacity: 0`。 |
| **删除** | 若页内另有 **图1 类整页「填充」切图区**，而交互已改为图2 下拉取色，须 **删除** 该页内块，避免两套取色。 |

### 需求文案（可复用）

1. **选型**：图1 → `el-color-picker-extend`；图2 → `el-color-picker`；不得颠倒。  
2. **唯一一套**：同一业务场景只保留一种取色实现，替换后删除旧 DOM 与仅服务于旧 DOM 的 data/methods。  
3. **图1 集成**：扩展组件外框 **高度随内容**，不与静态稿固定总高死绑。  
4. **图2 工具条**：自定义可见面 + 透明 `el-color-picker` 触发区，保证 **下拉面板可见**。

### 需求文案（评审 / 工单可粘贴）

- **颜色选择组件选型**  
  - 所有颜色选择均由「触发区 + 下拉面板」组成；**以下拉面板的版式为准**选定组件。  
  - **下拉为图1**（预设色块矩阵、填充标题、Hex/RGB/不透明度、最近使用、吸管等稿面定制布局）→ 使用 **`el-color-picker-extend`**，`v-model` 为 `rgba(...)`，`recent-storage-key` 区分业务。  
  - **下拉为图2**（Element UI 2 默认：SV 面 + 右侧竖向色相条 + 底部 Hex + 清空/确定）→ 使用 **`el-color-picker`**；小尺寸触发器（如 A+下划线）采用 **透明触发器叠层**，禁止对整颗组件根设置 `opacity: 0`。  
- **互斥与清理**：同一取色场景替换后须删除静态切图或重复面板，禁止图1 静态块与图2 官方下拉或 extend 并存。

### 常见错配与修复（问题修复）

| 现象 | 原因 | 修复 |
|------|------|------|
| 稿面是图1，用了 `el-color-picker` | 仅按「有个色块按钮」选型 | 改为 **`el-color-picker-extend`**，删除页内色格/滑条/hex 等静态 DOM |
| 稿面是图2，用了 `el-color-picker-extend` | 把「填充」类需求误套到字体颜色 | 改为 **`el-color-picker`** + 触发区叠层 |
| 下拉打不开或全透明 | 对 `.el-color-picker` **根节点** 设了 `opacity: 0` | 仅对 **`::v-deep .el-color-picker__trigger`** 隐藏，保证下拉挂载可见 |
| 图1 替换后底部空白很高 | 父级仍用静态稿 **固定 height/min-height** | 包裹层改为 **`height: auto`**，必要时去掉 **`min-height`** |

---

## 字体颜色触发器（Element UI 2 官方 `el-color-picker`）

与 **lanhu-code-2-el-vue 6.3.11** 对应：稿面「字体颜色」为 **A + 下划色条 + 下拉箭头**，且打开后为 **图2（Element 默认面板）** 时，用官方 **`el-color-picker`** 承接交互；**自定义外观**与 **删除页内图1 类静态「填充」区** 按本节执行。

### 识别

1. **工具条区**：`index.vue` 中「字体颜色」旁 **小框** 内为 **A**、**色条**、**箭头图**（或 **A + png**），尺寸多在 **48×24px** 量级（以 index.css 为准）。
2. **页内大面板（图1）**：同页常见 **group_9 / box_** 等 **整块「填充」**：含 **多张大图**（色格、滑条）、**# + hex**、**%**、**RGB 数字**、**最近使用** 等——应改为 **`el-color-picker-extend`** 并 **整段删除** 原静态 DOM；若该页字体颜色行已用 **图2** 的 **`el-color-picker`**，则 **不得** 再保留页内整块图1「填充」切图。

### 修复方法（无 trigger 插槽时的标准写法）

Element UI **2.x** 的 `el-color-picker` **没有** 自定义触发器插槽，须用 **叠层**：

1. 外层容器 **`position: relative`**，与子元素同 **宽高**（与稿面小框一致）。
2. **底层**：自定义面（A、`:style="{ backgroundColor }` 的色条、CSS 三角），设 **`pointer-events: none`**。
3. **上层**：`el-color-picker` **`position: absolute; left: 0; top: 0; width: 100%; height: 100%;`**，对 **`::v-deep .el-color-picker__trigger`**：`width/height: 100%`、`padding: 0`、`border: none`、**`opacity: 0`**（仅隐藏 **触发条**，勿隐藏整个组件根节点）。
4. **禁止**：给 **`.el-color-picker` 根** 设 **`opacity: 0`**——子级 **`picker-dropdown`** 仍挂在该根下时，会导致 **下拉面板不可见**。

### 需求文案（可复用）

- 字体颜色控件须 **像素级对齐** 稿面：**字 A**、**下划线颜色 = 当前 `v-model`**、**右侧下拉三角**。
- 取色交互仅保留 **Element 官方下拉**；**删除** 原稿 **页内整段** 填充/取色切图区（含静态「最近使用」色块），除非产品单独要求自研「最近使用」并在 script 中实现。

### 自检清单

- [ ] 点击自定义区域能打开/关闭官方取色面板，面板内选色、确定、清空正常。
- [ ] 下划线颜色随 `v-model` 更新；全透明时显示合理（如 `transparent`）。
- [ ] 页面 **无** 第二套静态大「填充」面板或重复「最近使用」切图。
- [ ] 多条「字体颜色」行若各放一个 `el-color-picker`，`v-model` 绑定一致或按产品拆分，无重复无效 DOM。

---

## 产品需求文案（可复用）

1. **双模式**  
   - **预设模式**：10×5 色块网格；首格为「无填充/透明」；当前选中格显示对勾。  
   - **调色板模式**：复用 Element UI `el-color-picker` 内部 **`sv-panel`、横向 `hue-slider`** 与 **`Color`** 类；布局顺序为 SV 面 → 色相条 →（共用）透明度条。  
   - **不透明度**：两种模式共用同一 **`alpha-slider`**（与官方 `el-color-picker` 默认透明度条一致），与 Hex、RGB、不透明度输入联动。

2. **模式切换（右上角）**  
   - 图标与 `shushi/Custom.vue`（及 `index.vue`）稿图一致，**`data:image/png;base64,...`** 内联于 **`el-color-picker-extend.vue`** 的 script 顶部常量 `TOGGLE_PALETTE_MODE_DATA_URI` / `TOGGLE_PRESET_MODE_DATA_URI`（源 PNG：`assets/img/SketchPng4ab504794463cdafc399f2fef83e40a6e8d920dc2a5259ed401c9b54aab26fbc.png` → 进调色板；`SketchPng03349d12d5f31759703250c8b25a810d416c8e99320e32395dec3f6c650b83fe.png` → 回预设）。组件为单文件完整交付，不依赖独立 `toggle-icons-data.js`。  
   - 「无填充」仅通过预设网格首格选择。

3. **数据绑定**  
   - 使用 `v-model`（Vue 2：`value` + `input` 事件）。  
   - 对外统一为 **`rgba(r,g,b,a)`** 字符串；全透明为 **`rgba(0,0,0,0)`**（便于与 CSS / Canvas 一致）。

4. **最近使用**  
   - 可折叠区块「最近使用」；点击色块应用颜色。  
   - 默认持久化到 `localStorage`，可通过 `recent-storage-key` 区分页面/业务；全透明不写入历史。  
   - **折叠后整块高度须随内容收缩**：外层容器不得沿用静态稿的固定 **`height` / `min-height`**，否则会出现底部空白、面板「撑不满也缩不短」的问题。

5. **吸管**  
   - 在支持 [EyeDropper API](https://developer.mozilla.org/en-US/docs/Web/API/EyeDropper) 的浏览器中可用；不支持时按钮禁用。

6. **无障碍与交互**  
   - 可点击控件具备 `cursor: pointer`、可见 `focus` 样式、`aria-label`；不透明度由 Element `alpha-slider` 与右侧百分比输入共同完成。

7. **不透明度数值 + 百分号布局**  
   - 数值与 **`%` 后缀**同处一行时，须保证 **`%` 不被挤出可视区域**（不出现横向溢出或裁切异常）。  
   - 若需保留浏览器为 **`type="number"`** 提供的 **步进（加减）控件**，应为 **数字区 + 步进器 + `%`** 预留足够总宽，**不得**用 `appearance` / `::-webkit-*-spin-button` 等样式擅自关掉步进器作为首选方案；仅在产品明确要求「极简窄条且无步进」时再考虑隐藏。

---

## 实现中常见问题 → 识别与修复 → 通用规则

| 问题现象 | 原因 | 修复要点 | 通用规则 |
|----------|------|----------|----------|
| Vue 2 父组件 `v-model` 不更新 | 未声明 `model: { prop, event }` 或子组件用错事件名 | 子组件 `model: { prop: 'value', event: 'input' }`，`$emit('input', next)` | **Vue 2 自定义 v-model 必须显式 model 选项**；与 Vue 3 `update:modelValue` 区分 |
| Hex/RGB/HSV 互相改写后出现 1 位偏差 | 浮点 HSV↔RGB 与 `Math.round` 时机不一致 | 单一真源（内部 `r,g,b,alpha`），展示前再 `round`；提交时再 emit | **颜色状态单一真源**；展示与存储分离，避免双向各算一遍 |
| 拖拽 SV/色相/Alpha 时频繁写历史或频繁 emit | 在 `mousemove` 上直接 `emit` / `pushRecent` | 仅在 `mouseup` 提交最终值；或防抖后提交 | **连续拖拽：move 只更新 UI，up 再提交** |
| 从最近使用点选导致重复压栈 | 应用颜色再次触发 `pushRecent` | 设置一次性标志 `skipRecentNext`，本帧不写入 | **回放历史数据时跳过「写入历史」副作用** |
| 透明与「无填充」语义混乱 | 有的用 `''`，有的用 `transparent` | 约定文档化：对外只用 `rgba(0,0,0,0)` | **透明色在工程内单一表示**，并在文档写明 |
| 预设格与当前色不一致仍显示对勾 | 仅用 hex 比较忽略 alpha，或忽略透明 | 透明格：`alpha <= ε`；有色格：RGB 相等（按需是否比 alpha） | **选中态判定与数据模型字段一致** |
| 色相滑块指示条偏移 | `top: n%` 未配合垂直居中 | `transform: translateY(-50%)` 或 `calc` 减半高 | **轨道百分比定位需补偿拇指/指示器半高** |
| 吸管点击无反应 | 非 HTTPS / 非安全上下文或浏览器不支持 | `!!window.EyeDropper` 检测；`disabled` + 不报错静默 | **浏览器 API 先特性检测再暴露 UI** |
| `localStorage` 写入失败 | 隐私模式、配额、序列化异常 | `try/catch` 吞掉并降级为仅内存 | **持久化不得阻断主流程** |
| 与 Element `el-color-picker` 混用概念混淆 | Element 2 面板与自研面板并存 | 自研组件独立命名、独立引入；勿假定与 `picker-dropdown` 替换逻辑耦合 | **扩展组件与官方 picker 解耦**，替换 webpack 补丁不影响本组件 |
| 调色板与外部 `v-model` 打架、循环更新 | 子组件内自算 HSV 与 Element `Color` 不同步 | 以 `r,g,b,alpha` 为展示真源；`elColor.fromString(rgba)` 用 `_syncingFromParent` 屏蔽回写期间的 `watch` | **嵌入第三方颜色对象时：父值同步进对象须加「同步中」标志，避免 deep watch 反向 emit** |
| 在调色板拖拽时「最近使用」刷屏 | 每帧 `pushRecent` | 对 Element 面板变更做 **防抖**（如 400ms）再写入最近使用 | **高频颜色变更与持久化历史解耦，防抖或仅在 mouseup 写入** |
| **`%` 后缀溢出父级或被顶到面板外** | 固定宽度过窄；`input` 使用 `width: 100%` 与后缀在同一 flex 行内争宽；`number` 步进器占宽 | 后缀 **`flex: 0 0 auto`**；输入框 **`flex: 1 1 0; min-width: 0; width: 0`**；容器 **加宽**（含步进器占位，如约 **90px+**）并设 **`gap`** | **「number + 后缀」行：可收缩的是中间数字区，后缀固定宽；总宽要覆盖浏览器原生控件** |
| **百分比输入无加减步进** | 曾用 `appearance: textfield`、`-moz-appearance` 或 `::-webkit-*-spin-button { appearance: none }` 去掉原生 UI | **删除**上述覆盖样式，恢复浏览器默认；靠 **加宽容器 + flex 分配** 解决溢出，而非默认关掉步进器 | **原生控件与布局冲突时优先「腾地方」；用 CSS 禁用控件需与产品一致并写进需求** |
| 数字输入在 flex 里把整行撑破 | 可替换内容默认 `min-width: auto` | 可收缩输入加 **`min-width: 0`** | **Flex 子项要收缩时显式 `min-width: 0`**（经典 flex 陷阱） |
| **「最近使用」收起后填充区仍很高、底部空白** | 页面壳子沿用 **`index.css` / 静态稿** 里对父级的 **`height: 354px`** 或集成时加的 **`min-height: 354px`**；折叠仅 `v-show` 隐藏子区域，外框高度被 CSS 锁死 | 在挂载该组件的容器上使用 **`height: auto`**，**去掉**为旧稿预留的 **`min-height`**；若与全局 `.group_2` 等同优先级冲突，用 **`.group_2.group_2--picker`** 等 **更高优先级选择器** 覆盖固定高度，必要时设 **`min-height: 0`** 允许 flex 子项收缩 | **静态转动态时：外框高度随内容；勿把设计稿总高写成父级 `height`/`min-height`；折叠区块不应对应固定外框占位** |

---

## Props

| 属性 | 类型 | 默认 | 说明 |
|------|------|------|------|
| `value` | String | `rgba(252, 123, 37, 1)` | 当前颜色（`v-model`） |
| `title` | String | `填充` | 左上角标题 |
| `recent-storage-key` | String | `el-color-picker-extend:recent` | 最近使用 localStorage 键 |
| `max-recent` | Number | `8` | 最近条目上限 |

## 事件

| 事件 | 载荷 | 说明 |
|------|------|------|
| `input` | `rgba(...)` | 与 `v-model` 同步 |
| `change` | `rgba(...)` | 用户确认变更（与 `input` 同时触发，便于监听） |

---

## 在页面中引用示例

```vue
<el-color-picker-extend
  v-model="fillColor"
  recent-storage-key="shushi:fill-recent"
/>
```

```js
data() {
  return { fillColor: 'rgba(252, 123, 37, 1)' };
}
```

若父级仍引用与静态 `index.vue` 相同的 **`index.css`**，注意其中 **`.group_2 { height: 354px; }`** 会锁死外框高度；需在包裹类上覆盖为 **`height: auto`** 且 **勿设** 与稿面总高相同的 **`min-height`**（`shushi/Custom.vue` 使用 **`.group_2.group_2--picker`** 覆盖）。

---

## 设计实现备注（ui-ux-pro-max）

- 图标使用 **SVG**，不用 emoji 作功能图标。  
- 可点击区域使用 **pointer 与 hover 反馈**，过渡约 **150–300ms**。  
- 尊重 **`prefers-reduced-motion`**，减弱动画。  
- 浅灰输入底 **`#f2f4f5`**、主文案 **`#212329`**，与现有 `shushi` 稿样式对齐。
