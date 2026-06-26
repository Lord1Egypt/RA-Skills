import fs from 'node:fs/promises';
import express, { Request, Response } from 'express';
import { bootstrapManagerRuntime } from '../skill/bootstrap';
import { healthHandler } from './health';
import { connectorInboundHandler, inboundHandler, processInboundMessage } from './inbound';
import { CloseSessionInput } from '../types';
import { getConnectorAdapter, listConnectorAdapters } from '../connectors/registry';
import { describePendingPromotion } from '../control-plane/shadow-classifier';
import { resolveBindHost, resolvePort } from '../skill/local-config';

const drainConnectorInbox = async (filePath: string) => {
  try {
    const text = await fs.readFile(filePath, 'utf8');
    await fs.writeFile(filePath, '', 'utf8');
    return text
      .split('\n')
      .map((line) => line.trim())
      .filter(Boolean)
      .map((line) => JSON.parse(line) as Record<string, unknown>);
  } catch {
    return [] as Record<string, unknown>[];
  }
};

const startServer = async () => {
  const runtime = await bootstrapManagerRuntime();
  const app = express();

  app.use(express.json({ limit: '1mb' }));

  app.get('/health', healthHandler(runtime.store));

  app.get('/sessions', async (_req: Request, res: Response) => {
    res.json(await runtime.sessionService.listSessions());
  });

  app.get('/sessions/map', async (_req: Request, res: Response) => {
    res.json(await runtime.attentionService.sessionMap());
  });

  app.get('/sessions/digest', async (_req: Request, res: Response) => {
    const sessionMap = await runtime.attentionService.sessionMap();
    const focus = await runtime.attentionService.focus();
    const promotionQueue = await runtime.shadowService.listPromotionQueue();
    const threadShadows = await runtime.shadowService.listShadows();
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
    const riskView = await runtime.attentionService.riskView();
    const driftView = await runtime.attentionService.driftView();
    res.json({
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
    });
  });

  app.get('/sessions/:id', async (req: Request, res: Response) => {
    const session = await runtime.sessionService.getSession(String(req.params.id));
    if (!session) {
      res.status(404).json({ error: 'Session not found.' });
      return;
    }
    const threadShadows = await runtime.shadowService.listShadows();
    res.json({
      session,
      runs: await runtime.sessionService.listRuns(session.session_id),
      attention: await runtime.attentionService.listForSession(session.session_id),
      shared_snapshots: await runtime.shareService.listSharedSnapshots(session.session_id),
      linked_shadows: threadShadows.filter((shadow) => shadow.linked_session_id === session.session_id),
    });
  });

  app.post('/sessions/adopt', async (req: Request, res: Response) => {
    const result = await runtime.shadowService.manualAdopt(req.body || {});
    res.status(201).json(result);
  });

  app.post('/sessions/:id/resume', async (req: Request, res: Response) => {
    const session = await runtime.sessionService.resume(
      String(req.params.id),
      String(req.body?.note || 'Resume requested')
    );
    await runtime.attentionService.refresh(await runtime.sessionService.listSessions());
    res.json(session);
  });

  app.post('/sessions/:id/checkpoint', async (req: Request, res: Response) => {
    const result = await runtime.sessionService.checkpoint(String(req.params.id), req.body || {});
    await runtime.attentionService.refresh(await runtime.sessionService.listSessions());
    res.json(result);
  });

  app.post('/sessions/:id/close', async (req: Request, res: Response) => {
    const session = await runtime.sessionService.close(String(req.params.id), (req.body || {}) as CloseSessionInput);
    const fact = await runtime.capabilityFactService.createFromClosure(session, req.body || {});
    const snapshot = await runtime.shareService.createSnapshot(session, 'capability_snapshot', {
      fact_id: fact.fact_id,
    });
    await runtime.attentionService.refresh(await runtime.sessionService.listSessions());

    res.json({
      session,
      capability_fact: fact,
      snapshot,
    });
  });

  app.get('/threads', async (_req: Request, res: Response) => {
    res.json({
      threads: await runtime.shadowService.listShadows(),
      promotion_queue: await runtime.shadowService.listPromotionQueue(),
    });
  });

  app.get('/threads/:id', async (req: Request, res: Response) => {
    const shadow = await runtime.shadowService.getShadow(String(req.params.id));
    if (!shadow) {
      res.status(404).json({ error: 'Thread shadow not found.' });
      return;
    }
    const session = shadow.linked_session_id
      ? await runtime.sessionService.getSession(shadow.linked_session_id)
      : null;
    res.json({
      shadow,
      linked_session: session,
    });
  });

  app.post('/threads/:id/promote', async (req: Request, res: Response) => {
    const result = await runtime.shadowService.promoteShadow(String(req.params.id), req.body || {});
    res.status(201).json(result);
  });

  app.post('/threads/:id/archive', async (req: Request, res: Response) => {
    const shadow = await runtime.shadowService.archiveShadow(String(req.params.id));
    res.json(shadow);
  });

  app.get('/attention', async (_req: Request, res: Response) => {
    res.json(await runtime.attentionService.list());
  });

  app.get('/attention/focus', async (_req: Request, res: Response) => {
    const focus = await runtime.attentionService.focus();
    res.json({
      ...focus,
      candidate_shadows: await runtime.shadowService.focusCandidates(),
    });
  });

  app.get('/attention/risk', async (_req: Request, res: Response) => {
    res.json(await runtime.attentionService.riskView());
  });

  app.get('/attention/drift', async (_req: Request, res: Response) => {
    res.json(await runtime.attentionService.driftView());
  });

  app.post('/inbound-message', inboundHandler(runtime.shadowService));

  app.get('/connectors', async (_req: Request, res: Response) => {
    const configs = await runtime.bindingService.listConnectorConfigs();
    res.json({
      adapters: listConnectorAdapters().map((adapter) => adapter.source_type),
      configs,
    });
  });

  app.post('/connectors/:name/config', async (req: Request, res: Response) => {
    const adapter = getConnectorAdapter(String(req.params.name));
    if (!adapter) {
      res.status(404).json({ error: 'Unknown connector.' });
      return;
    }
    const config = await runtime.bindingService.upsertConnectorConfig(
      adapter.defaultConfig(String(req.body?.identity_key || `${adapter.source_type}-default`))
    );
    res.status(201).json(config);
  });

  app.post('/connectors/:name/ingest', async (req: Request, res: Response, next: express.NextFunction) => {
    const adapter = getConnectorAdapter(String(req.params.name));
    if (!adapter) {
      res.status(404).json({ error: 'Unknown connector.' });
      return;
    }
    try {
      await connectorInboundHandler(adapter, runtime.shadowService)(req, res);
    } catch (error) {
      next(error);
    }
  });

  app.post('/connectors/:name/poll', async (req: Request, res: Response, next: express.NextFunction) => {
    const adapter = getConnectorAdapter(String(req.params.name));
    if (!adapter) {
      res.status(404).json({ error: 'Unknown connector.' });
      return;
    }
    const payloads = Array.isArray(req.body?.messages)
      ? (req.body.messages as Array<Record<string, unknown>>)
      : await drainConnectorInbox(runtime.store.connectorInboxFile(adapter.source_type));
    const results: Array<Record<string, unknown>> = [];
    try {
      for (const payload of payloads) {
        const normalized = adapter.normalize(payload);
        const result = await processInboundMessage(normalized, {
          shadowService: runtime.shadowService,
        });
        results.push({
          normalized,
          result,
        });
      }
      res.json({
        connector: adapter.source_type,
        polled_messages: payloads.length,
        preview: results,
      });
    } catch (error) {
      next(error);
    }
  });

  app.post('/share/:sessionId', async (req: Request, res: Response) => {
    const session = await runtime.sessionService.getSession(String(req.params.sessionId));
    if (!session) {
      res.status(404).json({ error: 'Session not found.' });
      return;
    }

    const snapshot = await runtime.shareService.createSnapshot(
      session,
      (req.body?.snapshot_kind as 'task_snapshot' | 'run_evidence' | 'capability_snapshot') || 'task_snapshot',
      req.body?.metadata || {}
    );

    res.status(201).json(snapshot);
  });

  app.get('/graph', async (_req: Request, res: Response) => {
    res.json(await runtime.capabilityFactService.graphSummary());
  });

  app.get('/exports/capability-facts', async (_req: Request, res: Response) => {
    res.json(await runtime.capabilityFactService.listAll());
  });

  app.get('/exports/capability-facts/anonymized', async (_req: Request, res: Response) => {
    res.json(await runtime.capabilityFactService.anonymizedExport());
  });

  app.use((error: Error, _req: Request, res: Response, _next: unknown) => {
    res.status(500).json({ error: error.message || 'Unexpected manager error.' });
  });

  const port = resolvePort();
  const bindHost = resolveBindHost();
  return new Promise<void>((resolve) => {
    app.listen(port, bindHost, () => {
      console.log(`OpenClaw Manager sidecar listening on ${bindHost}:${port}`);
      resolve();
    });
  });
};

if (require.main === module) {
  void startServer();
}

export { startServer };
