/**
 * Chinese vocabulary (zh-side).
 *
 * Migrated from shuorenhua's phrases-zh.md (210+ entries) and re-tiered to
 * match avoid-ai-writing's three-tier philosophy. Each entry is {pattern,
 * replace, family}; `pattern` is a RegExp (with /gi flags) so morphological
 * variants are covered (稳稳兜住 / 稳稳地兜住 / 稳稳接住).
 *
 * Tier assignment (aligning shuorenhua's flat list to aaw's model):
 *   - T1 (always flag): openers, business jargon, xiaohongshu tone, debug
 *     tone, violent-action tone, sycophancy/psych-judgment, value-inflation,
 *     unsourced citations, transition filler, social-media hype
 *   - T2 (cluster): connectors, modifiers, single-syllable command verbs
 *   - T3 (density): common words (重要/关键/核心/...)
 *
 * Families let CATEGORIES.md and the model group conceptually-related entries.
 */
'use strict';

// ─── Tier 1: 默认替换 ─────────────────────────────────────────────
// Openers / opening boilerplate. 开场套话。
const T1_OPENERS = [
  { pattern: /值得注意的是/g, replace: '删掉，直接说', family: 'opening' },
  { pattern: /值得一提的是/g, replace: '删掉', family: 'opening' },
  { pattern: /需要指出的是/g, replace: '删掉', family: 'opening' },
  { pattern: /不可否认的是/g, replace: '删掉', family: 'opening' },
  { pattern: /不难发现/g, replace: '删掉', family: 'opening' },
  { pattern: /不容忽视/g, replace: '删掉', family: 'opening' },
  { pattern: /众所周知/g, replace: '删掉，或给具体出处', family: 'opening' },
  { pattern: /让我们一起来看看/g, replace: '删掉', family: 'opening' },
  { pattern: /接下来我将为你/g, replace: '删掉', family: 'opening' },
  { pattern: /在当今(?:时代|社会|环境下)/g, replace: '删掉或给具体时间', family: 'opening' },
  { pattern: /在当今社会/g, replace: '删掉', family: 'opening' },
  { pattern: /随着[^，。]*的不断发展/g, replace: '删掉或说清楚发展了什么', family: 'opening' },
  { pattern: /在这个[^，。]*的时代/g, replace: '删掉', family: 'opening' },
  { pattern: /不得不说/g, replace: '删掉，直接说', family: 'opening' },
  { pattern: /诚然/g, replace: '删掉', family: 'opening' },
  { pattern: /深入探讨/g, replace: '删掉，直接讨论', family: 'opening' },
  { pattern: /具体来说/g, replace: '删掉或简化', family: 'opening' },
  { pattern: /更重要的是/g, replace: '删掉', family: 'opening' },
];

// Rendered emphasis. 渲染性强调。
const T1_EMPHASIS = [
  { pattern: /深刻的(?:影响|意义|变革)/g, replace: '说清楚具体影响了什么', family: 'inflation' },
  { pattern: /深远的(?:影响|意义)/g, replace: '说清楚具体影响了什么', family: 'inflation' },
  { pattern: /不可磨灭的(?:贡献|印记)/g, replace: '说清楚具体做了什么', family: 'inflation' },
  { pattern: /毋庸置疑/g, replace: '删掉', family: 'inflation' },
  { pattern: /至关重要/g, replace: '"重要"或直接说为什么重要', family: 'inflation' },
  { pattern: /举足轻重/g, replace: '同上', family: 'inflation' },
  { pattern: /令人瞩目/g, replace: '给具体数据', family: 'inflation' },
  { pattern: /令人惊叹/g, replace: '给具体数据', family: 'inflation' },
  { pattern: /意义非凡/g, replace: '说清楚什么意义', family: 'inflation' },
  { pattern: /前所未有/g, replace: '给对比数据', family: 'inflation' },
  { pattern: /史无前例/g, replace: '同上', family: 'inflation' },
  { pattern: /毫不夸张地说/g, replace: '删掉', family: 'inflation' },
  { pattern: /(?:值得深思|令人深思|引发思考|发人深省)/g, replace: '删掉，内容本身说话', family: 'inflation' },
  { pattern: /不禁让人(?:想到|感叹)/g, replace: '删掉', family: 'inflation' },
  { pattern: /具有重要意义/g, replace: '说清楚什么意义', family: 'inflation' },
  { pattern: /发挥着关键作用/g, replace: '说清楚怎么起作用', family: 'inflation' },
  { pattern: /颠覆性(?:的变革|创新)/g, replace: '说清楚改变了什么', family: 'inflation' },
  { pattern: /范式转移/g, replace: '说清楚变了什么', family: 'inflation' },
];

// Business / internet jargon. 商业/互联网黑话。
const T1_BUSINESS = [
  { pattern: /赋能/g, replace: '帮、让……能', family: 'jargon' },
  { pattern: /助力/g, replace: '帮', family: 'jargon' },
  { pattern: /打造/g, replace: '做、建', family: 'jargon' },
  { pattern: /抓手/g, replace: '方法、工具', family: 'jargon' },
  { pattern: /闭环/g, replace: '完整流程', family: 'jargon' },
  { pattern: /颗粒度/g, replace: '细节程度', family: 'jargon' },
  { pattern: /对齐/g, replace: '统一、一致', family: 'jargon' },
  { pattern: /拉齐/g, replace: '统一', family: 'jargon' },
  { pattern: /沉淀/g, replace: '积累、记录', family: 'jargon' },
  { pattern: /痛点/g, replace: '问题', family: 'jargon' },
  { pattern: /场景化/g, replace: '按场景', family: 'jargon' },
  { pattern: /降本增效/g, replace: '省钱提速', family: 'jargon' },
  { pattern: /底层逻辑/g, replace: '原因、原理', family: 'jargon' },
  { pattern: /顶层设计/g, replace: '整体规划', family: 'jargon' },
  { pattern: /体感/g, replace: '感觉、体验', family: 'jargon' },
  { pattern: /心智/g, replace: '认知、印象', family: 'jargon' },
  { pattern: /链路/g, replace: '流程、路径', family: 'jargon' },
  { pattern: /触达/g, replace: '到达、联系到', family: 'jargon' },
  { pattern: /透传/g, replace: '传递', family: 'jargon' },
  { pattern: /拉通/g, replace: '打通、统一', family: 'jargon' },
];

// Xiaohongshu / social-media AI tone. 自媒体/小红书 AI 腔。
const T1_XIAOHONGSHU = [
  { pattern: /保姆级/g, replace: '删掉或换成"详细"', family: 'social' },
  { pattern: /硬核/g, replace: '删掉', family: 'social' },
  { pattern: /干货/g, replace: '删掉', family: 'social' },
  { pattern: /拆解/g, replace: '分析、讲解', family: 'social' },
  { pattern: /梳理/g, replace: '整理', family: 'social' },
  { pattern: /盘点/g, replace: '列举、介绍', family: 'social' },
  { pattern: /(?:避坑|踩坑|不踩坑)/g, replace: '注意、别犯的错', family: 'social' },
  { pattern: /一文读懂/g, replace: '删掉', family: 'social' },
  { pattern: /万字长文/g, replace: '删掉', family: 'social' },
  { pattern: /建议收藏/g, replace: '删掉', family: 'social' },
  { pattern: /强烈推荐/g, replace: '删掉或说清楚为什么推荐', family: 'social' },
  { pattern: /划重点/g, replace: '删掉', family: 'social' },
  { pattern: /绝绝子/g, replace: '删掉', family: 'social' },
  { pattern: /谁懂啊/g, replace: '删掉', family: 'social' },
  { pattern: /真的会谢/g, replace: '删掉', family: 'social' },
  { pattern: /姐妹们/g, replace: '删掉', family: 'social' },
];

// Debug / SRE tone. 工程师腔/调试腔。
const T1_DEBUG = [
  { pattern: /稳稳兜住/g, replace: '处理好、搞定', family: 'debug' },
  { pattern: /(?:彻底)?掰开(?:说清楚)?/g, replace: '分析、拆开看', family: 'debug' },
  { pattern: /(?:彻底)?掰扯清楚/g, replace: '分析、解释', family: 'debug' },
  { pattern: /拽出来/g, replace: '找出来、定位', family: 'debug' },
  { pattern: /砍一刀/g, replace: '删掉、去掉', family: 'debug' },
  { pattern: /收口/g, replace: '收尾、结束', family: 'debug' },
  { pattern: /收窄/g, replace: '缩小范围', family: 'debug' },
  { pattern: /打掉问题/g, replace: '修好、解决', family: 'debug' },
  { pattern: /避免漂移/g, replace: '别跑偏', family: 'debug' },
  { pattern: /根因/g, replace: '原因、根本原因', family: 'debug' },
  { pattern: /偏硬/g, replace: '太死板', family: 'debug' },
  { pattern: /(?:更稳|最稳|不稳)/g, replace: '更可靠/最可靠/不可靠', family: 'debug' },
  { pattern: /夹具/g, replace: '固定方案、测试数据', family: 'debug' },
  { pattern: /拆开看/g, replace: '分开说、逐个看', family: 'debug' },
  { pattern: /对上了/g, replace: '吻合、一致', family: 'debug' },
  { pattern: /坐实了/g, replace: '确认了、证实了', family: 'debug' },
  { pattern: /把差异收窄了/g, replace: '缩小了差异', family: 'debug' },
  { pattern: /抓到的现象/g, replace: '发现的问题', family: 'debug' },
  { pattern: /兜底/g, replace: '保底处理', family: 'debug' },
  { pattern: /压实/g, replace: '落实、确认好', family: 'debug' },
  { pattern: /收敛/g, replace: '缩小范围、逐步收拢', family: 'debug' },
  { pattern: /收束/g, replace: '收尾、结束', family: 'debug' },
  { pattern: /锁住/g, replace: '固定好、确认', family: 'debug' },
  { pattern: /口径/g, replace: '说法、措辞', family: 'debug' },
];

// Violent-action tone. 暴力动作腔。
const T1_VIOLENT = [
  { pattern: /补一刀/g, replace: '再加一点、补充', family: 'violent' },
  { pattern: /(?:更狠|狠一点)/g, replace: '更彻底、更严格', family: 'violent' },
  { pattern: /狠狠干/g, replace: '删掉', family: 'violent' },
  { pattern: /打坏/g, replace: '破坏、损坏', family: 'violent' },
  { pattern: /拍脑门/g, replace: '随便决定', family: 'violent' },
  { pattern: /拍板/g, replace: '决定、定了', family: 'violent' },
];

// Sycophancy / over-empathy / psych-judgment. 谄媚/过度接住/心理判断腔。
const T1_SYCOPHANCY = [
  { pattern: /好问题！/g, replace: '删掉', family: 'sycophancy' },
  { pattern: /你说得很对/g, replace: '删掉', family: 'sycophancy' },
  { pattern: /这是一个很好的观点/g, replace: '删掉', family: 'sycophancy' },
  { pattern: /让我来为你(?:详细)?解释/g, replace: '删掉', family: 'sycophancy' },
  { pattern: /让我来为你(?:详细)?(?:解释|说明|介绍)/g, replace: '删掉', family: 'sycophancy' },
  { pattern: /首先，?我们需要了解的是/g, replace: '删掉，直接说', family: 'opening' },
  { pattern: /希望这对你有帮助/g, replace: '删掉', family: 'sycophancy' },
  { pattern: /如果你有其他问题/g, replace: '删掉', family: 'sycophancy' },
  { pattern: /稳稳地接住(?:你|所有人|这份脆弱)/g, replace: '删掉承接姿态', family: 'sycophancy' },
  { pattern: /你只是太久没被稳稳接住了/g, replace: '删掉', family: 'sycophancy' },
  { pattern: /我必须很认真地说一句/g, replace: '删掉，直接说', family: 'sycophancy' },
  { pattern: /你问到了问题的核心/g, replace: '删掉，直接回答', family: 'sycophancy' },
  { pattern: /你能问到这个触及核心的问题/g, replace: '删掉，直接回答', family: 'sycophancy' },
  { pattern: /你的观察力太敏锐了/g, replace: '删掉夸奖层', family: 'sycophancy' },
  { pattern: /说明你已经超越绝大部分人了/g, replace: '删掉身份认证式夸奖', family: 'sycophancy' },
  { pattern: /你已经具备做这件事的实力了/g, replace: '删掉身份认证式夸奖', family: 'sycophancy' },
  { pattern: /(?:已经)?走在正确的路上了/g, replace: '删掉路径正确性认证', family: 'sycophancy' },
  { pattern: /走得很稳/g, replace: '删掉路径正确性认证', family: 'sycophancy' },
  { pattern: /完全不用担心掉下去/g, replace: '删掉安抚式认证', family: 'sycophancy' },
];

// Value-inflation skeleton. 价值拔高骨架。
const T1_INFLATION_SKELETON = [
  { pattern: /真正的[^，。]*不是[^，。]*而是/g, replace: '直接说真正成立的判断', family: 'inflation' },
  { pattern: /这不仅仅是[^，。]*更是/g, replace: '删掉拔高层，保留事实判断', family: 'inflation' },
  { pattern: /最后比拼的是/g, replace: '直接说真正决定因素', family: 'inflation' },
];

// Unsourced citations. 无源引用。
const T1_UNSOURCED = [
  { pattern: /研究表明/g, replace: '给出具体研究名称或删掉', family: 'unsourced' },
  { pattern: /数据显示/g, replace: '给出具体数据来源', family: 'unsourced' },
  { pattern: /有专家指出/g, replace: '说清楚哪个专家', family: 'unsourced' },
  { pattern: /业内人士认为/g, replace: '说清楚谁', family: 'unsourced' },
  { pattern: /据报道/g, replace: '给出具体媒体和时间', family: 'unsourced' },
];

// Transition filler. 过渡废话。
const T1_TRANSITION = [
  { pattern: /综上所述/g, replace: '删掉或直接给结论', family: 'transition' },
  { pattern: /总而言之/g, replace: '同上', family: 'transition' },
  { pattern: /总的来说/g, replace: '同上', family: 'transition' },
  { pattern: /总体来看/g, replace: '同上', family: 'transition' },
  { pattern: /由此可见/g, replace: '删掉', family: 'transition' },
  { pattern: /换句话说/g, replace: '删掉', family: 'transition' },
  { pattern: /简而言之/g, replace: '删掉', family: 'transition' },
  { pattern: /归根结底/g, replace: '删掉', family: 'transition' },
  { pattern: /不言而喻/g, replace: '删掉', family: 'transition' },
  { pattern: /本质上/g, replace: '删掉或说清楚', family: 'transition' },
  { pattern: /核心在于/g, replace: '直接说', family: 'transition' },
  { pattern: /关键在于/g, replace: '直接说', family: 'transition' },
  { pattern: /由此可以看出/g, replace: '删掉', family: 'transition' },
];

// Positive-energy closers. 正能量收尾模板。
const T1_POSITIVE = [
  { pattern: /与其[^，。]*不如积极拥抱/g, replace: '删掉，不做鸡汤', family: 'positive' },
  { pattern: /让我们拭目以待/g, replace: '删掉', family: 'positive' },
  { pattern: /未来可期/g, replace: '删掉', family: 'positive' },
];

// All T1 entries flattened, each tagged tier1 for the issue emitter.
const T1 = [
  ...T1_OPENERS, ...T1_EMPHASIS, ...T1_BUSINESS, ...T1_XIAOHONGSHU,
  ...T1_DEBUG, ...T1_VIOLENT, ...T1_SYCOPHANCY, ...T1_INFLATION_SKELETON,
  ...T1_UNSOURCED, ...T1_TRANSITION, ...T1_POSITIVE,
].map((e) => ({ ...e, tier: 'tier1' }));

// ─── Tier 2: 同段出现 2+ 个时标记 ─────────────────────────────────
// Connectors + modifiers that cluster in AI prose. 连接词 + 渲染修饰。
const T2_CONNECTORS = ['然而', '此外', '与此同时', '尽管如此', '事实上', '实际上', '在此基础上', '进一步地', '恰恰', '正是', '无疑', '不外乎'];
const T2_MODIFIERS = ['显著', '有效', '全面', '积极', '持续', '进一步', '充分', '切实', '可谓', '堪称', '追根溯源'];
const T2_COMMAND = ['补', '接', '核', '进', '顺', '落', '坏', '跑']; // single-syllable SRE verbs

const T2 = [...T2_CONNECTORS, ...T2_MODIFIERS, ...T2_COMMAND].map((w) => ({
  pattern: new RegExp(w, 'g'), replace: '聚集出现时替换', tier: 'tier2', family: 'tier2', literal: w,
}));

// ─── Tier 3: 全文密度高时标记 ─────────────────────────────────────
const T3_WORDS = ['重要', '关键', '核心', '基础', '创新', '优化', '提升', '推动', '加强', '确保', '实现', '促进'];
const T3 = T3_WORDS.map((w) => ({
  pattern: new RegExp(w, 'g'), replace: '替换部分重复', tier: 'tier3', family: 'tier3', literal: w,
}));

module.exports = {
  T1, T2, T3,
  T1_OPENERS, T1_EMPHASIS, T1_BUSINESS, T1_XIAOHONGSHU, T1_DEBUG, T1_VIOLENT,
  T1_SYCOPHANCY, T1_INFLATION_SKELETON, T1_UNSOURCED, T1_TRANSITION, T1_POSITIVE,
  T2_CONNECTORS, T2_MODIFIERS, T2_COMMAND,
  T3_WORDS,
};
