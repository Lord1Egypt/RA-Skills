import path from 'node:path';
import { AttentionUnit, PromotionQueueEntry, SessionRecord, ThreadShadow } from '../types';
import { FsStore } from './fs-store';

export const writeSessionIndexes = async (store: FsStore, sessions: SessionRecord[]) => {
  await store.writeJson(path.join(store.indexesDir, 'sessions.json'), sessions);
  await store.writeJson(
    path.join(store.indexesDir, 'active_sessions.json'),
    sessions.filter((session) => !session.archived_at).map((session) => session.session_id)
  );
};

export const writeAttentionQueue = async (store: FsStore, items: AttentionUnit[]) => {
  await store.writeJson(path.join(store.indexesDir, 'attention_queue.json'), items);
};

export const writeThreadShadows = async (store: FsStore, shadows: ThreadShadow[]) => {
  await store.writeJson(store.threadShadowsFile, shadows);
};

export const writePromotionQueue = async (store: FsStore, items: PromotionQueueEntry[]) => {
  await store.writeJson(store.promotionQueueFile, items);
};
