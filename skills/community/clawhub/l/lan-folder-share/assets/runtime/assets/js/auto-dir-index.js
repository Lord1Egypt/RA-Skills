/* Locale: zh-CN (documented in SKILL.md metadata) — part of "Lan Folder Share",
 * a LAN knowledge-base tool for Chinese-speaking users; UI text and comments
 * are Chinese by design. 语言声明：本文件面向中文用户，界面与注释默认中文。
 * ---------------------------------------------------------------------------
 * 知识库目录页 —— docsify 插件（独立运行，不依赖 docsify 插件 API）
 *
 * 目录页显示 README 正文（如果有），并在正文下方列出本目录的「非 md 文件」
 * （表格 / 图片 / 视频 / 附件）。md 文档与子目录不在此列出，
 * 由左侧动态侧边栏负责导航，避免与正文重复、保持页面干净。
 *  - 有 README.md 的目录：正文照常显示，文件列表跟在正文下方。
 *  - 无 README.md 的目录：隐藏 docsify 默认的英文 404 正文，只显示文件列表。
 *  - 根路由（仓库首页）缺 README 时同样按目录页处理，不显示英文 404。
 *  - 非目录路由（内容文件页）：不显示文件列表。
 *
 * 可靠性要点：
 *  - 单例 host 节点：全站只有一个列表容器。切换路由只覆盖其内容，绝不重复/残留。
 *  - 同目录已填充则跳过重建（data-kb-dk + 子元素守卫），避免与 MutationObserver
 *    互相触发形成空转循环。
 *  - 列表容器放在 .markdown-section 之外（挂在 .content 下）：doc-inline 只扫描
 *    .markdown-section，不会把文件链接误铺开；table-preview 扫描 .content，
 *    目录页的表格链接仍能原地铺开成可查询表格。
 *
 * 依赖：window.KB_DIR_TREE（由 dynamic-data.js 从服务端 /api/tree 实时获取）
 */
(function () {
  'use strict';

  var doneSig = '__none__';          // 最近一次成功渲染的目录 key（README 模式幂等守卫）
  var lastSectionNode = null;        // 最近一次成功渲染时对应的 .markdown-section 节点
  var runTimer = null;
  var host = null;                   // 单例文件列表容器（全站唯一）
  var loadWaits = 0;                 // 目录路由连续「等待加载」次数（超时视为最终 404）

  var IMG_RE = /\.(jpe?g|png|gif|svg|webp|bmp)$/i;
  var VIDEO_RE = /\.(mp4|mov|webm)$/i;
  var AUDIO_RE = /\.(mp3|wav|ogg|m4a|aac|flac|wma)$/i;
  var HTML_RE = /\.html?(\?.*)?$/i;   // .htm / .html
  // 文档附件：可在右侧内容区预览的 Word / PDF / PPT（由 office-viewer.js 接管）
  var OFFICE_RE = /\.(pdf|docx?|pptx?)(\?.*)?$/i;
  var OFFICE_LABEL = { pdf: 'PDF', doc: 'WORD', docx: 'WORD', ppt: 'PPT', pptx: 'PPT' };
  // 字体文件（设计资源）：浏览器无内嵌预览，列出后在新标签打开 / 下载
  var FONT_RE = /\.(ttf|otf|woff2?|eot)(\?.*)?$/i;
  var FONT_LABEL = { ttf: 'TTF', otf: 'OTF', woff: 'WOFF', woff2: 'WOFF2', eot: 'EOT' };

  function el(tag, cls, html) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (html != null) n.innerHTML = html;
    return n;
  }
  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }
  function enc(p) { return p.split('/').map(encodeURIComponent).join('/'); }
  function siteBase() {
    return location.pathname.replace(/[^/]*$/, '');
  }
  function mediaSrc(dirKey, name) {
    return siteBase() + enc(dirKey ? dirKey + '/' + name : name);
  }

  function isAutoIndex(text) {
    return text && text.indexOf('自动生成的目录索引') > -1;
  }
  function isLoading(section) {
    if (!section) return false;
    var t = (section.textContent || '').replace(/\s+/g, '');
    return t === '' || /^Loading$/i.test(t) || /^加载中$/i.test(t);
  }

  function routeRaw() {
    var p = decodeURIComponent((location.hash || '').replace(/^#\/?/, ''));
    var q = p.indexOf('?'); if (q > -1) p = p.slice(0, q);
    var h = p.indexOf('#'); if (h > -1) p = p.slice(0, h);
    return p.replace(/\/+$/, '');
  }
  function dirKeyOf(raw) {
    if (/\/(README|INDEX)$/i.test(raw)) return raw.replace(/\/(README|INDEX)$/i, '');
    return raw;
  }
  function setSectionHidden(section, hide) {
    if (section) section.style.display = hide ? 'none' : '';
  }

  // 目录页平铺「可预览」文件：文档附件(Word/PDF/PPT) 与 网页报告(.html) → 入口列表
  // （点击后在右侧内容区预览）；图片 → 缩略图网格（点击大图预览）；
  // 视频 → 内联播放；音频 → 内联播放器。
  // md 文档、表格与子目录由左侧侧边栏导航，不在这里重复。
  function buildFileList(dirKey) {
    var T = window.KB_DIR_TREE;
    if (!T) return null;
    var children = T[dirKey];
    if (!children || !children.length) return null;

    var imgs = [], vids = [], audios = [], htmls = [], offices = [], fonts = [];
    children.forEach(function (c) {
      if (c.type === 'dir') return;
      if (c.ext === 'md') return;
      if (IMG_RE.test(c.name)) imgs.push(c);
      else if (VIDEO_RE.test(c.name)) vids.push(c);
      else if (AUDIO_RE.test(c.name)) audios.push(c);
      else if (HTML_RE.test(c.name)) htmls.push(c);
      else if (OFFICE_RE.test(c.name)) offices.push(c);
      else if (FONT_RE.test(c.name)) fonts.push(c);
    });
    if (!imgs.length && !vids.length && !audios.length && !htmls.length &&
        !offices.length && !fonts.length) return null;

    var wrap = el('div', 'kb-dir-index');
    wrap.setAttribute('data-kb-dk', dirKey);

    // 文档附件（Word / PDF / PPT）→ 入口列表：pdf 内嵌 iframe、
    // docx 由 office-viewer 用 mammoth 转 HTML、其余给下载卡
    if (offices.length) {
      wrap.appendChild(el('div', 'kb-dir-index-head', '文档附件（' + offices.length + '）'));
      var olist = el('div', 'kb-dir-office-list');
      offices.forEach(function (c) {
        var oExt = String(c.name).split('.').pop().toLowerCase();
        var oa = el('a', 'kb-dir-office-item');
        oa.href = '#/' + enc(dirKey ? dirKey + '/' + c.name : c.name);
        oa.title = '在页面内预览：' + c.name;
        oa.appendChild(el('span', 'kb-dir-office-ext', OFFICE_LABEL[oExt] || oExt.toUpperCase()));
        oa.appendChild(el('span', 'kb-dir-office-name', esc(c.name)));
        olist.appendChild(oa);
      });
      wrap.appendChild(olist);
    }

    // 字体文件（设计资源）→ 入口列表：浏览器无内嵌预览，点击在新标签打开 / 下载
    if (fonts.length) {
      wrap.appendChild(el('div', 'kb-dir-index-head', '字体文件（' + fonts.length + '）'));
      var flist = el('div', 'kb-dir-office-list');
      fonts.forEach(function (c) {
        var fExt = String(c.name).split('.').pop().toLowerCase();
        var fa = el('a', 'kb-dir-office-item');
        fa.href = enc(dirKey ? dirKey + '/' + c.name : c.name);
        fa.target = '_blank';
        fa.rel = 'noopener';
        fa.title = '打开 / 下载字体文件：' + c.name;
        fa.appendChild(el('span', 'kb-dir-office-ext', FONT_LABEL[fExt] || fExt.toUpperCase()));
        fa.appendChild(el('span', 'kb-dir-office-name', esc(c.name)));
        flist.appendChild(fa);
      });
      wrap.appendChild(flist);
    }

    // 网页报告（.html 自包含页面）→ 入口列表，点击后在右侧内容区 iframe 预览
    if (htmls.length) {
      wrap.appendChild(el('div', 'kb-dir-index-head', '网页报告（' + htmls.length + '）'));
      var hlist = el('div', 'kb-dir-html-list');
      htmls.forEach(function (c) {
        var a = el('a', 'kb-dir-html-item', '🖥️ ' + esc(c.name));
        a.href = '#/' + enc(dirKey ? dirKey + '/' + c.name : c.name);
        a.title = '在页面内预览：' + c.name;
        hlist.appendChild(a);
      });
      wrap.appendChild(hlist);
    }

    if (imgs.length === 1) {
      // 单图目录：默认放大、完整展示全图（无需手动点击放大）。
      // 净化模式：无外层灰底容器 / 卡片边框 / 底部文件名条，仅留标题。
      // 点击图片仍可进入灯箱查看原始大小（此时无前后切换按钮）。
      wrap.classList.add('kb-dir-index-single');
      // 单图净化：不显示"照片预览"标题与文件名底条，让图片成为页面上唯一主体
      var one = imgs[0];
      var srcOne = mediaSrc(dirKey, one.name);
      var single = el('div', 'kb-dir-media kb-dir-single');
      var sc = el('a', 'kb-dir-media-card kb-type-img kb-single-card');
      sc.href = srcOne;                    // 兜底：无 JS 点击时打开原图
      sc.title = one.name + '（点击查看大图）';
      var si = el('img');
      si.alt = one.name;
      si.src = srcOne;
      sc.appendChild(si);
      // 单图目录不显示底部文件名条（"底框"），文件名已通过 alt / title 保留
      sc.addEventListener('click', function (e) {
        e.preventDefault();                // 拦截：进入页面内大图查看
        openLightbox([{ src: srcOne, name: one.name }], 0);
      });
      single.appendChild(sc);
      wrap.appendChild(single);
    } else if (imgs.length > 1) {
      wrap.appendChild(el('div', 'kb-dir-index-head', '照片预览（' + imgs.length + '）'));
      var grid = el('div', 'kb-dir-media');
      // 同目录全部图片组成画廊：lightbox 支持键盘 ←/↑ →/↓ 切换
      var items = imgs.map(function (c) {
        return { src: mediaSrc(dirKey, c.name), name: c.name };
      });
      imgs.forEach(function (c, i) {
        var src = items[i].src;
        var card = el('a', 'kb-dir-media-card kb-type-img');
        card.href = src;                    // 兜底：无 JS 点击时打开原图
        var img = el('img');
        img.loading = 'lazy';               // 照片较多时按需加载
        img.alt = c.name;
        img.src = src;
        card.appendChild(img);
        card.appendChild(el('div', 'kb-dir-media-name', esc(c.name)));
        card.addEventListener('click', function (e) {
          e.preventDefault();              // 拦截：改为页面内画廊预览
          openLightbox(items, i);
        });
        grid.appendChild(card);
      });
      wrap.appendChild(grid);
    }

    if (vids.length) {
      wrap.appendChild(el('div', 'kb-dir-index-head', '视频（' + vids.length + '）'));
      var vgrid = el('div', 'kb-dir-media');
      vids.forEach(function (c) {
        var card = el('div', 'kb-dir-media-card kb-type-video');
        var v = el('video');
        v.src = mediaSrc(dirKey, c.name);
        v.controls = true;
        v.preload = 'metadata';
        card.appendChild(v);
        card.appendChild(el('div', 'kb-dir-media-name', esc(c.name)));
        vgrid.appendChild(card);
      });
      wrap.appendChild(vgrid);
    }

    if (audios.length) {
      wrap.appendChild(el('div', 'kb-dir-index-head', '音频（' + audios.length + '）'));
      var agrid = el('div', 'kb-dir-media');
      audios.forEach(function (c) {
        var card = el('div', 'kb-dir-media-card kb-type-audio');
        var au = el('audio');
        au.src = mediaSrc(dirKey, c.name);
        au.controls = true;
        au.preload = 'metadata';
        card.appendChild(au);
        card.appendChild(el('div', 'kb-dir-media-name', esc(c.name)));
        agrid.appendChild(card);
      });
      wrap.appendChild(agrid);
    }
    return wrap;
  }

  /* ---------- 图片画廊预览（lightbox，样式见 dir-index.css） ----------
   * 点击目录缩略图打开，同目录全部图片组成画廊：
   *   - 键盘 ← / ↑ 上一张，→ / ↓ 下一张（首尾环绕）；Esc / ✕ / 点击遮罩空白处关闭
   *   - 点击大图左半区上一张、右半区下一张；点图本身不关闭（便于查看细节）
   *   - 相邻图预加载 + 淡入切换，避免闪白 / 半载
   */
  var gallery = null;   // { items, index, imgEl, nameEl, countEl }
  var showSeq = 0;      // 切换序号：快速连按时丢弃过期预载回调，保证图与文件名同步
  function onKeydown(e) {
    if (e.key === 'Escape') { closeLightbox(); return; }
    if (!gallery || !gallery.items.length) return;
    if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') { e.preventDefault(); galleryPrev(); }
    else if (e.key === 'ArrowRight' || e.key === 'ArrowDown') { e.preventDefault(); galleryNext(); }
  }
  function galleryPreload(i) {
    var n = gallery.items.length; if (n < 2) return;
    [1, -1].forEach(function (d) {
      var it = gallery.items[(i + d + n) % n];
      var im = new Image(); im.src = it.src;
    });
  }
  function galleryShow(i) {
    var g = gallery; if (!g || !g.items.length) return;
    g.index = (i + g.items.length) % g.items.length;
    var it = g.items[g.index];
    var seq = ++showSeq;
    g.nameEl.textContent = it.name;
    g.countEl.textContent = (g.index + 1) + ' / ' + g.items.length;
    g.imgEl.classList.remove('kb-loaded');
    var pre = new Image();            // 目标图预载完成再换 src，避免切换闪白/半载
    pre.onload = function () {
      if (seq !== showSeq || !gallery) return;   // 已被更新的切换取代，丢弃
      g.imgEl.src = it.src;
      g.imgEl.alt = it.name;
      g.imgEl.title = '按 ←/↑ 上一张、→/↓ 下一张；Esc 关闭';
      g.imgEl.classList.add('kb-loaded');
      galleryPreload(g.index);
    };
    pre.onerror = function () {
      if (seq === showSeq && gallery) g.imgEl.classList.add('kb-loaded');
    };
    pre.src = it.src;
  }
  function galleryNext() { if (gallery) galleryShow(gallery.index + 1); }
  function galleryPrev() { if (gallery) galleryShow(gallery.index - 1); }
  function openLightbox(items, index) {
    closeLightbox();
    gallery = { items: items || [], index: 0 };

    var mask = el('div', 'kb-img-mask');
    var box = el('div', 'kb-img-box');
    var img = el('img');
    img.className = 'kb-img-full';
    box.appendChild(img);
    box.appendChild(el('div', 'kb-img-count', ''));
    box.appendChild(el('div', 'kb-img-meta', ''));

    var prev = el('button', 'kb-img-nav kb-img-prev', '‹');
    prev.type = 'button'; prev.title = '上一张（← / ↑）';
    prev.addEventListener('click', function (e) { e.stopPropagation(); galleryPrev(); });
    var next = el('button', 'kb-img-nav kb-img-next', '›');
    next.type = 'button'; next.title = '下一张（→ / ↓）';
    next.addEventListener('click', function (e) { e.stopPropagation(); galleryNext(); });
    // 仅单图（或当前仅一张）时不显示前后切换按钮
    if (gallery.items.length > 1) { box.appendChild(prev); box.appendChild(next); }

    var close = el('button', 'kb-img-close', '✕');
    close.type = 'button';
    close.title = '关闭（Esc）';
    close.addEventListener('click', function (e) { e.stopPropagation(); closeLightbox(); });
    box.appendChild(close);

    // 大图左右半区点击切换；只点遮罩空白处（padding 区）关闭
    img.addEventListener('click', function (e) {
      e.stopPropagation();
      var r = this.getBoundingClientRect();
      if (e.clientX - r.left < r.width * 0.42) galleryPrev();
      else galleryNext();
    });

    mask.appendChild(box);
    mask.addEventListener('click', function (e) { if (e.target === mask) closeLightbox(); });
    document.addEventListener('keydown', onKeydown);
    document.body.appendChild(mask);

    gallery.imgEl = box.querySelector('.kb-img-full');
    gallery.countEl = box.querySelector('.kb-img-count');
    gallery.nameEl = box.querySelector('.kb-img-meta');
    gallery.box = box;

    // 图片加载完成后按原图比例计算「适应屏幕」尺寸并定位居中，
    // 记录 data-fit-w/h 供 image-zoom.js 以该基准做 width/height 缩放（清晰，无 transform）。
    img.addEventListener('load', function () {
      if (!gallery || gallery.imgEl !== img) return;
      var nw = img.naturalWidth, nh = img.naturalHeight;
      if (!nw || !nh) return;
      var availW = Math.min(window.innerWidth * 0.94, window.innerWidth - 56) || 1;
      var availH = Math.min(window.innerHeight * 0.84, window.innerHeight - 56) || 1;
      var s = Math.min(availW / nw, availH / nh, 1);
      var fw = nw * s, fh = nh * s;
      box.style.width = fw + 'px';
      box.style.height = fh + 'px';
      img.style.width = fw + 'px';
      img.style.height = 'auto';   // 高度由浏览器按原图比例自动算，绝不拉伸变形
      img.style.left = '0px';
      img.style.top = '0px';
      img.setAttribute('data-fit-w', fw);
      img.setAttribute('data-fit-h', fh);
    });

    galleryShow(index);
  }
  function closeLightbox() {
    var m = document.querySelector('.kb-img-mask');
    if (m) m.remove();
    gallery = null;
    document.removeEventListener('keydown', onKeydown);
  }

  function ensureHost(main) {
    if (!host) host = el('div', 'kb-dir-index-host');
    if (host.parentNode !== main) main.appendChild(host);
    return host;
  }
  // 目录是否「完全无内容」：无 md 文档、无子目录、无任何非 md 文件
  function isTrulyEmptyDir(dirKey) {
    var T = window.KB_DIR_TREE;
    var children = T && T[dirKey];
    return !children || !children.length;
  }

  /* ---------- 空页面缺省效果（内容区没有可展示内容时的创意占位） ---------- */
  function buildEmptyState() {
    var wrap = el('div', 'kb-dir-empty');
    wrap.innerHTML = [
      '<div class="kb-dir-empty-art">',
      '<svg viewBox="0 0 200 150" role="img" aria-label="空目录">',
      '<path d="M96 18l3.4 6.9 7.6 1.1-5.5 5.4 1.3 7.6-6.8-3.6-6.8 3.6 1.3-7.6-5.5-5.4 7.6-1.1z" fill="#ffcf5c"/>',
      '<circle cx="152" cy="34" r="3.2" fill="#ffcf5c" opacity=".85"/>',
      '<circle cx="42" cy="26" r="2.6" fill="#ffcf5c" opacity=".6"/>',
      '<circle cx="168" cy="64" r="2" fill="#ffcf5c" opacity=".5"/>',
      '<path d="M100 52c-3 9 3 14 0 21" stroke="#ffcf5c" stroke-width="2.4" fill="none" stroke-linecap="round" opacity=".7"/>',
      '<path d="M34 84l7-24h118l7 24z" fill="#f3f6fb" stroke="#ccd6e4" stroke-width="2"/>',
      '<path d="M41 84l7-24h104l7 24z" fill="#fbfdff"/>',
      '<path d="M36 84h128l-10 52H46z" fill="#e9eef7" stroke="#ccd6e4" stroke-width="2"/>',
      '<path d="M41 84h118l-9 48H50z" fill="#f6f9fd"/>',
      '<path d="M88 84h24v18H88z" fill="#fff3d1" opacity=".9"/>',
      '</svg>',
      '</div>',
      '<div class="kb-dir-empty-title">这里还空空的</div>',
      '<div class="kb-dir-empty-sub">在永恒的序言里，第一粒字符尚未落笔，墨香已开始流淌，<br>而你，有缘人，必将书写绝妙的华章。</div>',
      '<button type="button" class="kb-dir-empty-btn">🏠 回到首页</button>'
    ].join('');
    var btn = wrap.querySelector('.kb-dir-empty-btn');
    if (btn) btn.addEventListener('click', function () { window.location.hash = '#/'; });
    return wrap;
  }
  // 目录有 md 文档 / 子目录 / 文档类文件（由左侧导航承载），但无 README、无媒体 → 轻提示
  function buildSidebarHint() {
    return el('div', 'kb-dir-hint', '📚 本目录的文档与子目录请从左侧导航查看');
  }

  function fillHost(dk, mode) {
    // 同目录且已有内容 → 跳过重建（防止与 MutationObserver 互相触发空转）
    if (host.getAttribute('data-kb-dk') === dk && host.childElementCount > 0) return;
    host.innerHTML = '';
    host.setAttribute('data-kb-dk', dk);
    var listing = buildFileList(dk);
    if (listing) { host.appendChild(listing); return; }
    if (mode === '404') {
      // 无 README 且无可展示附件：真空目录 → 创意空状态；有 md/子目录 → 侧边栏引导
      if (isTrulyEmptyDir(dk)) host.appendChild(buildEmptyState());
      else host.appendChild(buildSidebarHint());
    }
  }
  function showHost(main, dk, mode) {
    var h = ensureHost(main);
    fillHost(dk, mode);
    // 无非 md 文件的目录：隐藏空容器，避免出现空白盒子
    h.style.display = h.childElementCount > 0 ? '' : 'none';
    return h;
  }

  function run() {
    try {
      var raw = routeRaw();
      var dk = dirKeyOf(raw);
      var main = document.querySelector('.content') || document.querySelector('main') || document.body;
      if (!main) return;

      var T = window.KB_DIR_TREE;
      // 目录路由判定：目录树中存在的路径，或根路由（''，仓库首页）。
      // 根路由最终按哪种模式渲染由下方正文状态决定：
      //   根有 README → 正常首页正文；根无 README（--no-readme / 纯文件目录）→
      //   复用目录页逻辑（平铺根目录文件 / 空态提示），不再向用户暴露
      //   docsify 默认英文 404。
      var isDirRoute = T && (dk === '' || (dk in T));
      if (!isDirRoute) {
        // 非目录路由（内容文件页 / 未知路径）：隐藏并清空残留文件列表
        if (host && host.parentNode) { host.style.display = 'none'; host.innerHTML = ''; }
        // 恢复正文显示：docsify 复用同一个 .markdown-section 节点渲染新页面，
        // 上一页若是 404 目录可能残留 display:none，不恢复会导致正文被隐藏（空白页）
        var s2 = document.querySelector('.markdown-section');
        setSectionHidden(s2, false);
        doneSig = '__none__'; lastSectionNode = null;
        return;
      }

      var section = document.querySelector('.markdown-section');
      if (isLoading(section)) {
        // docsify 仍在加载（或目录无 README 时最终渲染为空）。
        // 有限次等待后仍未出内容 → 视为最终态（空 README / 加载失败），
        // 继续往下走：渲染文件列表 / 缺省效果，并隐藏空白正文，避免整页空白。
        if (loadWaits < 12) { loadWaits++; setTimeout(scheduleRun, 150); return; }
        loadWaits = 0;
      }

      var is404 = section && (/404/i.test(section.textContent || '') || !section.textContent.trim());
      var autoIdx = section && isAutoIndex(section.textContent);
      var mode = (is404 || autoIdx) ? '404' : 'readme';

      if (mode === 'readme') {
        // 真实 README：正文照常显示 + 文件列表跟在下方。
        // 幂等：同一路由 + 正文节点未变 → 跳过，避免抖动/重复处理
        if (doneSig === dk && section === lastSectionNode) return;
        showHost(main, dk, mode);
        setSectionHidden(section, false);
        doneSig = dk; lastSectionNode = section;
        return;
      }

      // 无 README 或正文是残留自动索引：隐藏 docsify 的 404 噪音，只显示文件列表 / 缺省效果
      showHost(main, dk, mode);
      if (section) setSectionHidden(section, true);
      doneSig = dk; lastSectionNode = null;
    } catch (e) { /* 单次失败不影响页面 */ }
  }

  /* ---------- 触发：hashchange + .content 子树变化，均防抖后重跑 ---------- */
  function scheduleRun() {
    if (runTimer) clearTimeout(runTimer);
    runTimer = setTimeout(run, 120);
  }
  window.addEventListener('hashchange', scheduleRun);

  function attachObserver() {
    var t = document.querySelector('.content') || document.querySelector('main') || document.body;
    if (!t) { setTimeout(attachObserver, 200); return; }
    var mo = new MutationObserver(function () { scheduleRun(); });
    mo.observe(t, { childList: true, subtree: true });   // 捕获 docsify 在 .content 内的重渲染
  }
  attachObserver();

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', scheduleRun);
  else scheduleRun();
  // 目录树数据就绪（dynamic-data.js 从 /api/tree 拉取完成）后重跑一次
  window.addEventListener('KB_DATA_READY', scheduleRun);
  setTimeout(scheduleRun, 400);
  setTimeout(scheduleRun, 1500);
  setTimeout(scheduleRun, 3000);   // 兜底：应对极慢的首次渲染 / 多次重渲染
})();
