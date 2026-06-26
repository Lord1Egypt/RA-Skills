export { initDatabase } from "./schema.ts";
export { initMetadataStore, getMetadataStore, destroyMetadataStore } from "./singleton.ts";
export { MetadataStore } from "./store.ts";
export { parseMetaCommand, isParseError } from "./command-parser.ts";
export type { ParsedCommand, ParseResult, ParseError, CommandAction } from "./command-parser.ts";
export { handleMetaCommand } from "./command-handler.ts";
export type { CommandContext } from "./command-handler.ts";
export { syncPrefixToMetadata, extractStatusPrefix, inferStatusFromRename } from "./prefix-sync.ts";
export type { MetadataStatus, PrefixExtraction } from "./prefix-sync.ts";
export type {
  MetadataFilter,
  TopicMetadata,
  TopicMetadataUpdate,
  TopicPriority,
  TopicRenameEntry,
  TopicStatus,
} from "./types.ts";
