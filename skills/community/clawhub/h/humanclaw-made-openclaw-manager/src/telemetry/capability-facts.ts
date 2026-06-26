import fs from 'node:fs/promises';
import path from 'node:path';
import { CapabilityFact, CloseSessionInput, SessionRecord, nowIso, uid } from '../types';
import { buildClosureMetrics } from './closure-metrics';
import { deriveScenarioSignature } from './scenario-tagging';
import { EventService } from '../control-plane/event-service';
import { SkillTraceService } from './skill-trace';
import { FsStore } from '../storage/fs-store';
import { CapabilityGraphService } from './capability-graph';
import { renderCapabilityMarkdown } from '../exporters/markdown-report';

export class CapabilityFactService {
  private readonly graphService = new CapabilityGraphService();

  constructor(
    private readonly store: FsStore,
    private readonly eventService: EventService,
    private readonly skillTraceService: SkillTraceService
  ) {}

  async createFromClosure(session: SessionRecord, closeInput: CloseSessionInput = {}) {
    if (!session.metadata.close_outcome && !session.archived_at) {
      throw new Error('Capability facts should be derived from a closed session.');
    }

    const runId =
      typeof session.metadata.last_closed_run_id === 'string'
        ? session.metadata.last_closed_run_id
        : typeof session.metadata.last_resumed_from_run_id === 'string'
          ? session.metadata.last_resumed_from_run_id
          : null;
    const candidateRunId = session.active_run_id || runId || null;
    if (!candidateRunId) {
      throw new Error('Cannot create capability facts without a related run.');
    }

    const events = await this.eventService.list(session.session_id, candidateRunId);
    const traces = await this.skillTraceService.list(session.session_id, candidateRunId);
    const dominantTrace = traces.find((trace) => trace.outcome === 'advanced') || traces[0] || null;
    const metrics = buildClosureMetrics(events, traces);

    const fact: CapabilityFact = {
      fact_id: uid('fact'),
      session_id: session.session_id,
      scenario_signature: deriveScenarioSignature(session, closeInput.closure_type || 'completed'),
      skill_name: dominantTrace?.skill_name || closeInput.reusable_skill_name || null,
      workflow_name: 'openclaw-manager-control-plane',
      style_family: closeInput.style_family || null,
      variant_label: closeInput.variant_label || null,
      closure_type: closeInput.closure_type || 'completed',
      metrics,
      confidence: traces.length ? 0.72 : 0.55,
      sample_size: Math.max(1, traces.length || events.length || 1),
      timestamp: nowIso(),
      anonymized_payload: {
        fact_id: uid('factpub'),
        scenario_signature: deriveScenarioSignature(session, closeInput.closure_type || 'completed'),
        skill_name: dominantTrace?.skill_name || closeInput.reusable_skill_name || null,
        workflow_name: 'openclaw-manager-control-plane',
        style_family: closeInput.style_family || null,
        variant_label: closeInput.variant_label || null,
        closure_type: closeInput.closure_type || 'completed',
        metrics,
        confidence: traces.length ? 0.72 : 0.55,
        sample_size: Math.max(1, traces.length || events.length || 1),
        timestamp: nowIso(),
      },
    };

    await this.store.appendJsonl(this.store.capabilityFactsFile, fact);
    if (candidateRunId) {
      await this.eventService.append(session.session_id, candidateRunId, 'capability_fact_derived', {
        fact_id: fact.fact_id,
        scenario_signature: fact.scenario_signature,
      });
    }
    return fact;
  }

  async listAll() {
    return this.store.readJsonl<CapabilityFact>(this.store.capabilityFactsFile);
  }

  async listBySession(sessionId: string) {
    const facts = await this.listAll();
    return facts.filter((fact) => fact.session_id === sessionId);
  }

  async graphSummary() {
    return this.graphService.buildSummary(await this.listAll());
  }

  async anonymizedExport() {
    return this.graphService.buildAnonymizedExport(await this.listAll());
  }

  async writeMarkdownReport(fileName = 'capability-report.md') {
    const facts = await this.listAll();
    const graph = this.graphService.buildSummary(facts);
    const reportPath = path.join(this.store.exportsDir, fileName);
    await fs.mkdir(this.store.exportsDir, { recursive: true });
    await fs.writeFile(reportPath, `${renderCapabilityMarkdown(facts, graph)}\n`, 'utf8');
    return reportPath;
  }
}
