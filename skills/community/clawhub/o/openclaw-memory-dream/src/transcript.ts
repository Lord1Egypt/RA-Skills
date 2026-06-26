import { readFile, readdir } from "fs/promises";
import { join } from "path";

interface JsonlMessage {
  role?: string;
  content?: unknown;
}

function extractText(content: unknown): string {
  if (typeof content === "string") return content;
  if (Array.isArray(content)) {
    return (content as Array<{ type?: string; text?: string }>)
      .filter((c) => c.type === "text")
      .map((c) => c.text ?? "")
      .join(" ");
  }
  return "";
}

function isHighValue(text: string): boolean {
  const lower = text.toLowerCase();
  return (
    lower.includes("actually") ||
    lower.includes("no, ") ||
    lower.includes("don't ") ||
    lower.includes("prefer") ||
    lower.includes("always ") ||
    lower.includes("never ") ||
    lower.includes("instead") ||
    lower.includes("wrong") ||
    lower.includes("remember") ||
    lower.includes("decided") ||
    lower.includes("important")
  );
}

async function parseJsonl(filePath: string): Promise<JsonlMessage[]> {
  try {
    const raw = await readFile(filePath, "utf-8");
    const messages: JsonlMessage[] = [];
    for (const line of raw.split("\n")) {
      const trimmed = line.trim();
      if (!trimmed) continue;
      try {
        messages.push(JSON.parse(trimmed));
      } catch {
        // skip malformed lines
      }
    }
    return messages;
  } catch {
    return [];
  }
}

export async function readRecentTranscripts(
  agentStateDir: string,
  maxEntries = 20
): Promise<string> {
  const candidates: string[] = [];

  try {
    const entries = await readdir(agentStateDir);
    for (const entry of entries) {
      if (entry.endsWith(".jsonl")) {
        candidates.push(join(agentStateDir, entry));
      }
    }
  } catch {
    return "(no transcript data available)";
  }

  if (candidates.length === 0) {
    return "(no transcript data available)";
  }

  // Most recent files first
  candidates.sort().reverse();
  const filesToRead = candidates.slice(0, 3);

  const pairs: string[] = [];

  for (const file of filesToRead) {
    const messages = await parseJsonl(file);

    let i = 0;
    while (i < messages.length && pairs.length < maxEntries) {
      const msg = messages[i];
      if (msg.role === "user") {
        const userText = extractText(msg.content);
        const next = messages[i + 1];
        const assistantText = next?.role === "assistant" ? extractText(next.content) : "";

        if (isHighValue(userText) || isHighValue(assistantText)) {
          const excerpt = [
            userText ? `User: ${userText.slice(0, 500)}` : null,
            assistantText ? `Assistant: ${assistantText.slice(0, 500)}` : null,
          ]
            .filter(Boolean)
            .join("\n");
          if (excerpt) pairs.push(excerpt);
        }
        i += 2;
      } else {
        i++;
      }
    }
  }

  return pairs.length > 0
    ? pairs.join("\n\n---\n\n")
    : "(no high-value transcript moments found)";
}
