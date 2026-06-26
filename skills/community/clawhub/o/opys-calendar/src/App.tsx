import { useEffect, useMemo, useState, useRef } from "react";
import FullCalendar from "@fullcalendar/react";
import dayGridPlugin from "@fullcalendar/daygrid";
import timeGridPlugin from "@fullcalendar/timegrid";
import interactionPlugin from "@fullcalendar/interaction";
import type { EventContentArg, EventInput } from "@fullcalendar/core";
import type { CalendarCategory, CalendarDocument, CalendarEvent } from "../shared/types";

type GoogleCalendarSummary = {
  id: string;
  summary: string;
  primary?: boolean;
  backgroundColor?: string;
  accessRole?: string;
};

type GoogleAuthStatus = {
  configured: boolean;
  authenticated: boolean;
  user?: {
    sub: string;
    email: string;
    name?: string;
    picture?: string;
  };
  calendars?: GoogleCalendarSummary[];
  selectedCalendarId?: string;
  error?: string;
};

type EditableCalendarEventArg = {
  event: {
    id: string;
    start: Date | null;
    end: Date | null;
    allDay: boolean;
  };
  revert: () => void;
};

async function fetchCalendar(): Promise<CalendarDocument> {
  const response = await fetch("/api/calendar", { credentials: "include" });
  if (!response.ok) {
    throw new Error("Unable to load calendar data");
  }
  return response.json();
}

async function fetchGoogleStatus(): Promise<GoogleAuthStatus> {
  const response = await fetch("/api/google/auth/status", { credentials: "include" });
  if (!response.ok) {
    throw new Error("Unable to load Google auth status");
  }
  return response.json();
}

function formatDateRange(event: CalendarEvent): string {
  if (event.allDay) {
    return `${event.start.slice(0, 10)} (all day)`;
  }
  const start = event.start.replace("T", " ").slice(0, 16);
  const end = event.end.replace("T", " ").slice(0, 16);
  return `${start} -> ${end}`;
}

import StatsView from "./StatsView";

function App() {
  const [document, setDocument] = useState<CalendarDocument | null>(null);
  const [selectedEventId, setSelectedEventId] = useState<string | null>(null);
  const [status, setStatus] = useState<string>("Loading calendar...");
  const [google, setGoogle] = useState<GoogleAuthStatus>({ configured: false, authenticated: false });
  const [syncing, setSyncing] = useState(false);
  const [authWorking, setAuthWorking] = useState(false);
  const [slotDuration, setSlotDuration] = useState<string>(() => localStorage.getItem("slotDuration") || "00:15:00");
  const [snapshotDays, setSnapshotDays] = useState<number>(14);
  const [workingHoursStart, setWorkingHoursStart] = useState<string>("09:00");
  const [workingHoursEnd, setWorkingHoursEnd] = useState<string>("17:00");
  const [workingDays, setWorkingDays] = useState<number[]>([1, 2, 3, 4, 5]);
  const [darkMode, setDarkMode] = useState<boolean>(() => localStorage.getItem("theme") === "dark");
  const [view, setView] = useState<"calendar" | "settings" | "stats">("calendar");
  const calendarRef = useRef<FullCalendar>(null);

  // To throttle horizontal scroll events
  const scrollTimeout = useRef<NodeJS.Timeout | null>(null);

  const handleWheel = (e: React.WheelEvent) => {
    // Only intercept horizontal scrolls
    if (Math.abs(e.deltaX) > Math.abs(e.deltaY) && Math.abs(e.deltaX) > 10) {
      if (scrollTimeout.current) return; // Prevent rapid-fire scrolling

      const calendarApi = calendarRef.current?.getApi();
      if (!calendarApi) return;

      if (e.deltaX > 0) {
        calendarApi.next();
      } else {
        calendarApi.prev();
      }

      scrollTimeout.current = setTimeout(() => {
        scrollTimeout.current = null;
      }, 300); // 300ms throttle
    }
  };

  useEffect(() => {
    localStorage.setItem("slotDuration", slotDuration);
  }, [slotDuration]);

  useEffect(() => {
    if (darkMode) {
      window.document.documentElement.setAttribute("data-theme", "dark");
      localStorage.setItem("theme", "dark");
    } else {
      window.document.documentElement.removeAttribute("data-theme");
      localStorage.setItem("theme", "light");
    }
  }, [darkMode]);

  useEffect(() => {
    async function loadSettings() {
      try {
        const res = await fetch("/api/settings");
        if (res.ok) {
          const data = await res.json();
          if (typeof data.snapshotDays === "number") {
            setSnapshotDays(data.snapshotDays);
          }
          if (typeof data.workingHoursStart === "string") setWorkingHoursStart(data.workingHoursStart);
          if (typeof data.workingHoursEnd === "string") setWorkingHoursEnd(data.workingHoursEnd);
          if (Array.isArray(data.workingDays)) setWorkingDays(data.workingDays);
        }
      } catch {
        // ignore
      }
    }
    void loadSettings();
  }, []);

  async function updateSnapshotDays(days: number) {
    setSnapshotDays(days);
    try {
      await fetch("/api/settings", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ snapshotDays: days })
      });
      setStatus(`Snapshot days updated to ${days}`);
    } catch {
      setStatus("Failed to update snapshot days");
    }
  }

  async function updateSettings(updates: Record<string, unknown>) {
    try {
      await fetch("/api/settings", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(updates)
      });
      setStatus("Settings saved");
    } catch {
      setStatus("Failed to save settings");
    }
  }

  const categories = document?.frontmatter.categories || [];

  async function refreshCalendar(message?: string) {
    const loaded = await fetchCalendar();
    setDocument(loaded);
    if (message) {
      setStatus(message);
    }
  }

  async function refreshGoogle() {
    const loaded = await fetchGoogleStatus();
    setGoogle(loaded);
  }

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const googleAuth = params.get("google_auth");
    const authToken = params.get("auth_token");
    const reason = params.get("reason");

    async function init() {
      await refreshCalendar();

      if (googleAuth === "success" && authToken) {
        try {
          await fetch("/api/google/auth/adopt", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            credentials: "include",
            body: JSON.stringify({ token: authToken })
          });
        } catch {
          // token exchange failed, will fall through to refreshGoogle
        }
        window.history.replaceState({}, "", window.location.pathname);
        await refreshGoogle();
        setStatus("Google account connected. Choose a calendar and sync.");
        return;
      }

      if (googleAuth === "error") {
        window.history.replaceState({}, "", window.location.pathname);
        await refreshGoogle();
        setStatus(`Google auth failed${reason ? `: ${reason}` : ""}`);
        return;
      }

      await refreshGoogle();
      setStatus("Synced with calendar.md");
    }

    init().catch((error) => {
      setStatus(error instanceof Error ? error.message : "Load failed");
    });
  }, []);

  const selectedEvent = useMemo(
    () => document?.events.find((event) => event.id === selectedEventId) || null,
    [document, selectedEventId]
  );

  const events: EventInput[] = useMemo(() => {
    if (!document) return [];

    return document.events.map((event) => {
      const category = categories.find((item) => item.id === event.category);
      // Determine the hex color. If it's a google colorId (1-11), map it back to a visually pleasing color, else use it directly, else fallback to category
      let eventColor = event.color || category?.color || "#64748b";

      // Color ID mapping Google uses:
      const googleColorMap: Record<string, string> = {
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
        "11": "#d50000", // Tomato
      };
      if (event.color && googleColorMap[event.color]) {
        eventColor = googleColorMap[event.color];
      }

      return {
        id: event.id,
        title: event.title,
        start: event.start,
        end: event.end,
        allDay: event.allDay,
        backgroundColor: eventColor,
        borderColor: eventColor,
        extendedProps: {
          completed: event.completed,
          category: event.category
        }
      };
    });
  }, [categories, document]);

  async function patchEvent(id: string, updates: Partial<CalendarEvent>, message: string) {
    const response = await fetch(`/api/events/${id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ updates })
    });

    if (!response.ok) {
      const body = await response.json().catch(() => ({}));
      throw new Error(body.error || "Unable to update event");
    }

    await refreshCalendar(message);
  }

  async function handleDragOrResize(arg: EditableCalendarEventArg) {
    const id = arg.event.id;
    const updates: Partial<CalendarEvent> = {
      start: arg.event.start?.toISOString(),
      end: arg.event.end?.toISOString() || arg.event.start?.toISOString(),
      allDay: arg.event.allDay
    };

    try {
      await patchEvent(id, updates, "Event moved in calendar.md");
    } catch (error) {
      arg.revert();
      setStatus(error instanceof Error ? error.message : "Could not move event");
    }
  }

  async function toggleCompleted(eventId: string, completed: boolean) {
    try {
      await patchEvent(eventId, { completed }, completed ? "Marked complete" : "Marked incomplete");
    } catch (error) {
      setStatus(error instanceof Error ? error.message : "Toggle failed");
    }
  }

  async function deleteSelected() {
    if (!selectedEvent) return;

    const response = await fetch(`/api/events/${selectedEvent.id}`, {
      method: "DELETE",
      credentials: "include"
    });

    if (!response.ok) {
      const body = await response.json().catch(() => ({}));
      setStatus(body.error || "Delete failed");
      return;
    }

    setSelectedEventId(null);
    await refreshCalendar("Event removed");
  }

  // Key down event to delete selected event with backspace/delete
  useEffect(() => {
    function handleKeyDown(e: KeyboardEvent) {
      if ((e.key === "Backspace" || e.key === "Delete") && selectedEventId) {
        void deleteSelected();
      }
    }
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [selectedEventId]);

  async function selectGoogleCalendar(calendarId: string) {
    try {
      const response = await fetch("/api/google/calendars/select", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ calendarId })
      });

      if (!response.ok) {
        const body = await response.json().catch(() => ({}));
        throw new Error(body.error || "Could not select calendar");
      }

      await refreshGoogle();
      setStatus("Google Calendar selected. Click Sync Now to merge updates.");
    } catch (error) {
      setStatus(error instanceof Error ? error.message : "Calendar selection failed");
    }
  }

  async function syncGoogleCalendar() {
    if (!google.authenticated || !google.selectedCalendarId) {
      setStatus("Sign in and choose a Google Calendar first.");
      return;
    }

    setSyncing(true);
    try {
      const response = await fetch("/api/google/sync", {
        method: "POST",
        credentials: "include"
      });

      const body = (await response.json().catch(() => ({}))) as {
        message?: string;
        error?: string;
      };

      if (!response.ok) {
        throw new Error(body.error || "Sync failed");
      }

      await Promise.all([refreshCalendar(), refreshGoogle()]);
      setStatus(body.message || "Two-way sync completed");
    } catch (error) {
      setStatus(error instanceof Error ? error.message : "Sync failed");
    } finally {
      setSyncing(false);
    }
  }

  async function signOutGoogle() {
    setAuthWorking(true);
    try {
      await fetch("/api/google/auth/logout", { method: "POST", credentials: "include" });
      await refreshGoogle();
      setStatus("Signed out from Google");
    } finally {
      setAuthWorking(false);
    }
  }

  const selectedGoogleCalendar = google.calendars?.find((item) => item.id === google.selectedCalendarId);

  if (view === "stats") {
    return (
      <StatsView
        document={document}
        categories={categories}
        workingHoursStart={workingHoursStart}
        workingHoursEnd={workingHoursEnd}
        workingDays={workingDays}
        onClose={() => setView("calendar")}
      />
    );
  }

  if (view === "settings") {
    return (
      <div className="settings-page">
        <header className="settings-header">
          <h2>Settings</h2>
          <button className="ghost-btn" onClick={() => setView("calendar")}>
            Done
          </button>
        </header>

        <div className="settings-grid">
          <div className="settings-card">
            <h3>Appearance</h3>
            <button type="button" onClick={() => setDarkMode(!darkMode)} className="ghost-btn">
              {darkMode ? "☀️ Switch to Light Mode" : "🌙 Switch to Dark Mode"}
            </button>
          </div>

          <div className="settings-card">
            <h3>Preferences</h3>
            <div className="settings-form-row">
              <label>Calendar Slot Size</label>
              <select value={slotDuration} onChange={(e) => setSlotDuration(e.target.value)}>
                <option value="00:15:00">15 minutes (4 slots/hour)</option>
                <option value="00:30:00">30 minutes (2 slots/hour)</option>
                <option value="01:00:00">60 minutes (1 slot/hour)</option>
              </select>
            </div>
            <div className="settings-form-row">
              <label>Agent Snapshot Days</label>
              <div style={{ display: "flex", gap: "0.5rem", alignItems: "center" }}>
                <input
                  type="number"
                  value={snapshotDays}
                  onChange={(e) => setSnapshotDays(parseInt(e.target.value) || 1)}
                  onBlur={(e) => void updateSnapshotDays(parseInt(e.target.value) || 14)}
                  min="1"
                  max="365"
                  style={{ flex: 1, minWidth: 0 }}
                />
                <button type="button" onClick={() => void updateSnapshotDays(snapshotDays)} className="sync-button">
                  Save
                </button>
              </div>
            </div>
            <div className="settings-form-row">
              <label>Working Hours</label>
              <div style={{ display: "flex", gap: "0.5rem", alignItems: "center" }}>
                <input type="time" value={workingHoursStart} onChange={(e) => setWorkingHoursStart(e.target.value)} onBlur={(e) => void updateSettings({ workingHoursStart: e.target.value })} style={{ flex: 1 }} />
                <span>to</span>
                <input type="time" value={workingHoursEnd} onChange={(e) => setWorkingHoursEnd(e.target.value)} onBlur={(e) => void updateSettings({ workingHoursEnd: e.target.value })} style={{ flex: 1 }} />
              </div>
            </div>
            <div className="settings-form-row">
              <label>Working Days</label>
              <div style={{ display: "flex", gap: "0.5rem", flexWrap: "wrap", fontSize: "0.85rem" }}>
                {["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].map((day, i) => (
                  <label key={i} style={{ display: "flex", alignItems: "center", gap: "0.2rem", fontWeight: "normal", cursor: "pointer" }}>
                    <input type="checkbox" checked={workingDays.includes(i)} onChange={(e) => {
                      const next = e.target.checked ? [...workingDays, i] : workingDays.filter(d => d !== i);
                      setWorkingDays(next);
                      void updateSettings({ workingDays: next });
                    }} />
                    {day}
                  </label>
                ))}
              </div>
            </div>
          </div>

          <div className="settings-card google-panel">
            <h3>Google Calendar Sync</h3>
            {!google.configured ? (
              <p className="google-help">
                Google OAuth is not configured. Add `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, and
                `GOOGLE_REDIRECT_URI` in your server environment.
              </p>
            ) : null}

            {google.configured && !google.authenticated ? (
              <a className="auth-link" href="/api/google/auth/start">
                Sign in with Google
              </a>
            ) : null}

            {google.configured && google.authenticated ? (
              <div className="google-controls">
                <div className="google-user-row">
                  <div>
                    Account:
                    <br />
                    <strong>{google.user?.email}</strong>
                  </div>
                  <button
                    type="button"
                    onClick={() => void signOutGoogle()}
                    disabled={authWorking}
                    className="ghost-btn"
                    style={{ fontSize: "0.75rem", padding: "0.2rem 0.4rem" }}
                  >
                    {authWorking ? "..." : "Sign out"}
                  </button>
                </div>

                <div className="calendar-buttons" style={{ flexDirection: "column", alignItems: "stretch" }}>
                  {(google.calendars || []).map((calendar) => {
                    const selected = google.selectedCalendarId === calendar.id;
                    return (
                      <button
                        key={calendar.id}
                        type="button"
                        onClick={() => void selectGoogleCalendar(calendar.id)}
                        className={`calendar-button ${selected ? "selected" : ""}`}
                      >
                        {calendar.summary}
                      </button>
                    );
                  })}
                </div>

                <div className="sync-row">
                  <button
                    type="button"
                    onClick={() => void syncGoogleCalendar()}
                    disabled={syncing || !google.selectedCalendarId}
                    className="sync-button"
                    style={{ width: "100%" }}
                  >
                    {syncing ? "Syncing..." : "Sync Now"}
                  </button>
                </div>
                <div className="sync-hint" style={{ marginTop: "-0.5rem" }}>
                  {selectedGoogleCalendar
                    ? `Selected: ${selectedGoogleCalendar.summary}`
                    : "Select a Google Calendar to start two-way sync"}
                </div>
              </div>
            ) : null}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="app-shell-max">
      {status && status !== "Synced with calendar.md" && status !== "Loading calendar..." && (
        <div className="floating-status">{status}</div>
      )}

      <div className="calendar-wrapper-relative">
        <div className="category-chips-overlay">
          {categories.map((category: CalendarCategory) => (
            <span key={category.id} className="category-chip" style={{ backgroundColor: category.color }}>
              {category.label}
            </span>
          ))}
        </div>

        <section className="calendar-panel-max" onWheel={handleWheel}>
          <FullCalendar
            ref={calendarRef}
            plugins={[dayGridPlugin, timeGridPlugin, interactionPlugin]}
            initialView="slidingWeek"
            views={{
              slidingWeek: {
                type: 'timeGrid',
                duration: { days: 7 },
                buttonText: 'sliding week',
                dateIncrement: { days: 1 }
              }
            }}
            customButtons={{
              settingsBtn: {
                text: "⚙️ Settings",
                click: () => setView("settings")
              },
              statsBtn: {
                text: "📊 Stats",
                click: () => setView("stats")
              }
            }}
            headerToolbar={{
              left: "settingsBtn statsBtn today prev,next",
              center: "",
              right: "dayGridMonth,slidingWeek,timeGridDay"
            }}
            editable
            events={events}
            eventDrop={handleDragOrResize}
            eventResize={handleDragOrResize}
            eventClick={(arg) => setSelectedEventId(arg.event.id)}
            nowIndicator
            slotDuration={slotDuration}
            height="100%"
          />
        </section>
      </div>
    </div>
  );
}

export default App;
