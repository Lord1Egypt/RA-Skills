# ChatCut 宿主实测行为档案

ChatCut 宿主实测行为的唯一权威位（2026-07 实战批量剪辑 + 一场约 15 分钟母片全片重构会话实证；其他分册引用本文件，不复制结论）。每条按「现象 → 判定 → 正确动作」。工具行为可能随版本变化：同类操作首次执行前用一个代表对象复验，复验失败以当前实测为准并回写你自己的档案副本。

## 几何与渲染

- **crop 语义 = 框内裁显示区**。`rect + crop` 的可见区 = rect 向内收缩（`可见左 = left + width×cropLeft`，余同），显示内容为源的对应中间部分。要让可见区落在目标框：反向放大 rect（`width = 目标宽/(1−cropL−cropR)`），再按可见区反推 left/top。
- **keepAspectRatio 校验层与渲染层语义不一致**：校验按「crop 后源比例 vs 框比例」拦截，渲染按上一条执行。绕过法 = 两步提交：先「rect+清 crop」（框比例≈源比例可过），再单独补 crop。禁止改框保留旧 crop（二次裁切事故，红线已列）。
- **编辑器预览（WebGL）与云端渲染对同一份数据可能给出不同画面**（crop 解释差异实证）。**成片以云端渲染帧（`view_timeline_frames`，renderedBy=cloud）为准**；用户在编辑器看到错位时，先渲染同帧云端对照再定性，并提醒刷新编辑器（旧几何有缓存）。
- **borderRadius 作用于裁后可见区**（非 rect 外框）。正圆判定沿用红线公式。

## 窗口动画（ChatCut 专属实现档）

- **MG 媒体槽失效**：`create_motion_graphic_from_code` 的 `video`/`image` 属性，资产引用对象与裸 assetId 两种格式均可存储，但运行时一律解析为空字符串（画面内打印 `item.props` 实证）。**过渡四档链第 2/3 档（JSX 实时媒体 MG / 接缝定帧 MG）在 ChatCut 当前版本直接跳过**，不再探针。
- **正解 = 满屏 item + 窗口 reframe shader**（与三层合成契约「不把 item 缩成 PiP」一致）：
  - `submit_shader` 生成 effect：参数 = 起/止窗口矩形+圆角（归一化，radius 基于画布高）、起/止源子矩形（归一化 UV）、feather；进度 = effect 覆盖区间内 0→1，ease-in-out cubic；窗外输出真透明。start=end 即静态稳定态窗。
  - 挂载：`mode:"track-bound"` + trackId + trackBoundFrom/Duration，**per-item 挂载，不跨 item 缝**（每个稳定段内逐 item 一个 FX；过渡 FX 单独约 12 帧）。
  - 过渡窗口默认放前段尾部约 12 帧（句前气口提前启动、关键句落稳）；纯录屏态→人物态的人物侧例外放后段头部（前段人物 opacity=0 不可见）。全屏态↔窗口态过渡：全屏端窗 = 全画幅 `(0,0,1,1,r0)` + 全幅源。
  - 圆窗参数换算示例（1080p）：可见圆 330px@(1470,528) → win(0.765625, 0.488889, 0.171875, 0.305556) r0.152778；源子矩形 = 旧 crop 区间（如 x0.218058 w0.562181）。数值属实测起点示例，按你的版式坐标重算。
- **框线与过渡的所有权**：框线 item 区间 = 稳定段区间抠掉段尾过渡窗口；过渡窗口内框线不在场（单一 owner），新段起点由入场动画（drawFrames）衔接。
- **shader 生成为 beta**：提交前按官方要求向用户提示并取得确认；生成后第一验证点 = 时间进度是否生效（渲染过渡中点帧）。

## S 态（纯录屏全屏）实现

- 窗口 shader 的收拢过渡把 endWin 尺寸设为极小值（如 0.0001）收到人物窗圆心，即「人物退场」观感。
- S 段的人物 item 先 `split_item` 造缝，再 opacity=0（音频 anchor 不断，人物仍唯一可听）。
- S 态进出的缝一律由 split 落在气口上，不在句中切。

## 字幕（ChatCut 分页引擎机器路径）

字幕文本真相源与词表刀法见 `captions-terminology.md`（权威位）；本节只记录 ChatCut 引擎的实测行为。

- **分页引擎默认按长度预算硬切**（break=length），会拆词断短语。这个预算只能当宿主约束，不能反过来充当语义分段器。按气口分卡的机器路径：
  1. `read_captions {json:{words:true}}` 拿词级 key（全片输出可能超限——落文件后 jq/python 提取；`frame` 参数实测无效，始终返回全片）。
  2. 先在宿主外完成「完整语义事件 → 阅读时长 → 像素宽度」分页；固定字符数不得产生断点。
  3. `edit_captions {action:"display_text", json:{overrides:[{key, forcePageBreak:true}]}}` 只在已审计的语义事件起点打强制分页。
  4. 让宿主承担同一语义事件内部的一至两行排版；若宿主仍插入 `break=length` 并产生新的时间事件，回到最近合法句法边界重分，禁止截断第 N 个字。
  5. 回读全片 `break` 原因；残留 `break=length` 必须逐处判断：若只是同一事件的视觉换行可保留，若导致新的出现/消失或拆开短语则失败，并复查用户 canary。
  6. `{key, hidden:true}` 隐藏 ASR 多转词；`{key, text}` 做词文本覆盖（低自由度规则见 `captions-terminology.md`）。
- **ChatCut 当前把“视觉行宽”和“时间卡容量”耦合在同一个 `maxCharactersPerLine` 上**：实测降低该值会把同一语义事件拆成先后出现的多张卡，提高该值又会把本应两行的长事件拉成一条过长单行；单独缩小 `layout.width` 时，云端字幕背景仍可能按文字内容自动扩张，不能保证视觉换行。因而不存在可跨项目照抄的固定字符数：必须先固定语义事件，再在代表长句上标定 `maxLines` / `maxCharactersPerLine`，同时回读时间卡和抽帧看真实行数。
- **`keepWithPrevious` 对短词槽断层可能失效**：AI Hero 案例中，同一源 item 内只相隔 1–7 帧的相邻词已显示 `merge-prev`，渲染器仍生成两张时间卡并标 `break=length`；把容量从 26 提到 36 也不改变结果。连续三轮无效后应记录 host canary 并停手，禁止用整句 display override 转移到单个短词 key 伪造合并。
- **源 item 边界（sourceStart 跳变处）的分页行为不稳定**：一次会话实测引擎自动强分页（跨缝句子无法合并），另一次实测可跨缝合页——按当次回读为准，跨缝合页必须显式验证，不合并时在缝前词打显式断点兜底。`split_item` 出来的连续两段始终可跨（源连续）。
- **hidden 词槽会阻断跨槽合页**：被 `{key,hidden:true}` 隐藏的词仍占分页槽位，其前后两页无法合并。需要合页时改用 un-hide + 文本覆盖方案绕开，或接受该处分页。
- **split_item 会更换 item id**：其名下词 key 前缀随之变化——`text`/`hidden` override 幸存，但 `forcePageBreak` 需按新前缀重设。**纪律 = 结构性 split 先做完，再设字幕断点。**
- 字幕字体必须 `search_fonts` 命中（Google Fonts 或项目自定义字体，如得意黑 = `Smiley Sans (custom)` 需已在项目字体库）。样式修改：`edit_captions` `action:"style"` + **`json` 参数**（`style`/平铺字段无效，报 "No style changes specified"）。

## 音频层基线

- audio item 省略 trackId 时自动建 A1（复用 compatible 轨）；显式给新 alias（如 `"A2"`）强制建新轨。
- library 音效直接用 `library:sound:<id>` 作 assetId。
- 实测起点音量：过渡 whoosh 约 `-12dB`、卡点重音约 `-10dB`、BGM（`submit_music` 生成 60s 循环铺底）约 `-24dB`；音量不夺讲解人 anchor。**听感必须标 `unverified` 交用户耳测**——参数正确不算通过。

## 外部 MG 章节卡链路（hyperframes 类工具）

静态章节卡枯燥时可走外部 motion-graphics 工具（如 hyperframes 的 kinetic-type workflow）产 MP4 再导入：

- 对比度门（WCAG 大字 3:1）会拦文字色，需调深（实测例：`#14B8A6` → `#0D9488`）。
- root 的 `data-duration` 锁死总帧数，改时长先改它。
- 渲染完成后 `import_media` 进 ChatCut，按普通素材摆放；MG 内音频保持静音，anchor 不变。

## 隐私扫描 SOP（源头规避优先）

1. 全源每 30s 抽帧拼 contact sheet（ffmpeg tile），人眼定位二维码/敏感窗口；危险区每 5–20s 精扫定边界。
2. 用 `find_transcript` 搜关键句锚定各段源时刻，再对撞码风险段逐 item 读 `sourceStartFromInSeconds`，求「段源区间 ∩ 敏感窗口」。**插叙段必查**——A-roll 跨插的句子源时刻可能远离本幕主体（实证：某片幕 1 的插叙句源时刻位于片尾二维码区）。
3. 命中处置：**观点段录屏镜像 sourceStart 平移到最近的语义贴合静止无码页**（演示段才要求同刻，观点段录屏是氛围证据）；无法平移才用独立不透明 redaction 层遮挡。平移后渲染复验。
4. 全量审计仍逐段渲染兜底——扫描阶段的遗漏以渲染帧为最后防线。

## 工具面杂项

- `apply_script` 结果可超限：落文件用 jq 提取 timelineMd/libraryDocs。转写段号 ≠ 文件行号，全量核对后再用。
- MG item 不支持 `playbackRate`（报错）；MG 资产时长动画用 `useVideoConfig().durationInFrames` 动态计算，不写死帧号。
- MG per-instance 属性字段名 = `propertyOverrides`；`edit_item` updates 字段 = `id`/`fromFrame`；deletes 元素是 `{id}` 对象。
- `track_progress`：`jobIds` 传裸字符串（数组会被字面化导致 not found）；`wait` 不真阻塞，配后台计时器轮询。
- 大批量 `edit_item` 超时 = 服务端可能仍在执行：等待后回读验证，不盲目重发。
- 宿主几何公式（蒙版原点/radius 语义/override 模式/lane 顺序/导出帧域）仅在 `templates/compatibility.template.json` 对应探针通过后使用；效果 lane 顺序陷阱与 fx-mask 坐标细则见 `face-reframe.md`（该处为权威位）。

## 双端预览（验收播放路由）

用户验收播放优先级（SKILL.md 验收节引用本节，此处为权威位）：

1. **本地 ChatCut Mac 客户端**（探测 `/Applications/ChatCut.app`，`open -a ChatCut` 可拉起）：引导用户在 App 中打开同一项目并跳到目标时间码验收——与代理进程独立，互不拖累。
2. 未安装时**提示一次**可从 chatcut.io 官网下载客户端（可选，不强推）。
3. 兜底 = 系统默认浏览器打开 `get_editor_url`（明示网页端可能卡顿，重画面验收建议装客户端）。

代理侧验证不受此影响：云端渲染帧始终是代理的像素证据源。
