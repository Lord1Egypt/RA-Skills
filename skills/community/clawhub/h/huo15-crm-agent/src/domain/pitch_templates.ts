import type { Tone } from '../shared.js';

/**
 * 财税获客话术骨架。
 *
 * 设计：每个场景给 3 个 tone 变体（formal / warm / neutral），
 * 文案中的 {占位符} 在 sales_pitch 工具运行时替换：
 *   - {client_name}    客户公司名
 *   - {decision_maker} 决策人称呼
 *   - {pain_point}     主痛点（来自 brief 工具识别）
 *   - {hook}           开场 hook（来自 persona）
 *   - {company_brand}  我方公司名
 *   - {region}         默认区域
 *   - {service}        推荐主服务
 */

export type Scene =
  | 'first_contact'
  | 'reengage'
  | 'price_objection'
  | 'decision_delay'
  | 'referral'
  | 'close';

export interface PitchTemplate {
  scene: Scene;
  display: string;
  variants: Record<Tone, string[]>;
  /** 配套的下一步动作建议（提示销售紧跟的动作，不直接执行）。 */
  next_step_hint: string;
}

export const PITCH_TEMPLATES: PitchTemplate[] = [
  {
    scene: 'first_contact',
    display: '首次接触（陌拜 / 初次电话）',
    next_step_hint: '通话结束前必须拿到一个具体下一步：要么约面谈，要么允许加微信发资料',
    variants: {
      formal: [
        '{decision_maker}您好，我是{company_brand}的财税顾问。我们最近在帮{region}的{service}方向客户做合规体检，{hook}。请问您方便沟通 3 分钟吗？',
        '{decision_maker}您好，冒昧打扰。我们刚刚帮一家与贵司同行业的客户做完{service}方案，{pain_point}这一块给他们省了一笔。想跟您简单交流下，看是否对贵司有参考价值。',
      ],
      warm: [
        '{decision_maker}您好~我是{company_brand}的小伙伴，做财税服务的。最近在跑{region}本地企业的"财税体检"小活动，{hook}。听起来有意思的话，我加您微信发个简介？',
        '{decision_maker}哈喽！冒昧加联系。前两周我们刚帮{region}一家差不多体量的公司处理了{pain_point}，效果挺意外。要不发您看看？不打扰的话两分钟就够。',
      ],
      neutral: [
        '{decision_maker}您好，{company_brand}财税顾问。我们关注到贵司可能涉及{pain_point}。我们手上有针对{service}方向的具体方案，是否方便约个 15 分钟简短沟通？',
        '{decision_maker}您好。我是{company_brand}，做{service}相关业务。{hook}。能否先发份资料给您过目，再决定是否进一步交流？',
      ],
    },
  },
  {
    scene: 'reengage',
    display: '二次跟进（拖延 / 没回复）',
    next_step_hint: '别催决定，给一个"轻动作"：发新内容、问近况、邀请参加活动',
    variants: {
      formal: [
        '{decision_maker}您好，前段时间发您的{service}方案，不知道您内部有没有进一步讨论？我们近期更新了几个最新案例，可以发您参考。',
        '{decision_maker}您好。最近{region}{pain_point}相关的新政有些变化，可能影响到贵司，整理了一份要点想发您。',
      ],
      warm: [
        '{decision_maker}哈喽~好久没联系。最近忙吗？前阵子那个{service}的事儿不急，但有个新案例挺有意思，发您看看？',
        '{decision_maker}您好~随便聊一句，最近我们在做{region}的客户答谢活动，您要不要参加？纯放松，顺便聊财税最近的几个变化。',
      ],
      neutral: [
        '{decision_maker}您好，前期发的{service}方案是否还有需要补充的信息？我们这边可以根据贵司新的情况调整。',
        '{decision_maker}最近{pain_point}有了新动作，提醒一下您方便的时候关注下，我把要点整理好了。',
      ],
    },
  },
  {
    scene: 'price_objection',
    display: '价格异议',
    next_step_hint: '不打折，先重新定义价值；如必须让步，用"延展服务"换价格而不是直接降',
    variants: {
      formal: [
        '{decision_maker}您说的价格我理解。咱们这个报价里包含了{service}的全套合规闭环，不是单纯做账。如果只看其中一部分，我可以拆开报，您看哪些是您必须要的？',
        '价格这个事我先说一句：我们这个报价对应的服务，对标贵司体量的客户，平均每年帮他们规避的{pain_point}相关风险，金额在报价的 5-10 倍。',
      ],
      warm: [
        '{decision_maker}懂您的意思。价格这事咱不绕弯。我可以这样：把整体方案拆成"基础+可选"，基础部分价格降下来，可选部分按需。但有一项不能拆 —— 就是{pain_point}这块的体检，那个是兜底的。',
        '其实我也希望咱合作能成。这样吧，我看看能不能给您加一项原本没在报价里的延展服务，比如{service}相关的季度复盘，价格不动，但您拿到的多一项。',
      ],
      neutral: [
        '价格我们可以再讨论。但建议先确认服务范围 —— 您具体要哪一块、不要哪一块，价格随之调整，比直接砍价合理。',
        '理解。我把报价拆细，您看每一项对应的工作量和预期产出，再决定整体如何取舍。',
      ],
    },
  },
  {
    scene: 'decision_delay',
    display: '决策拖延（内部还在讨论）',
    next_step_hint: '识别真实卡点：是钱、是优先级、还是决策人没拍板？分别有不同应对',
    variants: {
      formal: [
        '{decision_maker}方便问一下，目前主要还在讨论哪个点？是预算、范围、还是需要更多内部对齐？我可以针对那一点准备补充材料。',
        '为了不打扰您，我直接说：如果是因为内部需要更多信息，我可以约一次跟相关同事的简短沟通会；如果是优先级问题，我们也可以推到 Q2/Q3。',
      ],
      warm: [
        '{decision_maker}没事的，我也不催。就随手问问，是哪个点还在卡？说不定我能帮上忙呢，不能也没关系，咱保持联系。',
        '其实拖一拖也好，决策这事儿不能急。但有个小事，{pain_point}这块的窗口期就那么几个月，要不要我先帮您把那一块单独跑起来？',
      ],
      neutral: [
        '请问目前的决策卡点是哪一块？预算 / 范围 / 时间 / 决策人？我针对那一点准备材料更高效。',
        '如果近期不好定，可以先做一个最小试点：3 个月{service}基础服务，到期再决定是否扩大。',
      ],
    },
  },
  {
    scene: 'referral',
    display: '转介绍邀约（老客户带新客户）',
    next_step_hint: '降低被介绍人门槛 —— 提供价值再要联系方式，不是上来就要人',
    variants: {
      formal: [
        '{decision_maker}过去这一年咱合作得很顺。如果您身边有同行朋友也面临{pain_point}的问题，可以介绍我跟他认识吗？我送他一份免费的{service}体检作为见面礼。',
        '冒昧请教 —— 您身边有没有 1-2 位老板朋友，他们公司也是{region}的、{service}有需求的？我可以独立去拜访，不会借用您的名义施压。',
      ],
      warm: [
        '{decision_maker}您觉得我们服务还 OK 的话，能帮我牵个线不？您身边有没有差不多体量的老板，正好也烦{pain_point}？我请他喝杯茶聊聊就行。',
        '咱合作久了，我厚着脸皮问一句 —— 您朋友圈里有没有 1 位老板，您觉得他们公司财税这块该体检了？我给您一个体检券，您送给他做个人情。',
      ],
      neutral: [
        '是否方便推荐 1-2 位同行朋友？我们提供一次免费财税体检作为转介绍礼，无需付费、无强制后续。',
        '如果您觉得我们服务可以，麻烦推荐 1 位有{service}需求的朋友。我们独立沟通，不会让您难做。',
      ],
    },
  },
  {
    scene: 'close',
    display: '促成（合同临门一脚）',
    next_step_hint: '给一个明确的、有时限的"下一步动作" —— 最好是文档/合同/付款的具体节点',
    variants: {
      formal: [
        '{decision_maker}所有问题都讨论清楚了。我提议：本周内完成合同最终稿，下周一开始服务起算。这样{pain_point}这一块的{service}就能从{region}最新一轮申报开始覆盖。',
        '我们准备就绪。请您确认两件事：合同主体名称、付款节奏（一次性 / 季度）。两点确定后我今天发合同正本。',
      ],
      warm: [
        '{decision_maker}咱聊到这儿，差不多齐了。我直接说一句：本周签了，下周开干。{pain_point}这块的服务从最近一次申报就接得上。您看可以？',
        '我个人觉得已经很顺了。咱要不就推进吧，签了我安排团队周五就到位，{service}马上就能往前跑。',
      ],
      neutral: [
        '建议本周完成合同签署，下周服务起算。请确认主体与付款方式。',
        '当前已无大的悬而未决问题。请确认是否可以推进合同签署 —— 时间窗口建议本周内。',
      ],
    },
  },
];

export function findScene(scene: Scene): PitchTemplate {
  const t = PITCH_TEMPLATES.find((p) => p.scene === scene);
  if (!t) throw new Error(`unknown pitch scene: ${scene}`);
  return t;
}

export function fillTemplate(template: string, slots: Record<string, string | undefined>): string {
  return template.replace(/\{(\w+)\}/g, (_, key) => slots[key] ?? `{${key}}`);
}
