// layout/strategies.js — data-layout 三种策略的几何计算(浏览器端纯函数)
// 每个策略提供:
//   requireContainer: 对容器的要求(width 恒需要;height 仅 columns 需要)
//   readChild(el, errs): 读取并校验子级 data-layout-* 属性,返回 { el, ...几何参数 }
//   layout({ width, height, gap, cols, children }): 返回与子级同序的 [{x,y,w,h}](相对容器)
// 确定性约束:同 DOM + 同属性 → 同结果;不读任何计算样式。
(() => {
  const ns = (window.__htmlSlides = window.__htmlSlides || {});
  ns.layout = ns.layout || {};

  const num = (v) => {
    const m = /^(\d+(?:\.\d+)?)(px)?$/.exec(String(v == null ? "" : v).trim());
    return m ? parseFloat(m[1]) : null;
  };
  const fr = (v) => {
    const m = /^(\d+(?:\.\d+)?)fr$/.exec(String(v == null ? "" : v).trim());
    return m ? parseFloat(m[1]) : null;
  };
  const childLabel = (el) => `<${el.tagName.toLowerCase()}> "${(el.textContent || "").trim().slice(0, 16)}"`;

  ns.layout.strategies = {
    // 纵向堆叠:子级 x=0,w=容器宽,h=data-layout-h,y 累加 gap
    stack: {
      name: "stack",
      needsHeight: false,
      readChild(el, errs) {
        const h = num(el.getAttribute("data-layout-h"));
        if (h == null) errs.push(`stack 子级缺少合法的 data-layout-h(像素数): ${childLabel(el)}`);
        return { el, h: h || 0 };
      },
      layout({ width, gap, children }) {
        let y = 0;
        return children.map((c) => {
          const r = { x: 0, y, w: width, h: c.h };
          y += c.h + gap;
          return r;
        });
      },
    },

    // 横向分栏:子级 y=0,h=容器高,x 累加 gap。
    // 宽语义与浏览器 flex:1 一致:fr 份数分配的是"内容盒"(扣掉 padding+border),
    // 外宽 = 内容宽 + 各自横向 inset;data-layout-w 的像素值指外宽(border-box)。
    columns: {
      name: "columns",
      needsHeight: true,
      readChild(el, errs) {
        const raw = el.getAttribute("data-layout-w");
        if (raw == null) return { el, wFr: 1, wPx: null }; // 缺省 1fr
        const asFr = fr(raw), asPx = num(raw);
        if (asFr != null) return { el, wFr: asFr, wPx: null };
        if (asPx != null) return { el, wFr: 0, wPx: asPx };
        errs.push(`columns 子级 data-layout-w 非法: "${raw}"(应为像素数 "160" 或份数 "2fr"): ${childLabel(el)}`);
        return { el, wFr: 1, wPx: null };
      },
      layout({ width, height, gap, children }) {
        const insets = (el) => {
          const cs = getComputedStyle(el);
          return (
            (parseFloat(cs.paddingLeft) || 0) +
            (parseFloat(cs.paddingRight) || 0) +
            (parseFloat(cs.borderLeftWidth) || 0) +
            (parseFloat(cs.borderRightWidth) || 0)
          );
        };
        const fixed = children.reduce((s, c) => s + (c.wPx || 0), 0);
        const frKids = children.filter((c) => c.wPx == null);
        const insetSum = frKids.reduce((s, c) => s + insets(c.el), 0);
        const frTotal = frKids.reduce((s, c) => s + c.wFr, 0);
        const s0 = frTotal > 0 ? Math.max(0, width - fixed - gap * (children.length - 1) - insetSum) / frTotal : 0;
        let x = 0;
        return children.map((c) => {
          const w = c.wPx != null ? c.wPx : s0 * c.wFr + insets(c.el);
          const r = { x, y: 0, w, h: height };
          x += w + gap;
          return r;
        });
      },
    },

    // 等宽网格:列宽 = (容器宽 - (列数-1)*gap)/列数;行高 = 该行子级 data-layout-h 最大值
    grid: {
      name: "grid",
      needsHeight: false,
      needsCols: true,
      readChild(el, errs) {
        const h = num(el.getAttribute("data-layout-h"));
        if (h == null) errs.push(`grid 子级缺少合法的 data-layout-h(像素数): ${childLabel(el)}`);
        return { el, h: h || 0 };
      },
      layout({ width, gap, cols, children }) {
        const cellW = (width - gap * (cols - 1)) / cols;
        const rowCount = Math.ceil(children.length / cols);
        const rowH = [];
        for (let r = 0; r < rowCount; r++)
          rowH[r] = Math.max(...children.slice(r * cols, (r + 1) * cols).map((c) => c.h));
        const yOf = [];
        let acc = 0;
        for (let r = 0; r < rowCount; r++) {
          yOf[r] = acc;
          acc += rowH[r] + gap;
        }
        return children.map((c, i) => ({
          x: (i % cols) * (cellW + gap),
          y: yOf[Math.floor(i / cols)],
          w: cellW,
          h: c.h,
        }));
      },
    },
  };
})();
