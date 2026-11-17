# 被打回来的图长什么样：症状 → 原因 → 改法 → 对应命令

编辑部退图通常只写一句"figures do not meet our specifications"。下面这张表把这句话翻译成人话。

> 命令一栏里的命令都在仓库根的 `scripts/` 下，用法见 `SKILL.md` 命令表。
> `check` 的 issue code 以 `out/check.json` 实际输出为准，下表给的是常见 code，便于你对照。

## 速查表

| # | 症状 | 一句话原因 | 对应命令 |
|---|---|---|---|
| 1 | 图里字小到看不清（4 pt） | 按大尺寸画完再缩到栏宽，字号跟着缩 | `check` → 改 `font_size_pt` → `render` |
| 2 | 说是 300 dpi，实际不到 | 72 dpi 截图拼进去 / 导出时设错 | `check` → `export --dpi` |
| 3 | 红绿两条线分不出 | 用了默认红绿，没做色盲兜底 | `check` → 换 `palette` → `render` |
| 4 | 图里的字被裁掉一半 | 文本框比文字窄 / 元素出画布 | `check` → `render` |
| 5 | 中文宋体 + 英文 Times 混排 | 两个软件各画一半再拼 | 统一 `font` → `render` |
| 6 | 图注说的和图里画的不是一回事 | 改图没改图注 | `check`（图注一致性）→ 手改图注 |
| 7 | AI 图里文字是乱码 | 扩散模型不会写字 | `concept` 生成后 `render` 补字 |
| 8 | 颜色过饱和/荧光/渐变发光 | 用了屏幕审美配色 | 换 `palette` → `render` |
| 9 | 坐标轴没单位、没 n 值 | 图表默认配置 | `chart` + 改 `figure.json` 的 `data` 段 |
| 10 | 单栏图 120 mm，超栏宽 | 没按期刊栏宽画 | `check --journal X` → `render` |
| 11 | 字体不是期刊接受的 | 用了楷体/Comic Sans/思源宋体标题 | 改 `font` → `render` |
| 12 | Nature 主图交了 PNG/TIFF | 不知道 Nature 主图要矢量 | `export --formats pdf` |
| 13 | 箭头方向反了/AI 图箭头乱 | 生成模型不懂因果方向 | `prompt-library.md` 规避 + `render` 重画 |
| 14 | 面板编号乱、顺序反 | 拼图时没有统一编号 | `render` 面板编号 → `check` |
| 15 | AI 概念图被当成数据图 | 没看图就投出去了 | `check` 报 `AI_IMAGE_AS_DATA_FIGURE` |

---

## 1. 字号 4 pt

- **症状**：PDF 里放大才看得清；打印出来图例像蚂蚁；审稿人写"figure text is illegible"。
- **原因**：按 A4 或双栏 180 mm 画好，投单栏 89 mm 时整张缩了一半，7 pt 变 3.5 pt。字号是**成品尺寸**上的字号，不是画布上的。
- **改法**：先定栏宽（Nature 单栏 89 mm），在这个宽度下排字；`font_size_pt` 取期刊下限以上（Nature 5–7 pt、Elsevier 正文 7 pt、PLOS 8–12 pt）；字放不下就**减字/减节点**，不是缩字号。
- **命令**：`node scripts/fig.mjs check ./fig1 --journal nature` → 改 `figure.json` 的 `font_size_pt` → `render` → 再 `check`。
- **check code**：`FONT_SIZE_BELOW_MIN`

## 2. 300 dpi 不到

- **症状**：曲线有锯齿、文字边缘发毛；期刊系统提示 "resolution too low"。
- **原因**：把屏幕截图（72–96 dpi）拖进画布；或导出时没设 `--dpi`；或用 PPT 复制粘贴（会变成 72 dpi 位图）。
- **改法**：**能矢量就矢量**（SVG/PDF/EPS），一劳永逸；必须位图时按目标尺寸重导，不要"事后把 72 dpi 改标成 300 dpi"（那是骗自己，像素没多）。IEEE 要 >300 dpi、黑白线稿 >600 dpi；Elsevier 线稿 1000 dpi。
- **命令**：`node scripts/fig.mjs check ./fig1 --export` → `node scripts/fig.mjs export ./fig1 --formats png,pdf,tif --dpi 600`。
- **check code**：`DPI_BELOW_MIN`（导出位图时另有 `EXPORTED_PNG_DPI_LOW`）

## 3. 红绿并置

- **症状**：你看着"红=实验组、绿=对照组"很清楚，8% 的男性读者看到两条一样的线；灰度打印后完全重合。
- **原因**：默认调色板（Excel/Matplotlib 老默认）就是红绿；只靠颜色编码。
- **改法**：换色盲安全调色板（`okabe-ito`）；**再加一个通道**：线型（实/虚）、形状（方/圆/三角）、直接在线端标名字；灰度打印自检。
- **命令**：`check`（报红绿风险）→ 改 `figure.json` 的 `palette: "okabe-ito"` → `render` → `check` 复验。
- **check code**：`COLORBLIND_RED_GREEN`（红绿同图且无色盲兜底即报；另有 `COLORBLIND_LOW_LUMA_DIFF`）

## 4. 文字被裁 / 溢出

- **症状**：节点里的字跑出框外；图右侧的字被画布边缘切掉；图例压住曲线。
- **原因**：文字比框宽；画布尺寸按内容算小了；多面板拼图时坐标算错。
- **改法**：缩短 `label`，把细节放进 `sub`；加大 `layout.node_w_mm` / `gap_mm`；给画布留边（PLOS 建议四周 2 pt 白边）；长句拆成两行。
- **命令**：`check`（文字估算溢出 + 元素出画布）→ 改 `figure.json` → `render`。
- **check code**：`TEXT_OVERFLOW_PARENT`（字比框宽）/ `TEXT_OVERFLOW_CANVAS`（字出画布）/ `ELEMENT_OUT_OF_CANVAS`（整块元素跑出画布）

## 5. 中英混排

- **症状**：图里中文是宋体、英文是 Times，一行里两种字形气质；括号、单位、数字宽度不一。
- **原因**：不同软件各画一半再拼；或直接用了 PPT 默认（中文等线 + 英文 Calibri）。
- **改法**：**一张图一套字体策略**：Latin 用 Arial/Helvetica，中文用无衬线黑体系（思源黑体/微软雅黑）；数字与单位统一用 Latin 字体；全图字号只有 2–3 档（标题/正文/注释）。
- **命令**：`figure.json` 的 `font` 统一后 `render`；`check --journal X` 验字体是否在期刊接受列表。
- **check code**：`FONT_DECORATIVE`（装饰字体）/ `FONT_NOT_ACCEPTED`（期刊不接受）/ `CJK_FONT_MISSING`（中文没字形回退）

## 6. 图注与图不符

- **症状**：图注写"红色为对照组"，图里红色是实验组；图注说 (a)(b)(c)，图里只有 (a)(b)；图注写 n=3，图里误差棒是 n=5。
- **原因**：改图改了颜色/删了面板，忘了回头改图注；或图注是合作者写的，没人对过。
- **改法**：**逐项对表**：颜色 → 符号 → 面板编号 → 单位 → 统计方法 → n 值 → 缩写定义；图注第一句给结论，后面才是细节；缩写在图注里定义一次。
- **命令**：`check`（图注一致性检查项）→ 手改 `figure.json` 的 `caption` 与正文图注。
- **check code**：目前 `check` 不比对图注文字内容（图注是自然语言，确定性检查判不了）；这一项由 `review` 的信息维度扣分，见 `review-rubric.md`

## 7. AI 图文字乱码

- **症状**：图上写着 `Sclentlst`、`Resuit`、`Tab1e 2`；中文变成方块或臆造字。
- **原因**：扩散模型没有文字渲染能力，多小的模型都一样。
- **改法**：生成时就写 `no text, no letters, no words`；把标签位置留白；后期用矢量软件或本技能的 `render` 排字。中文/数字/化学式**一律不让 AI 画**。
- **命令**：`concept`（提示词见 `prompt-library.md`）→ `render` 补字 → `check`。
- **check code**：AI 产物固定带 `*.ai-generated.json`，`check` 会据此提示

## 8. 颜色过饱和 / 荧光 / 渐变发光

- **症状**：屏幕上很酷，印出来一片脏灰；同色系深浅差 3% 在纸上完全看不出。
- **原因**：RGB 屏幕审美 + 深色背景 + 霓虹渐变；没考虑印刷色域。
- **改法**：白底、低饱和、色相不超过 4 个；用明度差而不是纯色相差区分；避免纯 `#FF0000`/`#00FF00`；需要强调时用**加粗/加框**而不是加饱和。
- **命令**：`figure.json` 的 `palette` 换 `nature-cool` / `grayscale-safe` → `render`。
- **check code**：`TOO_MANY_COLORS`（颜色太多无语义）/ `COLORBLIND_RED_GREEN`

## 9. 坐标轴无单位

- **症状**：y 轴只写 `Accuracy`、`Loss`、`Time`；误差棒没有定义；x 轴类别顺序随机。
- **原因**：图表是默认模板直接出的，没写轴标题和量纲。
- **改法**：轴标题 = 物理量 + 单位（`Accuracy (%)`、`Latency (ms)`、`Time (s)`）；误差棒在图注写 SD/SEM 及 n；类别按语义排序（不是字母序）；必要时注明对数轴。
- **命令**：改 `figure.json` 的 `data.xlabel` / `data.ylabel` / `data.error` → `chart`。
- **check code**：这一项属信息维度，`check` 不报；由 `review` 扣分（见 `review-rubric.md` 信息 40 分档）

## 10. 尺寸超栏宽 / 超高度

- **症状**：单栏图 120 mm；整页图 200 mm 高被要求缩到 170 mm，字全糊。
- **原因**：按"看着好看"定尺寸，没按期刊栏宽。
- **改法**：先查 `references/journal-specs.md` 对应一行（Nature 89/183、高度 ≤170 mm；Elsevier 90/140/190；IEEE 88.9/182），再按这个宽度排版。
- **命令**：`check --journal nature`（报 `WIDTH_OVER` / `HEIGHT_OVER`）→ 改 `width` / `height_mm` → `render`。
- **check code**：`FIG_WIDTH_TOO_WIDE` / `FIG_WIDTH_TOO_NARROW` / `FIG_HEIGHT_TOO_TALL`

## 11. 字体不在期刊接受列表

- **症状**：用了楷体、宋体标题、Comic Sans、或某种手写体；EPS 里字体没嵌入，编辑部打开是别的字体。
- **原因**：中文字体默认宋体；EPS 未嵌入字体；转曲没做。
- **改法**：Latin 用 Arial/Helvetica（Nature 明示），PLOS 只接受 Arial/Times/Symbol；EPS/PDF 必须嵌字体或转曲。
- **命令**：`check`（字体校验）→ 改 `font` → `render` → `export`。
- **check code**：`FONT_NOT_ACCEPTED` / `FONT_DECORATIVE`

## 12. 格式交错了

- **症状**：Nature 主图交了 PNG；PLOS 交了 PDF；ACM 交了 Word 里画的流程图。
- **原因**：不知道各刊格式差异（Nature 主图**不收** jpeg/tiff/png；PLOS 只收 TIFF/EPS；IEEE 偏好 PS/EPS/PDF；ACM 收 SVG/PS/EPS/PDF/PNG/JPG/EMF/TIFF 但**不收 Word 图形对象**）。
- **改法**：查 `journal-specs.md` 对应行的"格式"一栏，按栏导出。
- **命令**：`export ./fig1 --formats pdf`（矢量优先）或 `--formats tif --dpi 300`（PLOS）。
- **check code**：`check` 不比对导出格式；`export` 输出后按 `journal-specs.md` 的“格式”一栏手工核

## 13. 箭头方向反 / 箭头成团

- **症状**：A→B 画成 B→A；一条线上两端都有箭头；三条箭头汇进一个框但有一条是反的。
- **原因**：AI 生成图不懂因果；手工画时复制箭头忘了翻转；`edges` 的 `from`/`to` 写反。
- **改法**：AI 图不让它画箭头（`no arrows`），用 `render` 的 `edges` 补；每条 `edge` 检查 `from`/`to`；箭头含义（数据流 vs 控制流）用线型区分并在图例说明。
- **命令**：改 `figure.json` 的 `edges` → `render`。
- **check code**：属信息维度，`review` 扣分

## 14. 面板编号与顺序

- **症状**：(a)(b)(c) 缺一个、顺序和正文引用不一致、大小写混用。
- **原因**：拼图时手工加字母，删面板忘了重排。
- **改法**：面板编号统一在 `panels[].id` 里，按阅读顺序排列（左→右、上→下）；正文引用顺序与之一致。
- **命令**：改 `figure.json` 的 `panels` → `render` → `check`。
- **check code**：`check` 不查面板顺序；由 `review` 判（属信息/视觉维度）

## 15. AI 概念图被当成数据图

- **症状**：图上有柱子/曲线/百分比，但数字是编的；图注写着"结果如图所示"。
- **原因**：把 `concept` 的产物直接拖进正文，当作结果图。
- **改法**：**这条没有"改法"，只有"删掉"**：AI 图只能做概念示意/封面/TOC；数据图必须由真数据经 `chart` 画出；保留 `*.ai-generated.json` 并在方法或致谢中按期刊要求声明。
- **命令**：`check` 会直接报 error；`chart ./fig1` 用真 CSV 重画。
- **check code**：`AI_IMAGE_AS_DATA_FIGURE`（error，直接阻断）；未打标 `AI_IMAGE_UNMARKED`、标记缺字段 `AI_MARKER_INCOMPLETE`、嵌入矢量 `AI_IMAGE_EMBEDDED_IN_VECTOR`、图注缺 AI 声明 `AI_CAPTION_MISSING_DISCLOSURE`

---

## 报错之后的标准动作

1. **看 `check.json` 的 `issues`**：每条都有 `level`（error/warn）、`code`、`message`、`fix`。
2. **先修 error，再看 warn**：error 会挡投稿，warn 只是更专业。
3. **一次只改一类**：改字号就只改字号，别同时换配色，否则下一次 `check` 你不知道是哪步修好的。
4. **改完重跑 `check`（免费）**，确认对应 code 消失。
5. **还是不知道差在哪**：`review` 一次（¥0.01–0.07），按 `review-rubric.md` 的格式拿修改清单。
