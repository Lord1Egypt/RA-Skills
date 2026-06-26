import { type ParsedCommand, isParseError, parseMetaCommand } from "./command-parser.ts";
import type { MetadataStore } from "./store.ts";
import type { TopicMetadata } from "./types.ts";

export interface CommandContext {
  streamId: number;
  topicName: string;
}

function formatMetadata(meta: TopicMetadata): string {
  const lines = [
    `📋 Topic: ${meta.topic_name}`,
    `├─ Status: ${meta.status}`,
    `├─ Priority: ${meta.priority ?? "—"}`,
    `├─ Assignee: ${meta.assignee ?? "—"}`,
    `├─ Labels: ${meta.labels.length > 0 ? `[${meta.labels.join(", ")}]` : "—"}`,
    `├─ Due: ${meta.due_date ?? "—"}`,
    `└─ Updated: ${meta.updated_at}`,
  ];
  return lines.join("\n");
}

function formatListItem(meta: TopicMetadata): string {
  const parts = [meta.topic_name, `(${meta.status})`];
  if (meta.assignee) {
    parts.push(`@${meta.assignee}`);
  }
  if (meta.labels.length > 0) {
    parts.push(`[${meta.labels.join(", ")}]`);
  }
  return parts.join(" ");
}

export function handleMetaCommand(store: MetadataStore, ctx: CommandContext, text: string): string {
  const parsed = parseMetaCommand(text);
  if (isParseError(parsed)) {
    return `❌ ${parsed.error}`;
  }
  return executeCommand(store, ctx, parsed);
}

function executeCommand(store: MetadataStore, ctx: CommandContext, cmd: ParsedCommand): string {
  switch (cmd.action) {
    case "show": {
      const meta = store.get(ctx.streamId, ctx.topicName);
      if (!meta) {
        return `📋 No metadata for topic: ${ctx.topicName}`;
      }
      return formatMetadata(meta);
    }

    case "set": {
      const meta = store.upsert(ctx.streamId, ctx.topicName, cmd.updates);
      return `✅ Updated metadata\n${formatMetadata(meta)}`;
    }

    case "label": {
      const meta =
        cmd.op === "add"
          ? store.addLabel(ctx.streamId, ctx.topicName, cmd.tag)
          : store.removeLabel(ctx.streamId, ctx.topicName, cmd.tag);
      const verb = cmd.op === "add" ? "Added" : "Removed";
      return `🏷️ ${verb} label: ${cmd.tag}\n${formatMetadata(meta)}`;
    }

    case "list": {
      const items = store.list(ctx.streamId, cmd.filter);
      if (items.length === 0) {
        return "📋 No topics found matching filter";
      }
      const header = `📋 Topics in stream (${items.length}):`;
      const lines = items.map((m) => `  • ${formatListItem(m)}`);
      return [header, ...lines].join("\n");
    }

    case "clear": {
      const removed = store.remove(ctx.streamId, ctx.topicName);
      return removed
        ? `🗑️ Cleared metadata for: ${ctx.topicName}`
        : `📋 No metadata to clear for: ${ctx.topicName}`;
    }
  }
}
