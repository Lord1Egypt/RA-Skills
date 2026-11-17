/* Shared by Node tests and the self-contained browser artifact. */
(function (scope) {
  'use strict';
  const library = typeof module !== 'undefined' ? require('./library.cjs') : scope.StyleLibrary;
  const hierarchy = typeof module !== 'undefined' ? require('./hierarchy.cjs') : scope.MindmapHierarchy;
  const layouts = [
    { id: 'balanced', name: '左右展开', english: 'Balanced mind map', purpose: '围绕一个主题，建立全局认知', relation: '主题 → 关联分支' },
    { id: 'right', name: '向右展开', english: 'Right-facing logic tree', purpose: '沿阅读方向，逐层梳理长内容', relation: '主题 → 子主题' },
    { id: 'down', name: '向下层级', english: 'Top-down hierarchy', purpose: '清晰表达分类、职责与层级', relation: '上位 → 下位' },
    { id: 'brace', name: '括号分解', english: 'Brace / part–whole map', purpose: '拆解系统，辨认整体与组成部分', relation: '整体 → 组成部分' },
    { id: 'outline', name: '缩进大纲', english: 'Indented outline', purpose: '沿缩进逐行阅读，适合长内容与深层知识', relation: '父主题 → 子主题' }
  ].map(l=>({...l,...library.axes.L.items.find(item=>item.id===l.id)}));
  // Legacy names are import aliases; visual properties live only in the unified catalogue.
  const themes = Object.entries(library.legacy).map(([id,preset])=>({id,preset,name:library.presets.find(p=>p.id===preset).name}));

  function parseMindmap(markdown) {
    if (typeof markdown !== 'string' || markdown.length > 120000) throw new Error('请输入不超过 120,000 字符的 Markdown。');
    const fences = [...markdown.matchAll(/^```mermaid\s*\r?\n([\s\S]*?)^```\s*$/gm)];
    if (fences.length !== 1) throw new Error('需要恰好一个 mermaid 代码块。');
    const raw = fences[0][1].split(/\r?\n/).filter(line => line.trim() && !line.trim().startsWith('%% '));
    if (!raw.length || raw.shift().trim() !== 'mindmap') throw new Error('代码块第一行必须是 mindmap。');
    let root = null;
    const stack = [];
    let count = 0;
    raw.forEach((line, i) => {
      if (line.includes('\t')) throw new Error(`第 ${i + 2} 行：请用空格缩进，不使用 Tab。`);
      const indent = line.length - line.trimStart().length;
      let text = line.trim();
      if (/^(?:%%|::|---)/.test(text)) throw new Error('此样例仅支持节点文字、缩进和常见节点外形，不支持指令、图标或样式类。');
      const shaped = text.match(/^([\w-]+)(?:\(\((.*)\)\)|\((.*)\)|\[(.*)\])$/u);
      if (shaped) text = shaped[2] ?? shaped[3] ?? shaped[4];
      if (/^mindbox_\d+\[/.test(line.trim())&&shaped) {
        try {text=JSON.parse(text);}catch{throw new Error('节点的文字编码无效。');}
        if(typeof text!=='string'||/[\x00-\x1f]/.test(text))throw new Error('节点文字不能含换行或控制字符。');
      }else if (text.startsWith('"') && text.endsWith('"')) text = text.slice(1, -1);
      if (!text || text.length > 500) throw new Error(`第 ${i + 2} 行：节点文字需为 1–500 个字符。`);
      while (stack.length && stack[stack.length - 1].indent >= indent) stack.pop();
      if (root && !stack.length) throw new Error('只能有一个根节点，其他节点需要缩进。');
      if (stack.length > 20) throw new Error('最多支持 20 层子节点，请拆分较深的导图。');
      const node = { id: `n${count++}`, text, depth: stack.length, children: [], branch: 0 };
      if (!root) root = node;
      else {
        const parent = stack[stack.length - 1].node;
        node.branch = parent === root ? root.children.length : parent.branch;
        parent.children.push(node);
      }
      stack.push({ indent, node });
    });
    if (!root) throw new Error('请至少添加一个根节点。');
    return root;
  }

  function wrapText(text, limit = 15) {
    const lines = [];
    let part = '', width = 0;
    for (const char of text) {
      const size = /[\x00-\x7F]/.test(char) ? 0.56 : 1;
      if (width + size > limit && part) { lines.push(part); part = ''; width = 0; }
      part += char; width += size;
    }
    if (part) lines.push(part);
    return lines;
  }

  function layoutTree(root, layoutId, collapsed = new Set(), maxDepth = Infinity, density = {rowGap:18,colGap:85}) {
    if (!layouts.some(l => l.id === layoutId)) throw new Error('未知布局');
    const nodes = [], edges = [];
    const getChildren = n => collapsed.has(n.id) || n.depth >= maxDepth ? [] : n.children;
    function measure(n) {
      const lines = wrapText(n.text, n.depth === 0 ? 12 : 15);
      const m=hierarchy.metrics(n.depth),fontSize=m.fontSize;
      const width = Math.max(n.depth === 0 ? (density.rootMinWidth||190) : (density.nodeMinWidth||112)*m.scale, Math.min(n.depth === 0 ? 300 : 285, Math.max(...lines.map(s => [...s].reduce((v, c) => v + (/[\x00-\x7F]/.test(c) ? fontSize * .58 : fontSize), 0))) + m.paddingX));
      return { ...n, lines, fontSize,lineHeight:m.lineHeight,w: width, h: Math.max(n.depth === 0 ? (density.rootMinHeight||58) : (density.nodeMinHeight||38)*m.scale, lines.length * m.lineHeight + (n.depth===0?(density.rootPadding||24):m.paddingY)), x: 0, y: 0 };
    }
    const dimensions = new Map();
    function size(n) {
      const v = measure(n); dimensions.set(n.id, v);
      const kids = getChildren(n);
      kids.forEach(size);
      v.span = layoutId === 'down'
        ? Math.max(v.w, kids.reduce((s, c) => s + dimensions.get(c.id).span, 0) + Math.max(0, kids.length - 1) * (density.rowGap+12))
        : Math.max(v.h + density.rowGap, kids.reduce((s, c) => s + dimensions.get(c.id).span, 0));
      return v;
    }
    const r = size(root);
    // Column width is shared across each depth so long labels cannot cross the next column.
    const cols = [];
    dimensions.forEach(n => { cols[n.depth] = Math.max(cols[n.depth] || 0, layoutId === 'down' ? n.h : n.w); });
    const offsets = [0];
    for (let i = 1; i < cols.length; i++) offsets[i] = offsets[i - 1] + cols[i - 1] / 2 + cols[i] / 2 + (layoutId === 'down' ? density.colGap*.85 : density.colGap);
    function place(n, center, direction = 1) {
      const v = dimensions.get(n.id);
      if (layoutId === 'down') { v.x = center; v.y = offsets[n.depth]; }
      else { v.x = direction * offsets[n.depth]; v.y = center; }
      v.direction = direction;
      nodes.push(v);
      const kids = getChildren(n);
      let cursor = center - kids.reduce((s, c) => s + dimensions.get(c.id).span, 0) / 2;
      if (layoutId === 'down') cursor -= Math.max(0, kids.length - 1) * (density.rowGap+12)/2;
      kids.forEach(child => {
        const span = dimensions.get(child.id).span;
        edges.push({ from: n.id, to: child.id, branch: child.branch });
        place(child, cursor + span / 2, direction);
        cursor += span + (layoutId === 'down' ? density.rowGap+12 : 0);
      });
    }
    if (layoutId === 'balanced') {
      r.x = 0; r.y = 0; r.direction = 1; nodes.push(r);
      const sides = [[], []], weights = [0, 0];
      getChildren(root).forEach(child => {
        const side = weights[0] <= weights[1] ? 0 : 1;
        sides[side].push(child); weights[side] += dimensions.get(child.id).span;
      });
      sides.forEach((kids, side) => {
        let y = -kids.reduce((s, c) => s + dimensions.get(c.id).span, 0) / 2;
        kids.forEach(child => {
          const span = dimensions.get(child.id).span;
          edges.push({ from: root.id, to: child.id, branch: child.branch });
          place(child, y + span / 2, side ? -1 : 1); y += span;
        });
      });
    } else if (layoutId === 'outline') {
      let cursor = 0;
      const walk = n => {
        const v=dimensions.get(n.id);
        if(n.depth===1)cursor+=density.sectionGap||0;
        v.x=n.depth*(density.colGap*.65)+v.w/2;v.y=cursor+v.h/2;v.direction=1;
        nodes.push(v);cursor+=v.h+density.rowGap;
        getChildren(n).forEach(child=>{edges.push({from:n.id,to:child.id,branch:child.branch});walk(child);});
      };
      walk(root);
    } else place(root, 0);
    const x1 = Math.min(...nodes.map(n => n.x - n.w / 2)) - 48;
    const y1 = Math.min(...nodes.map(n => n.y - n.h / 2)) - 48;
    const x2 = Math.max(...nodes.map(n => n.x + n.w / 2)) + 48;
    const y2 = Math.max(...nodes.map(n => n.y + n.h / 2)) + 48;
    return { layout:layoutId, nodes, edges, bounds: { x: x1, y: y1, w: x2 - x1, h: y2 - y1 } };
  }
  function descendants(n) { return n.children.reduce((s, c) => s + 1 + descendants(c), 0); }
  function parseOptions(markdown) {
    const front = markdown.match(/^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/);
    const options = {};
    if (!front) return options;
    const readField = key => front[1].match(new RegExp('^'+key+':\\s*([^\\r\\n]+)$','m'))?.[1].trim().replace(/^(["'])(.*)\1$/, '$2');
    const recipe = readField('style') || readField('preset');
    if (recipe) return {recipeCode:library.resolveRecipe(recipe).code};
    for (const field of ['layout','theme']) {
      const match = front[1].match(new RegExp('^'+field+':\\s*([^\\r\\n]+)$','m'));
      if (!match) continue;
      const value = match[1].trim().replace(/^(["'])(.*)\1$/, '$2');
      const choices = field === 'layout' ? layouts : themes;
      if (!choices.some(item => item.id === value)) throw new Error(`${field} 不支持 ${value}；可选：${choices.map(item=>item.id).join('、')}。`);
      options[field] = value;
    }
    return options;
  }
  function escapeXML(text) { return String(text).replace(/[&<>"']/g, c => ({ '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;' })[c]); }
  const api = { layouts, themes, library, hierarchy, parseMindmap, parseOptions, layoutTree, wrapText, descendants, escapeXML };
  if (typeof module !== 'undefined') module.exports = api;
  else scope.MindmapKit = api;
})(typeof globalThis !== 'undefined' ? globalThis : this);
