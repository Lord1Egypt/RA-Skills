import { FsStore } from '../storage/fs-store';
import { NormalizedInboundMessage, SpoolEntry, nowIso, uid } from '../types';

export class SpoolService {
  constructor(private readonly store: FsStore) {}

  async append(sessionId: string, runId: string, entryType: SpoolEntry['entry_type'], payload: Record<string, unknown>) {
    const entry: SpoolEntry = {
      spool_id: uid('spool'),
      session_id: sessionId,
      run_id: runId,
      entry_type: entryType,
      payload,
      created_at: nowIso(),
    };
    await this.store.appendJsonl(this.store.spoolFile(sessionId, runId), entry);
    return entry;
  }

  async appendInbound(sessionId: string, runId: string, message: NormalizedInboundMessage) {
    return this.append(sessionId, runId, 'normalized_inbound', {
      source_type: message.source_type,
      source_thread_key: message.source_thread_key,
      source_message_id: message.source_message_id || null,
      content: message.content,
      attachments: message.attachments,
      metadata: message.metadata,
    });
  }

  async list(sessionId: string, runId: string) {
    return this.store.readJsonl<SpoolEntry>(this.store.spoolFile(sessionId, runId));
  }
}
