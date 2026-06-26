/**
 * Emoji prefix → status sync logic for Zulip topic renames.
 *
 * Zulip topics can carry emoji prefixes that map to metadata statuses.
 * When a topic is renamed and the prefix changes, we infer a status transition.
 */

export type MetadataStatus = "open" | "wip" | "done";

export const STATUS_PREFIXES: ReadonlyMap<string, MetadataStatus> = new Map([
  ["\u{1F534}", "open"], // 🔴
  ["\u{1F7E1}", "wip"], // 🟡
  ["\u2705", "done"], // ✅
]);

export interface PrefixExtraction {
  prefix: string | null;
  status: MetadataStatus | null;
  baseName: string;
}

/**
 * Extract a status prefix from a topic name.
 * Returns the prefix emoji, mapped status, and the base name without the prefix.
 */
export function extractStatusPrefix(topicName: string): PrefixExtraction {
  const trimmed = topicName.trimStart();
  for (const [prefix, status] of STATUS_PREFIXES) {
    if (trimmed.startsWith(prefix)) {
      const baseName = trimmed.slice(prefix.length).trimStart();
      return { prefix, status, baseName };
    }
  }
  return { prefix: null, status: null, baseName: trimmed };
}

/**
 * Detect if a topic rename changed the status prefix.
 * Returns the new status if the prefix changed, or null if it didn't.
 */
export function inferStatusFromRename(oldTopic: string, newTopic: string): MetadataStatus | null {
  const oldExtracted = extractStatusPrefix(oldTopic);
  const newExtracted = extractStatusPrefix(newTopic);

  if (oldExtracted.prefix === newExtracted.prefix) {
    return null;
  }

  // Prefix changed — return new status (or null if prefix was removed)
  return newExtracted.status;
}

/**
 * Sync a topic rename to the metadata store.
 * Updates the topic name and, if the emoji prefix changed, infers a status transition.
 */
export function syncPrefixToMetadata(
  store: {
    handleRename(streamId: number, oldName: string, newName: string): void;
    upsert(streamId: number, topicName: string, updates: { status?: MetadataStatus }): unknown;
  },
  streamId: number,
  oldTopic: string,
  newTopic: string,
): void {
  store.handleRename(streamId, oldTopic, newTopic);
  const newStatus = inferStatusFromRename(oldTopic, newTopic);
  if (newStatus) {
    store.upsert(streamId, newTopic, { status: newStatus });
  }
}
