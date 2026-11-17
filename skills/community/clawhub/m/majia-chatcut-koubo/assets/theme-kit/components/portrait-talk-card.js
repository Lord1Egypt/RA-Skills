(function (global) {
  "use strict";

  const THEMES = [{"id": "deep-space-blue", "name": "深空蓝", "description": "专业稳重，科技感强", "layout": "diagonal-tech", "mode": "dark", "palette": ["#0B132B", "#1E3A8A", "#60A5FA", "#E2E8F0"], "recommendedFor": ["数据分析", "技术解释", "方法论", "AI 实战"]}, {"id": "emerald-gold", "name": "墨绿金", "description": "商务高级，信任感强", "layout": "executive-split", "mode": "dark", "palette": ["#0F2E2E", "#1E584E", "#D4AF37", "#F1EDE3"], "recommendedFor": ["业务复盘", "策略分享", "经营分析", "管理表达"]}, {"id": "warm-gray-orange", "name": "暖灰橙", "description": "温暖亲和，行动力强", "layout": "centered-editorial", "mode": "light", "palette": ["#F7F4F1", "#FF6A3D", "#F2B26C", "#333333"], "recommendedFor": ["干货分享", "日常内容", "门店培训", "用户故事"]}, {"id": "midnight-purple", "name": "午夜紫", "description": "神秘高端，差异化强", "layout": "orbit-focus", "mode": "dark", "palette": ["#1A1026", "#6D28D9", "#A78BFA", "#EDE9FE"], "recommendedFor": ["趋势洞察", "创新话题", "未来想象", "产品发布"]}, {"id": "minimal-black-white", "name": "极简黑白", "description": "极致简洁，信息聚焦", "layout": "minimal-column", "mode": "light", "palette": ["#111111", "#333333", "#999999", "#F5F5F5"], "recommendedFor": ["知识卡片", "观点输出", "问答栏目", "极简访谈"]}, {"id": "sea-salt-cyan", "name": "海盐青", "description": "清新干净，减压舒适", "layout": "fresh-frame", "mode": "light", "palette": ["#E6F4F1", "#14B8A6", "#5EEAD4", "#0F766E"], "recommendedFor": ["用户运营", "会员增长", "服务流程", "轻量科普"]}, {"id": "earth-brown", "name": "大地棕", "description": "沉稳可靠，质感高级", "layout": "earth-bands", "mode": "light", "palette": ["#3E2C23", "#8B5E34", "#D9B38C", "#F6F1E9"], "recommendedFor": ["商业思考", "案例复盘", "品牌故事", "管理总结"]}, {"id": "vitality-lime", "name": "活力青柠", "description": "年轻活力，轻快明亮", "layout": "playful-corner", "mode": "light", "palette": ["#ECFDF5", "#84CC16", "#A3E635", "#16A34A"], "recommendedFor": ["活动宣导", "轻松话题", "会员日", "上新传播"]}];
  const LAYOUTS = [{"id": "diagonal-tech", "name": "斜切科技"}, {"id": "executive-split", "name": "商务分栏"}, {"id": "centered-editorial", "name": "居中编辑"}, {"id": "orbit-focus", "name": "轨道聚焦"}, {"id": "minimal-column", "name": "极简长栏"}, {"id": "fresh-frame", "name": "清新框景"}, {"id": "earth-bands", "name": "大地带状"}, {"id": "playful-corner", "name": "轻快角落"}];
  const DEFAULT_COPY = {
    eyebrow: "连锁餐饮 AI 实战",
    title: "模型只是模块，\n底表才承重",
    lead: "真正决定结果的是",
    emphasis: "数据底表",
    cta: "底表才承重",
    subtitle: "真正影响门店结果的，往往不是模型，而是底层数据。",
    footer: "先补数据，再谈模型",
    meta: "运营方法论 · 08",
  };

  function esc(value) {
    return String(value ?? "")
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");
  }

  function nl(value) { return esc(value).replaceAll("\n", "<br>"); }

  function getTheme(id) { return THEMES.find((theme) => theme.id === id) || THEMES[0]; }

  function cardMarkup(options = {}) {
    const theme = getTheme(options.theme || THEMES[0].id);
    const layout = options.layout || theme.layout;
    const copy = { ...DEFAULT_COPY, ...(options.copy || {}) };
    const showSubtitle = options.showSubtitle === true || options.showSubtitle === "true";
    const showSafeArea = options.showSafeArea === true || options.showSafeArea === "true";
    return `
      <article class="talk-card" data-theme="${esc(theme.id)}" data-layout="${esc(layout)}" data-mode="${esc(theme.mode)}" data-show-subtitle="${showSubtitle}" data-show-safe-area="${showSafeArea}">
        <div class="talk-card__background" aria-hidden="true"></div>
        <div class="talk-card__ambient" aria-hidden="true"></div>
        <div class="talk-card__eyebrow">${esc(copy.eyebrow)}</div>
        <h1 class="talk-card__title">${nl(copy.title)}</h1>
        <p class="talk-card__lead">${esc(copy.lead)}</p>
        <p class="talk-card__emphasis">${esc(copy.emphasis)}</p>
        <div class="talk-card__cta">${esc(copy.cta)}</div>
        <div class="talk-card__speaker" aria-label="人物视频安全区">
          <div class="talk-card__speaker-figure" aria-hidden="true"></div>
        </div>
        <div class="talk-card__subtitle">${esc(copy.subtitle)}</div>
        <div class="talk-card__footer">${esc(copy.footer)}</div>
        <div class="talk-card__meta">${esc(copy.meta)}</div>
      </article>`;
  }

  function mount(target, options = {}) {
    const node = typeof target === "string" ? document.querySelector(target) : target;
    if (!node) throw new Error("PortraitTalkThemeKit.mount: target not found");
    node.innerHTML = cardMarkup(options);
    return node.firstElementChild;
  }

  function update(card, options = {}) {
    if (!card || !card.classList.contains("talk-card")) throw new Error("update expects .talk-card");
    const theme = getTheme(options.theme || card.dataset.theme);
    card.dataset.theme = theme.id;
    card.dataset.mode = theme.mode;
    card.dataset.layout = options.layout || card.dataset.layout || theme.layout;
    if (options.showSubtitle !== undefined) card.dataset.showSubtitle = String(Boolean(options.showSubtitle));
    if (options.showSafeArea !== undefined) card.dataset.showSafeArea = String(Boolean(options.showSafeArea));
    const copy = options.copy || {};
    const map = { eyebrow: ".talk-card__eyebrow", title: ".talk-card__title", lead: ".talk-card__lead", emphasis: ".talk-card__emphasis", cta: ".talk-card__cta", subtitle: ".talk-card__subtitle", footer: ".talk-card__footer", meta: ".talk-card__meta" };
    for (const [key, selector] of Object.entries(map)) {
      if (copy[key] === undefined) continue;
      const el = card.querySelector(selector);
      if (key === "title") el.innerHTML = nl(copy[key]); else el.textContent = copy[key];
    }
    return card;
  }

  function setSpeakerMedia(card, media, { cutout = true } = {}) {
    const slot = card.querySelector(".talk-card__speaker");
    if (!slot) throw new Error("speaker slot not found");
    slot.replaceChildren(media);
    media.classList.add("talk-card__speaker-media");
    slot.classList.toggle("is-cutout", cutout);
  }

  global.PortraitTalkThemeKit = { THEMES, LAYOUTS, DEFAULT_COPY, cardMarkup, mount, update, setSpeakerMedia };
})(window);
