import { AttentionService } from '../control-plane/attention-service';
import { BindingService } from '../control-plane/binding-service';
import { SessionService } from '../control-plane/session-service';
import { ShareService } from '../control-plane/share-service';
import { CapabilityFactService } from '../telemetry/capability-facts';
import { renderDigestMarkdown } from '../exporters/markdown-report';
import { listConnectorAdapters } from '../connectors/registry';
import { ShadowService } from '../control-plane/shadow-service';
import { describePendingPromotion } from '../control-plane/shadow-classifier';

export const buildCommandRegistry = (
  sessions: SessionService,
  attention: AttentionService,
  bindings: BindingService,
  share: ShareService,
  capabilityFacts: CapabilityFactService,
  shadows: ShadowService
) => ({
  '/tasks': async () => ({
    active_sessions: await attention.sessionMap(),
    promotion_queue: await shadows.listPromotionQueue(),
    connectors: listConnectorAdapters().map((adapter) => adapter.source_type),
  }),
  '/resume': (sessionId: string) => sessions.resume(sessionId),
  '/share': async (sessionId: string, input?: { snapshot_kind?: 'task_snapshot' | 'run_evidence' | 'capability_snapshot'; related_run_id?: string }) => {
    const session = await sessions.getSession(sessionId);
    if (!session) {
      throw new Error('Session not found.');
    }
    return share.createSnapshot(session, input?.snapshot_kind || 'task_snapshot', {
      related_run_id: input?.related_run_id || session.active_run_id,
    });
  },
  '/bind': async (input: { channel: string; external_thread_key: string; session_id: string; identity_key?: string }) => {
    const binding = await bindings.add(input);
    const adapter = listConnectorAdapters().find((item) => item.source_type === input.channel);
    if (adapter) {
      await bindings.upsertConnectorConfig(adapter.defaultConfig(input.identity_key || `${input.channel}-default`));
    }
    return binding;
  },
  '/focus': async () => {
    const focus = await attention.focus();
    return {
      ...focus,
      candidate_shadows: await shadows.focusCandidates(),
    };
  },
  '/graph': () => capabilityFacts.graphSummary(),
  '/digest': async () => {
    const sessionMap = await attention.sessionMap();
    const focus = await attention.focus();
    const riskView = await attention.riskView();
    const driftView = await attention.driftView();
    const promotionQueue = await shadows.listPromotionQueue();
    const threadShadows = await shadows.listShadows();
    const threadObservations = threadShadows
      .filter((shadow) => !shadow.linked_session_id && shadow.state !== 'archived' && shadow.state !== 'promoted')
      .map((shadow) => ({
        shadow_id: shadow.shadow_id,
        title: shadow.title,
        state: shadow.state,
        promotion_score: shadow.promotion_score,
        effective_turn_count: shadow.effective_turn_count,
        noise_turn_count: shadow.noise_turn_count,
        last_signal_kind: shadow.last_signal_kind,
        pending_reason: describePendingPromotion(shadow),
      }));
    return {
      session_map: sessionMap,
      focus: {
        ...focus,
        candidate_shadows: promotionQueue.slice(0, 5),
      },
      promotion_queue: promotionQueue,
      thread_shadows: threadShadows,
      thread_observations: threadObservations,
      risk_view: riskView,
      drift_view: driftView,
      markdown: renderDigestMarkdown({
        sessionMap,
        focus: {
          ...focus,
          candidate_shadows: promotionQueue.slice(0, 5),
        },
        riskView,
        driftView,
      }),
    };
  },
  '/checkpoint': (sessionId: string, input?: Record<string, unknown>) => sessions.checkpoint(sessionId, input || {}),
  '/close': (sessionId: string, input?: Record<string, unknown>) => sessions.close(sessionId, input || {}),
  '/adopt': (input: Record<string, unknown>) => shadows.manualAdopt(input),
  '/threads': () => shadows.listShadows(),
  '/promote': (shadowId: string, input?: Record<string, unknown>) =>
    shadows.promoteShadow(String(shadowId), {
      title: typeof input?.title === 'string' ? input.title : undefined,
      objective: typeof input?.objective === 'string' ? input.objective : undefined,
      owner: typeof input?.owner === 'string' ? input.owner : undefined,
      source_channels: Array.isArray(input?.source_channels) ? (input?.source_channels as string[]) : undefined,
      priority:
        input?.priority === 'low' || input?.priority === 'normal' || input?.priority === 'high'
          ? input.priority
          : undefined,
      tags: Array.isArray(input?.tags) ? (input?.tags as string[]) : undefined,
      initial_message: typeof input?.initial_message === 'string' ? input.initial_message : undefined,
      metadata: typeof input?.metadata === 'object' && input.metadata ? (input.metadata as Record<string, unknown>) : {},
    }),
  '/archive-thread': (shadowId: string) => shadows.archiveShadow(String(shadowId)),
});

export type CommandRegistry = ReturnType<typeof buildCommandRegistry>;
