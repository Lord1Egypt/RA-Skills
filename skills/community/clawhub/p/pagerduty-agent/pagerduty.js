#!/usr/bin/env node
/**
 * pagerduty-agent — OpenClaw skill
 * Zero dependencies. Native Node.js https. { command, params } dispatch.
 * All responses are structured JSON.
 *
 * Usage:
 *   echo '{"command":"list_incidents","params":{"status":"triggered","limit":10}}' | node pagerduty.js
 */

"use strict";

const https = require("https");
const http = require("http");

const BASE_URL = process.env.PAGERDUTY_BASE_URL || "https://api.pagerduty.com";
const API_KEY = process.env.PAGERDUTY_API_KEY;
const FROM_EMAIL = process.env.PAGERDUTY_FROM_EMAIL;

// ---------------------------------------------------------------------------
// HTTP client
// ---------------------------------------------------------------------------

function request(method, path, body) {
  return new Promise((resolve, reject) => {
    if (!API_KEY) {
      return reject(new Error("PAGERDUTY_API_KEY environment variable is not set"));
    }

    const payload = body ? JSON.stringify(body) : null;
    const url = new URL(BASE_URL + path);

    const headers = {
      "Authorization": `Token token=${API_KEY}`,
      "Accept": "application/vnd.pagerduty+json;version=2",
      "Content-Type": "application/json",
    };

    if (FROM_EMAIL) {
      headers["From"] = FROM_EMAIL;
    }

    if (payload) {
      headers["Content-Length"] = Buffer.byteLength(payload);
    }

    const transport = url.protocol === "https:" ? https : http;
    const options = {
      hostname: url.hostname,
      port: url.port || (url.protocol === "https:" ? 443 : 80),
      path: url.pathname + url.search,
      method,
      headers,
    };

    const req = transport.request(options, (res) => {
      const chunks = [];
      res.on("data", (c) => chunks.push(c));
      res.on("end", () => {
        const raw = Buffer.concat(chunks).toString();
        let data = null;
        try { data = JSON.parse(raw); } catch (_) { data = raw; }

        if (res.statusCode >= 400) {
          const apiMsg =
            (data && data.error && data.error.message) ||
            (data && data.error) ||
            null;

          let msg;
          if (res.statusCode === 401) {
            msg = "Invalid API key — check your PAGERDUTY_API_KEY";
          } else if (res.statusCode === 403) {
            msg = "Permission denied — your API key does not have access to this resource";
          } else if (res.statusCode === 404) {
            // Derive a contextual hint from the request path
            const p = options.path.split("?")[0];
            if (p.match(/\/incidents\/[^/]+\/notes/)) {
              msg = "Incident not found — verify incident_id exists in your PagerDuty account";
            } else if (p.match(/\/incidents\/[^/]+/)) {
              msg = "Incident not found — verify incident_id exists in your PagerDuty account";
            } else if (p.match(/\/services\/[^/]+/)) {
              msg = "Service not found — verify service_id exists in your PagerDuty account";
            } else if (p.match(/\/schedules\/[^/]+/)) {
              msg = "Schedule not found — verify schedule_id exists in your PagerDuty account";
            } else if (p.match(/\/maintenance_windows\/[^/]+/)) {
              msg = "Maintenance window not found — verify the ID exists in your PagerDuty account";
            } else {
              msg = apiMsg || "Resource not found — verify the ID exists in your PagerDuty account";
            }
          } else if (res.statusCode === 429) {
            const retryAfter = res.headers["retry-after"];
            msg = retryAfter
              ? `Rate limit exceeded — retry after ${retryAfter}s`
              : "Rate limit exceeded — slow down requests or contact PagerDuty support";
          } else if (res.statusCode >= 500) {
            msg = `PagerDuty server error (HTTP ${res.statusCode}) — try again shortly`;
          } else {
            msg = apiMsg || `HTTP ${res.statusCode}`;
          }

          return reject(new Error(msg));
        }
        resolve(data);
      });
    });

    req.on("error", reject);
    if (payload) req.write(payload);
    req.end();
  });
}

function get(path) { return request("GET", path, null); }
function post(path, body) { return request("POST", path, body); }
function put(path, body) { return request("PUT", path, body); }

// ---------------------------------------------------------------------------
// Command handlers
// ---------------------------------------------------------------------------

async function trigger_incident({ service_id, title, severity, body }) {
  if (!service_id) throw new Error("params.service_id is required");
  if (!title) throw new Error("params.title is required");

  const urgency = ["critical", "error"].includes(severity) ? "high" : "low";

  const payload = {
    incident: {
      type: "incident",
      title,
      urgency,
      service: { id: service_id, type: "service_reference" },
    },
  };

  if (body) {
    payload.incident.body = { type: "incident_body", details: body };
  }

  const data = await post("/incidents", payload);
  const inc = data.incident;
  return {
    id: inc.id,
    incident_number: inc.incident_number,
    title: inc.title,
    status: inc.status,
    urgency: inc.urgency,
    html_url: inc.html_url,
    created_at: inc.created_at,
    service: { id: inc.service.id, name: inc.service.summary },
  };
}

async function acknowledge_incident({ incident_id }) {
  if (!incident_id) throw new Error("params.incident_id is required");

  const data = await put(`/incidents/${incident_id}`, {
    incident: { type: "incident", status: "acknowledged" },
  });
  const inc = data.incident;
  return {
    id: inc.id,
    incident_number: inc.incident_number,
    title: inc.title,
    status: inc.status,
    acknowledged_at: inc.last_status_change_at,
  };
}

async function resolve_incident({ incident_id }) {
  if (!incident_id) throw new Error("params.incident_id is required");

  const data = await put(`/incidents/${incident_id}`, {
    incident: { type: "incident", status: "resolved" },
  });
  const inc = data.incident;
  return {
    id: inc.id,
    incident_number: inc.incident_number,
    title: inc.title,
    status: inc.status,
    resolved_at: inc.last_status_change_at,
  };
}

async function list_incidents({ status, limit } = {}) {
  const qs = new URLSearchParams();
  if (status) qs.set("statuses[]", status);
  qs.set("limit", limit ? String(limit) : "25");
  qs.set("total", "true");

  const data = await get(`/incidents?${qs}`);

  return {
    total: data.total,
    more: data.more,
    limit: data.limit,
    offset: data.offset,
    incidents: (data.incidents || []).map((inc) => ({
      id: inc.id,
      incident_number: inc.incident_number,
      title: inc.title,
      status: inc.status,
      urgency: inc.urgency,
      created_at: inc.created_at,
      service: { id: inc.service.id, name: inc.service.summary },
      assigned_to: (inc.assignments || []).map((a) => a.assignee.summary),
    })),
  };
}

async function get_incident({ incident_id }) {
  if (!incident_id) throw new Error("params.incident_id is required");

  const data = await get(`/incidents/${incident_id}`);
  const inc = data.incident;
  return {
    id: inc.id,
    incident_number: inc.incident_number,
    title: inc.title,
    status: inc.status,
    urgency: inc.urgency,
    html_url: inc.html_url,
    created_at: inc.created_at,
    last_status_change_at: inc.last_status_change_at,
    service: { id: inc.service.id, name: inc.service.summary },
    assigned_to: (inc.assignments || []).map((a) => a.assignee.summary),
    escalation_policy: inc.escalation_policy
      ? { id: inc.escalation_policy.id, name: inc.escalation_policy.summary }
      : null,
    body: inc.body ? inc.body.details : null,
  };
}

async function add_incident_note({ incident_id, content }) {
  if (!incident_id) throw new Error("params.incident_id is required");
  if (!content) throw new Error("params.content is required");

  const data = await post(`/incidents/${incident_id}/notes`, {
    note: { content },
  });
  const note = data.note;
  return {
    id: note.id,
    content: note.content,
    created_at: note.created_at,
    user: note.user ? note.user.summary : null,
  };
}

async function get_oncall({ schedule_id } = {}) {
  const qs = new URLSearchParams();
  qs.set("limit", "25");
  if (schedule_id) qs.set("schedule_ids[]", schedule_id);

  const data = await get(`/oncalls?${qs}`);
  return {
    oncalls: (data.oncalls || []).map((oc) => ({
      user: { id: oc.user.id, name: oc.user.summary },
      schedule: oc.schedule
        ? { id: oc.schedule.id, name: oc.schedule.summary }
        : null,
      escalation_policy: oc.escalation_policy
        ? { id: oc.escalation_policy.id, name: oc.escalation_policy.summary }
        : null,
      escalation_level: oc.escalation_level,
      start: oc.start,
      end: oc.end,
    })),
  };
}

async function list_schedules() {
  const data = await get("/schedules?limit=100");
  return {
    total: data.total,
    schedules: (data.schedules || []).map((s) => ({
      id: s.id,
      name: s.name,
      description: s.description,
      time_zone: s.time_zone,
      html_url: s.html_url,
      users: (s.users || []).map((u) => ({ id: u.id, name: u.summary })),
    })),
  };
}

async function list_services() {
  const data = await get("/services?limit=100");
  return {
    total: data.total,
    services: (data.services || []).map((s) => ({
      id: s.id,
      name: s.name,
      description: s.description,
      status: s.status,
      html_url: s.html_url,
      escalation_policy: s.escalation_policy
        ? { id: s.escalation_policy.id, name: s.escalation_policy.summary }
        : null,
    })),
  };
}

async function get_service({ service_id }) {
  if (!service_id) throw new Error("params.service_id is required");

  const data = await get(`/services/${service_id}`);
  const s = data.service;
  return {
    id: s.id,
    name: s.name,
    description: s.description,
    status: s.status,
    html_url: s.html_url,
    created_at: s.created_at,
    escalation_policy: s.escalation_policy
      ? { id: s.escalation_policy.id, name: s.escalation_policy.summary }
      : null,
    integrations: (s.integrations || []).map((i) => ({
      id: i.id,
      name: i.summary,
    })),
    alert_grouping: s.alert_grouping || null,
    alert_grouping_timeout: s.alert_grouping_timeout || null,
  };
}

async function create_maintenance_window({
  service_ids,
  start_time,
  end_time,
  description,
}) {
  if (!service_ids || !service_ids.length)
    throw new Error("params.service_ids (array) is required");
  if (!start_time) throw new Error("params.start_time is required (ISO 8601)");
  if (!end_time) throw new Error("params.end_time is required (ISO 8601)");

  const data = await post("/maintenance_windows", {
    maintenance_window: {
      type: "maintenance_window",
      start_time,
      end_time,
      description: description || "",
      services: service_ids.map((id) => ({ id, type: "service_reference" })),
    },
  });
  const mw = data.maintenance_window;
  return {
    id: mw.id,
    description: mw.description,
    start_time: mw.start_time,
    end_time: mw.end_time,
    html_url: mw.html_url,
    services: (mw.services || []).map((s) => ({ id: s.id, name: s.summary })),
  };
}

async function list_maintenance_windows() {
  const data = await get("/maintenance_windows?limit=100");
  return {
    total: data.total,
    maintenance_windows: (data.maintenance_windows || []).map((mw) => ({
      id: mw.id,
      description: mw.description,
      start_time: mw.start_time,
      end_time: mw.end_time,
      html_url: mw.html_url,
      services: (mw.services || []).map((s) => ({ id: s.id, name: s.summary })),
    })),
  };
}

// ---------------------------------------------------------------------------
// Dispatch
// ---------------------------------------------------------------------------

const COMMANDS = {
  trigger_incident,
  acknowledge_incident,
  resolve_incident,
  list_incidents,
  get_incident,
  add_incident_note,
  get_oncall,
  list_schedules,
  list_services,
  get_service,
  create_maintenance_window,
  list_maintenance_windows,
};

function fail(obj) {
  process.exitCode = 1;
  process.stdout.write(JSON.stringify(obj) + "\n");
}

async function main() {
  let input = "";
  process.stdin.setEncoding("utf8");
  for await (const chunk of process.stdin) input += chunk;

  let parsed;
  try {
    parsed = JSON.parse(input.trim());
  } catch (_) {
    return fail({ error: "Invalid JSON input. Expected { command, params }." });
  }

  const { command, params = {} } = parsed;

  if (!command) {
    return fail({
      error: "Missing `command` field.",
      available_commands: Object.keys(COMMANDS),
    });
  }

  const handler = COMMANDS[command];
  if (!handler) {
    return fail({
      error: `Unknown command: "${command}"`,
      available_commands: Object.keys(COMMANDS),
    });
  }

  try {
    const result = await handler(params);
    process.stdout.write(JSON.stringify(result, null, 2) + "\n");
  } catch (err) {
    fail({ error: err.message });
  }
}

main();
