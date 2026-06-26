import {
  AdoptSessionInput,
  NormalizedInboundMessage,
  PromotionQueueEntry,
  PromotionReason,
  SessionRecord,
  ThreadShadow,
  nowIso,
  uid,
} from '../types';
import { FsStore } from '../storage/fs-store';
import { writePromotionQueue, writeThreadShadows } from '../storage/indexes';
import { withNamedLock } from '../storage/locks';
import { AttentionService } from './attention-service';
import { BindingService } from './binding-service';
import { EventService } from './event-service';
import { SessionService } from './session-service';
import { SpoolService } from './spool-service';
import { classifyInboundMessage, describePendingPromotion } from './shadow-classifier';

const summarize = (text: string, max = 160) => {
  const normalized = text.replace(/\s+/g, ' ').trim();
  return normalized.length > max ? `${normalized.slice(0, max - 1)}...` : normalized;
};

const uniqueReasons = (reasons: PromotionReason[]) => Array.from(new Set(reasons));

const uniqueStrings = (items: string[]) => Array.from(new Set(items.map((item) => item.trim()).filter(Boolean)));

const asRecord = (value: unknown) =>
  typeof value === 'object' && value !== null ? (value as Record<string, unknown>) : {};

const threadTitle = (message: NormalizedInboundMessage) => {
  const metadata = asRecord(message.metadata);
  const explicit =
    (typeof metadata.thread_title === 'string' && metadata.thread_title) ||
    (typeof metadata.chat_title === 'string' && metadata.chat_title) ||
    (typeof metadata.repo === 'string' && metadata.repo) ||
    '';
  return explicit || `Observed ${message.source_type} thread`;
};

const observedArchiveHours = 24 * 7;
const candidateArchiveHours = 24 * 14;

const hoursSince = (iso: string) => (Date.now() - new Date(iso).getTime()) / 36e5;

const shouldAutoArchive = (shadow: ThreadShadow) => {
  if (shadow.linked_session_id || shadow.state === 'promoted' || shadow.archived_at) {
    return false;
  }
  if (shadow.state === 'observed' && shadow.promotion_score === 0) {
    return hoursSince(shadow.updated_at) >= observedArchiveHours;
  }
  if (shadow.state === 'candidate' && shadow.last_effective_at) {
    return hoursSince(shadow.last_effective_at) >= candidateArchiveHours;
  }
  return false;
};

const defaultObjective = (shadow: ThreadShadow) => {
  if (shadow.source_type === 'chat') {
    return 'Continue the observed local thread as a managed session.';
  }
  return `Follow up on the observed ${shadow.source_type} thread.`;
};

export class ShadowService {
  constructor(
    private readonly store: FsStore,
    private readonly sessionService: SessionService,
    private readonly eventService: EventService,
    private readonly attentionService: AttentionService,
    private readonly bindingService: BindingService,
    private readonly spoolService: SpoolService
  ) {}

  private async readShadowsRaw() {
    return this.store.readJson<ThreadShadow[]>(this.store.threadShadowsFile, []);
  }

  private toQueueEntry(shadow: ThreadShadow): PromotionQueueEntry {
    return {
      shadow_id: shadow.shadow_id,
      title: shadow.title,
      source_type: shadow.source_type,
      source_thread_key: shadow.source_thread_key,
      state: shadow.state,
      turn_count: shadow.turn_count,
      effective_turn_count: shadow.effective_turn_count,
      noise_turn_count: shadow.noise_turn_count,
      promotion_reasons: shadow.promotion_reasons,
      promotion_score: shadow.promotion_score,
      latest_summary: shadow.latest_summary,
      last_message_at: shadow.last_message_at,
      last_signal_kind: shadow.last_signal_kind,
      hard_promotion_ready: shadow.hard_promotion_ready,
      pending_reason: describePendingPromotion(shadow),
      linked_session_id: shadow.linked_session_id,
    };
  }

  private async writeShadows(shadows: ThreadShadow[]) {
    const now = nowIso();
    const normalized = shadows
      .map((shadow) =>
        shouldAutoArchive(shadow)
          ? {
              ...shadow,
              state: 'archived' as const,
              archived_at: shadow.archived_at || now,
              updated_at: now,
            }
          : shadow
      )
      .sort((a, b) => b.updated_at.localeCompare(a.updated_at));

    const queue = normalized
      .filter((shadow) => !shadow.linked_session_id && shadow.state !== 'archived' && shadow.state !== 'promoted')
      .filter((shadow) => shadow.promotion_score >= 2)
      .map((shadow) => this.toQueueEntry(shadow))
      .sort((a, b) => b.promotion_score - a.promotion_score || b.last_message_at.localeCompare(a.last_message_at));

    await writeThreadShadows(this.store, normalized);
    await writePromotionQueue(this.store, queue);
  }

  private async readManagedShadows() {
    const shadows = await this.readShadowsRaw();
    await this.writeShadows(shadows);
    return this.readShadowsRaw();
  }

  private shadowState(shadow: ThreadShadow, shouldPromote: boolean) {
    if (shadow.archived_at) {
      return 'archived' as const;
    }
    if (shadow.linked_session_id || shouldPromote) {
      return 'promoted' as const;
    }
    if (shadow.promotion_score >= 1 || shadow.effective_turn_count > 0 || shadow.high_priority) {
      return 'candidate' as const;
    }
    return 'observed' as const;
  }

  private shouldPromote(shadow: ThreadShadow) {
    if (shadow.linked_session_id) {
      return false;
    }
    if (shadow.hard_promotion_ready) {
      return true;
    }
    return shadow.effective_turn_count >= 2 && shadow.promotion_score >= 3;
  }

  private upsertObservedShadow(
    shadows: ThreadShadow[],
    message: NormalizedInboundMessage,
    options: {
      linked_session_id?: string | null;
      manual_adopt?: boolean;
      manual_promote?: boolean;
      high_priority?: boolean;
    } = {}
  ) {
    const index = shadows.findIndex(
      (item) =>
        item.source_type === message.source_type && item.source_thread_key === message.source_thread_key
    );
    const existing = index >= 0 ? shadows[index] : null;
    const now = nowIso();
    const classification = classifyInboundMessage(message, options);
    const metadata = asRecord(message.metadata);
    const highPriority =
      Boolean(options.high_priority) || metadata.high_priority === true || existing?.high_priority || false;
    const base: ThreadShadow =
      existing || {
        shadow_id: uid('shadow'),
        source_type: message.source_type,
        source_thread_key: message.source_thread_key,
        title: threadTitle(message),
        latest_summary: summarize(message.content),
        turn_count: 0,
        effective_turn_count: 0,
        noise_turn_count: 0,
        promotion_score: 0,
        last_message_at: message.timestamp || now,
        last_effective_at: null,
        last_signal_kind: null,
        hard_promotion_ready: false,
        state: 'observed',
        promotion_reasons: [],
        linked_session_id: null,
        high_priority: false,
        metadata: {},
        created_at: now,
        updated_at: now,
        archived_at: null,
      };

    const nextPromotionScore =
      base.promotion_score + classification.score_delta + (classification.connector_followup ? 1 : 0);

    const next: ThreadShadow = {
      ...base,
      title: base.title || threadTitle(message),
      latest_summary: summarize(message.content) || base.latest_summary,
      turn_count: base.turn_count + 1,
      effective_turn_count: base.effective_turn_count + (classification.effective ? 1 : 0),
      noise_turn_count: base.noise_turn_count + (classification.signal_kind === 'noise' ? 1 : 0),
      promotion_score: nextPromotionScore,
      last_message_at: message.timestamp || now,
      last_effective_at: classification.effective ? message.timestamp || now : base.last_effective_at,
      last_signal_kind: classification.signal_kind,
      hard_promotion_ready: classification.hard_promotion_ready,
      high_priority: highPriority,
      linked_session_id: options.linked_session_id ?? base.linked_session_id,
      metadata: {
        ...base.metadata,
        ...metadata,
        last_message_type: message.message_type,
        last_message_id: message.source_message_id || null,
        last_author_id: message.source_author_id || null,
        last_author_name: message.source_author_name || null,
        connector_followup: classification.connector_followup,
      },
      updated_at: now,
      archived_at: null,
    };

    next.promotion_reasons = uniqueReasons([
      ...base.promotion_reasons,
      ...classification.promotion_reasons,
      ...(classification.connector_followup ? (['connector_followup'] as PromotionReason[]) : []),
    ]);

    const shouldPromote = this.shouldPromote(next);
    next.state = this.shadowState(next, shouldPromote);

    if (index >= 0) {
      shadows[index] = next;
    } else {
      shadows.push(next);
    }

    return { shadow: next, shouldPromote };
  }

  private async appendInboundToSession(session: SessionRecord, message: NormalizedInboundMessage) {
    let target = session;
    if (!target.active_run_id || target.current_state === 'archived') {
      target = await this.sessionService.resume(
        target.session_id,
        `Resume from ${message.source_type} thread update.`
      );
    }

    if (!target.active_run_id) {
      throw new Error(`Session ${target.session_id} has no active run after inbound processing.`);
    }

    await this.eventService.append(target.session_id, target.active_run_id, 'message_received', {
      source_type: message.source_type,
      source_thread_key: message.source_thread_key,
      source_message_id: message.source_message_id,
      source_author_id: message.source_author_id,
      source_author_name: message.source_author_name,
      content: message.content,
    });
    await this.spoolService.appendInbound(target.session_id, target.active_run_id, message);

    const sessions = await this.sessionService.refreshIndexes();
    await this.attentionService.refresh(sessions);
    return target;
  }

  async listShadows() {
    const shadows = await this.readManagedShadows();
    return shadows.sort((a, b) => b.updated_at.localeCompare(a.updated_at));
  }

  async listPromotionQueue() {
    await this.readManagedShadows();
    return this.store.readJson<PromotionQueueEntry[]>(this.store.promotionQueueFile, []);
  }

  async getShadow(shadowId: string) {
    const shadows = await this.readManagedShadows();
    return shadows.find((shadow) => shadow.shadow_id === shadowId) || null;
  }

  async findByThread(sourceType: string, sourceThreadKey: string) {
    const shadows = await this.readManagedShadows();
    return (
      shadows.find(
        (shadow) =>
          shadow.source_type === sourceType && shadow.source_thread_key === sourceThreadKey
      ) || null
    );
  }

  async focusCandidates(limit = 5) {
    const queue = await this.listPromotionQueue();
    return queue.filter((item) => item.promotion_score >= 3 || item.hard_promotion_ready).slice(0, limit);
  }

  async archiveShadow(shadowId: string) {
    return withNamedLock('manager:thread-shadows', async () => {
      const shadows = await this.readManagedShadows();
      const index = shadows.findIndex((shadow) => shadow.shadow_id === shadowId);
      if (index < 0) {
        throw new Error(`Thread shadow not found: ${shadowId}`);
      }
      const next: ThreadShadow = {
        ...shadows[index],
        state: 'archived',
        archived_at: nowIso(),
        updated_at: nowIso(),
      };
      shadows[index] = next;
      await this.writeShadows(shadows);
      return next;
    });
  }

  private async promoteFromShadows(
    shadows: ThreadShadow[],
    index: number,
    input: Partial<AdoptSessionInput> = {},
    extraReasons: PromotionReason[] = []
  ) {
    const shadow = shadows[index];
    let session =
      shadow.linked_session_id ? await this.sessionService.getSession(shadow.linked_session_id) : null;

    if (!session) {
      session = await this.sessionService.adopt({
        title: input.title?.trim() || shadow.title,
        objective: input.objective?.trim() || defaultObjective(shadow),
        owner: input.owner ?? null,
        source_channels: uniqueStrings([shadow.source_type, ...(input.source_channels || [])]),
        priority: input.priority || (shadow.high_priority ? 'high' : 'normal'),
        tags: uniqueStrings(['shadow-promoted', ...(input.tags || [])]),
        initial_message: input.initial_message?.trim() || shadow.latest_summary,
        metadata: {
          ...shadow.metadata,
          ...(input.metadata || {}),
          shadow_id: shadow.shadow_id,
          source_thread_key: shadow.source_thread_key,
          promotion_reasons: uniqueReasons([...shadow.promotion_reasons, ...extraReasons]),
        },
      });
    } else if (!session.active_run_id || session.current_state === 'archived') {
      session = await this.sessionService.resume(session.session_id, 'Resume promoted thread shadow.');
    }

    if (shadow.source_thread_key) {
      await this.bindingService.add({
        channel: shadow.source_type,
        external_thread_key: shadow.source_thread_key,
        session_id: session.session_id,
      });
    }

    const nextShadow: ThreadShadow = {
      ...shadow,
      state: 'promoted',
      linked_session_id: session.session_id,
      promotion_reasons: uniqueReasons([...shadow.promotion_reasons, ...extraReasons]),
      hard_promotion_ready: false,
      updated_at: nowIso(),
      archived_at: null,
    };
    shadows[index] = nextShadow;
    await this.writeShadows(shadows);

    const sessions = await this.sessionService.refreshIndexes();
    await this.attentionService.refresh(sessions);

    return {
      shadow: nextShadow,
      session,
    };
  }

  async promoteShadow(
    shadowId: string,
    input: Partial<AdoptSessionInput> = {},
    extraReasons: PromotionReason[] = []
  ) {
    return withNamedLock('manager:thread-shadows', async () => {
      const shadows = await this.readManagedShadows();
      const index = shadows.findIndex((shadow) => shadow.shadow_id === shadowId);
      if (index < 0) {
        throw new Error(`Thread shadow not found: ${shadowId}`);
      }
      return this.promoteFromShadows(shadows, index, input, extraReasons);
    });
  }

  async manualAdopt(input: Record<string, unknown>) {
    return withNamedLock('manager:thread-shadows', async () => {
      const shadowId = typeof input.shadow_id === 'string' ? input.shadow_id : null;
      if (shadowId) {
        const shadows = await this.readManagedShadows();
        const index = shadows.findIndex((shadow) => shadow.shadow_id === shadowId);
        if (index < 0) {
          throw new Error(`Thread shadow not found: ${shadowId}`);
        }
        return this.promoteFromShadows(
          shadows,
          index,
          {
            title: typeof input.title === 'string' ? input.title : undefined,
            objective: typeof input.objective === 'string' ? input.objective : undefined,
            owner: typeof input.owner === 'string' ? input.owner : undefined,
            source_channels: Array.isArray(input.source_channels) ? (input.source_channels as string[]) : undefined,
            priority:
              input.priority === 'low' || input.priority === 'normal' || input.priority === 'high'
                ? input.priority
                : undefined,
            tags: Array.isArray(input.tags) ? (input.tags as string[]) : undefined,
            initial_message: typeof input.initial_message === 'string' ? input.initial_message : undefined,
            metadata: asRecord(input.metadata),
          },
          ['manual_adopt']
        );
      }

      const sourceType = typeof input.source_type === 'string' ? input.source_type : 'chat';
      const sourceThreadKey =
        typeof input.source_thread_key === 'string' && input.source_thread_key.trim()
          ? input.source_thread_key.trim()
          : `manual:${uid('thread')}`;
      const message: NormalizedInboundMessage = {
        request_id: uid('req'),
        external_trigger_id: uid('evt'),
        source_type: sourceType,
        source_thread_key: sourceThreadKey,
        source_message_id: null,
        source_author_id: null,
        source_author_name: null,
        target_session_id: null,
        message_type: 'user_message',
        content:
          (typeof input.initial_message === 'string' && input.initial_message.trim()) ||
          (typeof input.objective === 'string' && input.objective.trim()) ||
          'Manual adoption requested.',
        attachments: [],
        timestamp: nowIso(),
        metadata: {
          ...asRecord(input.metadata),
          high_priority: input.priority === 'high',
          thread_title: typeof input.title === 'string' ? input.title : undefined,
        },
      };

      const shadows = await this.readManagedShadows();
      const { shadow } = this.upsertObservedShadow(shadows, message, {
        manual_adopt: true,
        high_priority: input.priority === 'high',
      });
      const index = shadows.findIndex((item) => item.shadow_id === shadow.shadow_id);
      return this.promoteFromShadows(
        shadows,
        index,
        {
          title: typeof input.title === 'string' ? input.title : shadow.title,
          objective: typeof input.objective === 'string' ? input.objective : defaultObjective(shadow),
          owner: typeof input.owner === 'string' ? input.owner : undefined,
          source_channels: Array.isArray(input.source_channels) ? (input.source_channels as string[]) : undefined,
          priority:
            input.priority === 'low' || input.priority === 'normal' || input.priority === 'high'
              ? input.priority
              : undefined,
          tags: Array.isArray(input.tags) ? (input.tags as string[]) : undefined,
          initial_message:
            (typeof input.initial_message === 'string' && input.initial_message.trim()) || shadow.latest_summary,
          metadata: asRecord(input.metadata),
        },
        ['manual_adopt']
      );
    });
  }

  async handleInbound(message: NormalizedInboundMessage) {
    return withNamedLock('manager:thread-shadows', async () => {
      const binding = await this.bindingService.resolve(message.source_type, message.source_thread_key);
      const shadows = await this.readManagedShadows();
      const linkedShadow =
        shadows.find(
          (shadow) =>
            shadow.source_type === message.source_type &&
            shadow.source_thread_key === message.source_thread_key
        ) || null;
      const targetSessionId =
        message.target_session_id || binding?.session_id || linkedShadow?.linked_session_id || null;
      const { shadow, shouldPromote } = this.upsertObservedShadow(shadows, message, {
        linked_session_id: targetSessionId,
      });

      if (targetSessionId) {
        const session = await this.sessionService.getSession(targetSessionId);
        if (!session) {
          shadow.linked_session_id = null;
          shadow.state = this.shadowState(shadow, shouldPromote);
        } else {
          const updatedSession = await this.appendInboundToSession(session, message);
          shadow.state = 'promoted';
          shadow.linked_session_id = updatedSession.session_id;
          await this.writeShadows(shadows);
          return {
            accepted: true,
            mode: 'promoted' as const,
            shadow_id: shadow.shadow_id,
            shadow_state: shadow.state,
            promotion_score: shadow.promotion_score,
            effective_turn_count: shadow.effective_turn_count,
            hard_promotion_ready: shadow.hard_promotion_ready,
            session_id: updatedSession.session_id,
            active_run_id: updatedSession.active_run_id,
          };
        }
      }

      if (shouldPromote) {
        const index = shadows.findIndex((item) => item.shadow_id === shadow.shadow_id);
        const promoted = await this.promoteFromShadows(shadows, index, {
          title: shadow.title,
          objective: defaultObjective(shadow),
          initial_message: message.content,
          metadata: {
            ...shadow.metadata,
            source_message_id: message.source_message_id,
            source_author_id: message.source_author_id,
            source_author_name: message.source_author_name,
          },
        });
        return {
          accepted: true,
          mode: 'promoted' as const,
          shadow_id: promoted.shadow.shadow_id,
          shadow_state: promoted.shadow.state,
          promotion_score: promoted.shadow.promotion_score,
          effective_turn_count: promoted.shadow.effective_turn_count,
          hard_promotion_ready: promoted.shadow.hard_promotion_ready,
          session_id: promoted.session.session_id,
          active_run_id: promoted.session.active_run_id,
        };
      }

      await this.writeShadows(shadows);
      return {
        accepted: true,
        mode: 'shadowed' as const,
        shadow_id: shadow.shadow_id,
        shadow_state: shadow.state,
        promotion_score: shadow.promotion_score,
        effective_turn_count: shadow.effective_turn_count,
        hard_promotion_ready: shadow.hard_promotion_ready,
      };
    });
  }
}
