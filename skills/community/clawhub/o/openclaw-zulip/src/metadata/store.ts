import type { DatabaseSync, StatementSync } from "node:sqlite";
import type {
  MetadataFilter,
  TopicMetadata,
  TopicMetadataUpdate,
  TopicRenameEntry,
} from "./types.ts";

interface RawTopicMetadata extends Omit<TopicMetadata, "labels"> {
  labels: string;
}

function parseRow(row: RawTopicMetadata): TopicMetadata {
  return { ...row, labels: JSON.parse(row.labels) as string[] };
}

export class MetadataStore {
  private db: DatabaseSync;
  private stmtGet: StatementSync;
  private stmtInsert: StatementSync;
  private stmtDelete: StatementSync;
  private stmtLogRename: StatementSync;
  private stmtRenameHistory: StatementSync;
  private stmtUpdateTopicName: StatementSync;

  constructor(db: DatabaseSync) {
    this.db = db;
    this.stmtGet = db.prepare(
      "SELECT * FROM topic_metadata WHERE stream_id = ? AND topic_name = ?",
    );
    this.stmtInsert = db.prepare(
      `INSERT INTO topic_metadata (stream_id, topic_name, status, priority, assignee, labels, due_date, context)
			 VALUES (?, ?, ?, ?, ?, ?, ?, ?)
			 ON CONFLICT(stream_id, topic_name) DO UPDATE SET
				status = excluded.status,
				priority = excluded.priority,
				assignee = excluded.assignee,
				labels = excluded.labels,
				due_date = excluded.due_date,
				context = excluded.context,
				updated_at = datetime('now')`,
    );
    this.stmtDelete = db.prepare(
      "DELETE FROM topic_metadata WHERE stream_id = ? AND topic_name = ?",
    );
    this.stmtLogRename = db.prepare(
      "INSERT INTO topic_rename_log (stream_id, old_name, new_name) VALUES (?, ?, ?)",
    );
    this.stmtRenameHistory = db.prepare(
      "SELECT * FROM topic_rename_log WHERE stream_id = ? AND (old_name = ? OR new_name = ?) ORDER BY renamed_at ASC",
    );
    this.stmtUpdateTopicName = db.prepare(
      "UPDATE topic_metadata SET topic_name = ?, updated_at = datetime('now') WHERE stream_id = ? AND topic_name = ?",
    );
  }

  get(streamId: number, topicName: string): TopicMetadata | null {
    const row = this.stmtGet.get(streamId, topicName) as RawTopicMetadata | undefined;
    return row ? parseRow(row) : null;
  }

  upsert(streamId: number, topicName: string, updates: TopicMetadataUpdate): TopicMetadata {
    const existing = this.get(streamId, topicName);
    const status = updates.status ?? existing?.status ?? "open";
    const priority = updates.priority ?? existing?.priority ?? null;
    const assignee = updates.assignee ?? existing?.assignee ?? null;
    const labels = updates.labels ?? existing?.labels ?? [];
    const due_date = updates.due_date ?? existing?.due_date ?? null;
    const context = updates.context ?? existing?.context ?? null;

    this.stmtInsert.run(
      streamId,
      topicName,
      status,
      priority,
      assignee,
      JSON.stringify(labels),
      due_date,
      context,
    );

    return this.get(streamId, topicName)!;
  }

  list(streamId: number, filter?: MetadataFilter): TopicMetadata[] {
    const conditions = ["stream_id = ?"];
    const params: (string | number)[] = [streamId];

    if (filter?.status) {
      conditions.push("status = ?");
      params.push(filter.status);
    }
    if (filter?.assignee) {
      conditions.push("assignee = ?");
      params.push(filter.assignee);
    }

    const sql = `SELECT * FROM topic_metadata WHERE ${conditions.join(" AND ")} ORDER BY id ASC`;
    const stmt = this.db.prepare(sql);
    const rows = stmt.all(...params) as unknown as RawTopicMetadata[];

    let results = rows.map(parseRow);

    if (filter?.label) {
      results = results.filter((r) => r.labels.includes(filter.label!));
    }

    return results;
  }

  remove(streamId: number, topicName: string): boolean {
    const result = this.stmtDelete.run(streamId, topicName);
    return result.changes > 0;
  }

  addLabel(streamId: number, topicName: string, label: string): TopicMetadata {
    const existing = this.get(streamId, topicName);
    const labels = existing?.labels ?? [];
    if (!labels.includes(label)) {
      labels.push(label);
    }
    return this.upsert(streamId, topicName, { labels });
  }

  removeLabel(streamId: number, topicName: string, label: string): TopicMetadata {
    const existing = this.get(streamId, topicName);
    const labels = (existing?.labels ?? []).filter((l) => l !== label);
    return this.upsert(streamId, topicName, { labels });
  }

  logRename(streamId: number, oldName: string, newName: string): void {
    this.stmtLogRename.run(streamId, oldName, newName);
  }

  handleRename(streamId: number, oldName: string, newName: string): void {
    this.stmtUpdateTopicName.run(newName, streamId, oldName);
    this.logRename(streamId, oldName, newName);
  }

  getRenameHistory(streamId: number, topicName: string): TopicRenameEntry[] {
    return this.stmtRenameHistory.all(
      streamId,
      topicName,
      topicName,
    ) as unknown as TopicRenameEntry[];
  }
}
