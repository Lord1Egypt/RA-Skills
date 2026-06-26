import fs from "node:fs/promises";
import path from "node:path";
import matter from "gray-matter";
import { nanoid } from "nanoid";
import YAML from "yaml";
import type { CalendarCategory, CalendarDocument, CalendarEvent } from "./types";

const EVENT_BLOCK_REGEX = /```event\n([\s\S]*?)```/g;

export const DEFAULT_CATEGORIES: CalendarCategory[] = [
  { id: "school", label: "School", color: "#3f51b5", description: "Classes, homework, studying" },
  { id: "projects", label: "Projects", color: "#039be5", description: "Builds, client work, coding sprints" },
  { id: "life", label: "Life", color: "#d50000", description: "Family, errands, admin, personal" }
];

function nowIso(): string {
  return new Date().toISOString();
}

function parseTimestamp(value?: string): number {
  const parsed = Date.parse(value || "");
  return Number.isFinite(parsed) ? parsed : 0;
}

function normalizeGoogleEventIds(value: unknown): Record<string, string> | undefined {
  if (!value || typeof value !== "object") {
    return undefined;
  }

  const entries = Object.entries(value as Record<string, unknown>).reduce<Array<[string, string]>>((acc, [calendarId, eventId]) => {
    if (typeof calendarId === "string" && calendarId.length > 0 && typeof eventId === "string" && eventId.length > 0) {
      acc.push([calendarId, eventId]);
    }
    return acc;
  }, []);

  if (!entries.length) {
    return undefined;
  }

  return Object.fromEntries(entries);
}

export function ensureCalendarEvent(event: CalendarEvent): CalendarEvent {
  const id = event.id || `evt_${nanoid(8)}`;

  return {
    ...event,
    id,
    externalId: event.externalId?.trim() ? event.externalId : `md_${id}`,
    updatedAt: parseTimestamp(event.updatedAt) > 0 ? event.updatedAt : nowIso(),
    googleEventIds: normalizeGoogleEventIds(event.googleEventIds)
  };
}

function dedupeEventsByExternalId(events: CalendarEvent[]): CalendarEvent[] {
  const deduped = new Map<string, CalendarEvent>();

  for (const raw of events) {
    const event = ensureCalendarEvent(raw);
    const existing = deduped.get(event.externalId);

    if (!existing || parseTimestamp(event.updatedAt) >= parseTimestamp(existing.updatedAt)) {
      deduped.set(event.externalId, event);
    }
  }

  return Array.from(deduped.values());
}

export function createDefaultCalendar(): CalendarDocument {
  const now = nowIso();
  const defaultId = `evt_${nanoid(8)}`;
  return {
    frontmatter: {
      version: 1,
      title: "Opy's Calendar",
      timezone: "local",
      updatedAt: now,
      categories: DEFAULT_CATEGORIES
    },
    events: [
      {
        id: defaultId,
        externalId: `md_${defaultId}`,
        updatedAt: now,
        title: "Weekly planning",
        start: new Date(new Date().setHours(9, 0, 0, 0)).toISOString(),
        end: new Date(new Date().setHours(10, 0, 0, 0)).toISOString(),
        allDay: false,
        category: "projects",
        completed: false,
        notes: "Review priorities and blockers for the week"
      }
    ]
  };
}

function normalizeCategory(category: unknown): CalendarCategory | null {
  if (!category || typeof category !== "object") {
    return null;
  }

  const c = category as Record<string, unknown>;
  if (typeof c.id !== "string" || typeof c.label !== "string" || typeof c.color !== "string") {
    return null;
  }

  return {
    id: c.id,
    label: c.label,
    color: c.color,
    description: typeof c.description === "string" ? c.description : undefined
  };
}

function normalizeEvent(raw: unknown): CalendarEvent | null {
  if (!raw || typeof raw !== "object") {
    return null;
  }

  const e = raw as Record<string, unknown>;
  if (typeof e.title !== "string" || typeof e.start !== "string" || typeof e.end !== "string") {
    return null;
  }

  const id = typeof e.id === "string" && e.id ? e.id : `evt_${nanoid(8)}`;

  return ensureCalendarEvent({
    id,
    externalId: typeof e.externalId === "string" ? e.externalId : `md_${id}`,
    updatedAt: typeof e.updatedAt === "string" ? e.updatedAt : nowIso(),
    title: e.title,
    start: e.start,
    end: e.end,
    allDay: Boolean(e.allDay),
    category: typeof e.category === "string" && e.category ? e.category : "life",
    completed: Boolean(e.completed),
    notes: typeof e.notes === "string" ? e.notes : undefined,
    location: typeof e.location === "string" ? e.location : undefined,
    color: typeof e.color === "string" ? e.color : undefined,
    googleEventIds: normalizeGoogleEventIds(e.googleEventIds)
  });
}

function sortEvents(events: CalendarEvent[]): CalendarEvent[] {
  return [...events].sort((a, b) => a.start.localeCompare(b.start));
}

function displayWindow(event: CalendarEvent): string {
  if (event.allDay) {
    return `${event.start.slice(0, 10)} (all day)`;
  }
  return `${event.start.replace("T", " ").slice(0, 16)} -> ${event.end.replace("T", " ").slice(0, 16)}`;
}

export function serializeCalendarMarkdown(document: CalendarDocument): string {
  const sorted = sortEvents(dedupeEventsByExternalId(document.events));
  const frontmatter = YAML.stringify(document.frontmatter).trim();

  const categoryRows = document.frontmatter.categories
    .map((category) => {
      const description = category.description?.replace(/\|/g, "\\|") ?? "";
      return `| ${category.id} | ${category.label} | ${category.color} | ${description} |`;
    })
    .join("\n");

  const checklist = sorted
    .map((event) => {
      const mark = event.completed ? "x" : " ";
      return `- [${mark}] \`${event.id}\` | ${displayWindow(event)} | **${event.title}** (\`${event.category}\`)`;
    })
    .join("\n");

  const records = sorted
    .map((event) => {
      const payload: Record<string, unknown> = {
        id: event.id,
        externalId: event.externalId,
        updatedAt: event.updatedAt,
        title: event.title,
        start: event.start,
        end: event.end,
        allDay: event.allDay,
        category: event.category,
        completed: event.completed
      };

      if (event.googleEventIds) {
        payload.googleEventIds = event.googleEventIds;
      }
      if (event.location) {
        payload.location = event.location;
      }
      if (event.notes) {
        payload.notes = event.notes;
      }
      if (event.color) {
        payload.color = event.color;
      }

      const yaml = YAML.stringify(payload).trim();
      return `### ${event.id} - ${event.title}\n\n\`\`\`event\n${yaml}\n\`\`\``;
    })
    .join("\n\n");

  return `---\n${frontmatter}\n---

# Calendar

This file is the single source of truth for the calendar app and CLI.
The authoritative event data lives in the \`Event Records\` section.

## Categories

| id | label | color | description |
| --- | --- | --- | --- |
${categoryRows}

## Event Checklist

${checklist || "_No events yet._"}

## Event Records

${records || "_No event records yet._"}
`;
}

export function parseCalendarMarkdown(markdown: string): CalendarDocument {
  const parsed = matter(markdown);
  const fm = parsed.data as Record<string, unknown>;

  const categories = Array.isArray(fm.categories)
    ? fm.categories.map(normalizeCategory).filter((value): value is CalendarCategory => value !== null)
    : [];

  const frontmatter = {
    version: typeof fm.version === "number" ? fm.version : 1,
    title: typeof fm.title === "string" ? fm.title : "Opy's Calendar",
    timezone: typeof fm.timezone === "string" ? fm.timezone : "local",
    updatedAt: typeof fm.updatedAt === "string" ? fm.updatedAt : nowIso(),
    categories: categories.length ? categories : DEFAULT_CATEGORIES
  };

  const events: CalendarEvent[] = [];
  let match: RegExpExecArray | null;
  EVENT_BLOCK_REGEX.lastIndex = 0;

  while ((match = EVENT_BLOCK_REGEX.exec(parsed.content)) !== null) {
    const raw = YAML.parse(match[1]) as unknown;
    const event = normalizeEvent(raw);
    if (event) {
      events.push(event);
    }
  }

  return {
    frontmatter,
    events: sortEvents(dedupeEventsByExternalId(events))
  };
}

export async function loadCalendarFromFile(filePath: string): Promise<CalendarDocument> {
  try {
    const markdown = await fs.readFile(filePath, "utf8");
    return parseCalendarMarkdown(markdown);
  } catch (error) {
    const isMissingFile =
      typeof error === "object" &&
      error !== null &&
      "code" in error &&
      (error as { code?: string }).code === "ENOENT";

    if (!isMissingFile) {
      throw error;
    }

    const fallback = createDefaultCalendar();
    await saveCalendarToFile(filePath, fallback);
    return fallback;
  }
}

export async function saveCalendarToFile(filePath: string, document: CalendarDocument): Promise<void> {
  const normalized: CalendarDocument = {
    ...document,
    frontmatter: {
      ...document.frontmatter,
      updatedAt: nowIso()
    },
    events: sortEvents(dedupeEventsByExternalId(document.events.map((event) => ensureCalendarEvent(event))))
  };

  const markdown = serializeCalendarMarkdown(normalized);
  await fs.mkdir(path.dirname(filePath), { recursive: true });
  await fs.writeFile(filePath, markdown, "utf8");
}
