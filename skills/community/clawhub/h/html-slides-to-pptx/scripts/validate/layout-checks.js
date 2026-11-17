// validate/layout-checks.js — 布局检查(Phase 2 新增;浏览器端自包含函数)
// 规则设计约束:对旧 29 页(纯绝对定位写法)零命中 —— 已由 test/survey.js 预扫描证实:
//   嵌套标记 0 处、未标记流式可见元素 0 处、布局容器内重叠倒挂 0 对。
// 2026-08-02 重构 D 期:新增设计检查(对齐离群/子级溢出),design.tier 驱动;
// 2026-08-06 起缺省档即 presentation(默认开启),显式 design.tier:"" 才休眠。
function layoutChecks(arg) {
  const design = (arg && arg.design) || {};
  const tierOn = !!design.tier;
  // 阈值取自 config/default.config.js 的 design.thresholds(唯一事实源,2026-08-06 P2);
  // `?? 默认值` 仅为旧调用方兜底,不是第二份事实源。
  const T = design.thresholds || {};
  const issues = [];
  const OBJ = '[data-object="true"]';
  const container = document.querySelector(".slide-container");
  if (!container) return issues;
  const hidden = (cs) => cs.display === "none" || cs.visibility === "hidden";
  // 只看"自身"可见性:直接文本节点/自身背景(后代已标记时,后代文字不应让容器误报)
  const visibleContent = (el, cs) =>
    cs.backgroundColor !== "rgba(0, 0, 0, 0)" ||
    (cs.backgroundImage && cs.backgroundImage !== "none") ||
    Array.from(el.childNodes).some((n) => n.nodeType === 3 && n.textContent.trim() !== "");
  const isLayoutContainer = (cs) => cs.display.includes("flex") || cs.display.includes("grid");

  // 0) SVG 图标 currentColor 陷阱(2026-08-05 第三轮重构 B0 实测):
  //    截图前页面文字会被 *{color:transparent} 隐藏,stroke/fill=currentColor 随之变透明 →
  //    图标在 PPTX 里空白(浏览器预览正常,极隐蔽)。旧夹具/资产全文无 currentColor(grep 证实),基线零新增。
  document.querySelectorAll(".slide-container svg").forEach((el) => {
    if (/currentColor/i.test(el.outerHTML))
      issues.push({
        level: "WARN",
        msg: "SVG 含 currentColor:转换截图时会被文字隐藏规则变透明,图标将空白",
        fix: "stroke/fill 改显式 hex(或 style=\"stroke:var(--色)\");见 assets/icons.md 铁律",
      });
  });

  // 1) 嵌套 data-object → ERROR(H2:语义不明,提取器只认外层)
  document.querySelectorAll(OBJ).forEach((el) => {
    if (el.parentElement && el.parentElement.closest(OBJ))
      issues.push({
        level: "ERROR",
        msg: `data-object 嵌套:内层标记无效且语义不明: <${el.tagName.toLowerCase()}> "${(el.textContent || "").trim().slice(0, 20)}"`,
        fix: "拆成两个并列的 data-object,或去掉内层标记(外层容器内的子元素本就会按位置逐个提取)",
      });
  });

  // 2) 布局容器(flex/grid)的可见流入子级必须可归结到某个 data-object
  document.querySelectorAll(".slide-container *").forEach((el) => {
    const cs = getComputedStyle(el);
    if (!isLayoutContainer(cs) || hidden(cs)) return;
    Array.from(el.children).forEach((c) => {
      if (c.closest(OBJ)) return; // 自身或祖先已标记 → 会被提取
      const ccs = getComputedStyle(c);
      if (hidden(ccs)) return;
      const r = c.getBoundingClientRect();
      if (r.width < 2 || r.height < 2) return;
      if (visibleContent(c, ccs))
        issues.push({
          level: "ERROR",
          msg: `布局容器(${cs.display})的可见子级未标记 data-object,转换时会被忽略: <${c.tagName.toLowerCase()}> "${(c.textContent || "").trim().slice(0, 20)}"`,
          fix: '给该子级补 data-object="true" data-object-type="textbox|shape",或并入已标记的兄弟元素',
        });
    });
  });

  // 3) 重叠倒挂预警(仅布局容器内的 data-object):PPTX 按 DOM 序叠放,浏览器按 z-index;
  //    两序倒挂且区域重叠时,PPTX 与浏览器视觉分叉(H3)。旧绝对定位页的规则见 html-spec.md。
  document.querySelectorAll(".slide-container *").forEach((parent) => {
    const pcs = getComputedStyle(parent);
    if (!isLayoutContainer(pcs)) return;
    const kids = Array.from(parent.children)
      .filter((c) => c.matches(OBJ))
      .map((c, i) => {
        const z = getComputedStyle(c).zIndex;
        return { el: c, dom: i, z: z === "auto" ? 0 : parseInt(z, 10) || 0, r: c.getBoundingClientRect() };
      });
    for (let i = 0; i < kids.length; i++)
      for (let j = i + 1; j < kids.length; j++) {
        const a = kids[i], b = kids[j];
        const overlap = a.r.left < b.r.right && b.r.left < a.r.right && a.r.top < b.r.bottom && b.r.top < a.r.bottom;
        if (a.z > b.z && overlap)
          issues.push({
            level: "WARN",
            msg: `布局容器内两个 data-object 重叠且 z-index 与 DOM 顺序倒挂,PPTX 叠放(按 DOM 序)将与浏览器不同: "${(b.el.textContent || "").trim().slice(0, 16)}" 会被压到 "${(a.el.textContent || "").trim().slice(0, 16)}" 之下`,
            fix: "调整 DOM 顺序(想压底的放前面),不要再依赖 z-index",
          });
      }
  });

  // 5) 文字对比度(2026-08-06 第四轮 P1;design.tier 驱动,缺省档即开启)
  //    动机:97 页标题曾因 --on-navy-text 未定义回退成近黑压深蓝,PPTX 里整页标题不可见,
  //    而三层 golden 把它当"正确"锁了基线 —— 没有任何检查在看"文字看不看得见"。
  //    口径(经全 44 页实测标定):
  //      · 底色回溯必须穿过 tr/table —— 表格底纹挂在 <tr> 上(H12),td 自身背景是透明的;
  //      · 渐变/图片底色跳过(单色比值无意义,且这类区域走截图路径);
  //      · 字号 ≥120px 的巨型数字是"幽灵水印"设计手法(01/03/21/97 页均为同色系叠压),豁免;
  //      · 纯符号(无字母/数字/汉字)且 ≤2 字符豁免 —— 竖线分隔符、图例色块本就该淡,不是正文;
  //    双档阈值:97 页实测 1.22:1(#1F1F1F 压 #0A2E5C),故 <1.3 判 ERROR(确定不可见),
  //    1.3–1.6 判 WARN(可疑但可能是刻意的弱对比)。豁免后全 44 页命中 0 处,老页基线零 diff。
  if (tierOn) {
    const parseRgb = (s) => {
      const m = /rgba?\(([^)]+)\)/.exec(s || "");
      if (!m) return null;
      const a = m[1].split(",").map((v) => parseFloat(v));
      if (a.length > 3 && a[3] < 0.9) return null; // 半透明:混合结果不可判
      return a.slice(0, 3);
    };
    const relLum = (rgb) => {
      const f = (v) => {
        v /= 255;
        return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
      };
      return 0.2126 * f(rgb[0]) + 0.7152 * f(rgb[1]) + 0.0722 * f(rgb[2]);
    };
    const hasGradient = (cs) => /gradient\(|url\(/.test(cs.backgroundImage || "none");
    const container = document.querySelector(".slide-container");
    document.querySelectorAll(".slide-container *").forEach((el) => {
      const own = Array.from(el.childNodes)
        .filter((n) => n.nodeType === 3)
        .map((n) => n.textContent)
        .join("")
        .trim();
      if (own === "") return;
      // 装饰符号豁免:竖线分隔符 "|"、图例色块 "■" 等本就该淡
      if (own.length <= 2 && !/[\p{L}\p{N}]/u.test(own)) return;
      const cs = getComputedStyle(el);
      if (hidden(cs)) return;
      const fg = parseRgb(cs.color);
      if (!fg) return;
      if (parseFloat(cs.fontSize) >= (T.watermarkFontPx || 120)) return; // 幽灵水印数字
      // 有效底色两条独立线索,取"更近的那层":
      //   ① 祖先链(含 tr/table):表格底纹挂 <tr>,而 elementsFromPoint 不命中 tr(H12 同源)
      //   ② 几何叠压:绝对定位文字压在"兄弟"形状上(chevron/trapezoid 图示页的主力写法),
      //      祖先链看不到它,必须按浏览器绘制序在文字中心做一次命中测试
      // 两者都命中时以"祖先链非画布"优先 —— 祖先背景一定比画布更贴近文字;
      // 命中测试的结果只在祖先链没找到、或祖先链只找到画布本身时才采用。
      // 任一级遇渐变/图片即放弃判定(单色比值无意义,且这类区域走截图路径)。
      let bgAncestor = null, ancestorIsCanvas = false;
      for (let n = el; n && n !== document.documentElement; n = n.parentElement) {
        const ncs = getComputedStyle(n);
        if (hasGradient(ncs)) return;
        const q = parseRgb(ncs.backgroundColor);
        if (q) { bgAncestor = q; ancestorIsCanvas = (n === container || n === document.body); break; }
      }
      let bgOverlap = null;
      const r = el.getBoundingClientRect();
      if (r.width >= 1 && r.height >= 1 && document.elementsFromPoint) {
        const x = Math.min(Math.max(r.left + Math.min(r.width / 2, 20), 1), window.innerWidth - 1);
        const y = Math.min(Math.max(r.top + r.height / 2, 1), window.innerHeight - 1);
        for (const n of document.elementsFromPoint(x, y)) {
          if (n === el || el.contains(n)) continue;
          const ncs = getComputedStyle(n);
          if (hasGradient(ncs)) return;
          const q = parseRgb(ncs.backgroundColor);
          if (q) { bgOverlap = q; break; } // 绘制序最靠前者 = 文字真正压着的底
        }
      }
      const bg = (bgAncestor && !ancestorIsCanvas) ? bgAncestor : (bgOverlap || bgAncestor);
      if (!bg) return;
      const l1 = relLum(fg), l2 = relLum(bg);
      const ratio = (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
      if (ratio < (T.contrastWarn ?? 1.6))
        issues.push({
          level: ratio < (T.contrastError ?? 1.3) ? "ERROR" : "WARN",
          msg: `文字与底色几乎同色(对比度 ${ratio.toFixed(2)}:1),PPTX 里将不可见: "${own.slice(0, 18)}"`,
          fix: "换文字色或底色(深底页用 --on-navy-text/--on-navy-sub);若是刻意的水印效果,放大到 ≥120px",
        });
    });
  }

  // 4) 设计检查(2026-08-02,tier 配置后启用)
  if (tierOn) {
    // 4a) 对齐误差两种:
    //  ① 边缘离群:同父 data-object ≥3 个,某元素 left/top 与主簇(≥2 同值)差 1-6px
    //  ② 等距网格突变:同宽同行的 ≥3 个兄弟,相邻间距偏离中位间距 2-8px(卡片网格 typical 事故)
    const parents = new Set();
    document.querySelectorAll(OBJ).forEach((el) => el.parentElement && parents.add(el.parentElement));
    parents.forEach((p) => {
      const kids = Array.from(p.children).filter((c) => c.matches && c.matches(OBJ));
      if (kids.length < 3) return;
      const rects = kids.map((el) => ({ el, r: el.getBoundingClientRect() }));
      // ① 边缘离群(left/top)
      [["left", (r) => r.left], ["top", (r) => r.top]].forEach(([name, fn]) => {
        const edges = rects.map((e) => ({ el: e.el, v: fn(e.r) }));
        const clusters = [];
        edges.forEach((e) => {
          const c = clusters.find((cl) => Math.abs(cl.v - e.v) <= 0.5);
          if (c) c.items.push(e);
          else clusters.push({ v: e.v, items: [e] });
        });
        clusters.sort((a, b) => b.items.length - a.items.length);
        const main = clusters[0];
        if (!main || main.items.length < 2) return;
        clusters.slice(1).forEach((cl) => {
          const d = Math.abs(cl.v - main.v);
          if (d >= 1 && d <= 6)
            cl.items.forEach((e) =>
              issues.push({
                level: "WARN",
                msg: `元素 ${name} 边 ${Math.round(e.v)}px,与同类 ${Math.round(main.v)}px 差 ${d.toFixed(1)}px,疑似对齐误差: "${(e.el.textContent || "").trim().slice(0, 16)}"`,
                fix: `若非刻意错位,对齐到 ${Math.round(main.v)}px`,
              })
            );
        });
      });
      // ② 等距网格突变(横向行)
      const rows = new Map();
      rects.forEach((e) => {
        const key = `${Math.round(e.r.top)}|${Math.round(e.r.width)}`;
        if (!rows.has(key)) rows.set(key, []);
        rows.get(key).push(e);
      });
      rows.forEach((group) => {
        if (group.length < 3) return;
        group.sort((a, b) => a.r.left - b.r.left);
        const gaps = [];
        for (let i = 1; i < group.length; i++)
          gaps.push(group[i].r.left - (group[i - 1].r.left + group[i - 1].r.width));
        const sorted = gaps.slice().sort((a, b) => a - b);
        const median = sorted[Math.floor(sorted.length / 2)];
        gaps.forEach((g, i) => {
          const dev = g - median;
          if (Math.abs(dev) >= 2 && Math.abs(dev) <= 8)
            issues.push({
              level: "WARN",
              msg: `网格间距异常:第 ${i + 2} 个元素与前一元素间距 ${g.toFixed(1)}px(其余约 ${median.toFixed(1)}px): "${(group[i + 1].el.textContent || "").trim().slice(0, 16)}"`,
              fix: "等距网格请保持间距一致(或改用方式 B/C 由布局引擎均分)",
            });
        });
      });
    });

    // 4b) 子级溢出父对象:data-object 的直接子级矩形超出自身 >4px
    //    只查"自带视觉"的子级(背景/边框/图):纯文本子级的溢出归 dom-checks 文字适配管
    document.querySelectorAll(OBJ).forEach((el) => {
      const pr = el.getBoundingClientRect();
      Array.from(el.children).forEach((c) => {
        const cr = c.getBoundingClientRect();
        if (cr.width < 2 || cr.height < 2) return;
        const ccs = getComputedStyle(c);
        const visual =
          (ccs.backgroundColor && ccs.backgroundColor !== "rgba(0, 0, 0, 0)") ||
          (ccs.backgroundImage && ccs.backgroundImage !== "none") ||
          parseFloat(ccs.borderTopWidth) > 0 || parseFloat(ccs.borderRightWidth) > 0 ||
          parseFloat(ccs.borderBottomWidth) > 0 || parseFloat(ccs.borderLeftWidth) > 0 ||
          ["IMG", "SVG", "CANVAS", "TABLE", "VIDEO"].includes(c.tagName);
        if (!visual) return;
        const over = Math.max(cr.right - pr.right, cr.bottom - pr.bottom, pr.left - cr.left, pr.top - cr.top);
        if (over > 4)
          issues.push({
            level: "WARN",
            msg: `子元素溢出父对象 ${Math.round(over)}px: "${(c.textContent || "").trim().slice(0, 16)}"`,
            fix: "收小子元素宽高/字号,或加大父对象",
          });
      });
    });
  }

  // 6) 非对称 padding 垂直居中陷阱(2026-08-14)
  //    动机:14-four-conditions.html 中心圆 padding-top:64px + padding-bottom:0 推文字下移,
  //    浏览器看着居中,但提取器因非对称 padding 判为多行 top 对齐 → PPTX 文字上偏。
  //    text.js L149-155 的对称性守卫是设计:非对称 padding 在 valign:middle 下无法精确还原。
  //    规则:textbox 的直接子级(文字容器)有非对称垂直 padding(差 ≥4px)且容器有固定高度 → WARN。
  document.querySelectorAll('[data-object="true"][data-object-type="textbox"]').forEach((tb) => {
    const tbCs = getComputedStyle(tb);
    if (hidden(tbCs)) return;
    const tbH = tb.getBoundingClientRect().height;
    if (tbH < 10) return;
    Array.from(tb.children).forEach((c) => {
      const cs = getComputedStyle(c);
      const padT = parseFloat(cs.paddingTop) || 0;
      const padB = parseFloat(cs.paddingBottom) || 0;
      const asymmetry = Math.abs(padT - padB);
      if (asymmetry >= 4)
        issues.push({
          level: "WARN",
          msg: `textbox 子级用非对称 padding 推动垂直位置(上${Math.round(padT)}px/下${Math.round(padB)}px),浏览器有效但 PPTX 会顶对齐: "${(c.textContent || "").trim().slice(0, 20)}"`,
          fix: "改用 flexbox 居中(父级 display:flex;flex-direction:column;justify-content:center)或 line-height=容器高度(单行徽章)",
        });
    });
  });

  // 7) 限定词落地检查(2026-08-06 第六轮 P4)
  //    动机:content-deepening 第一章要求"反向验证通不过的论断降级为观点,标注'我们认为'",
  //    但此前 Step 3.5 六条自查、validate 全部规则、design-principles 都没有承接这一条 ——
  //    降级只存在于措辞层,写完页之后无法核验哪些断言是被降级过的。
  //    机制:该页在 design.hedgePages 里 → 页面内容区必须出现至少一个限定词。
  //    边界:只查"该标的地方标了没有",**不判断内容真伪**(真伪是用户在 Q5 的判断,机器不越位)。
  //    对旧夹具零影响:hedgePages 缺省 [],任何未登记的页不进入本检查。
  if (arg && arg.needsHedge) {
    const words = (design.hedgeWords || []).length
      ? design.hedgeWords
      : ["我们认为", "有待验证", "预估", "初步", "假设", "尚需", "待确认"];
    // 只看内容区文字(页脚/页码不算);备注 template 不参与(它不显示给观众)
    const bodyText = Array.from(container.querySelectorAll("*"))
      .filter((el) => {
        if (el.tagName === "TEMPLATE" || el.closest("template")) return false;
        const cs = getComputedStyle(el);
        if (hidden(cs)) return false;
        const r = el.getBoundingClientRect();
        return r.top < (T.footerZoneTop || 980);
      })
      .map((el) =>
        Array.from(el.childNodes)
          .filter((n) => n.nodeType === 3)
          .map((n) => n.textContent)
          .join("")
      )
      .join(" ");
    if (!words.some((w) => bodyText.includes(w)))
      issues.push({
        level: "WARN",
        msg: `本页在 design.hedgePages 中(承载降级论断),但正文未出现任何限定词:${words.slice(0, 4).join("/")}`,
        fix: "给被降级的断言加限定词(如\"我们认为…\"\"该数据有待验证\");若本页已无降级论断,从 hedgePages 移除",
      });
  }

  return issues;
}

module.exports = { layoutChecks };
