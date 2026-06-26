import fs from 'node:fs/promises';
import path from 'node:path';
import { SessionRecord, SnapshotManifest, nowIso, uid } from '../types';
import { FsStore } from '../storage/fs-store';
import { EventService } from './event-service';
import { RunService } from './run-service';
import { CheckpointService } from './checkpoint-service';
import { SpoolService } from './spool-service';
import { renderSnapshotHtml } from '../exporters/snapshot-html';
import { renderSessionMarkdown } from '../exporters/markdown-report';

export class ShareService {
  constructor(
    private readonly store: FsStore,
    private readonly eventService: EventService,
    private readonly runService: RunService,
    private readonly checkpointService: CheckpointService,
    private readonly spoolService: SpoolService
  ) {}

  async createSnapshot(session: SessionRecord, kind: SnapshotManifest['snapshot_kind'], metadata: Record<string, unknown> = {}) {
    const snapshotId = uid('snap');
    const snapshotDir = this.store.snapshotDir(snapshotId);
    await fs.mkdir(snapshotDir, { recursive: true });

    const relatedRunId =
      (typeof metadata.related_run_id === 'string' ? metadata.related_run_id : null) || session.active_run_id || null;
    const checkpoint = relatedRunId ? await this.checkpointService.get(session.session_id, relatedRunId) : null;
    const summary = await this.store.readText(this.store.summaryFile(session.session_id), session.derived_summary || `# ${session.title}\n`);
    const events = relatedRunId ? await this.eventService.list(session.session_id, relatedRunId) : [];
    const spool = relatedRunId ? await this.spoolService.list(session.session_id, relatedRunId) : [];

    const artifactRefs = Array.from(
      new Set([
        ...(checkpoint?.artifact_refs || []),
        ...(Array.isArray(metadata.artifact_refs) ? (metadata.artifact_refs as string[]) : []),
      ])
    );
    const keyDecisions = Array.from(
      new Set([
        ...(checkpoint?.pending_human_decisions || []),
        ...(Array.isArray(metadata.key_decisions) ? (metadata.key_decisions as string[]) : []),
      ])
    );

    const summaryPath = path.join(snapshotDir, 'summary.md');
    const htmlPath = path.join(snapshotDir, 'index.html');
    const reportText = renderSessionMarkdown(session, checkpoint);
    const manifest: SnapshotManifest = {
      snapshot_id: snapshotId,
      session_id: session.session_id,
      snapshot_kind: kind,
      title: session.title,
      created_at: nowIso(),
      summary_path: summaryPath,
      html_path: htmlPath,
      artifact_refs: artifactRefs,
      key_decisions: keyDecisions,
      related_run_id: relatedRunId,
      redacted: true,
      metadata,
    };

    const html = renderSnapshotHtml({
      manifest,
      session,
      summary,
      checkpoint,
      events: kind === 'run_evidence' ? events : [],
      spool: kind === 'run_evidence' ? spool : [],
    });

    await fs.writeFile(summaryPath, `${reportText}\n`, 'utf8');
    await fs.writeFile(htmlPath, html, 'utf8');
    await fs.writeFile(path.join(snapshotDir, 'manifest.json'), `${JSON.stringify(manifest, null, 2)}\n`, 'utf8');
    await fs.writeFile(
      path.join(this.store.shareDir(session.session_id), `${snapshotId}.json`),
      `${JSON.stringify({ snapshot_id: snapshotId, snapshot_kind: kind, html_path: htmlPath }, null, 2)}\n`,
      'utf8'
    );

    return manifest;
  }

  async listSharedSnapshots(sessionId: string) {
    try {
      const entries = await fs.readdir(this.store.shareDir(sessionId), { withFileTypes: true });
      const items = await Promise.all(
        entries
          .filter((entry) => entry.isFile() && entry.name.endsWith('.json'))
          .map((entry) => this.store.readJson<Record<string, unknown> | null>(path.join(this.store.shareDir(sessionId), entry.name), null))
      );
      return items.filter((item): item is Record<string, unknown> => Boolean(item));
    } catch {
      return [] as Record<string, unknown>[];
    }
  }

  async latestSnapshot(sessionId: string) {
    const snapshots = await this.listSharedSnapshots(sessionId);
    return snapshots.at(-1) || null;
  }
}
