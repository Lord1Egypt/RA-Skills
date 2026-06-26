/**
 * 5-dimension behavioral classification system.
 * LLM does qualitative analysis → JS stores, filters, and matches.
 */

// ── Dimension definitions ──

export const DIMENSIONS = {
  工作方式: {
    key: 'work',
    a: { char: '架', label: '架构型', desc: '先搭框架、写大纲、列步骤' },
    b: { char: '探', label: '探索型', desc: '先动手试试、边做边调整' },
  },
  沟通模式: {
    key: 'comm',
    a: { char: '精', label: '精炼型', desc: '简洁直接、结论先行、不废话' },
    b: { char: '叙', label: '叙事型', desc: '先讲背景、铺陈上下文、娓娓道来' },
  },
  关注焦点: {
    key: 'focus',
    a: { char: '事', label: '事务型', desc: '关注任务、进度、结果、效率' },
    b: { char: '人', label: '人际型', desc: '关注关系、氛围、感受、共识' },
  },
  能量来源: {
    key: 'energy',
    a: { char: '内', label: '内收型', desc: '独立工作、深度思考、社交消耗能量' },
    b: { char: '外', label: '外放型', desc: '协作讨论、头脑风暴、社交获取能量' },
  },
  情感倾向: {
    key: 'affect',
    a: { char: '理', label: '理性型', desc: '情绪稳定、用逻辑处理冲突、决策靠数据和证据' },
    b: { char: '感', label: '感性型', desc: '情绪外显、用共情处理冲突、决策靠直觉和价值判断' },
  },
};

// ── 32-type lookup table (5-char code → name + summary) ──

export const TYPE_TABLE = {
  '架精事内理': { name: '精算师', summary: '精准谋划，独自高效执行' },
  '架精事内感': { name: '实干家', summary: '安静做事，心中有标准，用行动说话' },
  '架精事外理': { name: '领航员', summary: '定好方向，带团队高效抵达' },
  '架精事外感': { name: '破风手', summary: '冲在最前，为团队劈开阻力' },
  '架精人内理': { name: '洞察者', summary: '冷眼看透人与事，精准给出判断' },
  '架精人内感': { name: '倾听者', summary: '看见每个人的需要，默默安排好一切' },
  '架精人外理': { name: '召集人', summary: '把对的人聚在一起，让事情自然发生' },
  '架精人外感': { name: '连心桥', summary: '连接人与人的温度，走到哪暖到哪' },
  '架叙事内理': { name: '求真者', summary: '凡事追根溯源，厘清逻辑才行动' },
  '架叙事内感': { name: '深耕者', summary: '需要理解意义才能全力投入，急不来但走得远' },
  '架叙事外理': { name: '启明者', summary: '把复杂的事讲通透，带众人看清方向' },
  '架叙事外感': { name: '感召者', summary: '用故事凝聚人心，让每个人看见意义' },
  '架叙人内理': { name: '静观者', summary: '在角落看透人心，不轻易开口但开口就准' },
  '架叙人内感': { name: '守护者', summary: '所有人的后盾，倾听但不评判' },
  '架叙人外理': { name: '引路人', summary: '一对一帮人看清方向，点亮他人的路' },
  '架叙人外感': { name: '暖心人', summary: '温暖不灼人，所到之处如春风拂面' },
  '探精事内理': { name: '行动派', summary: '看到问题立即动手，用结果说话' },
  '探精事内感': { name: '孤勇者', summary: '一个人默默试，用行动表达在乎' },
  '探精事外理': { name: '破局者', summary: '带团队冲破僵局，不破不立' },
  '探精事外感': { name: '点燃者', summary: '冲在最前，用热情点燃整个团队' },
  '探精人内理': { name: '解铃人', summary: '精准发现关系中的症结，一语道破' },
  '探精人内感': { name: '润物者', summary: '不声不响，但每个人都被他滋养' },
  '探精人外理': { name: '联络官', summary: '快速连接人与资源，精准高效' },
  '探精人外感': { name: '发光者', summary: '自然成为人群的中心，照亮身边的人' },
  '探叙事内理': { name: '探路者', summary: '对新领域充满好奇，先研究透了再说' },
  '探叙事内感': { name: '梦想家', summary: '脑子里充满可能性的世界，不急但不停' },
  '探叙事外理': { name: '开拓者', summary: '带团队闯向未知，边走边讲清路线' },
  '探叙事外感': { name: '筑梦人', summary: '用理想感染众人，一起把梦建成现实' },
  '探叙人内理': { name: '静思者', summary: '享受一对一的深度对话，在安静中洞察' },
  '探叙人内感': { name: '善解者', summary: '用细腻的感受力理解每一个独特的灵魂' },
  '探叙人外理': { name: '连接者', summary: '把人脉和资源编织成有意义的生态' },
  '探叙人外感': { name: '凝聚者', summary: '走到哪都自然聚合一群人，气氛永远热烈' },
};

// ── Helpers ──

export function getTypeName(code) {
  return TYPE_TABLE[code]?.name ?? null;
}

export function getTypeSummary(code) {
  return TYPE_TABLE[code]?.summary ?? null;
}

/** Validate 5-char code */
export function isValidCode(code) {
  return typeof code === 'string' && code.length === 5 && code in TYPE_TABLE;
}

/** 5-char code → 10 dimension values (for story tag matching) */
export function codeToDimValues(code) {
  const map = {
    '架': '架构', '探': '探索',
    '精': '精炼', '叙': '叙事',
    '事': '事务', '人': '人际',
    '内': '内收', '外': '外放',
    '理': '理性', '感': '感性',
  };
  return [...code].map(c => map[c]).filter(Boolean);
}

/** True if last evaluation was > 30 days ago */
export function needsReEvaluation(lastEvaluatedDate) {
  if (!lastEvaluatedDate) return true;
  const days = (Date.now() - new Date(lastEvaluatedDate).getTime()) / 86400000;
  return days > 30;
}

// ── Story corpus filtering ──

/**
 * Score and filter story corpus by dimension match + context.
 * @param {string} code - 5-char dimension code
 * @param {Array} corpus - story corpus array
 * @param {object} context - { season?, lifePhase?, emotion? }
 * @returns {Array} top 8 candidates
 */
export function filterCorpus(code, corpus, context = {}) {
  const dimValues = new Set(codeToDimValues(code));
  const { season, lifePhase, emotion } = context;

  const scored = corpus.map(entry => {
    const t = entry.tags || {};
    let score = 0;
    // Personality fit: +2 per matching dimension value
    if (t.personality_fit) {
      score += t.personality_fit.filter(v => dimValues.has(v)).length * 2;
    }
    // Seasonal: +1
    if (season && t.seasonal_fit?.includes(season)) score += 1;
    // Life phase: +1
    if (lifePhase && t.life_situations?.includes(lifePhase)) score += 1;
    // Emotion: +0.5
    if (emotion && t.emotions?.includes(emotion)) score += 0.5;
    return { entry, score };
  });

  return scored
    .filter(s => s.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, 8)
    .map(s => s.entry);
}
