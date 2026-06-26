import { NormalizedInboundMessage, PromotionReason, ShadowSignalKind } from '../types';

const asRecord = (value: unknown) =>
  typeof value === 'object' && value !== null ? (value as Record<string, unknown>) : {};

const normalizeText = (value: string) => value.replace(/\s+/g, ' ').trim().toLowerCase();

const NOISE_PHRASES = ['好的', '好哦', '收到', '明白', '知道了', '谢谢', '辛苦了', '嗯', '嗯嗯', '可以', '行'];

const TASK_INTENT_PHRASES = [
  '帮我写',
  '帮我整理',
  '帮我总结',
  '帮我分析',
  '帮我规划',
  '帮我跟进',
  '帮我追踪',
  '帮我修',
  '帮我改',
  '继续做',
  '继续推进',
  '继续处理',
  '接着做',
  '做一个',
  '处理一下',
];

const CONTEXT_PHRASES = ['参考', '背景', '约束', '要求', '资料', '附件', '链接', '素材', '上下文', '补充'];

const BLOCKER_PHRASES = ['卡住', '需要决定', '缺关键信息', '等你确认', '等确认', '需要你判断'];

const NOISE_PATTERNS = [
  /^(ok|okay|kk|got it|roger|thanks|thank you|cool|sure|noted|received)$/i,
  /^[+*!.?~\-_=]+$/,
];

const TASK_INTENT_PATTERNS = [
  /\b(help me|write|draft|summarize|analy[sz]e|plan|track|follow up|continue|fix|revise|organize|review)\b/i,
];

const CONTEXT_PATTERNS = [/\b(context|reference|background|constraint|requirement|attachment|link|brief|notes?)\b/i];

const BLOCKER_PATTERNS = [/\b(blocked|waiting for decision|need input|need approval|missing key info|waiting_human)\b/i];

const containsAnyPhrase = (content: string, phrases: string[]) =>
  phrases.some((phrase) => content.includes(phrase));

const containsUrl = (content: string) => /https?:\/\/|www\./i.test(content);

const hasStructuredContext = (message: NormalizedInboundMessage) => {
  const metadata = asRecord(message.metadata);
  return (
    (Array.isArray(message.attachments) && message.attachments.length > 0) ||
    containsUrl(message.content) ||
    Boolean(metadata.context_payload === true) ||
    Boolean(metadata.reference_bundle)
  );
};

const isNoise = (content: string) => {
  const trimmed = content.trim();
  if (!trimmed) {
    return true;
  }
  return containsAnyPhrase(trimmed, NOISE_PHRASES) || NOISE_PATTERNS.some((pattern) => pattern.test(trimmed));
};

const isTaskIntent = (content: string) =>
  containsAnyPhrase(content, TASK_INTENT_PHRASES) || TASK_INTENT_PATTERNS.some((pattern) => pattern.test(content));

const isContextPayload = (content: string, message: NormalizedInboundMessage) =>
  hasStructuredContext(message) ||
  containsAnyPhrase(content, CONTEXT_PHRASES) ||
  CONTEXT_PATTERNS.some((pattern) => pattern.test(content)) ||
  content.length >= 180 ||
  content.split('\n').length >= 4;

const isBlocker = (message: NormalizedInboundMessage, content: string) => {
  const metadata = asRecord(message.metadata);
  return (
    message.message_type === 'blocked' ||
    message.message_type === 'waiting_human' ||
    metadata.current_state === 'blocked' ||
    metadata.current_state === 'waiting_human' ||
    containsAnyPhrase(content, BLOCKER_PHRASES) ||
    BLOCKER_PATTERNS.some((pattern) => pattern.test(content))
  );
};

const isExecutionSignal = (message: NormalizedInboundMessage) => {
  const metadata = asRecord(message.metadata);
  return (
    message.message_type === 'tool_called' ||
    message.message_type === 'artifact_created' ||
    message.message_type === 'skill_invoked' ||
    metadata.tool_called === true ||
    metadata.artifact_created === true ||
    metadata.skill_invoked === true
  );
};

export interface ShadowClassification {
  signal_kind: ShadowSignalKind;
  effective: boolean;
  score_delta: number;
  hard_promotion_ready: boolean;
  promotion_reasons: PromotionReason[];
  connector_followup: boolean;
}

export const classifyInboundMessage = (
  message: NormalizedInboundMessage,
  options: {
    manual_adopt?: boolean;
    manual_promote?: boolean;
    high_priority?: boolean;
  } = {}
): ShadowClassification => {
  const content = normalizeText(message.content || '');
  const metadata = asRecord(message.metadata);
  const connectorFollowup = metadata.requires_followup === true || message.message_type === 'followup_required';
  const manualPriority =
    options.manual_adopt || options.manual_promote || options.high_priority || metadata.high_priority === true;

  if (options.manual_adopt || options.manual_promote) {
    return {
      signal_kind: 'manual_priority',
      effective: false,
      score_delta: 2,
      hard_promotion_ready: true,
      promotion_reasons: ['manual_adopt'],
      connector_followup: connectorFollowup,
    };
  }

  if (isExecutionSignal(message)) {
    const reasons: PromotionReason[] = [];
    if (message.message_type === 'tool_called' || metadata.tool_called === true) {
      reasons.push('tool_called');
    }
    if (message.message_type === 'artifact_created' || metadata.artifact_created === true) {
      reasons.push('artifact_created');
    }
    if (message.message_type === 'skill_invoked' || metadata.skill_invoked === true) {
      reasons.push('skill_invoked');
    }
    return {
      signal_kind: 'execution_signal',
      effective: true,
      score_delta: 3,
      hard_promotion_ready: true,
      promotion_reasons: reasons,
      connector_followup: connectorFollowup,
    };
  }

  if (isBlocker(message, content)) {
    const reasons: PromotionReason[] = [];
    if (message.message_type === 'blocked' || metadata.current_state === 'blocked' || content.includes('卡住')) {
      reasons.push('blocked');
    }
    if (
      message.message_type === 'waiting_human' ||
      metadata.current_state === 'waiting_human' ||
      containsAnyPhrase(content, ['需要决定', '等你确认', '需要你判断'])
    ) {
      reasons.push('waiting_human');
    }
    return {
      signal_kind: 'blocker_signal',
      effective: true,
      score_delta: 3,
      hard_promotion_ready: true,
      promotion_reasons: reasons.length ? reasons : ['waiting_human'],
      connector_followup: connectorFollowup,
    };
  }

  if (isTaskIntent(content)) {
    return {
      signal_kind: 'task_intent',
      effective: true,
      score_delta: 2,
      hard_promotion_ready: false,
      promotion_reasons: manualPriority ? ['task_intent', 'high_priority'] : ['task_intent'],
      connector_followup: connectorFollowup,
    };
  }

  if (manualPriority) {
    return {
      signal_kind: 'manual_priority',
      effective: false,
      score_delta: 2,
      hard_promotion_ready: false,
      promotion_reasons: ['high_priority'],
      connector_followup: connectorFollowup,
    };
  }

  if (isContextPayload(content, message)) {
    return {
      signal_kind: 'context_payload',
      effective: true,
      score_delta: 1,
      hard_promotion_ready: false,
      promotion_reasons: ['context_payload'],
      connector_followup: connectorFollowup,
    };
  }

  return {
    signal_kind: 'noise',
    effective: false,
    score_delta: 0,
    hard_promotion_ready: false,
    promotion_reasons: [],
    connector_followup: connectorFollowup,
  };
};

export const describePendingPromotion = (shadow: {
  effective_turn_count: number;
  promotion_score: number;
  hard_promotion_ready: boolean;
  last_signal_kind: ShadowSignalKind | null;
  promotion_reasons: PromotionReason[];
}) => {
  if (shadow.hard_promotion_ready) {
    return 'Hard promotion signal detected; promote immediately.';
  }
  if (shadow.effective_turn_count < 2) {
    return 'Need one more effective turn before automatic promotion.';
  }
  if (shadow.promotion_score < 3) {
    return 'Need stronger task/context signals before automatic promotion.';
  }
  if (shadow.last_signal_kind === 'noise') {
    return 'Recent activity looks like low-value chatter; keep observing.';
  }
  return 'Candidate is close to promotion; keep watching the next effective message.';
};
