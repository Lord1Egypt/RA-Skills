#!/usr/bin/env node
// render.mjs — 橙墨（orangeink）headless 渲染器
// 逻辑基准：orangeink v1.1.0 src/template.html（函数级移植，勿随意改样式逻辑；
// orangeink 升版后须重跑对拍：浏览器版 __tool.copyHTML() vs 本脚本输出，diff 应为 0）
//
// 用法：
//   node render.mjs <input.md> [options]
// 选项：
//   -o, --out <file>       纯净 HTML 片段输出路径（默认 <input>.oimd.html）
//   --copy-page <file>     同时生成「一键复制页」（浏览器打开→点按钮→粘贴公众号）
//   --draft <file>         同时生成公众号 draft/add API 请求体 JSON
//   --title <t>            draft 标题（默认取 H1 或文件名）
//   --author <a>           draft 作者（默认「登叔」）
//   --digest <d>           draft 摘要（默认取首段前 54 字）
//   --theme <name>         orangeink|inkblue|pine|gold|haitang（默认 orangeink）
//   --zoom <n>             字号倍率 0.94|1|1.06（默认 1）
//   --pad <n>              两侧安全边距 px 0|14|22（默认 14）
//   --quiet                仅输出关键结果行
//   --meta <file>          输出元数据 JSON（字数/图片清单/自检结果）
//
// 退出码：0=成功且自检 0 项；1=渲染失败；2=自检有 error 级违规
import { createRequire } from 'module';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { JSDOM } from 'jsdom';

const require_ = createRequire(import.meta.url);
const __dirname = path.dirname(fileURLToPath(import.meta.url));
// markdown-it 为 npm 依赖（package.json 精确锁版本），不经 vendor 打包——
// 避免平台安全审计对 dist 内 Unicode 正则的 obfuscated_code 误报
const markdownit = require_('markdown-it');

/* ===== 排版参数（对齐 template.html BASE/OPT 默认值） ===== */
const BASE = { p:16, h1:22, h2:19, h3:17, h4:16, quote:15, lead:17, code:13.5, cap:13, tab:14 };

/* ===== 主题注册表（对齐 template.html THEMES，2026-09 v1.1.0） ===== */
const THEMES = {
  orangeink: {
    name:'橙墨 · 炭黑×亮橙（默认）',
    C:{
      ORANGE:'#ff5a00', DEEP:'#1c1917', EMBER:'#c94a00', STRONG:'#c93600',
      CHIP:'#d03800', LINK:'#c23a00', BROWN:'#8c5a2b', TAN:'#8a663a',
      TEXT:'#26221c', TEXT2:'#6b6154', TXTQ:'#57503f',
      WARMBG:'#fff3e7', WARMBG2:'#faf0e2', CODEBG:'#ffe9cc', CODE:'#b84300',
      ZEBRA:'#faf6ef', LIST2:'#ff8a3d', BORDER:'#e8e0d2', PTEYE:'#ff9a4d', PTNOTE:'#f3e2ca'
    },
    alerts:{ NOTE:['#fff3e7','#ff5a00'], TIP:['#f9f3ea','#8c5a2b'], IMPORTANT:['#ffeee8','#c93600'],
             WARNING:['#fff5e0','#e08a00'], CAUTION:['#fdeeea','#cf3b2a'] }
  },
  inkblue: {
    name:'墨蓝 × 朱砂',
    C:{
      ORANGE:'#bf3b1e', DEEP:'#1b2430', EMBER:'#2f4d6e', STRONG:'#a83317',
      CHIP:'#bf3b1e', LINK:'#a83317', BROWN:'#44566e', TAN:'#6e5f4b',
      TEXT:'#262a2e', TEXT2:'#5c6670', TXTQ:'#2f4d6e',
      WARMBG:'#f2f4f7', WARMBG2:'#eef1f5', CODEBG:'#e8ecf4',
      ZEBRA:'#f7f9fb', LIST2:'#d96a52', BORDER:'#d9dee6', PTEYE:'#e08a6e', PTNOTE:'#c9d4e4'
    },
    alerts:{ NOTE:['#f7e9e5','#bf3b1e'], TIP:['#eef1f5','#44566e'], IMPORTANT:['#f4e6e1','#a83317'],
             WARNING:['#f6f0e0','#a06300'], CAUTION:['#f6e7e4','#cf3b2a'] }
  },
  pine: {
    name:'松烟 × 陶土',
    C:{
      ORANGE:'#2e6b46', DEEP:'#1d2b20', EMBER:'#3f5d46', STRONG:'#a84e20',
      CHIP:'#2e6b46', LINK:'#a84e20', BROWN:'#4c6b55', TAN:'#77624a',
      TEXT:'#262b26', TEXT2:'#5d665c', TXTQ:'#3f5d46',
      WARMBG:'#eef2ec', WARMBG2:'#e7efe9', CODEBG:'#dfe9e1',
      ZEBRA:'#f6f8f5', LIST2:'#5e9673', BORDER:'#d5ddd6', PTEYE:'#7fb593', PTNOTE:'#d5ddd2'
    },
    alerts:{ NOTE:['#e7efe9','#2e6b46'], TIP:['#eaf0ea','#4c6b55'], IMPORTANT:['#f2e9e2','#a84e20'],
             WARNING:['#f3efe0','#a06300'], CAUTION:['#f3e8e4','#cf3b2a'] }
  },
  gold: {
    name:'石墨 × 鎏金',
    C:{
      ORANGE:'#d9a514', DEEP:'#201d26', EMBER:'#4a3f63', STRONG:'#8a5f0e',
      CHIP:'#8a5f0e', LINK:'#8a5f0e', BROWN:'#7a5a14', TAN:'#7a6a50',
      TEXT:'#26242a', TEXT2:'#6d675c', TXTQ:'#4a3f63',
      WARMBG:'#f6f2e8', WARMBG2:'#f0ead9', CODEBG:'#ede4c8',
      ZEBRA:'#faf7ef', LIST2:'#e3bd4e', BORDER:'#e0d9c6', PTEYE:'#e9c76a', PTNOTE:'#e6ddc4'
    },
    alerts:{ NOTE:['#f3ecdb','#d9a514'], TIP:['#f1edda','#7a5a14'], IMPORTANT:['#f0e8d5','#8a5f0e'],
             WARNING:['#f4efd9','#a06300'], CAUTION:['#f5e6e0','#cf3b2a'] }
  },
  /* 海棠 × 黛蓝（v1.2.7）：小说连载专用主题，首册《九千九百九十九张》（公众号「纸上行舟小说集」）。
     novel 为多书范式注册层：结构规则（novel_structure）读到 novel 才激活。
     AA 注：卡其金 #a58650 只做装饰，卡其系文字一律 BROWN #6b5433（7.2:1）。 */
  haitang: {
    name:'海棠 × 黛蓝（小说 · 九千九百九十九张）',
    C:{
      ORANGE:'#a58650', DEEP:'#274770', EMBER:'#33587d', STRONG:'#9e3b33',
      CHIP:'#7a6140', LINK:'#2f5a85', BROWN:'#6b5433', TAN:'#7d6c4e',
      TEXT:'#2b2a26', TEXT2:'#6d675c', TXTQ:'#33587d',
      WARMBG:'#f7efe6', WARMBG2:'#f3ebe0', CODEBG:'#ece2cf', CODE:'#7a4a1f',
      ZEBRA:'#f8f4eb', LIST2:'#8a6d3f', BORDER:'#e3d9c8', PTEYE:'#b99a68', PTNOTE:'#e8dcc6'
    },
    alerts:{ NOTE:['#f7efe6','#a58650'], TIP:['#f1ece2','#6b5433'], IMPORTANT:['#f6e8e4','#9e3b33'],
             WARNING:['#f5efdd','#a06300'], CAUTION:['#f6e7e4','#cf3b2a'] },
    novel:{ book:'九千九百九十九张', journal:'纸上行舟小说集', seal:'行', sealColor:'#c23b2e' }
  }
};

/* ===== 渲染上下文（theme/zoom/pad 可配，对应浏览器版 OPT） ===== */
function makeCtx({ theme='orangeink', zoom=1, pad=14 } = {}) {
  const OPT = { zoom, pad, theme };
  const C = THEMES[OPT.theme].C;

  const hexRgba = (h, a) => {
    const v = /^#([0-9a-f]{6})$/i.exec(h); if (!v) return h;
    return 'rgba(' + parseInt(v[1].slice(0,2),16) + ',' + parseInt(v[1].slice(2,4),16) + ',' + parseInt(v[1].slice(4,6),16) + ',' + a + ')';
  };
  const px = v => Math.round(v * OPT.zoom * 10) / 10 + 'px';
  /* 行高一律 px（勿改回无单位：线上旧口径会把 1.8 当 1.8px 误判行高叠字） */
  const lh = (fontBase, ratio) => 'line-height:' + px(fontBase * ratio) + ';';

  function buildS() {
    return {
      p:'margin:0 0 22px;font-size:'+px(BASE.p)+';'+lh(BASE.p,1.8)+'color:'+C.TEXT+';letter-spacing:.3px',
      lead:'margin:0 0 24px;font-size:'+px(BASE.lead)+';'+lh(BASE.lead,1.85)+'color:'+C.TEXT+';letter-spacing:.3px',
      h1:'margin:0 0 26px;font-size:'+px(BASE.h1)+';'+lh(BASE.h1,1.45)+'font-weight:700;color:'+C.DEEP+';letter-spacing:.5px;padding-bottom:12px;border-bottom:3px solid '+C.ORANGE,
      h2:'margin:32px 0 16px;font-size:'+px(BASE.h2)+';'+lh(BASE.h2,1.5)+'font-weight:700;color:'+C.DEEP+';letter-spacing:.3px;padding-left:12px;border-left:4px solid '+C.ORANGE,
      h3:'margin:26px 0 12px;font-size:'+px(BASE.h3)+';'+lh(BASE.h3,1.5)+'font-weight:700;color:'+C.EMBER+';letter-spacing:.3px',
      h4:'margin:22px 0 10px;font-size:'+px(BASE.h4)+';'+lh(BASE.h4,1.5)+'font-weight:600;color:'+C.BROWN+';letter-spacing:.3px',
      strong:'font-weight:700;color:'+C.STRONG,
      em:'font-style:italic;color:'+C.TEXT2,
      a:'color:'+C.LINK+';text-decoration:none;border-bottom:1px solid '+hexRgba(C.LINK,0.35),
      code:'background:'+C.CODEBG+';color:'+(C.CODE||C.EMBER)+';padding:2px 6px;border-radius:3px;font-size:'+px(BASE.code)+';'+lh(BASE.code,1.6),
      pre:'background:'+C.WARMBG2+';color:'+C.TXTQ+';padding:14px 16px;border-radius:6px;overflow:auto;font-size:'+px(BASE.code)+';'+lh(BASE.code,1.75)+'margin:0 0 22px;border-left:3px solid '+C.ORANGE+';white-space:pre',
      blockquote:'margin:0 0 22px;padding:13px 16px;background:'+C.WARMBG+';border-left:4px solid '+C.ORANGE+';color:'+C.TXTQ+';font-size:'+px(BASE.quote)+';'+lh(BASE.quote,1.85)+'border-radius:0 6px 6px 0',
      ul:'margin:0 0 22px;padding-left:22px;font-size:'+px(BASE.p)+';'+lh(BASE.p,1.8)+'color:'+C.ORANGE+';letter-spacing:.3px',
      ol:'margin:0 0 22px;padding-left:22px;font-size:'+px(BASE.p)+';'+lh(BASE.p,1.8)+'color:'+C.ORANGE+';letter-spacing:.3px',
      ul2:'margin:10px 0 0;padding-left:20px;font-size:'+px(15)+';'+lh(15,1.8)+'color:'+C.LIST2+';list-style-type:square;letter-spacing:.3px',
      ol2:'margin:10px 0 0;padding-left:20px;font-size:'+px(15)+';'+lh(15,1.8)+'color:'+C.LIST2+';letter-spacing:.3px',
      li:'margin:0 0 10px;font-size:'+px(BASE.p)+';'+lh(BASE.p,1.8)+'color:'+C.ORANGE,
      li2:'margin:0 0 8px;font-size:'+px(15)+';'+lh(15,1.8)+'color:'+C.LIST2,
      caption:'margin:-10px 0 24px;text-align:center;font-size:'+px(BASE.cap)+';'+lh(BASE.cap,1.6)+'color:'+C.TEXT2+';letter-spacing:.3px',
      table:'width:100%;border-collapse:collapse;margin:0 0 22px;font-size:'+px(BASE.tab)+';'+lh(BASE.tab,1.7),
      th:'background:'+C.DEEP+';color:#fff;padding:10px 12px;border:1px solid '+C.DEEP+';text-align:left;font-weight:600;font-size:'+px(BASE.tab)+';'+lh(BASE.tab,1.6),
      td:'padding:10px 12px;border:1px solid '+C.BORDER+';color:'+C.TEXT+';font-size:'+px(BASE.tab)+';'+lh(BASE.tab,1.7),
      zebra:'background:'+C.ZEBRA,
      img:'max-width:100%;height:auto;border-radius:6px;display:block;margin:16px auto',
      alertBox: t => {
        const map = (THEMES[OPT.theme] && THEMES[OPT.theme].alerts) || THEMES.orangeink.alerts;
        const c = map[t] || map.NOTE;
        return 'margin:0 0 22px;padding:14px 16px;background:'+c[0]+';border-left:4px solid '+c[1]+';color:'+C.TEXT+';font-size:'+px(15)+';'+lh(15,1.85)+'border-radius:0 6px 6px 0';
      },
      alertP:'margin:0;font-size:'+px(15)+';'+lh(15,1.85)+'color:'+C.TEXT+';letter-spacing:.3px',
      /* 小说稿落款（——千槿）：右对齐灰卡其小字（novel_structure 识别后套用） */
      novelSig:'margin:6px 0 22px;font-size:'+px(14)+';'+lh(14,1.8)+'color:'+C.TAN+';text-align:right;letter-spacing:.5px',
      alertIcon:'font-size:14px;font-weight:700;margin-right:7px'
    };
  }

  return { OPT, C, hexRgba, px, lh, S: buildS() };
}

/* ===== markdown-it + 橙墨核心规则 ===== */
function makeMd(ctx) {
  const { OPT, C, px, lh, S } = ctx;
  const md = markdownit({ html:true, breaks:false, linkify:true, typographer:false });

  /* linkify 全角消毒（v1.2.1）：linkify-it 会把紧贴 URL 的全角标点连同后续汉字一起吸进自动链接
     （如「…orangeink，装到用户级目录」→ href 里带 %EF%BC%8C…，点开即坏链）。
     注意 token 层 href 已被百分号编码、链接文字是原文——解码后一致才认定自动链接；
     截断 href 与链接文字，余文还原为普通文本。手写 []() 链接不受影响。 */
  md.core.ruler.after('linkify', 'oimd_linkify_cjk', function(state){
    state.tokens.forEach(tok => {
      if (tok.type!=='inline' || !tok.children) return;
      const ch = tok.children;
      for (let i=0; i<ch.length; i++) {
        if (ch[i].type!=='link_open') continue;
        const href = ch[i].attrGet('href');
        if (!href) continue;
        const nxt = ch[i+1];
        if (!nxt || nxt.type!=='text') continue;
        let raw; try { raw = decodeURIComponent(href); } catch(e) { raw = href; }
        if (raw !== nxt.content) continue;
        const m = raw.search(/[^\x21-\x7e]/);
        if (m<=0) continue;
        ch[i].attrSet('href', raw.slice(0,m));
        nxt.content = raw.slice(0,m);
        const rest = new state.Token('text','',0);
        rest.content = raw.slice(m);
        for (let j=i+2; j<ch.length; j++) {
          if (ch[j].type==='link_close' && ch[j].level===ch[i].level) { ch.splice(j+1,0,rest); break; }
        }
      }
    });
    return true;
  });

  const ICONS_ZH = { NOTE:'说明', TIP:'提示', IMPORTANT:'重点', WARNING:'注意', CAUTION:'警告' };
  const escapeHtml = s => s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
  const mdInline = s => s ? md.renderInline(s) : '';
  const n2 = i => i < 10 ? '0'+i : ''+i;

  const alertParas = new WeakSet();
  md.core.ruler.push('gfm_alert', function(state){
    const toks = state.tokens;
    let i, j, k, depth, m;
    const re = /^\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\][ \t]*\n?/;
    for (i=0; i<toks.length; i++) {
      if (toks[i].type === 'blockquote_open') {
        j = i+1;
        while (j<toks.length && toks[j].type!=='inline' && toks[j].type!=='blockquote_close') j++;
        if (j<toks.length && toks[j].type==='inline' && (m=re.exec(toks[j].content))) {
          toks[i].attrSet('data-alert', m[1]);
          toks[j].content = toks[j].content.slice(m[0].length);
          if (toks[j].children && toks[j].children.length && toks[j].children[0].type==='text') {
            toks[j].children[0].content = toks[j].children[0].content.replace(re,'');
          }
          const LABC = { NOTE:C.CHIP, TIP:C.BROWN, IMPORTANT:C.STRONG, WARNING:'#a06300', CAUTION:'#cf3b2a' };
          if (toks[j].children) {
            const ch = toks[j].children;
            while (ch.length && ((ch[0].type==='text' && ch[0].content.trim()==='') || ch[0].type==='softbreak')) ch.shift();
            const icon = new state.Token('html_inline','',0);
            icon.content = '<span style="padding:1px 7px;margin-right:8px;background:'+
              (LABC[m[1]]||C.BROWN)+';color:#fff;border-radius:3px;font-size:12px;font-weight:700;letter-spacing:1px;'+lh(12,1.6)+'">'+
              (ICONS_ZH[m[1]]||'提示')+'</span>';
            ch.unshift(icon);
          }
          depth = 0;
          for (k=i; k<toks.length; k++) {
            if (toks[k].type==='blockquote_open') depth++;
            else if (toks[k].type==='blockquote_close') { depth--; if (depth===0) break; }
            else if (toks[k].type==='paragraph_open' && depth>=1) alertParas.add(toks[k]);
          }
        }
      }
    }
    return true;
  });

  md.core.ruler.push('quote_breaks', function(state){
    const toks = state.tokens;
    let depth = 0;
    for (let i=0; i<toks.length; i++) {
      if (toks[i].type==='blockquote_open') depth++;
      else if (toks[i].type==='blockquote_close') depth--;
      else if (depth>0 && toks[i].type==='inline' && toks[i].children) {
        for (let j=0; j<toks[i].children.length; j++) {
          if (toks[i].children[j].type==='softbreak') {
            const br = new state.Token('html_inline','',0);
            br.content = '<br>';
            toks[i].children[j] = br;
          }
        }
      }
    }
    return true;
  });

  md.core.ruler.push('cjk_spacing', function(state){
    state.tokens.forEach(tok => {
      if (tok.type==='inline' && tok.children) {
        tok.children.forEach(c => {
          if (c.type==='text') {
            c.content = c.content
              .replace(/([\u4e00-\u9fa5])([a-zA-Z0-9])/g,'$1 $2')
              .replace(/([a-zA-Z0-9])([\u4e00-\u9fa5])/g,'$1 $2');
          }
        });
      }
    });
    return true;
  });

  const leadParas = new WeakSet(), capParas = new WeakSet();
  md.core.ruler.push('zh_typeset', function(state){
    const t = state.tokens;
    let i, j;
    for (i=0; i<t.length; i++) {
      if (t[i].type==='heading_close' && t[i].tag==='h1') {
        j = i+1;
        while (j<t.length && t[j].type!=='paragraph_open' && t[j].type!=='heading_open'
               && t[j].type!=='blockquote_open' && t[j].type!=='fence') j++;
        if (j<t.length && t[j].type==='paragraph_open') leadParas.add(t[j]);
        break;
      }
    }
    for (i=0; i<t.length; i++) {
      if (t[i].type==='inline' && t[i].children && t[i].children.length===1
          && t[i].children[0].type==='image'
          && t[i+2] && t[i+2].type==='paragraph_open' && t[i+3] && t[i+3].type==='inline') {
        const c = t[i+3].children;
        if (c && c.length>=3 && c[0].type==='em_open' && c[c.length-1].type==='em_close') capParas.add(t[i+2]);
      }
    }
    return true;
  });

  /* ===== 小说连载结构规则（v1.2.7 范式层）：只对「novel 主题 + 小说稿形态」生效 =====
     与 template.html novel_structure 同口径（对拍基准），文稿规格行 → 统一版式：
     # N-001-上 → 刊头；> 引子： → 并入刊头；章节行 → 章节牌；——千槿 → 落款；
     > 结尾帧： → 结尾帧卡；文末补刊尾行。形态门不满足整套静默跳过。 */
  const sigParas = new WeakSet();
  md.core.ruler.push('novel_structure', function(state){
    const NV = THEMES[OPT.theme] && THEMES[OPT.theme].novel;
    if (!NV) return true;
    const toks = state.tokens;
    let i, j, m;
    const plain = tok => { let s='', c=tok.children||[]; for (let x=0;x<c.length;x++){ if (c[x].type==='text') s+=c[x].content; } return s; };
    const escH = s => String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
    const bqClose = idx => { let d=0; for (let x=idx;x<toks.length;x++){ if (toks[x].type==='blockquote_open') d++; else if (toks[x].type==='blockquote_close'){ d--; if (!d) return x; } } return -1; };
    const toHtml = (tok, html) => { tok.type='html_block'; tok.content=html; tok.children=null; };
    /* 细装饰线：2px 高 + nbsp 防剥（1px 空 span 会被微信粘贴解析剥掉） */
    const hairline = w => '<span style="display:inline-block;width:'+w+'px;height:2px;background:'+C.ORANGE+';vertical-align:middle;overflow:hidden;font-size:2px;'+lh(2,1)+'">&#160;</span>';

    /* 形态门：首个 h1 = N-<数字>-<上|中|下> */
    let h1In=-1, epNum='', epPart='';
    for (i=0;i<toks.length;i++){
      if (toks[i].type==='heading_open' && toks[i].tag==='h1'){
        for (j=i+1;j<toks.length && toks[j].type!=='heading_close';j++){ if (toks[j].type==='inline'){ h1In=j; break; } }
        if (h1In>0 && (m=/^N[-－·](\d{1,3})[-－·]([上中下])$/.exec((toks[h1In].content||'').replace(/\s+/g,'')))){ epNum=m[1]; epPart=m[2]; }
        break;
      }
    }
    if (!epNum) return true;
    const pad3 = ('00'+epNum).slice(-3);
    const epLabel = '第 '+pad3+' 集 · '+epPart;

    /* 扫描：首个章节行→章题；落款→sigParas；引子/结尾帧引用块→文本并整块隐藏 */
    const chapRe=/^第[0-9〇零一二两三四五六七八九十百千]+章[\s　]+(.{1,14})$/;
    let chTitle='', introTxt='', endRaw='', endIdx=-1;
    for (i=0;i<toks.length;i++){
      if (toks[i].type!=='blockquote_open'){
        if (toks[i].type==='inline' && toks[i-1] && toks[i-1].type==='paragraph_open' && toks[i-1].level===0){
          const bt = plain(toks[i]).trim();
          if (!chTitle && (m=chapRe.exec(bt))) chTitle=m[1].trim();
          if (/^——.{1,6}$/.test(bt)) sigParas.add(toks[i-1]);
        }
        continue;
      }
      const jc = bqClose(i); if (jc<0) continue;
      let inner=-1;
      for (j=i+1;j<jc;j++){ if (toks[j].type==='inline'){ inner=j; break; } }
      if (inner<0) continue;
      const btx = (toks[inner].content||'').trim();
      if (!introTxt && /^引子[：:]/.test(btx)){
        introTxt = btx.replace(/^引子[：:]\s*/,'');
        toHtml(toks[i],'');
        /* render() 不检查 inline 自身 hidden → inline 需转空 html_block 才真隐藏 */
        for (j=i+1;j<=jc;j++){ if (toks[j].type==='inline'){ toHtml(toks[j],''); } else { toks[j].hidden=true; } }
      } else if (!endRaw && /^结尾帧[：:]/.test(btx)){
        endRaw=btx; endIdx=i;
        toHtml(toks[i],'');
        for (j=i+1;j<=jc;j++){ if (toks[j].type==='inline'){ toHtml(toks[j],''); } else { toks[j].hidden=true; } }
      }
    }
    /* 刊头大字替代 h1 后，导语放大规则不适用于小说稿 */
    for (i=0;i<toks.length;i++){ if (toks[i].type==='paragraph_open') leadParas.delete(toks[i]); }

    /* H1 → 刊头（与视频号封面同构） */
    if (h1In>0){
      toks[h1In-1].hidden=true;
      for (j=h1In+1;j<toks.length;j++){ if (toks[j].type==='heading_close'){ toks[j].hidden=true; break; } }
      toHtml(toks[h1In],
        '<section style="margin:2px 0 14px;">'
        +'<section style="overflow:hidden;">'
        +'<span style="display:inline-block;width:20px;height:20px;background:'+(NV.sealColor||'#c23b2e')+';color:#fff;font-size:12px;'+lh(12,1.67)+'font-weight:700;text-align:center;border-radius:3px;vertical-align:middle;">'+escH(NV.seal||'行')+'</span>'
        +'<span style="font-size:13px;font-weight:700;color:'+C.DEEP+';margin-left:7px;vertical-align:middle;">'+escH(NV.journal)+'</span>'
        +hairline(88)
        +'<span style="font-size:11px;color:'+C.BROWN+';font-weight:700;letter-spacing:1px;vertical-align:middle;">'+escH(epLabel)+'</span>'
        +'</section>'
        +'<section style="margin-top:12px;font-size:12px;'+lh(12,1.7)+'color:'+C.BROWN+';font-weight:700;letter-spacing:1px;"><span style="display:inline-block;width:8px;height:8px;background:'+C.ORANGE+';margin-right:7px;vertical-align:middle;overflow:hidden;font-size:8px;'+lh(8,1)+'">&#160;</span>'+escH(NV.book)+' · '+pad3+'</section>'
        +'<section style="border-left:4px solid '+C.ORANGE+';padding-left:12px;font-size:26px;'+lh(26,1.5)+'font-weight:700;color:'+C.DEEP+';letter-spacing:3px;margin-top:12px;">'+escH(chTitle?chTitle+' · '+epPart:epLabel)+'</section>'
        +(introTxt?'<section style="font-size:13px;'+lh(13,1.8)+'color:'+C.TEXT2+';letter-spacing:2px;margin-top:12px;">'+escH(introTxt.replace(/，/g,'　　').replace(/[。．]$/,''))+'</section>':'')
        +'</section>');
    }
    md.__novelTitle = chTitle ? (chTitle+' · '+epPart) : (NV.book+' · '+pad3+epPart);

    /* 章节行 → 章节牌（A 案细线夹注） */
    for (i=0;i<toks.length;i++){
      if (toks[i].type!=='inline' || !toks[i-1] || toks[i-1].type!=='paragraph_open' || toks[i-1].level!==0) continue;
      const bt2 = plain(toks[i]).trim();
      if (chapRe.test(bt2)){
        toks[i-1].hidden=true;
        if (toks[i+1] && toks[i+1].type==='paragraph_close') toks[i+1].hidden=true;
        toHtml(toks[i],
          '<section style="text-align:center;margin:30px 0 22px;">'
          +hairline(26)
          +'<span style="display:inline-block;vertical-align:middle;font-size:17px;'+lh(17,1.6)+'font-weight:700;color:'+C.DEEP+';letter-spacing:5px;margin:0 12px;">'+escH(bt2)+'</span>'
          +hairline(26)
          +'</section>');
      }
    }

    /* 结尾帧引用块 → 结尾帧卡（海棠纸底 · STRONG 原句（「；」后折行）· BROWN 预告行） */
    if (endRaw && endIdx>=0){
      const mo=/原句[「"]+([^」"]+)[」"]+/.exec(endRaw), mp2=/下集预告[「"]+([^」"]+)[」"]+/.exec(endRaw);
      const q1=mo?mo[1].trim():'', q2=mp2?mp2[1].trim():'';
      toks[endIdx].content=
        '<section style="background:'+C.WARMBG+';border-radius:8px;padding:20px 18px 16px;margin:4px 0 24px;">'
        +'<section style="text-align:center;font-size:11px;'+lh(11,1.6)+'letter-spacing:3px;color:'+C.BROWN+';font-weight:700;">本集 · 收束</section>'
        +(q1?'<section style="text-align:center;font-size:17px;'+lh(17,1.7)+'font-weight:700;color:'+C.STRONG+';margin:10px 0 12px;letter-spacing:.5px;">'+escH(q1).replace(/；/g,'；<br>')+'</section>':'')
        +'<section style="text-align:center;margin:0 auto 12px;width:28px;height:2px;background:'+C.ORANGE+';overflow:hidden;font-size:2px;'+lh(2,1)+'">&#160;</section>'
        +(q2?'<section style="text-align:center;font-size:13px;'+lh(13,1.8)+'color:'+C.BROWN+';">下集 · '+escH(q2)+'</section>':'')
        +'</section>';
    }

    /* 刊尾行：细线 + 刊名 · 刊—001·上（呼应封面底行） */
    const foot = new state.Token('html_block','',0);
    foot.content='<section style="text-align:center;margin:26px 0 6px;">'
      +hairline(64)
      +'<span style="display:inline-block;vertical-align:middle;font-size:11px;'+lh(11,1.6)+'color:'+C.BROWN+';letter-spacing:1px;margin:0 10px;">'+escH(NV.journal)+' · 刊—'+pad3+'·'+epPart+'</span>'
      +hairline(64)
      +'</section>';
    toks.push(foot);
    return true;
  });

  function setStyle(tok, style){ tok.attrSet('style', style); return tok; }
  function wrap(tokens, idx, options, env, self, style){
    setStyle(tokens[idx], style); return self.renderToken(tokens, idx, options);
  }
  md.renderer.rules.paragraph_open = function(t,i,o,e,s){
    let st = S.p;
    if (capParas.has(t[i])) st = S.caption;
    else if (alertParas.has(t[i])) st = S.alertP;
    else if (leadParas.has(t[i])) st = S.lead;
    else if (sigParas.has(t[i])) st = S.novelSig;
    return wrap(t,i,o,e,s,st);
  };
  md.renderer.rules.heading_open = function(t,i,o,e,s){
    const st = S[t[i].tag] || S.h4; return wrap(t,i,o,e,s,st);
  };
  md.renderer.rules.strong_open = function(t,i,o,e,s){ return wrap(t,i,o,e,s,S.strong); };
  md.renderer.rules.em_open     = function(t,i,o,e,s){ return wrap(t,i,o,e,s,S.em); };
  md.renderer.rules.link_open = function(t,i,o,e,s){
    /* 长 URL 链接断行（v1.2.2）：链接文字本身是完整 URL（无空格长串）时，窄容器内无断行点
       会横向溢出（手机模拟 375px 实测）→ 对这类链接追加 word-break:break-all。
       只对「文字=URL」的链接生效，普通文字链接（含中文）不受影响。 */
    let st = S.a, inner = '';
    for (let k=i+1; k<t.length; k++) {
      if (t[k].type==='link_close') break;
      if (t[k].type==='text') inner += t[k].content;
    }
    if (/^(https?:\/\/|www\.)\S+$/i.test(inner.trim())) st += 'word-break:break-all;';
    return wrap(t,i,o,e,s,st);
  };
  let listDepth = 0;
  md.renderer.rules.bullet_list_open  = function(t,i,o,e,s){ listDepth++; return wrap(t,i,o,e,s, listDepth>1?S.ul2:S.ul); };
  md.renderer.rules.bullet_list_close = function(t,i,o,e,s){ listDepth--; return s.renderToken(t,i,o); };
  md.renderer.rules.ordered_list_open = function(t,i,o,e,s){ listDepth++; return wrap(t,i,o,e,s, listDepth>1?S.ol2:S.ol); };
  md.renderer.rules.ordered_list_close= function(t,i,o,e,s){ listDepth--; return s.renderToken(t,i,o); };
  md.renderer.rules.list_item_open    = function(t,i,o,e,s){ return wrap(t,i,o,e,s, listDepth>1?S.li2:S.li); };
  md.renderer.rules.hr = function(){
    return '<section style="text-align:center;margin:34px 0">'+
      '<span style="display:inline-block;width:36px;height:4px;border-radius:2px;background:'+C.ORANGE+';vertical-align:middle;overflow:hidden;font-size:4px;'+lh(4,1)+'">&#160;</span></section>';
  };
  md.renderer.rules.table_open = function(t,i,o,e,s){ return wrap(t,i,o,e,s,S.table); };
  md.renderer.rules.th_open    = function(t,i,o,e,s){ return wrap(t,i,o,e,s,S.th); };
  md.renderer.rules.td_open    = function(t,i,o,e,s){ return wrap(t,i,o,e,s,S.td); };
  md.renderer.rules.image      = function(t,i,o,e,s){
    const tok = t[i], ai = tok.attrIndex('alt');
    if (ai>=0) tok.attrs[ai][1] = s.renderInlineAsText(tok.children,o,e);
    setStyle(tok,S.img); return s.renderToken(t,i,o);
  };
  md.renderer.rules.code_inline = function(t,i,o,e,s){
    return '<code style="'+S.code+'">'+escapeHtml(t[i].content)+'</code>';
  };
  md.renderer.rules.fence = function(t,i,o,e,s){
    return '<pre style="'+S.pre+'">'+escapeHtml(t[i].content)+'</pre>';
  };
  md.renderer.rules.code_block = md.renderer.rules.fence;
  md.renderer.rules.blockquote_open = function(t,i,o,e,s){
    const a = t[i].attrGet('data-alert');
    return '<section style="'+(a?S.alertBox(a):S.blockquote)+'">';
  };
  md.renderer.rules.blockquote_close = function(t,i){ return t[i].hidden ? '' : '</section>'; };

  /* ===== 结构化模块（:::intro/quote/steps/point） ===== */
  const DIRECTIVES = {
    intro(o){
      return '<section style="margin:0 0 26px;padding:18px 16px 16px;background:'+C.WARMBG+';border-top:3px solid '+C.ORANGE+';border-radius:0 4px 4px 4px">'+
        (o.eyebrow?'<section style="margin:0 0 10px;font-size:'+px(12.5)+';'+lh(12.5,1.6)+'color:'+C.DEEP+';letter-spacing:2px;font-weight:700">'+esc(o.eyebrow)+'</section>':'')+
        (o.title?'<section style="margin:0 0 10px;font-size:'+px(22)+';'+lh(22,1.45)+'font-weight:700;color:'+C.DEEP+';letter-spacing:.5px">'+esc(o.title)+'</section>':'')+
        (o.subtitle?'<section style="margin:0;font-size:'+px(15)+';'+lh(15,1.8)+'color:'+C.TEXT2+';letter-spacing:.3px">'+mdInline(o.subtitle)+'</section>':'')+
        (o.meta?'<section style="margin:12px 0 0;padding-top:10px;border-top:1px solid #ffffff;font-size:'+px(12.5)+';'+lh(12.5,1.6)+'color:'+C.TAN+';letter-spacing:1px">'+esc(o.meta)+'</section>':'')+
        '</section>';
    },
    quote(o){
      return '<section style="margin:0 0 26px;padding:20px 18px;background:'+C.WARMBG+';border-left:4px solid '+C.ORANGE+';border-radius:0 6px 6px 0">'+
        '<section style="margin:0 0 6px;color:'+C.STRONG+';font-size:'+px(30)+';'+lh(30,1)+'font-weight:700">&#8220;</section>'+
        '<section style="margin:0;font-size:'+px(18)+';'+lh(18,1.8)+'color:'+C.DEEP+';font-weight:700;letter-spacing:.3px">'+mdInline(o.text||o.quote||'')+'</section>'+
        (o.from?'<section style="margin:12px 0 0;font-size:'+px(13)+';'+lh(13,1.6)+'color:'+C.TAN+';text-align:right;letter-spacing:.5px">&#8212; '+esc(o.from)+'</section>':'')+
        '</section>';
    },
    steps(o, title, raw){
      const items = (raw||[]).map(l => {
        const p = l.split('|');
        return { t:(p[0]||'').trim(), d:(p[1]||'').trim() };
      }).filter(it => it.t !== '');
      if (!items.length) return '';
      const rows = items.map((it, idx) => {
        const last = (idx === items.length-1), pb = last ? '0' : '16px';
        const line = idx===0 ? '' : 'border-top:1px solid #ffffff;';
        const padTop = idx===0 ? '0' : '16px';
        return '<tr>'+
          '<td style="'+line+'width:30px;vertical-align:top;padding:'+padTop+' 0 '+pb+'">'+
            '<span style="display:inline-block;width:24px;height:24px;background:'+C.CHIP+';color:#fff;border-radius:50%;text-align:center;font-size:'+px(12)+';'+lh(12,2)+'font-weight:700">'+n2(idx+1)+'</span>'+
          '</td>'+
          '<td style="'+line+'vertical-align:top;padding:'+padTop+' 0 '+pb+'">'+
            '<section style="margin:0 0 3px;font-size:'+px(BASE.p)+';'+lh(BASE.p,1.7)+'font-weight:700;color:'+C.DEEP+';letter-spacing:.3px">'+mdInline(it.t)+'</section>'+
            (it.d?'<section style="margin:0;font-size:'+px(15)+';'+lh(15,1.8)+'color:'+C.TXTQ+';letter-spacing:.3px">'+mdInline(it.d)+'</section>':'')+
          '</td>'+
        '</tr>';
      }).join('');
      return '<section style="margin:0 0 26px;padding:18px 16px;background:'+C.WARMBG+';border-left:4px solid '+C.ORANGE+';border-radius:0 6px 6px 0">'+
        (title?'<section style="margin:0 0 14px;font-size:'+px(15)+';'+lh(15,1.6)+'font-weight:700;color:'+C.DEEP+';letter-spacing:.5px">'+esc(title)+'</section>':'')+
        '<table style="width:100%;border-collapse:collapse;border:none;font-size:'+px(BASE.p)+';'+lh(BASE.p,1.7)+'">'+rows+'</table>'+
        '</section>';
    },
    point(o){
      return '<section style="margin:0 0 26px;padding:18px 16px;background:'+C.DEEP+';border-radius:6px">'+
        (o.eyebrow?'<section style="margin:0 0 8px;font-size:'+px(12.5)+';'+lh(12.5,1.6)+'color:'+C.PTEYE+';letter-spacing:2px;font-weight:700">'+esc(o.eyebrow)+'</section>':'')+
        '<section style="margin:0;font-size:'+px(18)+';'+lh(18,1.75)+'color:#ffffff;font-weight:700;letter-spacing:.3px">'+mdInline(o.text||o.title||'')+'</section>'+
        (o.note?'<section style="margin:10px 0 0;font-size:'+px(13)+';'+lh(13,1.7)+'color:'+C.PTNOTE+';letter-spacing:.3px">'+esc(o.note)+'</section>':'')+
        '</section>';
    }
  };
  function esc(s){ return escapeHtml(s==null ? '' : String(s)); }

  function expandDirectives(src){
    if (src.indexOf(':::') === -1) return src;
    const lines = src.split('\n'), out = [];
    let i = 0;
    const OPEN = /^:::([a-zA-Z][\w-]*)\s*(?:\[([^\]]*)\])?\s*$/;
    const KV   = /^\s*([A-Za-z][\w-]*)\s*:\s*(.*)$/;
    while (i < lines.length) {
      const m = OPEN.exec(lines[i]);
      if (!m) { out.push(lines[i]); i++; continue; }
      const type = m[1].toLowerCase(), title = (m[2]||'').trim();
      const body = [];
      let j = i+1;
      while (j<lines.length && lines[j].trim()!==':::') { body.push(lines[j]); j++; }
      const fn = DIRECTIVES[type];
      if (fn) {
        const o = {}, raw = [];
        body.forEach(l => {
          const mm = KV.exec(l);
          if (mm) o[mm[1].toLowerCase()] = mm[2].trim();
          else if (l.trim() !== '') raw.push(l);
        });
        out.push('', fn(o, title, raw, body), '');
      } else {
        out.push(lines[i]); body.forEach(l => out.push(l));
        if (j < lines.length) out.push(':::');
      }
      i = (j < lines.length ? j+1 : j);
    }
    return out.join('\n');
  }

  /* ===== 脚注（被动渲染） ===== */
  const fnSup = n => '<sup style="font-size:'+px(11)+';'+lh(11,1.4)+'color:'+C.EMBER+';font-weight:700">['+n+']</sup>';
  function extractFootnotes(src){
    const lines = src.split('\n'), kept = [], defs = {}, defOrder = [];
    let fence = false;
    for (let i=0; i<lines.length; i++) {
      const ln = lines[i];
      if (/^\s*(```|~~~)/.test(ln)) fence = !fence;
      if (!fence) {
        const dm = /^\[\^([^\]\s]+)\]\s*:\s*(.*)$/.exec(ln);
        if (dm) { if (defs[dm[1]]==null) { defs[dm[1]]=dm[2]; defOrder.push(dm[1]); } continue; }
      }
      kept.push(ln);
    }
    if (!defOrder.length) return { text:src, html:'', refCount:0, defCount:0 };
    const text0 = kept.join('\n'), nums = {};
    let seq = 0; const refsFound = [];
    const lines2 = text0.split('\n'); fence = false;
    for (let j=0; j<lines2.length; j++) {
      let L = lines2[j];
      if (/^\s*(```|~~~)/.test(L)) fence = !fence;
      if (fence) continue;
      const re = /\[\^([^\]\s]+)\]/g; let fm, changed = false;
      while ((fm = re.exec(L))) {
        const id = fm[1];
        if (nums[id]==null) { seq++; nums[id]=seq; refsFound.push(id); }
        L = L.replace(fm[0], fnSup(nums[id]));
        re.lastIndex = 0; changed = true;
      }
      if (changed) lines2[j] = L;
    }
    const text = lines2.join('\n');
    const cmap = {}; defOrder.forEach(id => { if (id!=='r0') cmap[id]=defs[id]; });
    const ordered = [];
    refsFound.forEach(id => { if (cmap[id]!=null) { ordered.push({n:nums[id],content:cmap[id]}); delete cmap[id]; } });
    defOrder.forEach(id => { if (cmap[id]!=null) ordered.push({n:0,content:cmap[id]}); });
    let html = '';
    if (ordered.length) {
      const rows = ordered.map(it =>
        '<section style="margin:0 0 8px;font-size:'+px(13)+';'+lh(13,1.7)+'color:'+C.TXTQ+';letter-spacing:.3px">'+
        '<span style="color:'+C.EMBER+';font-weight:700;font-size:'+px(12.5)+';'+lh(12.5,1.5)+'">['+(it.n||'·')+']</span> '+
        mdInline(it.content)+'</section>'
      ).join('');
      html = '<section style="margin:36px 0 0;padding-top:14px;border-top:1px solid '+C.BORDER+'">'+
        '<section style="margin:0 0 10px;font-size:'+px(13.5)+';'+lh(13.5,1.5)+'font-weight:700;color:'+C.BROWN+';letter-spacing:2px">参考</section>'+
        rows+'</section>';
    }
    return { text, html, refCount:refsFound.length, defCount:ordered.length };
  }

  return { md, expandDirectives, extractFootnotes, escapeHtml };
}

/* ===== DOM 层（jsdom）：polish + 复制净化 ===== */
function makeDom() {
  const dom = new JSDOM('<!DOCTYPE html><html><body></body></html>', { url:'http://localhost/' });
  return dom;
}

function wrapTextRuns(ctx, root, doc) {
  const { C } = ctx;
  const els = root.querySelectorAll('*');
  for (let i=0; i<els.length; i++) {
    const el = els[i];
    let liColor = null;
    if (el.tagName === 'LI') {
      let d = 0, n = el;
      while (n && n !== root) { if (n.tagName==='UL'||n.tagName==='OL') d++; n = n.parentElement; }
      liColor = d>1 ? C.TXTQ : C.TEXT;
    }
    const kids = [].slice.call(el.childNodes);
    for (let j=0; j<kids.length; j++) {
      const n = kids[j];
      if (n.nodeType !== 3) continue;
      if (!n.textContent.trim().length) continue;
      const sp = doc.createElement('span');
      sp.setAttribute('leaf','');
      if (liColor) sp.setAttribute('style','color:'+liColor);
      el.insertBefore(sp, n);
      sp.appendChild(n);
    }
  }
}

const LI_BLOCK = { P:1,DIV:1,SECTION:1,UL:1,OL:1,TABLE:1,PRE:1,BLOCKQUOTE:1,
                   H1:1,H2:1,H3:1,H4:1,H5:1,H6:1,IMG:1,HR:1 };
function wrapLiSections(ctx, root, doc) {
  const { C } = ctx;
  root.querySelectorAll('li').forEach(li => {
    let hasBlock = false;
    for (let k=0; k<li.children.length; k++) {
      if (LI_BLOCK[li.children[k].tagName]) { hasBlock = true; break; }
    }
    if (hasBlock || !li.children.length) return;
    let d = 0, n = li;
    while (n && n !== root) { if (n.tagName==='UL'||n.tagName==='OL') d++; n = n.parentElement; }
    const sec = doc.createElement('section');
    sec.setAttribute('style','margin:0;color:'+(d>1?C.TXTQ:C.TEXT));
    while (li.firstChild) sec.appendChild(li.firstChild);
    li.appendChild(sec);
  });
}

function polish(ctx, root, doc) {
  wrapLiSections(ctx, root, doc);                    /* li 内容先包 section（须在 wrapTextRuns 之前） */
  root.querySelectorAll('table').forEach(tb => {
    Array.prototype.forEach.call(tb.querySelectorAll('tr'), (tr,i) => {
      if (tr.querySelector('th')) return;
      if (i%2 === 1) tr.querySelectorAll('td').forEach(td => { td.style.background = ctx.S.zebra; });
    });
  });
  /* 引用块/警告块「下松上紧」修复：末子元素 margin-bottom 清零 */
  root.querySelectorAll('section').forEach(q => {
    const st = q.getAttribute('style') || '';
    if (st.indexOf('border-radius:0 6px 6px 0') < 0) return;
    const kids = q.children;
    if (kids.length) kids[kids.length-1].style.marginBottom = '0';
  });
  wrapTextRuns(ctx, root, doc);                      /* 必须最后做 */
}

/* ===== 复制净化（对齐 template.html sanitizeStyle/cleanCopyHTML） ===== */
function normalizeFont(s){ return (s||'').replace(/["']/g,'').replace(/\s+/g,' ').trim(); }
function sanitizeStyle(win, el, originEl){
  const st = el.getAttribute('style'); if (!st) return;
  let out = st;
  out = out.replace(/text-align\s*:\s*start/gi,'text-align:left')
           .replace(/text-align\s*:\s*end/gi,'text-align:right');
  out = out.replace(/font-family\s*:[^;]*;?/gi,'');
  out = out.replace(/(orphans|widows|text-indent|word-spacing|-webkit-text-stroke-width|text-transform|font-variant-ligatures)\s*:[^;]*;?/gi,'');
  const m = /line-height\s*:\s*([^;\s]+)/i.exec(out);
  if (m && !/^\d*\.?\d+px$/i.test(m[1])) {
    /* 正常输出恒为 px 行高，此分支仅兜底；jsdom 无布局，读不到 computed 则删除 */
    let cpx = NaN;
    try { cpx = parseFloat(win.getComputedStyle(originEl).lineHeight); } catch(e) {}
    if (isFinite(cpx) && cpx>0) out = out.replace(/line-height\s*:\s*[^;\s]+/i,'line-height:'+Math.round(cpx*10)/10+'px');
    else out = out.replace(/line-height\s*:\s*[^;\s]+;?/i,'');
  }
  out = out.replace(/;\s*;/g,';').replace(/^\s*;+|;+\s*$/g,'');
  if (out) el.setAttribute('style',out); else el.removeAttribute('style');
}
function cleanCopyHTML(ctx, root, win){
  const src = root.querySelector('.fm-article') || root;
  const box = src.cloneNode(true);
  box.removeAttribute('class');
  box.querySelectorAll('.__hl').forEach(e => e.classList.remove('__hl'));
  const orig = src.querySelectorAll('*'), cl = box.querySelectorAll('*');
  for (let i=0; i<orig.length; i++) sanitizeStyle(win, cl[i], orig[i]);
  sanitizeStyle(win, box, src);
  return box.outerHTML;
}

/* ===== 字数（公众号口径，2026-09-16 用 08 期真文校准） ===== */
function wechatCount(s){
  const m = s.match(/[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef\u201c\u201d\u2018\u2019\u2014\u2026\u00b7\u300c\u300d\u300e\u300f]|[\uD83C-\uD83E][\uDC00-\uDFFF]|[\u2600-\u27BF]|[A-Za-z0-9]/g);
  return m ? m.length : 0;
}

/* ===== 主渲染入口 ===== */
export function renderOrangeink(src, opts = {}) {
  const ctx = makeCtx(opts);
  const { md, expandDirectives, extractFootnotes } = makeMd(ctx);
  const dom = makeDom();
  const doc = dom.window.document;
  const preview = doc.body;

  const expanded = expandDirectives(src);
  const fn = extractFootnotes(expanded);
  const padStyle = ctx.OPT.pad>0 ? ('padding:0 '+ctx.OPT.pad+'px;box-sizing:border-box') : 'box-sizing:border-box';
  preview.innerHTML = '<section class="fm-article" style="'+padStyle+'">'+md.render(fn.text)+fn.html+'</section>';
  polish(ctx, preview, doc);
  const html = cleanCopyHTML(ctx, preview, dom.window);

  /* 元数据：标题/摘要候选/字数/图片清单 */
  const root = preview.querySelector('.fm-article');
  const h1 = root.querySelector('h1');
  /* 小说稿刊头取代 H1 → 标题回退到 novel_structure 产出的「章题 · 部」（无则空） */
  const title = h1 ? h1.textContent.trim() : (md.__novelTitle || '');
  const firstP = root.querySelector('p');
  const digest = firstP ? firstP.textContent.trim().slice(0,54) : '';
  const images = [].map.call(root.querySelectorAll('img'), im => ({ src: im.getAttribute('src'), alt: im.getAttribute('alt')||'' }));
  const meta = {
    title, digest,
    charsWechat: wechatCount(root.textContent),
    charsSource: src.length,
    footnotes: { refs: fn.refCount, defs: fn.defCount },
    images,
    theme: ctx.OPT.theme, zoom: ctx.OPT.zoom, pad: ctx.OPT.pad
  };
  return { html, meta, dom };
}

/* ===== 静态合规自检（jsdom 可覆盖的规则子集；布局类规则留浏览器端/probe.py） ===== */
export function checkStatic(html) {
  const dom = new JSDOM('<body>'+html+'</body>');
  const doc = dom.window.document;
  const issues = [];
  const all = [].slice.call(doc.body.querySelectorAll('*'));
  const ALLOW_FF = normalizeFont('"mp-quote", PingFang SC, system-ui, -apple-system');
  all.forEach(el => {
    const st = el.getAttribute('style') || '';
    let m;
    m = st.match(/line-height\s*:\s*([\d.]+)\s*(?=;|$)/i);
    if (m) issues.push({ rule:'1.3 行高单位', sev:'error', tag:el.tagName,
      desc:'line-height:'+m[1]+' 是无单位值，线上会误判行高叠字（渲染器不应产出，出现即管线异常）' });
    m = st.match(/text-align\s*:\s*(start|end)\b/i);
    if (m) issues.push({ rule:'1.6 text-align', sev:'error', tag:el.tagName,
      desc:'显式 text-align:'+m[1]+'（违禁值）' });
    m = /font-family\s*:\s*([^;]+)/i.exec(st);
    if (m && normalizeFont(m[1]).indexOf(ALLOW_FF)!==0) issues.push({ rule:'3 字体', sev:'error', tag:el.tagName,
      desc:'font-family 不在官方白名单内（渲染器不应产出 font-family）' });
    m = st.match(/width\s*:\s*(\d+)\s*px/i);
    if (m && parseInt(m[1],10)>677) issues.push({ rule:'1.4 宽度溢出', sev:'warn', tag:el.tagName,
      desc:'width '+m[1]+'px 超 677px 安全区' });
  });
  /* 块容器直接文本（官方叠字检测兜底口径的静态近似——正常应恒 0） */
  const BLOCKS = ['p','div','section','h1','h2','h3','h4','h5','h6','li','td'];
  all.forEach(el => {
    if (BLOCKS.indexOf(el.tagName.toLowerCase())===-1) return;
    let direct = false;
    Array.prototype.forEach.call(el.childNodes, c => {
      if (c.nodeType===3 && (c.textContent||'').trim().length) direct = true;
    });
    if (direct) issues.push({ rule:'1.3 行高叠字（结构）', sev:'error', tag:el.tagName,
      desc:'块容器存在直接文本节点（应包 <span leaf>；正常管线恒 0，出现即 wrapTextRuns 未生效）' });
  });
  doc.body.querySelectorAll('table').forEach(tb => {
    const tr = tb.querySelector('tr');
    if (tr && tr.children.length>4) issues.push({ rule:'表格列数', sev:'warn', tag:'table',
      desc:tr.children.length+' 列在手机端会挤压，建议 ≤4 列或改列表' });
  });
  doc.body.querySelectorAll('pre').forEach(el => {
    const t = el.textContent||'';
    if (t.length>40 && t.indexOf('\n')===-1) issues.push({ rule:'1.8 pre', sev:'warn', tag:'pre', desc:'pre 内长文本无换行，建议改用 p' });
  });
  doc.body.querySelectorAll('a').forEach(el => {
    if ((el.textContent||'').trim()==='' && !el.querySelector('img')) issues.push({ rule:'空链接', sev:'warn', tag:'a', desc:'空 <a> 标签' });
  });
  /* 3.1 嵌套深度（同标签+同样式单子链 >15 层会被删节点） */
  const NEST_MAX = 15;
  (function walkNest(node){
    if (!node || node.nodeType!==1) return;
    const tag = node.tagName.toLowerCase(), st = node.getAttribute('style')||'';
    let n = 1, cur = node;
    while (cur.children.length===1) {
      const ch = cur.firstElementChild;
      if (ch && ch.tagName.toLowerCase()===tag && (ch.getAttribute('style')||'')===st) { n++; cur = ch; }
      else break;
    }
    if (n>NEST_MAX) issues.push({ rule:'3.1 嵌套过深', sev:'error', tag,
      desc:'同标签+同样式连续嵌套 '+n+' 层（>'+NEST_MAX+'），公众号会自动删节点' });
    for (let k=0; k<node.children.length; k++) walkNest(node.children[k]);
  })(doc.body);
  /* v1.2.1 加粗/斜体未生效（裸星号残留）——移植自浏览器版：CommonMark 分隔符「左右翼」规则，
     中文紧贴标点（引号/书名号/「」/句号）时 ** 开/收失败；code/pre 内星号属合法，跳过。 */
  (function(){
    const seenB = {};
    all.forEach(el => {
      if (el.closest && el.closest('code,pre')) return;
      Array.prototype.forEach.call(el.childNodes, c => {
        if (c.nodeType !== 3) return;
        const t = c.textContent || '';
        const EMPH = /(?:\*\*|\*){1,3}/g; let m;
        while ((m = EMPH.exec(t)) !== null) {
          const key = m[0] + '|' + t.slice(Math.max(0,m.index-20), m.index+m[0].length+20);
          if (seenB[key]) continue; seenB[key] = 1;
          const ctx = t.slice(Math.max(0,m.index-28), m.index+m[0].length+28).replace(/\s+/g,' ');
          issues.push({ rule:'2.1 加粗/斜体未生效', sev:'warn', tag:el.tagName,
            desc:'正文里残留裸星号「'+m[0]+'」：「…'+ctx+'…」。多半是 ** 紧贴中文标点（引号/书名号/「」/句号）导致开/收失败。'+
                 '改法：把标点移到标记外，或在 ** 前加空格，或整句独立成行' });
        }
      });
    });
  })();
  /* v1.2.1 行内代码含完整链接：微信编辑器会把代码里的 URL 自动转成可点链接，破坏代码样式；
     且长代码不可断行，会引发公众号默认两端对齐的整行拉伸。 */
  doc.body.querySelectorAll('code').forEach(el => {
    if (el.closest && el.closest('pre')) return;
    if (/https?:\/\//i.test(el.textContent||''))
      issues.push({ rule:'2.2 代码内含链接', sev:'warn', tag:'code',
        desc:'行内代码里有完整 URL——微信编辑器会把它自动转成可点链接，破坏代码样式；长代码不可断行，还会引发两端对齐拉伸。'+
             '改法：命令放代码样式，URL 移到代码外（普通文本或手动链接）' });
  });
  return issues;
}

/* ===== 一键复制页（浏览器端：一键复制 + 二次微调栏 + 品牌位） ===== */
const VERSION = '1.2.8';
const COLOR_KEYS = ['ORANGE','DEEP','EMBER','STRONG','CHIP','LINK','BROWN','TAN','TEXT','TEXT2','TXTQ','WARMBG','WARMBG2','CODEBG','CODE','ZEBRA','LIST2','BORDER','PTEYE','PTNOTE'];
const ALERT_ORDER = ['NOTE','TIP','IMPORTANT','WARNING','CAUTION'];
function themeColorList(t){
  const th = THEMES[t], C = th.C;
  const list = COLOR_KEYS.map(k => C[k] || C.EMBER);
  ALERT_ORDER.forEach(a => { list.push(th.alerts[a][0], th.alerts[a][1]); });
  return list;
}
/* 深色（夜读）调色板：与 themeColorList 顺序一一对应（20 个主色 + 5 组警告块 bg/border） */
const DARK_LIST = ['#ff6a1a','#ece7de','#ff8a4d','#ff7a3d','#ff6a3d','#ff9459','#c9a06a','#b39872','#d8d2c8','#a89f92','#b3a996',
  '#2a241c','#26201a','#33291e','#ffb37a','#221e19','#ff8a3d','#3a332a','#ff9a4d','#d8cbb4',
  '#2a241c','#ff6a1a','#26211a','#c9a06a','#2b211c','#ff7a3d','#2a2519','#e0a13d','#2e211f','#ff6a5a'];

function makeCopyPage(html, title, opts = {}) {
  const escTitle = title.replace(/&/g,'&amp;').replace(/</g,'&lt;');
  const palettes = {};
  ['orangeink','inkblue','pine','gold','haitang'].forEach(t => { palettes[t] = themeColorList(t); });
  palettes.dark = DARK_LIST;
  const optTheme = opts.theme || 'orangeink', optZoom = opts.zoom || 1, optPad = opts.pad == null ? 14 : opts.pad;
  const themeOpts = [['orangeink','橙墨 · 炭黑×亮橙'],['inkblue','墨蓝 × 朱砂'],['pine','松烟 × 陶土'],['gold','石墨 × 鎏金'],['haitang','海棠 × 黛蓝 · 小说']]
    .map(([v,n]) => '<option value="'+v+'"'+(v===optTheme?' selected':'')+'>'+n+'</option>').join('');
  const zoomOpts = [['0.94','小'],['1','标准'],['1.06','大']]
    .map(([v,n]) => '<option value="'+v+'"'+(parseFloat(v)===optZoom?' selected':'')+'>'+n+'</option>').join('');
  const padOpts = [['0','无'],['14','窄 14'],['22','宽 22']]
    .map(([v,n]) => '<option value="'+v+'"'+(parseInt(v,10)===optPad?' selected':'')+'>'+n+'</option>').join('');
  return '<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n<meta charset="UTF-8">\n'+
'<meta name="viewport" content="width=device-width,initial-scale=1">\n'+
'<title>橙墨复制页 · '+escTitle+'</title>\n'+
'<style>\n'+
'body{margin:0;background:#efeae3;font-family:-apple-system,"Segoe UI","Microsoft YaHei",sans-serif}\n'+
'#bar{position:sticky;top:0;background:#1c1917;color:#fff;padding:8px 16px;z-index:9}\n'+
'#barTop{display:flex;gap:12px;align-items:center}\n'+
'#bar b{font-size:14px}#bar small{color:#bbb;font-size:12px}\n'+
'#copyBtn{margin-left:auto;background:#ff5a00;color:#fff;border:none;border-radius:6px;padding:9px 22px;font-size:14px;font-weight:700;cursor:pointer}\n'+
'#copyBtn:hover{filter:brightness(1.08)}\n'+
'#barOpt{display:flex;gap:14px;align-items:center;margin-top:7px;flex-wrap:wrap;font-size:12px;color:#ccc}\n'+
'#barOpt select{background:#2a2622;color:#fff;border:1px solid #555;border-radius:4px;padding:2px 4px;font-size:12px}\n'+
'#barOpt label{display:flex;gap:4px;align-items:center;cursor:pointer}\n'+
'#stage{max-width:677px;margin:20px auto;background:#fff;padding:20px 18px;box-shadow:0 2px 12px rgba(0,0,0,.08)}\n'+
'body.phone #stage{max-width:375px;padding:14px 10px}\n'+
'#tip{color:#7ddb8f;font-size:13px;display:none}\n'+
'#foot{max-width:677px;margin:0 auto 30px;text-align:center;color:#8a8177;font-size:12px;letter-spacing:.5px}\n'+
'#foot b{color:#c94a00}\n'+
'</style>\n</head>\n<body>\n'+
'<div id="bar">\n'+
'<div id="barTop"><b>橙墨 · 一键复制</b><small>orangeink · oimd v'+VERSION+'</small><span id="tip">✓ 已复制（到公众号编辑器 Ctrl+V）</span>'+
'<button id="copyBtn">一键复制到公众号</button></div>\n'+
'<div id="barOpt">\n'+
'<label>主题 <select id="optTheme">'+themeOpts+'</select></label>\n'+
'<label>字号 <select id="optZoom">'+zoomOpts+'</select></label>\n'+
'<label>边距 <select id="optPad">'+padOpts+'</select></label>\n'+
'<label><input type="checkbox" id="optDark"> 深色（夜读配色）</label>\n'+
'<label><input type="checkbox" id="optPhone" checked> 手机预览</label>\n'+
'</div>\n</div>\n'+
'<div id="stage">'+html+'\n</div>\n'+
'<div id="foot">由 <b>orangeink</b> · oimd v'+VERSION+' 排版引擎生成 · github.com/aladooo/orangeink</div>\n'+
'<script>\n'+
'(function(){\n'+
'  var ORIG=document.getElementById("stage").innerHTML;\n'+
'  var P='+JSON.stringify(palettes)+';\n'+
'  var st={theme:"'+optTheme+'",zoom:'+optZoom+',pad:'+optPad+',dark:false,phone:true};\n'+
'  function rgbOf(hex){var m=/^#([0-9a-f]{6})$/i.exec(hex);if(!m)return null;var v=m[1];'+
'    return parseInt(v.slice(0,2),16)+","+parseInt(v.slice(2,4),16)+","+parseInt(v.slice(4,6),16);}\n'+
'  function mapColors(html,from,to,isDark){\n'+
'    var D=from[1];\n'+
'    if(isDark){\n'+
'      html=html.split("background:"+D+";color:#fff").join("background:"+to[1]+";color:#1c1917");\n'+
'      html=html.split("background:"+D+";border-radius:6px").join("background:#2a2622;border-radius:6px");\n'+
'    }\n'+
'    for(var i=0;i<from.length;i++){\n'+
'      if(!from[i]||from[i]===to[i])continue;\n'+
'      html=html.split(from[i]).join(to[i]);\n'+
'      var r1=rgbOf(from[i]),r2=rgbOf(to[i]);\n'+
'      if(r1&&r2)html=html.split("rgba("+r1+",").join("rgba("+r2+",");\n'+
'    }\n'+
'    return html;\n'+
'  }\n'+
'  function mapZoom(html,z){return html.replace(/(font-size|line-height):([\\d.]+)px/g,function(m,p,v){'+
'    return p+":"+Math.round(parseFloat(v)*z*10)/10+"px";});}\n'+
'  function mapPad(html,pad){\n'+
'    if(/padding:0 \\d+px;box-sizing:border-box/.test(html))\n'+
'      return html.replace(/padding:0 \\d+px;box-sizing:border-box/,'+
'        pad>0?("padding:0 "+pad+"px;box-sizing:border-box"):"box-sizing:border-box");\n'+
'    return pad>0?html.replace("box-sizing:border-box","padding:0 "+pad+"px;box-sizing:border-box"):html;\n'+
'  }\n'+
'  function apply(){\n'+
'    var html=ORIG;\n'+
'    if(st.theme!=="'+optTheme+'")html=mapColors(html,P["'+optTheme+'"],P[st.theme],false);\n'+
'    if(st.dark){html=mapColors(html,P[st.theme],P.dark,true);'+
'      html=html.replace("box-sizing:border-box","box-sizing:border-box;background:#141312");}\n'+
'    if(st.zoom!==1)html=mapZoom(html,st.zoom);\n'+
'    html=mapPad(html,st.pad);\n'+
'    var stage=document.getElementById("stage");\n'+
'    stage.innerHTML=html;\n'+
'    stage.style.background=st.dark?"#141312":"#fff";\n'+
'    document.body.className=st.phone?"phone":"";\n'+
'  }\n'+
'  function bind(id,key,parse){var el=document.getElementById(id);'+
'    el.addEventListener("change",function(){st[key]=parse(el.value);apply();});}\n'+
'  bind("optTheme","theme",function(v){return v;});\n'+
'  bind("optZoom","zoom",parseFloat);\n'+
'  bind("optPad","pad",parseInt);\n'+
'  ["optDark","optPhone"].forEach(function(id){var el=document.getElementById(id);'+
'    var k=id==="optDark"?"dark":"phone";'+
'    el.addEventListener("change",function(){st[k]=el.checked;apply();});});\n'+
'  apply();\n'+
'  window.__oimd={apply:apply,state:st,original:function(){return ORIG;}};\n'+
'  document.getElementById("copyBtn").addEventListener("click", function(){\n'+
'    var HTML=document.getElementById("stage").innerHTML;\n'+
'    var TEXT=document.getElementById("stage").innerText.trim();\n'+
'    var done=function(){var t=document.getElementById("tip");t.style.display="inline";setTimeout(function(){t.style.display="none"},2600);};\n'+
'    var ok=false;\n'+
'    function onCopy(e){try{e.clipboardData.setData("text/html",HTML);e.clipboardData.setData("text/plain",TEXT);e.preventDefault();ok=true;}catch(err){ok=false;}}\n'+
'    document.addEventListener("copy",onCopy,true);\n'+
'    var range=document.createRange();range.selectNodeContents(document.getElementById("stage"));\n'+
'    var sel=window.getSelection();sel.removeAllRanges();sel.addRange(range);\n'+
'    try{ok=document.execCommand("copy")&&ok;}catch(e){}\n'+
'    sel.removeAllRanges();\n'+
'    document.removeEventListener("copy",onCopy,true);\n'+
'    if(ok){done();return;}\n'+
'    if(navigator.clipboard&&window.ClipboardItem){\n'+
'      navigator.clipboard.write([new ClipboardItem({"text/html":new Blob([HTML],{type:"text/html"}),"text/plain":new Blob([TEXT],{type:"text/plain"})})]).then(done).catch(function(){alert("复制失败，请手动全选复制");});\n'+
'      return;\n'+
'    }\n'+
'    alert("复制失败，请手动全选复制");\n'+
'  });\n'+
'})();\n'+
'<\/script>\n</body>\n</html>\n';
}

/* ===== CLI ===== */
function parseArgs(argv) {
  // 查找表式解析：每个 flag 声明取值行为，无分支链，便于审计（响应 ClawHub "Tool Parameter Abuse" 误报）
  const args = { _:[] };
  const VAL = { // 带值的 flag：flag → 赋值函数
    '-o': v => { args.out = v; }, '--out': v => { args.out = v; },
    '--copy-page': v => { args.copyPage = v; }, '--draft': v => { args.draft = v; },
    '--title': v => { args.title = v; }, '--author': v => { args.author = v; },
    '--digest': v => { args.digest = v; }, '--theme': v => { args.theme = v; },
    '--zoom': v => { args.zoom = parseFloat(v); }, '--pad': v => { args.pad = parseInt(v, 10); },
    '--meta': v => { args.meta = v; },
  };
  const BOOL = { // 布尔开关：不消费后续参数
    '--quiet': () => { args.quiet = true; }, '--no-check': () => { args.noCheck = true; },
  };
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (VAL[a]) { i += 1; VAL[a](argv[i]); }
    else if (BOOL[a]) { BOOL[a](); }
    else { args._.push(a); }
  }
  return args;
}

function main() {
  const args = parseArgs(process.argv);
  if (!args._.length) {
    console.error('用法: node render.mjs <input.md> [-o out.html] [--copy-page f] [--draft f] [--theme t] [--zoom n] [--pad n] [--meta f]');
    process.exit(1);
  }
  const input = path.resolve(args._[0]);
  const mdSrc = fs.readFileSync(input, 'utf-8');
  const base = path.basename(input, path.extname(input));

  let result;
  try {
    result = renderOrangeink(mdSrc, { theme:args.theme||'orangeink', zoom:args.zoom||1, pad:args.pad==null?14:args.pad });
  } catch (err) {
    console.error('渲染失败:', err.message);
    process.exit(1);
  }

  const outHtml = args.out || input.replace(/\.(md|markdown|txt)$/i,'') + '.oimd.html';
  fs.writeFileSync(outHtml, result.html, 'utf-8');

  const outCopy = args.copyPage || (args.copyPage===null ? null : outHtml.replace(/\.html$/,'') + '.copy.html');
  if (args.copyPage !== undefined && outCopy) {
    const pageOpts = { theme: args.theme||'orangeink', zoom: args.zoom||1, pad: args.pad==null?14:args.pad };
    fs.writeFileSync(outCopy, makeCopyPage(result.html, args.title || result.meta.title || base, pageOpts), 'utf-8');
  }

  const issues = args.noCheck ? [] : checkStatic(result.html);
  const errCount = issues.filter(i => i.sev==='error').length;

  /* draft JSON（公众号 draft/add 请求体；图片需先传素材库——见 SKILL.md 图片章节） */
  if (args.draft) {
    const draft = {
      articles: [{
        title: args.title || result.meta.title || base,
        author: args.author || '登叔',
        digest: args.digest || result.meta.digest,
        content: result.html,
        need_save_comment: 0,
        only_fans_can_comment: 0
      }]
    };
    fs.writeFileSync(args.draft, JSON.stringify(draft, null, 2), 'utf-8');
  }

  if (args.meta) fs.writeFileSync(args.meta, JSON.stringify({ ...result.meta, check: issues }, null, 2), 'utf-8');

  if (!args.quiet) {
    console.log('✓ 已渲染: ' + outHtml);
    if (args.copyPage !== undefined && outCopy) console.log('✓ 复制页: ' + outCopy);
    if (args.draft) console.log('✓ draft:  ' + args.draft);
    console.log('  正文(公众号口径) ' + result.meta.charsWechat + ' 字 / 源文 ' + result.meta.charsSource + ' 字 / 图片 ' + result.meta.images.length + ' 张 / 脚注 ' + result.meta.footnotes.refs);
    if (result.meta.images.length) {
      console.log('  ⚠ 图片清单（draft/add 会过滤外链图片，发布前需传素材库换链接）:');
      result.meta.images.forEach(im => console.log('    - ' + im.src));
    }
  }
  console.log('自检: ' + (issues.length===0 ? '✓ 0 项（静态规则全过）' : issues.length + ' 项（error ' + errCount + ' / warn ' + (issues.length-errCount) + '）'));
  issues.forEach(it => console.log('  [' + it.sev + '] ' + it.rule + ' <' + (it.tag||'') + '>: ' + it.desc));
  process.exit(errCount>0 ? 2 : 0);
}

const isMain = process.argv[1] && path.resolve(process.argv[1]) === path.resolve(fileURLToPath(import.meta.url));
if (isMain) main();
