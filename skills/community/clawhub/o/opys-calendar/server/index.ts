import "dotenv/config";
import fs from "node:fs";
import fsp from "node:fs/promises";
import path from "node:path";
import express from "express";
import cors from "cors";
import { nanoid } from "nanoid";
import {
  ensureCalendarEvent,
  loadCalendarFromFile,
  parseCalendarMarkdown,
  saveCalendarToFile,
  serializeCalendarMarkdown
} from "../shared/calendarMarkdown";
import type { CalendarCategory, CalendarDocument, CalendarEvent } from "../shared/types";

const app = express();
const port = Number(process.env.PORT || 8787);
const root = process.cwd();
const calendarPath = path.join(root, "calendar.md");
const distPath = path.join(root, "dist");
const syncStatePath = path.join(root, ".calendar-google-sync-state.json");
const settingsPath = path.join(root, ".calendar-settings.json");
const sessionCookieName = "calendar_sid";
const oauthScope = ["openid", "email", "profile", "https://www.googleapis.com/auth/calendar"].join(" ");

type SessionTokens = {
  accessToken: string;
  refreshToken?: string;
  expiryAt: number;
  scope?: string;
  tokenType?: string;
};

type SessionUser = {
  sub: string;
  email: string;
  name?: string;
  picture?: string;
};

type SessionData = {
  oauthState?: string;
  tokens?: SessionTokens;
  user?: SessionUser;
  selectedCalendarId?: string;
};

type GoogleCalendarSummary = {
  id: string;
  summary: string;
  primary?: boolean;
  accessRole?: string;
  backgroundColor?: string;
};

type GoogleEventDateValue = {
  date?: string;
  dateTime?: string;
  timeZone?: string;
};

type GoogleEvent = {
  id: string;
  status?: string;
  summary?: string;
  description?: string;
  location?: string;
  updated?: string;
  colorId?: string;
  start?: GoogleEventDateValue;
  end?: GoogleEventDateValue;
  extendedProperties?: {
    private?: Record<string, string>;
  };
};

type GoogleSyncState = {
  version: 1;
  mappings: Record<string, Record<string, string>>;
};

type SyncCounts = {
  insertedLocal: number;
  updatedLocal: number;
  deletedLocal: number;
  insertedGoogle: number;
  updatedGoogle: number;
  deletedGoogle: number;
};

class ApiError extends Error {
  status: number;

  constructor(status: number, message: string) {
    super(message);
    this.status = status;
  }
}

const sessions = new Map<string, SessionData>();
const sessionStorePath = path.join(root, ".calendar-sessions.json");

const authTokens = new Map<string, { sid: string; expiresAt: number }>();
const AUTH_TOKEN_TTL = 60_000;

function loadSessionsFromDisk() {
  if (!fs.existsSync(sessionStorePath)) return;
  try {
    const raw = fs.readFileSync(sessionStorePath, "utf-8");
    const parsed = JSON.parse(raw) as Record<string, SessionData>;
    Object.entries(parsed || {}).forEach(([sid, data]) => {
      sessions.set(sid, data || {});
    });
  } catch {
    // ignore corrupt session store
  }
}

function persistSessionsToDisk() {
  try {
    const data: Record<string, SessionData> = {};
    sessions.forEach((value, key) => {
      data[key] = value;
    });
    fs.writeFileSync(sessionStorePath, JSON.stringify(data, null, 2));
  } catch {
    // ignore write errors
  }
}

loadSessionsFromDisk();

declare global {
  namespace Express {
    interface Request {
      sessionId: string;
      sessionData: SessionData;
    }
  }
}

function nowIso(): string {
  return new Date().toISOString();
}

function parseTimestamp(value?: string): number {
  const parsed = Date.parse(value || "");
  return Number.isFinite(parsed) ? parsed : 0;
}

function cookieMap(raw: string | undefined): Record<string, string> {
  if (!raw) {
    return {};
  }

  return raw.split(";").reduce<Record<string, string>>((acc, token) => {
    const [name, ...rest] = token.trim().split("=");
    if (!name) {
      return acc;
    }
    acc[name] = decodeURIComponent(rest.join("="));
    return acc;
  }, {});
}

function getGoogleConfig() {
  return {
    clientId: process.env.GOOGLE_CLIENT_ID?.trim() || "",
    clientSecret: process.env.GOOGLE_CLIENT_SECRET?.trim() || "",
    redirectUri: process.env.GOOGLE_REDIRECT_URI?.trim() || "",
    appBaseUrl: process.env.APP_BASE_URL?.trim() || "http://localhost:5173"
  };
}

function isGoogleConfigured(): boolean {
  const config = getGoogleConfig();
  return Boolean(config.clientId && config.clientSecret && config.redirectUri);
}

function findEventIndex(document: CalendarDocument, id: string): number {
  return document.events.findIndex((event) => event.id === id);
}

function validateEventInput(event: Partial<CalendarEvent>): string | null {
  if (!event.title || !event.start || !event.end) {
    return "Event requires title, start, and end";
  }
  return null;
}

function requireGoogleSession(session: SessionData): asserts session is SessionData & { user: SessionUser; tokens: SessionTokens } {
  if (!session.user || !session.tokens) {
    throw new ApiError(401, "Sign in with Google first");
  }
}

function getGoogleExternalId(event: GoogleEvent): string | undefined {
  const externalId = event.extendedProperties?.private?.externalId;
  if (typeof externalId === "string" && externalId.trim().length > 0) {
    return externalId;
  }
  return undefined;
}

function toDateOnly(iso: string): string {
  return iso.slice(0, 10);
}

function addDay(dateOnly: string): string {
  const [year, month, day] = dateOnly.split("-").map((value) => Number(value));
  const date = new Date(Date.UTC(year, month - 1, day));
  date.setUTCDate(date.getUTCDate() + 1);
  return date.toISOString().slice(0, 10);
}

function toGoogleDatePayload(event: CalendarEvent): { start: Record<string, string>; end: Record<string, string> } {
  if (event.allDay) {
    const startDate = toDateOnly(event.start);
    const rawEndDate = toDateOnly(event.end);
    const endDate = rawEndDate > startDate ? rawEndDate : addDay(startDate);
    return {
      start: { date: startDate },
      end: { date: endDate }
    };
  }

  return {
    start: { dateTime: event.start },
    end: { dateTime: event.end }
  };
}

function toLocalDateValue(dateValue: GoogleEventDateValue | undefined): string | undefined {
  if (!dateValue) {
    return undefined;
  }
  if (typeof dateValue.dateTime === "string" && dateValue.dateTime) {
    return dateValue.dateTime;
  }
  if (typeof dateValue.date === "string" && dateValue.date) {
    return `${dateValue.date}T00:00:00.000Z`;
  }
  return undefined;
}

function googleEventToLocal(
  googleEvent: GoogleEvent,
  calendarId: string,
  document: CalendarDocument,
  existing?: CalendarEvent
): CalendarEvent | null {
  const start = toLocalDateValue(googleEvent.start);
  const end = toLocalDateValue(googleEvent.end);

  if (!start || !end) {
    return null;
  }

  const privateFields = googleEvent.extendedProperties?.private || {};
  const suggestedCategory = privateFields.category;
  const category =
    suggestedCategory && document.frontmatter.categories.some((item) => item.id === suggestedCategory)
      ? suggestedCategory
      : existing?.category || "life";

  const externalId = getGoogleExternalId(googleEvent) || existing?.externalId || `gcal_${googleEvent.id}`;
  const mappedIds = { ...(existing?.googleEventIds || {}) };
  mappedIds[calendarId] = googleEvent.id;

  return ensureCalendarEvent({
    id: privateFields.localId || existing?.id || `evt_${nanoid(8)}`,
    externalId,
    updatedAt: googleEvent.updated || nowIso(),
    title: googleEvent.summary || existing?.title || "(Untitled)",
    start,
    end,
    allDay: Boolean(googleEvent.start?.date),
    category,
    color: googleEvent.colorId ? GOOGLE_COLORS[googleEvent.colorId] : undefined,
    completed: privateFields.completed === "true" ? true : existing?.completed || false,
    location: googleEvent.location || undefined,
    notes: googleEvent.description || undefined,
    googleEventIds: mappedIds
  });
}

const GOOGLE_COLORS: Record<string, string> = {
  "1": "#7986cb", // Lavender
  "2": "#33b679", // Sage
  "3": "#8e24aa", // Grape
  "4": "#e67c73", // Flamingo
  "5": "#f6bf26", // Banana
  "6": "#f4511e", // Tangerine
  "7": "#039be5", // Peacock
  "8": "#616161", // Graphite
  "9": "#3f51b5", // Blueberry
  "10": "#0b8043", // Basil
  "11": "#d50000" // Tomato
};

function resolveColorToGoogleColorId(colorHex: string | undefined): string | undefined {
  if (!colorHex) return undefined;
  // Google Calendar API uses specific string IDs 1-11 for colors. 
  // We'll map our local hex values to the closest Google Color ID.
  const hex = colorHex.toLowerCase();

  for (const [id, color] of Object.entries(GOOGLE_COLORS)) {
    if (hex.includes(color.replace('#', ''))) return id;
    if (hex === color) return id;
  }

  // Custom fallback mappings for existing hexes
  if (hex.includes("2563eb")) return "9"; // math -> Blueberry
  if (hex.includes("7c3aed")) return "3"; // physics -> Grape 
  if (hex.includes("16a34a")) return "10"; // chem -> Basil
  if (hex.includes("f59e0b")) return "5"; // english -> Banana
  if (hex.includes("f97316")) return "6"; // history -> Tangerine
  if (hex.includes("0ea5a4")) return "7"; // multi -> Peacock
  if (hex.includes("9333ea")) return "3"; // b2a -> Grape
  if (hex.includes("e11d48")) return "11"; // life -> Tomato
  if (hex.includes("9ca3af")) return "8"; // constants -> Graphite
  if (hex.includes("2f63ff")) return "9"; // default old blue

  return undefined; // Fallback to default calendar color
}

function localEventToGooglePayload(event: CalendarEvent, categories: CalendarCategory[]): Record<string, unknown> {
  const dates = toGoogleDatePayload(event);
  const privateFields: Record<string, string> = {
    externalId: event.externalId,
    localId: event.id,
    category: event.category,
    completed: String(event.completed)
  };

  const categoryMatch = categories.find(c => c.id === event.category);
  const eventColorHex = event.color || categoryMatch?.color;
  const colorId = resolveColorToGoogleColorId(eventColorHex);

  const payload: Record<string, unknown> = {
    summary: event.title,
    description: event.notes,
    location: event.location,
    colorId,
    start: dates.start,
    end: dates.end,
    extendedProperties: {
      private: privateFields
    }
  };

  if (!event.notes) {
    delete payload.description;
  }
  if (!event.location) {
    delete payload.location;
  }

  return payload;
}

async function readSyncState(): Promise<GoogleSyncState> {
  try {
    const raw = await fsp.readFile(syncStatePath, "utf8");
    const parsed = JSON.parse(raw) as GoogleSyncState;
    if (parsed && parsed.version === 1 && parsed.mappings && typeof parsed.mappings === "object") {
      return parsed;
    }
  } catch (error) {
    const isMissing =
      typeof error === "object" &&
      error !== null &&
      "code" in error &&
      (error as { code?: string }).code === "ENOENT";

    if (!isMissing) {
      console.warn("Could not read sync state, creating new state file");
    }
  }

  return { version: 1, mappings: {} };
}

async function writeSyncState(state: GoogleSyncState): Promise<void> {
  await fsp.writeFile(syncStatePath, JSON.stringify(state, null, 2), "utf8");
}

async function requestGoogleToken(form: URLSearchParams): Promise<Record<string, unknown>> {
  const response = await fetch("https://oauth2.googleapis.com/token", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded"
    },
    body: form
  });

  const text = await response.text();
  const data = text ? (JSON.parse(text) as Record<string, unknown>) : {};

  if (!response.ok) {
    throw new ApiError(response.status, `Google token exchange failed: ${data.error_description || data.error || response.statusText}`);
  }

  return data;
}

async function refreshAccessToken(session: SessionData): Promise<void> {
  const config = getGoogleConfig();
  const refreshToken = session.tokens?.refreshToken;
  if (!refreshToken) {
    throw new ApiError(401, "Google session expired. Sign in again.");
  }

  const tokenResult = await requestGoogleToken(
    new URLSearchParams({
      client_id: config.clientId,
      client_secret: config.clientSecret,
      refresh_token: refreshToken,
      grant_type: "refresh_token"
    })
  );

  const accessToken = typeof tokenResult.access_token === "string" ? tokenResult.access_token : "";
  if (!accessToken) {
    throw new ApiError(502, "Google did not return an access token");
  }

  const expiresIn = typeof tokenResult.expires_in === "number" ? tokenResult.expires_in : 3600;
  session.tokens = {
    accessToken,
    refreshToken,
    expiryAt: Date.now() + expiresIn * 1000,
    scope: typeof tokenResult.scope === "string" ? tokenResult.scope : session.tokens?.scope,
    tokenType: typeof tokenResult.token_type === "string" ? tokenResult.token_type : session.tokens?.tokenType
  };
}

async function ensureAccessToken(session: SessionData): Promise<string> {
  if (!session.tokens?.accessToken) {
    throw new ApiError(401, "Sign in with Google first");
  }

  if (session.tokens.expiryAt > Date.now() + 60_000) {
    return session.tokens.accessToken;
  }

  await refreshAccessToken(session);
  if (!session.tokens?.accessToken) {
    throw new ApiError(401, "Google session expired. Sign in again.");
  }

  return session.tokens.accessToken;
}

async function googleApi<T>(
  session: SessionData,
  url: string,
  init: RequestInit = {},
  retryOnAuthFailure = true
): Promise<T> {
  const accessToken = await ensureAccessToken(session);
  const headers = new Headers(init.headers || {});
  headers.set("Authorization", `Bearer ${accessToken}`);

  const response = await fetch(url, {
    ...init,
    headers
  });

  if (response.status === 401 && retryOnAuthFailure && session.tokens?.refreshToken) {
    session.tokens.expiryAt = 0;
    await refreshAccessToken(session);
    return googleApi<T>(session, url, init, false);
  }

  if (!response.ok) {
    const body = await response.text();
    throw new ApiError(response.status, `Google API error (${response.status}): ${body || response.statusText}`);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return (await response.json()) as T;
}

async function fetchGoogleUser(session: SessionData): Promise<SessionUser> {
  const userInfo = await googleApi<Record<string, unknown>>(session, "https://openidconnect.googleapis.com/v1/userinfo");
  const sub = typeof userInfo.sub === "string" ? userInfo.sub : "";
  const email = typeof userInfo.email === "string" ? userInfo.email : "";

  if (!sub || !email) {
    throw new ApiError(502, "Google user profile did not include a stable id and email");
  }

  return {
    sub,
    email,
    name: typeof userInfo.name === "string" ? userInfo.name : undefined,
    picture: typeof userInfo.picture === "string" ? userInfo.picture : undefined
  };
}

async function listGoogleCalendars(session: SessionData): Promise<GoogleCalendarSummary[]> {
  type CalendarListResponse = { items?: Array<Record<string, unknown>> };
  const response = await googleApi<CalendarListResponse>(
    session,
    "https://www.googleapis.com/calendar/v3/users/me/calendarList?maxResults=250"
  );

  const calendars = (response.items || [])
    .map((item): GoogleCalendarSummary | null => {
      const id = typeof item.id === "string" ? item.id : "";
      const summary = typeof item.summary === "string" ? item.summary : "";
      if (!id || !summary) {
        return null;
      }

      return {
        id,
        summary,
        primary: Boolean(item.primary),
        accessRole: typeof item.accessRole === "string" ? item.accessRole : undefined,
        backgroundColor: typeof item.backgroundColor === "string" ? item.backgroundColor : undefined
      };
    })
    .filter((value): value is GoogleCalendarSummary => value !== null)
    .sort((a, b) => {
      if (a.primary && !b.primary) return -1;
      if (!a.primary && b.primary) return 1;
      return a.summary.localeCompare(b.summary);
    });

  return calendars;
}

async function listGoogleEvents(session: SessionData, calendarId: string): Promise<GoogleEvent[]> {
  const events: GoogleEvent[] = [];
  let pageToken: string | undefined;

  do {
    const params = new URLSearchParams({
      singleEvents: "true",
      showDeleted: "true",
      maxResults: "2500"
    });

    if (pageToken) {
      params.set("pageToken", pageToken);
    }

    type EventsResponse = {
      items?: GoogleEvent[];
      nextPageToken?: string;
    };

    const response = await googleApi<EventsResponse>(
      session,
      `https://www.googleapis.com/calendar/v3/calendars/${encodeURIComponent(calendarId)}/events?${params.toString()}`
    );

    if (Array.isArray(response.items)) {
      events.push(...response.items.filter((event) => Boolean(event.id)));
    }

    pageToken = response.nextPageToken;
  } while (pageToken);

  return events;
}

async function upsertGoogleEvent(session: SessionData, calendarId: string, event: CalendarEvent, categories: CalendarCategory[]): Promise<GoogleEvent> {
  const payload = localEventToGooglePayload(event, categories);
  const mappedId = event.googleEventIds?.[calendarId];

  if (mappedId) {
    try {
      return await googleApi<GoogleEvent>(
        session,
        `https://www.googleapis.com/calendar/v3/calendars/${encodeURIComponent(calendarId)}/events/${encodeURIComponent(mappedId)}`,
        {
          method: "PATCH",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify(payload)
        }
      );
    } catch (error) {
      if (!(error instanceof ApiError) || (error.status !== 404 && error.status !== 410)) {
        throw error;
      }
    }
  }

  return googleApi<GoogleEvent>(
    session,
    `https://www.googleapis.com/calendar/v3/calendars/${encodeURIComponent(calendarId)}/events`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    }
  );
}

async function deleteGoogleEvent(session: SessionData, calendarId: string, eventId: string): Promise<void> {
  try {
    await googleApi<void>(
      session,
      `https://www.googleapis.com/calendar/v3/calendars/${encodeURIComponent(calendarId)}/events/${encodeURIComponent(eventId)}`,
      {
        method: "DELETE"
      }
    );
  } catch (error) {
    if (error instanceof ApiError && (error.status === 404 || error.status === 410)) {
      return;
    }
    throw error;
  }
}

function buildLocalMap(document: CalendarDocument): Map<string, CalendarEvent> {
  const byExternalId = new Map<string, CalendarEvent>();

  for (const raw of document.events) {
    const event = ensureCalendarEvent(raw);
    const existing = byExternalId.get(event.externalId);
    if (!existing || parseTimestamp(event.updatedAt) >= parseTimestamp(existing.updatedAt)) {
      byExternalId.set(event.externalId, event);
    }
  }

  return byExternalId;
}

async function syncGoogleCalendar(session: SessionData, calendarId: string): Promise<{ counts: SyncCounts; events: number }> {
  requireGoogleSession(session);

  const counts: SyncCounts = {
    insertedLocal: 0,
    updatedLocal: 0,
    deletedLocal: 0,
    insertedGoogle: 0,
    updatedGoogle: 0,
    deletedGoogle: 0
  };

  const document = await loadCalendarFromFile(calendarPath);
  const localByExternalId = buildLocalMap(document);
  const remoteEvents = await listGoogleEvents(session, calendarId);

  const remoteById = new Map<string, GoogleEvent>();
  const remoteByExternalId = new Map<string, GoogleEvent>();
  const cancelledRemote = new Map<string, GoogleEvent>();

  for (const remote of remoteEvents) {
    if (remote.status === "cancelled") {
      cancelledRemote.set(remote.id, remote);
      continue;
    }

    remoteById.set(remote.id, remote);
    const externalId = getGoogleExternalId(remote);
    if (externalId) {
      const existing = remoteByExternalId.get(externalId);
      if (!existing || parseTimestamp(remote.updated) >= parseTimestamp(existing.updated)) {
        remoteByExternalId.set(externalId, remote);
      }
    }
  }

  const handledRemoteIds = new Set<string>();
  const state = await readSyncState();
  const stateKey = `${session.user.sub}:${calendarId}`;
  const previousMapping = state.mappings[stateKey] || {};

  for (const localEvent of localByExternalId.values()) {
    const mappedId = localEvent.googleEventIds?.[calendarId] || previousMapping[localEvent.externalId];
    let remote = mappedId ? remoteById.get(mappedId) : undefined;

    if (!remote) {
      remote = remoteByExternalId.get(localEvent.externalId);
    }

    if (!remote) {
      const created = await upsertGoogleEvent(session, calendarId, localEvent, document.frontmatter.categories);
      if (created.id) {
        const mappedIds = { ...(localEvent.googleEventIds || {}) };
        mappedIds[calendarId] = created.id;
        localByExternalId.set(
          localEvent.externalId,
          ensureCalendarEvent({
            ...localEvent,
            googleEventIds: mappedIds,
            updatedAt: created.updated || nowIso()
          })
        );
        counts.insertedGoogle += 1;
        handledRemoteIds.add(created.id);
      }
      continue;
    }

    handledRemoteIds.add(remote.id);
    const localUpdatedAt = parseTimestamp(localEvent.updatedAt);
    const remoteUpdatedAt = parseTimestamp(remote.updated);

    if (remoteUpdatedAt > localUpdatedAt + 1000) {
      const merged = googleEventToLocal(remote, calendarId, document, localEvent);
      if (merged) {
        localByExternalId.set(localEvent.externalId, merged);
        counts.updatedLocal += 1;
      }
      continue;
    }

    if (localUpdatedAt > remoteUpdatedAt + 1000) {
      const mappedIds = { ...(localEvent.googleEventIds || {}) };
      mappedIds[calendarId] = remote.id;

      const updatedRemote = await googleApi<GoogleEvent>(
        session,
        `https://www.googleapis.com/calendar/v3/calendars/${encodeURIComponent(calendarId)}/events/${encodeURIComponent(remote.id)}`,
        {
          method: "PATCH",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify(localEventToGooglePayload({ ...localEvent, googleEventIds: mappedIds }, document.frontmatter.categories))
        }
      );

      localByExternalId.set(
        localEvent.externalId,
        ensureCalendarEvent({
          ...localEvent,
          googleEventIds: mappedIds,
          updatedAt: updatedRemote.updated || nowIso()
        })
      );
      counts.updatedGoogle += 1;
      continue;
    }

    const mappedIds = { ...(localEvent.googleEventIds || {}) };
    mappedIds[calendarId] = remote.id;
    localByExternalId.set(localEvent.externalId, ensureCalendarEvent({ ...localEvent, googleEventIds: mappedIds }));
  }

  for (const remote of remoteById.values()) {
    if (handledRemoteIds.has(remote.id)) {
      continue;
    }

    const externalId = getGoogleExternalId(remote) || `gcal_${remote.id}`;
    const existing = localByExternalId.get(externalId);
    if (existing) {
      const mergedIds = { ...(existing.googleEventIds || {}) };
      mergedIds[calendarId] = remote.id;
      localByExternalId.set(externalId, ensureCalendarEvent({ ...existing, googleEventIds: mergedIds }));
      continue;
    }

    const converted = googleEventToLocal(remote, calendarId, document);
    if (converted) {
      localByExternalId.set(converted.externalId, converted);
      counts.insertedLocal += 1;
    }
  }

  for (const remote of cancelledRemote.values()) {
    const externalId = getGoogleExternalId(remote);

    if (externalId && localByExternalId.has(externalId)) {
      localByExternalId.delete(externalId);
      counts.deletedLocal += 1;
      continue;
    }

    for (const [candidateExternalId, local] of localByExternalId.entries()) {
      if (local.googleEventIds?.[calendarId] === remote.id) {
        localByExternalId.delete(candidateExternalId);
        counts.deletedLocal += 1;
        break;
      }
    }
  }

  const currentExternalIds = new Set(localByExternalId.keys());
  for (const [externalId, eventId] of Object.entries(previousMapping)) {
    if (currentExternalIds.has(externalId)) {
      continue;
    }

    if (remoteById.has(eventId)) {
      await deleteGoogleEvent(session, calendarId, eventId);
      counts.deletedGoogle += 1;
    }
  }

  document.events = Array.from(localByExternalId.values()).map((event) => ensureCalendarEvent(event));
  await saveCalendarToFile(calendarPath, document);

  const nextMapping: Record<string, string> = {};
  for (const event of document.events) {
    const mappedId = event.googleEventIds?.[calendarId];
    if (mappedId) {
      nextMapping[event.externalId] = mappedId;
    }
  }

  state.mappings[stateKey] = nextMapping;
  await writeSyncState(state);

  return {
    counts,
    events: document.events.length
  };
}

function jsonError(res: express.Response, error: unknown, fallbackMessage: string, fallbackStatus = 500) {
  if (error instanceof ApiError) {
    res.status(error.status).json({ error: error.message });
    return;
  }

  const message = error instanceof Error ? error.message : fallbackMessage;
  res.status(fallbackStatus).json({ error: message });
}

app.use(
  cors({
    origin: true,
    credentials: true
  })
);
app.use(express.json({ limit: "1mb" }));

app.use((req, res, next) => {
  const sidFromCookie = cookieMap(req.headers.cookie)[sessionCookieName];
  const existing = sidFromCookie ? sessions.get(sidFromCookie) : undefined;

  if (sidFromCookie && existing) {
    req.sessionId = sidFromCookie;
    req.sessionData = existing;
    next();
    return;
  }

  if (sidFromCookie && !existing) {
    loadSessionsFromDisk();
    const reloaded = sessions.get(sidFromCookie);
    if (reloaded) {
      req.sessionId = sidFromCookie;
      req.sessionData = reloaded;
      next();
      return;
    }
  }

  const sid = `sid_${nanoid(24)}`;
  const session: SessionData = {};
  sessions.set(sid, session);
  persistSessionsToDisk();

  req.sessionId = sid;
  req.sessionData = session;

  res.cookie(sessionCookieName, sid, {
    httpOnly: true,
    sameSite: "lax",
    maxAge: 1000 * 60 * 60 * 24 * 30,
    path: "/"
  });

  next();
});

app.get("/api/health", (_req, res) => {
  res.json({ ok: true });
});

app.get("/api/settings", async (_req, res) => {
  try {
    const raw = await fsp.readFile(settingsPath, "utf8");
    res.json(JSON.parse(raw));
  } catch {
    res.json({});
  }
});

app.post("/api/settings", async (req, res) => {
  try {
    let current = {};
    try {
      const raw = await fsp.readFile(settingsPath, "utf8");
      current = JSON.parse(raw);
    } catch {
      // ignore
    }
    const next = { ...current, ...req.body };
    await fsp.writeFile(settingsPath, JSON.stringify(next, null, 2), "utf8");
    res.json(next);
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    res.status(500).json({ error: message });
  }
});

app.get("/api/calendar", async (_req, res) => {
  const document = await loadCalendarFromFile(calendarPath);
  res.json(document);
});

app.get("/api/calendar/export", async (_req, res) => {
  const document = await loadCalendarFromFile(calendarPath);
  res.type("text/markdown").send(serializeCalendarMarkdown(document));
});

app.post("/api/calendar/import", async (req, res) => {
  const markdown = req.body?.markdown;
  if (typeof markdown !== "string" || markdown.trim().length === 0) {
    res.status(400).json({ error: "Body must include a markdown string" });
    return;
  }

  try {
    const parsed = parseCalendarMarkdown(markdown);
    await saveCalendarToFile(calendarPath, parsed);
    res.json(parsed);
  } catch (error) {
    const message = error instanceof Error ? error.message : "Unable to import markdown";
    res.status(400).json({ error: message });
  }
});

app.post("/api/events", async (req, res) => {
  const incoming = req.body?.event as Partial<CalendarEvent> | undefined;
  if (!incoming) {
    res.status(400).json({ error: "Request must include an event object" });
    return;
  }

  const id = incoming.id || `evt_${nanoid(8)}`;
  const event = ensureCalendarEvent({
    id,
    externalId: incoming.externalId || `ext_${nanoid(12)}`,
    updatedAt: nowIso(),
    title: incoming.title || "",
    start: incoming.start || "",
    end: incoming.end || "",
    allDay: Boolean(incoming.allDay),
    category: incoming.category || "life",
    completed: Boolean(incoming.completed),
    notes: incoming.notes,
    location: incoming.location,
    googleEventIds: incoming.googleEventIds
  });

  const validationError = validateEventInput(event);
  if (validationError) {
    res.status(400).json({ error: validationError });
    return;
  }

  const document = await loadCalendarFromFile(calendarPath);
  document.events = [...document.events.filter((existing) => existing.id !== event.id), event];
  await saveCalendarToFile(calendarPath, document);
  res.status(201).json({ event });
});

app.patch("/api/events/:id", async (req, res) => {
  const id = req.params.id;
  const updates = (req.body?.updates || {}) as Partial<CalendarEvent>;

  const document = await loadCalendarFromFile(calendarPath);
  const index = findEventIndex(document, id);

  if (index < 0) {
    res.status(404).json({ error: `No event found with id ${id}` });
    return;
  }

  const updatedEvent = ensureCalendarEvent({
    ...document.events[index],
    ...updates,
    id,
    updatedAt: nowIso()
  });

  const validationError = validateEventInput(updatedEvent);
  if (validationError) {
    res.status(400).json({ error: validationError });
    return;
  }

  document.events[index] = updatedEvent;
  await saveCalendarToFile(calendarPath, document);
  res.json({ event: updatedEvent });
});

app.delete("/api/events/:id", async (req, res) => {
  const id = req.params.id;
  const document = await loadCalendarFromFile(calendarPath);
  const before = document.events.length;
  document.events = document.events.filter((event) => event.id !== id);

  if (document.events.length === before) {
    res.status(404).json({ error: `No event found with id ${id}` });
    return;
  }

  await saveCalendarToFile(calendarPath, document);
  res.json({ ok: true });
});

app.get("/api/google/auth/status", async (req, res) => {
  if (!isGoogleConfigured()) {
    res.json({ configured: false, authenticated: false });
    return;
  }

  try {
    requireGoogleSession(req.sessionData);
  } catch {
    res.json({
      configured: true,
      authenticated: false
    });
    return;
  }

  let calendars: GoogleCalendarSummary[] = [];
  let calendarError: string | undefined;

  try {
    calendars = await listGoogleCalendars(req.sessionData);
  } catch (error) {
    if (error instanceof ApiError && error.status === 401) {
      const session = req.sessionData as SessionData;
      session.tokens = undefined;
      session.user = undefined;
      session.selectedCalendarId = undefined;
      persistSessionsToDisk();

      res.json({
        configured: true,
        authenticated: false,
        error: error.message
      });
      return;
    }

    calendarError = error instanceof Error ? error.message : "Could not load Google calendars";
  }

  const selectedCalendarId = req.sessionData.selectedCalendarId;
  const hasSelected = selectedCalendarId ? calendars.some((item) => item.id === selectedCalendarId) : false;
  if (selectedCalendarId && !hasSelected) {
    req.sessionData.selectedCalendarId = undefined;
  }

  res.json({
    configured: true,
    authenticated: true,
    user: req.sessionData.user,
    calendars,
    selectedCalendarId: req.sessionData.selectedCalendarId,
    error: calendarError
  });
});

app.get("/api/google/auth/start", (req, res) => {
  if (!isGoogleConfigured()) {
    res.status(500).json({ error: "Google OAuth is not configured on this server" });
    return;
  }

  const stateNonce = `state_${nanoid(18)}`;
  const state = `${req.sessionId}:${stateNonce}`;
  req.sessionData.oauthState = stateNonce;
  persistSessionsToDisk();
  const config = getGoogleConfig();

  const params = new URLSearchParams({
    response_type: "code",
    client_id: config.clientId,
    redirect_uri: config.redirectUri,
    scope: oauthScope,
    access_type: "offline",
    include_granted_scopes: "true",
    prompt: "consent",
    state
  });

  res.redirect(`https://accounts.google.com/o/oauth2/v2/auth?${params.toString()}`);
});

app.get("/api/google/auth/callback", async (req, res) => {
  const config = getGoogleConfig();
  const redirectBase = config.appBaseUrl || "http://localhost:5173";
  const state = typeof req.query.state === "string" ? req.query.state : "";
  const code = typeof req.query.code === "string" ? req.query.code : "";
  const error = typeof req.query.error === "string" ? req.query.error : "";

  if (error) {
    res.redirect(`${redirectBase}?google_auth=error&reason=${encodeURIComponent(error)}`);
    return;
  }

  const [stateSid, stateNonce] = state.split(":");

  if (stateSid && (!req.sessionId || req.sessionId !== stateSid)) {
    let restored = sessions.get(stateSid);

    if (!restored) {
      loadSessionsFromDisk();
      restored = sessions.get(stateSid);
    }

    if (restored) {
      req.sessionId = stateSid;
      req.sessionData = restored;
      res.cookie(sessionCookieName, stateSid, {
        httpOnly: true,
        sameSite: "lax",
        maxAge: 1000 * 60 * 60 * 24 * 30,
        path: "/"
      });
    }
  }

  if (!stateNonce || !code || req.sessionData.oauthState !== stateNonce) {
    res.redirect(`${redirectBase}?google_auth=error&reason=state_mismatch`);
    return;
  }

  req.sessionData.oauthState = undefined;

  try {
    const tokenResult = await requestGoogleToken(
      new URLSearchParams({
        code,
        client_id: config.clientId,
        client_secret: config.clientSecret,
        redirect_uri: config.redirectUri,
        grant_type: "authorization_code"
      })
    );

    const accessToken = typeof tokenResult.access_token === "string" ? tokenResult.access_token : "";
    if (!accessToken) {
      throw new ApiError(502, "Google did not return an access token");
    }

    const refreshToken = typeof tokenResult.refresh_token === "string" ? tokenResult.refresh_token : undefined;
    const expiresIn = typeof tokenResult.expires_in === "number" ? tokenResult.expires_in : 3600;

    req.sessionData.tokens = {
      accessToken,
      refreshToken,
      expiryAt: Date.now() + expiresIn * 1000,
      scope: typeof tokenResult.scope === "string" ? tokenResult.scope : undefined,
      tokenType: typeof tokenResult.token_type === "string" ? tokenResult.token_type : undefined
    };

    req.sessionData.user = await fetchGoogleUser(req.sessionData);
    req.sessionData.selectedCalendarId = undefined;
    persistSessionsToDisk();

    const authToken = `atok_${nanoid(24)}`;
    authTokens.set(authToken, { sid: req.sessionId, expiresAt: Date.now() + AUTH_TOKEN_TTL });
    res.redirect(`${redirectBase}?google_auth=success&auth_token=${encodeURIComponent(authToken)}`);
  } catch (callbackError) {
    const reason = callbackError instanceof Error ? callbackError.message : "oauth_callback_failed";
    req.sessionData.tokens = undefined;
    req.sessionData.user = undefined;
    req.sessionData.selectedCalendarId = undefined;
    persistSessionsToDisk();
    res.redirect(`${redirectBase}?google_auth=error&reason=${encodeURIComponent(reason)}`);
  }
});

app.post("/api/google/auth/adopt", (req, res) => {
  const token = typeof req.body?.token === "string" ? req.body.token.trim() : "";
  if (!token) {
    res.status(400).json({ error: "token is required" });
    return;
  }

  const entry = authTokens.get(token);
  authTokens.delete(token);

  if (!entry || entry.expiresAt < Date.now()) {
    res.status(400).json({ error: "Invalid or expired auth token" });
    return;
  }

  const session = sessions.get(entry.sid);
  if (!session) {
    res.status(400).json({ error: "Session not found" });
    return;
  }

  req.sessionId = entry.sid;
  req.sessionData = session;

  res.cookie(sessionCookieName, entry.sid, {
    httpOnly: true,
    sameSite: "lax",
    maxAge: 1000 * 60 * 60 * 24 * 30,
    path: "/"
  });

  res.json({ ok: true });
});

app.post("/api/google/auth/logout", (req, res) => {
  req.sessionData.oauthState = undefined;
  req.sessionData.tokens = undefined;
  req.sessionData.user = undefined;
  req.sessionData.selectedCalendarId = undefined;
  persistSessionsToDisk();
  res.json({ ok: true });
});

app.get("/api/google/calendars", async (req, res) => {
  try {
    requireGoogleSession(req.sessionData);
    const calendars = await listGoogleCalendars(req.sessionData);
    res.json({ calendars, selectedCalendarId: req.sessionData.selectedCalendarId || null });
  } catch (error) {
    jsonError(res, error, "Unable to load Google calendars");
  }
});

app.post("/api/google/calendars/select", async (req, res) => {
  const calendarId = typeof req.body?.calendarId === "string" ? req.body.calendarId.trim() : "";
  if (!calendarId) {
    res.status(400).json({ error: "calendarId is required" });
    return;
  }

  try {
    requireGoogleSession(req.sessionData);
    const calendars = await listGoogleCalendars(req.sessionData);
    const selected = calendars.find((item) => item.id === calendarId);

    if (!selected) {
      throw new ApiError(400, "Selected calendar is not available for this account");
    }

    req.sessionData.selectedCalendarId = calendarId;
    persistSessionsToDisk();
    res.json({ selectedCalendarId: calendarId });
  } catch (error) {
    jsonError(res, error, "Unable to select Google calendar");
  }
});

app.post("/api/google/sync", async (req, res) => {
  try {
    requireGoogleSession(req.sessionData);
    const calendarId = req.sessionData.selectedCalendarId;

    if (!calendarId) {
      throw new ApiError(400, "Select a Google Calendar first");
    }

    const result = await syncGoogleCalendar(req.sessionData, calendarId);

    res.json({
      ok: true,
      calendarId,
      counts: result.counts,
      events: result.events,
      message: `Synced ${result.events} local event(s) with Google Calendar`
    });
  } catch (error) {
    jsonError(res, error, "Google sync failed");
  }
});

if (fs.existsSync(distPath)) {
  app.use(express.static(distPath));
  app.get(/.*/, (_req, res) => {
    res.sendFile(path.join(distPath, "index.html"));
  });
}

app.listen(port, async () => {
  await loadCalendarFromFile(calendarPath);
  console.log(`Calendar API running on http://localhost:${port}`);
});
