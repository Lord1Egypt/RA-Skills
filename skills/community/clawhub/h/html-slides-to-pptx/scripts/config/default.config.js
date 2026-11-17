// default.config.js — 转换器全部可调项(唯一事实源)
// 冻结对象;项目级覆盖见 config/merge.js 与 convert.js 的 slides.config.json 加载。
// ⚠️ 任何默认值改动都会改变 29 页黄金基线的 L2 输出 —— 改默认值前必须先跑 golden verify 确认影响。
const config = {
  // 画布与版面:1920×1080 px ↔ 13.333×7.5 in(16:9)
  canvas: { width: 1920, height: 1080 },
  slide: { widthIn: 13.333, heightIn: 7.5 },
  layout: { name: "W16x9" },
  viewport: { width: 1920, height: 1080 },
  settleMs: 200, // 页面加载后等待字体/CSS 稳定的时间

  // 浏览器端提取参数(序列化传入页面)
  extract: {
    boldThreshold: 600,       // font-weight ≥ 此值 → PPTX 粗体
    singleLineFactor: 1.3,    // 盒高 ≤ 行高×此系数 → 判定单行
    defaultColorHex: "1A1A1A", // 取不到文字颜色时的兜底色
    // Phase 2 加固(测绘证实对旧 29 页零影响,默认开启):
    gridBlockifiesChildren: true, // H4:grid item 与 flex item 一样块级化递归,不拍平
    guardNestedObjects: true,     // H2:嵌套 data-object 的内层不重复提取(由外层 walk 到达)
  },

  // 截图还原(红线③:截图前隐藏文字,避免重影)
  // 隐藏全部文字,而非仅 textbox:方式 B/C 下文字可作为 shape 对象的子元素存在,
  // 任何可见文字都会被提取为原生文本框,因此截图里不应保留任何文字
  capture: {
    hideTextCss: "*{color:transparent !important; text-shadow:none !important;}",
    // 截图分辨率倍数(2026-07-27 起 2x ≈ 288dpi,投影/打印不糊):
    // 浏览器 deviceScaleFactor;clip 仍按 CSS px,贴回尺寸不变,仅位图像素密度提升。
    // 改回 1 可恢复旧行为;此开关改变 L2 内嵌图数据(基线已于当日重建)。
    scale: 2,
    // 截图格式(2026-07-27 P1):'png'(默认,矢量/文字边缘锐利) | 'jpeg'(照片型背景体积降 5-10×)
    imageType: "png",
    quality: 80, // 仅 imageType:'jpeg' 生效(0-100)
  },

  // 原生线性渐变(2026-07-27 D2 拍板):默认关。
  // 开启时(预计 P2 实施):extract 检测 linear-gradient → 渲染端 XML 后处理注入 a:gradFill,
  // 产出可编辑原生渐变形状(覆盖渐变条/渐变卡片高频场景);色停含透明度/hint 超集时回退截图。
  // 关闭时:渐变走 capture 截图路径(2x DPI),观感达标但不可编辑。
  // radial/conic-gradient 恒走截图,与本开关无关。
  nativeGradient: false,

  // P2 2.1 母版(2026-07-27):defineSlideMaster 承接重复页眉/页脚/页码。
  // 页码:每页右下角显示页码(仅当页数 > 1 时有意义)
  // 页脚:每页底部居中文字(如公司名/保密声明)
  // 页脚色:页脚文字颜色(默认灰色)
  // 开关关(false)时不创建母版,每页独立(旧行为)
  master: {
    pageNumbers: false,
    footer: "",
    footerColor: "999999",
  },

  // P2 2.8:增量缓存(默认开)。基于 HTML 内容 hash + config hash 缓存提取+截图结果,
  // 未变化页跳过浏览器交互。缓存目录:slides/.cache/(手动删除即清空)。
  // 设为 false 可关闭(如调试提取管线时)。
  incrementalCache: true,

  // 设计质量检查(2026-08-02 重构 D 期,仅 validate 使用;转换器不读)。
  // tier: "presentation"|"mixed"|"reading";minBodyPx: 字号绝对下限;
  // fillThreshold: 内容区利用率下限(0.85 → 内容带底 ≥ 约 850px);
  // airyPages: 豁免填充检查的 airy 页文件名(封面/分隔/大字观点/引用/收尾);
  // formProfile(2026-08-05 第三轮):视觉形式偏好档 ""/"text"/"balanced"/"rich",
  //   空串或 text = deck 级形式检查休眠(纯文字占比/同形式连排不查);
  //   balanced = 纯文字内容页 ≤50% + 同形式连排 ≤3;rich = ≤30% + ≤2(口径见 design-principles 第五章)。
  //
  // 2026-08-06 第四轮 P2:**默认开启**(此前 tier/formProfile 缺省空串 = 全部检查休眠)。
  // 改因:休眠是"新项目零门槛"设计,但实测代价是新 deck 可以 0 ERROR 通过却小字、单调、
  // 上重下空 —— 最该被检查的正是新写的页。故缺省即 presentation + balanced;
  // 需要休眠的项目(如本仓库的旧夹具页)在项目级 slides.config.json 显式写
  // { "design": { "tier": "", "formProfile": "" } } 退出。
  design: {
    tier: "presentation",
    minBodyPx: 14,
    fillThreshold: 0.85,
    airyPages: [],
    formProfile: "balanced",
    // 语义密度(2026-08-06 第五轮 P1)。动机:此前七道门禁全是几何统计量,
    // 实测可被"两块大色块 + 三行企业黑话"完整满足(0 ERROR/0 WARN),
    // 即门禁在压制"小字堆上半截"的同时,为"大色块 + 空话"开了合法通道。
    // buzzPerK: 一档黑话每千汉字命中率上限(全语料实测最高 11.5,对照空话页 270.8);
    // buzzMin: 绝对命中次数下限 —— 少于此不报(避免长页里偶发一个词就判负);
    // semanticMinCjk: 只对内容区汉字数 ≥ 此值的页做语义判定
    //   (图示型页面的文字是标签,如 113-cycle 仅 52 字,判它"不具体"是误报)。
    buzzPerK: 40,
    buzzMin: 3,
    semanticMinCjk: 80,

    // hedgePages(2026-08-06 第六轮 P4):需要限定词的页面文件名。
    // 来源:content-deepening 第一章的洞察清单里"反向验证=降级"的论断所在页,
    // 或裸主题档用户选"就按假设写"的相关页。
    // 作用:把"降级为观点"从措辞变成可审计的机器约束 —— validate 检查这些页
    // **确实出现了限定词**(我们认为/有待验证/预估/初步/假设),缺失报 WARN。
    // 边界:门禁只查"该标的地方标了没有",**不判断内容真伪**(真伪是用户在 Q5 的判断)。
    // 此前"通不过降级为观点并标注"只写在文档里,Step 3.5 六条自查与 validate 规则
    // 都没有承接 —— 降级只是措辞,事后完全不可审计。
    hedgePages: [],
    hedgeWords: ["我们认为", "有待验证", "预估", "初步", "假设", "尚需", "待确认"],

    // ── 判据阈值表(2026-08-06 第五轮 P2:唯一事实源)──────────────────────
    // 此前这些常数硬编码在 dom-checks.js / layout-checks.js / index.js 里,
    // 同时又各写一份在 design-principles.md、density-tiers.md、SKILL.md 与
    // exemplar-checks.js —— 单个阈值散落 4-8 处,改一处漏一处就产生
    // "文档说 A、代码判 B"的静默分叉。现全部收敛到此处,代码只读不写常量。
    // 改这里的值 = 改产品行为;`test/threshold-parity.js` 会断言文档与本表一致。
    thresholds: {
      // 档内字号下限(px):正文 / 注释。绝对下限另见 minBodyPx
      tierBodyMin: { presentation: 22, mixed: 18, reading: 16 },
      tierNoteMin: { presentation: 16, mixed: 15, reading: 14 },
      bodyMinFallback: 16, // tier 值不在表内时的兜底
      noteMinFallback: 14,
      bodyHeuristicChars: 20, // >此字数的文本才按"正文"判字号下限
      noteZoneTop: 840, // top ≥ 此值且 ≥ 档内注释下限 → 底部注释区豁免
      footerZoneTop: 980, // top ≥ 此值 = 页脚区,不计入内容带

      // 内容区(320-940)与满填四判据
      contentTop: 320,
      contentBottom: 940,
      inkRowMin: 0.55, // 墨迹行覆盖率下限
      maxGapPx: 200, // 内容区内部最大连续空白
      skewMax: 0.88, // 墨迹面积任一半的上限
      inkRowPx: 10, // 分行粒度

      // 字号层级
      titleBodyRatioMin: 1.6, // 页标题/正文比值下限(设计目标 1.8,留一档余量)
      distinctSizesMin: 3, // 页内字号档数下限
      hierarchyMinSamples: 4, // 少于此样本数不判字号档数

      // 结构色面
      colorBlockMinArea: 15000, // 计一块结构色面的最小面积 px²
      colorPctMin: 8, // 无整块时的色面占比兜底下限(%)

      // 文字对比度(layout-checks 规则 5)
      contrastError: 1.3, // <此值 = ERROR(确定不可见)
      contrastWarn: 1.6, // <此值 = WARN(可疑弱对比)
      watermarkFontPx: 120, // ≥此字号视为幽灵水印,豁免对比度

      // deck 级视觉形式(index.js)
      formLimits: {
        balanced: { ratio: 0.5, streak: 3 },
        rich: { ratio: 0.3, streak: 2 },
      },
      formMinPages: 4, // 内容页少于此数不做 deck 级形式判定

      // ── 用色纪律(2026-08-17 第九轮 P3;R1/R2/R3)────────────────────
      // 动机(实测):theme.css 是"约束"但零机器校验 —— 真实 deck 里
      // 34 页 var() 用量 0、裸色声明 1074 处,且所用色板逐值等于**另一套**预设
      // (整套色板被换掉也 0 ERROR 通过)。三条规则把色板从自觉变成可审计约束。
      // 口径:只查 background/color/border-color 的裸色值;<svg> 内豁免
      // (H7 要求图标显式着色,CSS 属性形态的 var() 也算合规)。
      paletteTolerance: 6, // 与色板色的 ΔRGB ≤ 此值视为"同色重打"(仍报,但归因更准)
      offPaletteMax: 3, // 同页去重后色板外色 ≥ 此数 → 升级为"整页脱离色板"
      paletteMinDecls: 4, // 色声明少于此数的页不做 var() 占比判定(样本太小)
      paletteVarPctMin: 70, // var() 占比下限(%);实测样张中位 95、坏 deck 0
      paletteOverlapMin: 3, // deck 级:高频用色与色板的交集下限(低于 = 疑似整套色板未生效)
      paletteTopColors: 8, // deck 级:参与交集判定的高频色**窗口**(不足 8 种时按实有数判)
      // deck 级最小样本:裸色种类少于此数不做 R3 判定 —— 全程用 var() 的 deck 裸色本就极少,
      // 对它算"交集"无意义(0/0)。实测:两个坏 deck 各 21 种,两个好 deck 15/16 种。
      paletteMinDistinct: 5,
    },
  },

  // 图标字体自动截图(2026-07-27 P1):命中下列字体族的文字元素整体转截图,
  // 避免 PPTX 端字体缺失导致 glyph 错字。命中子串即触发(大小写不敏感)。
  iconFonts: ["iconfont", "FontAwesome", "Material Icons", "material-icons", "Material+Icons"],

  // box-shadow 的固定近似(规范已声明为"近似浅阴影")
  shadow: { type: "outer", blur: 6, offset: 3, angle: 90, color: "000000", opacity: 0.25 },

  // 字体映射(2026-07-23 起默认开启,用户决策):中文 → Microsoft YaHei,西文/数字 → Arial。
  // PPTX 受众(Windows/Office)大多没装 Noto Sans SC / Inter,原字体名会随机回退;
  // 需要保留页面原字体名时,在项目级 slides.config.json 设 { "applyFontMap": false }。
  fontMap: {
    "Noto Sans SC": "Microsoft YaHei",
    "Inter": "Arial",
    "PingFang SC": "Microsoft YaHei",
  },
  applyFontMap: true,
};

module.exports = Object.freeze(config);
