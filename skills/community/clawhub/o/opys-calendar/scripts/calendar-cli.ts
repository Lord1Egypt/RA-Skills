#!/usr/bin/env node
import fs from "node:fs/promises";
import path from "node:path";
import readline from "node:readline/promises";
import { stdin as input, stdout as output } from "node:process";
import { Command } from "commander";
import { nanoid } from "nanoid";
import {
  ensureCalendarEvent,
  loadCalendarFromFile,
  parseCalendarMarkdown,
  saveCalendarToFile,
  serializeCalendarMarkdown
} from "../shared/calendarMarkdown";
import type { CalendarDocument, CalendarEvent } from "../shared/types";

const program = new Command();
const calendarPath = path.join(process.cwd(), "calendar.md");
const defaultSnapshotPath = path.join(process.cwd(), "agent-snapshot.md");
const upcomingWindowDays = 7;

interface TimeRange {
  startMs: number;
  endMs: number;
}

interface TimeConflict {
  event: CalendarEvent;
  startMs: number;
  endMs: number;
}

interface ConflictResolutionOptions {
  allowOverlap?: boolean;
  shiftToNext?: boolean;
}

interface ResolvedWindow {
  start: string;
  end: string;
  acceptedOverlap: boolean;
  shifted: boolean;
}

function findEvent(document: CalendarDocument, id: string): CalendarEvent {
  const event = document.events.find((item) => item.id === id);
  if (!event) {
    throw new Error(`No event found with id: ${id}`);
  }
  return event;
}

function nowIso(): string {
  return new Date().toISOString();
}

function parseIsoToMs(value: string, fieldName: string): number {
  const parsed = Date.parse(value);
  if (!Number.isFinite(parsed)) {
    throw new Error(`Invalid ${fieldName}: ${value}`);
  }
  return parsed;
}

function parseEventRange(event: CalendarEvent): TimeRange {
  const startMs = parseIsoToMs(event.start, `start for event ${event.id}`);
  const endMs = parseIsoToMs(event.end, `end for event ${event.id}`);
  if (endMs <= startMs) {
    throw new Error(`Invalid range for event ${event.id}: end must be after start`);
  }
  return { startMs, endMs };
}

function formatIsoCompact(iso: string): string {
  return iso.replace("T", " ").replace(".000Z", "Z");
}

function formatWindow(startMs: number, endMs: number): string {
  return `${new Date(startMs).toISOString()} -> ${new Date(endMs).toISOString()}`;
}

function getConflicts(document: CalendarDocument, startMs: number, endMs: number, excludeId?: string): TimeConflict[] {
  const conflicts: TimeConflict[] = [];

  for (const event of document.events) {
    if (excludeId && event.id === excludeId) {
      continue;
    }

    const range = parseEventRange(event);
    const overlaps = startMs < range.endMs && endMs > range.startMs;
    if (overlaps) {
      conflicts.push({ event, ...range });
    }
  }

  conflicts.sort((a, b) => a.startMs - b.startMs);
  return conflicts;
}

function findNextAvailableWindow(document: CalendarDocument, startMs: number, durationMs: number, excludeId?: string): TimeRange {
  if (durationMs <= 0) {
    throw new Error("Event duration must be greater than zero");
  }

  let candidateStart = startMs;
  for (let i = 0; i < 10000; i += 1) {
    const candidateEnd = candidateStart + durationMs;
    const overlaps = getConflicts(document, candidateStart, candidateEnd, excludeId);
    if (!overlaps.length) {
      return { startMs: candidateStart, endMs: candidateEnd };
    }

    candidateStart = Math.max(...overlaps.map((conflict) => conflict.endMs));
  }

  throw new Error("Unable to find a non-overlapping time window");
}

async function promptConflictResolution(
  document: CalendarDocument,
  payload: { title: string; start: string; end: string },
  options: ConflictResolutionOptions,
  excludeId?: string
): Promise<ResolvedWindow> {
  const allowOverlap = Boolean(options.allowOverlap);
  const shiftToNext = Boolean(options.shiftToNext);
  if (allowOverlap && shiftToNext) {
    throw new Error("Use only one of --allow-overlap or --shift-to-next");
  }

  let startMs = parseIsoToMs(payload.start, "start");
  let endMs = parseIsoToMs(payload.end, "end");
  if (endMs <= startMs) {
    throw new Error("End must be after start");
  }

  const initialConflicts = getConflicts(document, startMs, endMs, excludeId);
  if (!initialConflicts.length) {
    return { start: payload.start, end: payload.end, acceptedOverlap: false, shifted: false };
  }

  if (allowOverlap) {
    return { start: payload.start, end: payload.end, acceptedOverlap: true, shifted: false };
  }

  const getNextWindow = (): TimeRange => findNextAvailableWindow(document, startMs, endMs - startMs, excludeId);
  if (shiftToNext) {
    const nextWindow = getNextWindow();
    return {
      start: new Date(nextWindow.startMs).toISOString(),
      end: new Date(nextWindow.endMs).toISOString(),
      acceptedOverlap: false,
      shifted: true
    };
  }

  if (!input.isTTY || !output.isTTY) {
    throw new Error(
      "Conflicting event detected in non-interactive mode. Re-run with --allow-overlap or --shift-to-next."
    );
  }

  const printConflicts = (conflicts: TimeConflict[]) => {
    console.log(`Conflict detected for "${payload.title}" at ${formatWindow(startMs, endMs)}`);
    for (const conflict of conflicts) {
      console.log(
        `- ${conflict.event.id} | ${formatWindow(conflict.startMs, conflict.endMs)} | ${conflict.event.title}`
      );
    }
    const nextWindow = getNextWindow();
    console.log(`Suggestion (next available): ${formatWindow(nextWindow.startMs, nextWindow.endMs)}`);
  };

  printConflicts(initialConflicts);
  const rl = readline.createInterface({ input, output });
  try {
    while (true) {
      const choiceRaw = await rl.question(
        "Choose: [1] accept overlap, [2] shift to next available, [3] enter custom start/end: "
      );
      const choice = choiceRaw.trim();

      if (choice === "1" || choice.toLowerCase() === "accept") {
        return {
          start: new Date(startMs).toISOString(),
          end: new Date(endMs).toISOString(),
          acceptedOverlap: true,
          shifted: false
        };
      }

      if (choice === "2" || choice.toLowerCase() === "shift") {
        const nextWindow = getNextWindow();
        return {
          start: new Date(nextWindow.startMs).toISOString(),
          end: new Date(nextWindow.endMs).toISOString(),
          acceptedOverlap: false,
          shifted: true
        };
      }

      if (choice === "3" || choice.toLowerCase() === "custom") {
        const customStart = (await rl.question("Custom start (ISO): ")).trim();
        const customEnd = (await rl.question("Custom end (ISO): ")).trim();
        const customStartMs = parseIsoToMs(customStart, "start");
        const customEndMs = parseIsoToMs(customEnd, "end");
        if (customEndMs <= customStartMs) {
          console.log("End must be after start. Try again.");
          continue;
        }

        const customConflicts = getConflicts(document, customStartMs, customEndMs, excludeId);
        if (!customConflicts.length) {
          return {
            start: new Date(customStartMs).toISOString(),
            end: new Date(customEndMs).toISOString(),
            acceptedOverlap: false,
            shifted: true
          };
        }

        startMs = customStartMs;
        endMs = customEndMs;
        printConflicts(customConflicts);
        continue;
      }

      console.log("Please choose 1, 2, or 3.");
    }
  } finally {
    rl.close();
  }
}

function parsePositiveInt(value: string | undefined, fallback: number): number {
  if (!value) {
    return fallback;
  }
  const parsed = Number.parseInt(value, 10);
  if (!Number.isFinite(parsed) || parsed <= 0) {
    return fallback;
  }
  return parsed;
}

function toSnapshotRow(event: CalendarEvent): string {
  const status = event.completed ? "x" : " ";
  return `| [${status}] | ${formatIsoCompact(event.start)} | ${formatIsoCompact(event.end)} | ${event.title.replace(/\|/g, "\\|")} | ${event.category.replace(/\|/g, "\\|")} | ${event.id.replace(/\|/g, "\\|")} |`;
}

function buildSnapshotSection(events: CalendarEvent[]): string {
  if (!events.length) {
    return "_No events in this window._";
  }

  const rows = events
    .slice()
    .sort((a, b) => a.start.localeCompare(b.start))
    .map(toSnapshotRow)
    .join("\n");

  return `| done | start | end | title | category | id |
| --- | --- | --- | --- | --- | --- |
${rows}`;
}

function collectWindowEvents(document: CalendarDocument, fromMs: number, toMs: number): CalendarEvent[] {
  return document.events.filter((event) => {
    const { startMs, endMs } = parseEventRange(event);
    return startMs <= toMs && endMs >= fromMs;
  });
}

async function writeRecentSnapshot(document: CalendarDocument, overridePath?: string): Promise<string> {
  const snapshotPath = overridePath || process.env.CALENDAR_AGENT_SNAPSHOT?.trim() || defaultSnapshotPath;
  const settingsPath = path.join(process.cwd(), ".calendar-settings.json");
  let snapshotDays = parsePositiveInt(process.env.CALENDAR_AGENT_DAYS, 14);
  try {
    const raw = await fs.readFile(settingsPath, "utf8");
    const settings = JSON.parse(raw);
    if (typeof settings.snapshotDays === "number" && settings.snapshotDays > 0) {
      snapshotDays = settings.snapshotDays;
    }
  } catch {
    // ignore
  }

  const recentDays = snapshotDays;
  const nowMs = Date.now();
  const dayMs = 24 * 60 * 60 * 1000;
  const recentFromMs = nowMs - recentDays * dayMs;
  const upcomingToMs = nowMs + upcomingWindowDays * dayMs;

  const recentEvents = collectWindowEvents(document, recentFromMs, nowMs);
  const upcomingEvents = document.events.filter((event) => {
    const { startMs } = parseEventRange(event);
    return startMs > nowMs && startMs <= upcomingToMs;
  });

  const snapshot = `# Calendar Snapshot

Updated: ${nowIso()}
Source: ${calendarPath}
Recent Window: last ${recentDays} day(s)
Upcoming Window: next ${upcomingWindowDays} day(s)

## Recent

${buildSnapshotSection(recentEvents)}

## Upcoming

${buildSnapshotSection(upcomingEvents)}
`;

  await fs.mkdir(path.dirname(snapshotPath), { recursive: true });
  await fs.writeFile(snapshotPath, snapshot, "utf8");
  return snapshotPath;
}

async function saveWithSnapshot(document: CalendarDocument): Promise<{ snapshotPath?: string; warning?: string }> {
  await saveCalendarToFile(calendarPath, document);
  const normalized = await loadCalendarFromFile(calendarPath);
  const targetSnapshotPath = process.env.CALENDAR_AGENT_SNAPSHOT?.trim() || defaultSnapshotPath;

  try {
    const snapshotPath = await writeRecentSnapshot(normalized, targetSnapshotPath);
    return { snapshotPath };
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    return {
      warning: `Snapshot write failed at ${targetSnapshotPath}: ${message}. Set CALENDAR_AGENT_SNAPSHOT to a writable path.`
    };
  }
}

function printSnapshotResult(result: { snapshotPath?: string; warning?: string }) {
  if (result.snapshotPath) {
    console.log(`Snapshot updated at ${result.snapshotPath}`);
  } else if (result.warning) {
    console.warn(result.warning);
  }
}

function printSummary(document: CalendarDocument) {
  console.log(`Title: ${document.frontmatter.title}`);
  console.log(`Timezone: ${document.frontmatter.timezone}`);
  console.log(`Updated: ${document.frontmatter.updatedAt}`);
  console.log(`Categories: ${document.frontmatter.categories.map((category) => category.id).join(", ")}`);
  console.log(`Events: ${document.events.length}`);

  for (const event of document.events) {
    const mark = event.completed ? "x" : " ";
    console.log(
      `- [${mark}] ${event.id} | ${event.start} -> ${event.end} | ${event.title} (${event.category}) [ext:${event.externalId}]`
    );
  }
}

program
  .name("calendar-cli")
  .description("Manage calendar.md through a stable CLI interface")
  .version("0.1.0");

program
  .command("summary")
  .description("Print calendar summary and event list")
  .action(async () => {
    const document = await loadCalendarFromFile(calendarPath);
    printSummary(document);
  });

program
  .command("export")
  .description("Export markdown to stdout or a file")
  .option("-o, --out <path>", "Output file path")
  .action(async (options: { out?: string }) => {
    const document = await loadCalendarFromFile(calendarPath);
    const markdown = serializeCalendarMarkdown(document);

    if (options.out) {
      await fs.writeFile(path.resolve(options.out), markdown, "utf8");
      console.log(`Exported to ${path.resolve(options.out)}`);
      return;
    }

    console.log(markdown);
  });

program
  .command("import")
  .description("Import markdown from a file and overwrite calendar.md")
  .requiredOption("-i, --in <path>", "Input markdown file path")
  .action(async (options: { in: string }) => {
    const markdown = await fs.readFile(path.resolve(options.in), "utf8");
    const parsed = parseCalendarMarkdown(markdown);
    const snapshotResult = await saveWithSnapshot(parsed);
    console.log(`Imported ${parsed.events.length} event(s) into ${calendarPath}`);
    printSnapshotResult(snapshotResult);
  });

program
  .command("add")
  .description("Add a new event")
  .requiredOption("--title <title>", "Event title")
  .requiredOption("--start <iso>", "Start datetime, ISO format")
  .requiredOption("--end <iso>", "End datetime, ISO format")
  .option("--category <id>", "Category id", "life")
  .option("--location <text>", "Location")
  .option("--notes <text>", "Notes")
  .option("--all-day", "All-day event", false)
  .option("--done", "Mark complete", false)
  .option("--allow-overlap", "Accept overlap without prompt", false)
  .option("--shift-to-next", "Auto-shift to next available window", false)
  .action(async (options) => {
    const document = await loadCalendarFromFile(calendarPath);
    const id = `evt_${nanoid(8)}`;

    const requested = {
      title: String(options.title),
      start: String(options.start),
      end: String(options.end)
    };
    const resolution = await promptConflictResolution(document, requested, {
      allowOverlap: Boolean(options.allowOverlap),
      shiftToNext: Boolean(options.shiftToNext)
    });

    const event = ensureCalendarEvent({
      id,
      externalId: `ext_${nanoid(12)}`,
      updatedAt: nowIso(),
      title: requested.title,
      start: resolution.start,
      end: resolution.end,
      allDay: Boolean(options.allDay),
      category: String(options.category),
      completed: Boolean(options.done),
      location: options.location ? String(options.location) : undefined,
      notes: options.notes ? String(options.notes) : undefined
    });

    document.events.push(event);
    const snapshotResult = await saveWithSnapshot(document);
    console.log(`Added event ${event.id} (externalId ${event.externalId})`);
    if (resolution.shifted) {
      console.log(`Shifted to ${event.start} -> ${event.end}`);
    }
    if (resolution.acceptedOverlap) {
      console.log("Overlap accepted.");
    }
    printSnapshotResult(snapshotResult);
  });

program
  .command("update")
  .description("Update an existing event")
  .requiredOption("--id <id>", "Event id")
  .option("--title <title>", "Event title")
  .option("--start <iso>", "Start datetime")
  .option("--end <iso>", "End datetime")
  .option("--category <id>", "Category id")
  .option("--location <text>", "Location")
  .option("--notes <text>", "Notes")
  .option("--all-day", "Set all-day true")
  .option("--not-all-day", "Set all-day false")
  .option("--done", "Set completed true")
  .option("--undone", "Set completed false")
  .option("--allow-overlap", "Accept overlap without prompt", false)
  .option("--shift-to-next", "Auto-shift to next available window", false)
  .action(async (options) => {
    const document = await loadCalendarFromFile(calendarPath);
    const event = findEvent(document, String(options.id));
    const hasTimeChange = Boolean(options.start || options.end);

    let resolvedWindow: ResolvedWindow | null = null;
    if (hasTimeChange) {
      resolvedWindow = await promptConflictResolution(
        document,
        {
          title: options.title ? String(options.title) : event.title,
          start: options.start ? String(options.start) : event.start,
          end: options.end ? String(options.end) : event.end
        },
        {
          allowOverlap: Boolean(options.allowOverlap),
          shiftToNext: Boolean(options.shiftToNext)
        },
        event.id
      );
    } else if (options.allowOverlap || options.shiftToNext) {
      throw new Error("--allow-overlap and --shift-to-next are only valid when changing --start or --end");
    }

    if (options.title) event.title = String(options.title);
    if (resolvedWindow) {
      event.start = resolvedWindow.start;
      event.end = resolvedWindow.end;
    }
    if (options.category) event.category = String(options.category);
    if (options.location !== undefined) event.location = String(options.location);
    if (options.notes !== undefined) event.notes = String(options.notes);

    if (options.allDay) event.allDay = true;
    if (options.notAllDay) event.allDay = false;
    if (options.done) event.completed = true;
    if (options.undone) event.completed = false;

    event.updatedAt = nowIso();

    const snapshotResult = await saveWithSnapshot(document);
    console.log(`Updated event ${event.id}`);
    if (resolvedWindow?.shifted) {
      console.log(`Shifted to ${event.start} -> ${event.end}`);
    }
    if (resolvedWindow?.acceptedOverlap) {
      console.log("Overlap accepted.");
    }
    printSnapshotResult(snapshotResult);
  });

program
  .command("check")
  .description("Mark an event done or undone")
  .requiredOption("--id <id>", "Event id")
  .option("--undone", "Mark incomplete", false)
  .action(async (options) => {
    const document = await loadCalendarFromFile(calendarPath);
    const event = findEvent(document, String(options.id));
    event.completed = !options.undone;
    event.updatedAt = nowIso();
    const snapshotResult = await saveWithSnapshot(document);
    console.log(`${event.id} is now ${event.completed ? "done" : "not done"}`);
    printSnapshotResult(snapshotResult);
  });

program
  .command("delete")
  .description("Delete an event")
  .requiredOption("--id <id>", "Event id")
  .action(async (options) => {
    const document = await loadCalendarFromFile(calendarPath);
    const before = document.events.length;
    document.events = document.events.filter((event) => event.id !== String(options.id));

    if (document.events.length === before) {
      throw new Error(`No event found with id: ${options.id}`);
    }

    const snapshotResult = await saveWithSnapshot(document);
    console.log(`Deleted event ${options.id}`);
    printSnapshotResult(snapshotResult);
  });

program
  .command("category-add")
  .description("Add a new category/tag")
  .requiredOption("--id <id>", "Category id")
  .requiredOption("--label <label>", "Display label")
  .requiredOption("--color <hex>", "Hex color, e.g. #9ca3af")
  .option("--description <text>", "Description")
  .action(async (options) => {
    const document = await loadCalendarFromFile(calendarPath);
    const id = String(options.id).trim();
    if (!id) throw new Error("Category id is required");
    if (document.frontmatter.categories.some((cat) => cat.id === id)) {
      throw new Error(`Category already exists: ${id}`);
    }

    document.frontmatter.categories.push({
      id,
      label: String(options.label),
      color: String(options.color),
      description: options.description ? String(options.description) : ""
    });

    const snapshotResult = await saveWithSnapshot(document);
    console.log(`Added category ${id}`);
    printSnapshotResult(snapshotResult);
  });

program
  .command("category-remove")
  .description("Remove a category/tag")
  .requiredOption("--id <id>", "Category id")
  .option("--reassign <id>", "Reassign events to this category (default: life)", "life")
  .action(async (options) => {
    const document = await loadCalendarFromFile(calendarPath);
    const id = String(options.id).trim();
    if (!id) throw new Error("Category id is required");
    const reassign = String(options.reassign || "life").trim();

    if (!document.frontmatter.categories.some((cat) => cat.id === id)) {
      throw new Error(`Category not found: ${id}`);
    }
    if (id === reassign) {
      throw new Error("Reassign category must be different from the removed category");
    }
    if (!document.frontmatter.categories.some((cat) => cat.id === reassign)) {
      throw new Error(`Reassign category not found: ${reassign}`);
    }

    document.frontmatter.categories = document.frontmatter.categories.filter((cat) => cat.id !== id);
    for (const event of document.events) {
      if (event.category === id) {
        event.category = reassign;
        event.updatedAt = nowIso();
      }
    }

    const snapshotResult = await saveWithSnapshot(document);
    console.log(`Removed category ${id}. Reassigned events to ${reassign}.`);
    printSnapshotResult(snapshotResult);
  });

program.parseAsync(process.argv).catch((error) => {
  console.error(error instanceof Error ? error.message : String(error));
  process.exit(1);
});
