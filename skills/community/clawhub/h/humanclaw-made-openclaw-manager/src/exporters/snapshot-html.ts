import { CheckpointRecord, EventRecord, SessionRecord, SnapshotManifest, SpoolEntry } from '../types';

const escapeHtml = (value: string) =>
  value.replace(/[<>&"]/g, (character) => ({ '<': '&lt;', '>': '&gt;', '&': '&amp;', '"': '&quot;' }[character] || character));

const renderList = (items: string[]) => (items.length ? `<ul>${items.map((item) => `<li>${escapeHtml(item)}</li>`).join('')}</ul>` : '<p>None.</p>');

const renderRecords = (title: string, rows: string[]) =>
  `<section><h2>${escapeHtml(title)}</h2>${rows.length ? `<pre>${escapeHtml(rows.join('\n'))}</pre>` : '<p>None.</p>'}</section>`;

export const renderSnapshotHtml = (params: {
  manifest: SnapshotManifest;
  session: SessionRecord;
  summary: string;
  checkpoint: CheckpointRecord | null;
  events: EventRecord[];
  spool: SpoolEntry[];
}) => {
  const { manifest, session, summary, checkpoint, events, spool } = params;
  return `<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>${escapeHtml(session.title)} - ${escapeHtml(manifest.snapshot_kind)}</title>
    <style>
      body { font-family: Georgia, 'Times New Roman', serif; margin: 32px auto; max-width: 960px; line-height: 1.55; color: #1f2937; }
      h1, h2 { color: #111827; }
      .meta { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px; margin: 24px 0; }
      .card { border: 1px solid #d1d5db; border-radius: 12px; padding: 16px; background: #f9fafb; }
      pre { white-space: pre-wrap; background: #f3f4f6; border-radius: 12px; padding: 16px; }
      section { margin-top: 28px; }
    </style>
  </head>
  <body>
    <h1>${escapeHtml(session.title)}</h1>
    <p>${escapeHtml(session.objective)}</p>
    <div class="meta">
      <div class="card"><strong>Snapshot kind</strong><div>${escapeHtml(manifest.snapshot_kind)}</div></div>
      <div class="card"><strong>Current state</strong><div>${escapeHtml(session.current_state)}</div></div>
      <div class="card"><strong>Owner</strong><div>${escapeHtml(session.owner || 'local')}</div></div>
      <div class="card"><strong>Created</strong><div>${escapeHtml(manifest.created_at)}</div></div>
    </div>

    <section>
      <h2>Summary</h2>
      <pre>${escapeHtml(summary)}</pre>
    </section>

    <section>
      <h2>Blockers</h2>
      ${renderList(checkpoint?.blockers || session.blockers)}
    </section>

    <section>
      <h2>Pending Human Decisions</h2>
      ${renderList(checkpoint?.pending_human_decisions || session.pending_human_decisions)}
    </section>

    <section>
      <h2>Key Decisions</h2>
      ${renderList(manifest.key_decisions)}
    </section>

    <section>
      <h2>Artifacts</h2>
      ${renderList(manifest.artifact_refs)}
    </section>

    ${renderRecords(
      'Run Evidence',
      events.map((event) => `${event.timestamp} ${event.event_type} ${JSON.stringify(event.payload)}`)
    )}

    ${renderRecords(
      'Spool Preview',
      spool.map((entry) => `${entry.created_at} ${entry.entry_type} ${JSON.stringify(entry.payload)}`)
    )}
  </body>
</html>
`;
};
