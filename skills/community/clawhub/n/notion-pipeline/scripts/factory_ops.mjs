#!/usr/bin/env node

import fs from "node:fs/promises";
import { spawn } from "node:child_process";
import { loadLocalEnv } from "./local_env.mjs";

const CRON_JOBS_FILE = "/Users/dellymac/.openclaw/cron/jobs.json";

function getEnv(name, fallback = "") {
  return process.env[name] || fallback;
}

function notionToken() {
  return getEnv("OPENCLAW_NOTION_TOKEN") || getEnv("NOTION_TOKEN");
}

function notionVersion() {
  return getEnv("OPENCLAW_NOTION_VERSION", "2022-06-28");
}

function timezone() {
  return getEnv("OPENCLAW_TIMEZONE", "Europe/Istanbul");
}

function aliasMap() {
  return {
    research: getEnv("OPENCLAW_NOTION_DB_RESEARCH_SIGNALS"),
    ideas: getEnv("OPENCLAW_NOTION_DB_PROJECT_IDEAS"),
    projects: getEnv("OPENCLAW_NOTION_DB_PROJECTS"),
    runs: getEnv("OPENCLAW_NOTION_DB_NIGHTLY_RUNS"),
  };
}

function usage() {
  console.error(
    "usage: factory_ops.mjs <write-signals|list-signals|apply-signal-reviews|list-archived-signals|write-ideas|list-ideas|apply-evaluations|handle-approval|record-report-delivery|get-project|update-project-pack|find-page|list-page-children|mark-block-done> [args]"
  );
}

function currentDate() {
  return new Intl.DateTimeFormat("en-CA", {
    timeZone: timezone(),
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  }).format(new Date());
}

function resolveDatabase(value) {
  const aliases = aliasMap();
  return aliases[value] || value;
}

async function readJsonArg(file) {
  const raw = file === "-" ? await readStdin() : await fs.readFile(file, "utf8");
  return JSON.parse(raw);
}

async function readStdin() {
  let data = "";
  for await (const chunk of process.stdin) {
    data += chunk;
  }
  return data;
}

async function notionRequest(pathname, { method = "GET", body } = {}) {
  if (!notionToken()) {
    throw new Error("OPENCLAW_NOTION_TOKEN is missing");
  }
  const response = await fetch(`https://api.notion.com/v1${pathname}`, {
    method,
    headers: {
      Authorization: `Bearer ${notionToken()}`,
      "Notion-Version": notionVersion(),
      "Content-Type": "application/json",
    },
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  const text = await response.text();
  let json;
  try {
    json = text ? JSON.parse(text) : {};
  } catch {
    json = { raw: text };
  }
  if (!response.ok) {
    const error = new Error(`Notion request failed: ${response.status}`);
    error.details = json;
    throw error;
  }
  return json;
}

async function queryDatabase(databaseAliasOrId, body = {}) {
  return notionRequest(`/databases/${resolveDatabase(databaseAliasOrId)}/query`, {
    method: "POST",
    body,
  });
}

async function createPage(databaseAliasOrId, payload) {
  const databaseId = resolveDatabase(databaseAliasOrId);
  return notionRequest("/pages", {
    method: "POST",
    body: {
      parent: payload.parent || { database_id: databaseId },
      ...payload,
    },
  });
}

async function updatePage(pageId, payload) {
  return notionRequest(`/pages/${pageId}`, {
    method: "PATCH",
    body: payload,
  });
}

function normalizeName(name) {
  return String(name || "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "");
}

function normalizeId(value) {
  return String(value || "").replace(/-/g, "").trim().toLowerCase();
}

function parseJsonMaybe(value) {
  if (!value || !String(value).trim()) {
    return null;
  }
  try {
    return JSON.parse(value);
  } catch {
    return null;
  }
}

function plainTextFromRichText(items = []) {
  return (items || []).map((item) => item.plain_text || "").join("").trim();
}

function richTextArrayForBlock(block) {
  const content = block?.[block?.type];
  if (!content) {
    return [];
  }
  if (Array.isArray(content.rich_text)) {
    return content.rich_text;
  }
  return [];
}

function blockPlainText(block) {
  return plainTextFromRichText(richTextArrayForBlock(block));
}

function isBlockDone(block) {
  if (!block) {
    return false;
  }
  if (block.type === "to_do") {
    return Boolean(block.to_do?.checked);
  }
  const richText = richTextArrayForBlock(block);
  return richText.length > 0 && richText.every((item) => item.annotations?.strikethrough);
}

function pickProperty(properties, names) {
  const wanted = new Set(names.map(normalizeName));
  for (const [name, prop] of Object.entries(properties || {})) {
    if (wanted.has(normalizeName(name))) {
      return prop;
    }
  }
  return null;
}

function titleText(prop) {
  if (!prop || prop.type !== "title") {
    return "";
  }
  return prop.title.map((item) => item.plain_text || "").join("").trim();
}

function richText(prop) {
  if (!prop) {
    return "";
  }
  if (prop.type === "rich_text") {
    return prop.rich_text.map((item) => item.plain_text || "").join("").trim();
  }
  if (prop.type === "title") {
    return titleText(prop);
  }
  if (prop.type === "select") {
    return prop.select?.name || "";
  }
  if (prop.type === "status") {
    return prop.status?.name || "";
  }
  if (prop.type === "url") {
    return prop.url || "";
  }
  if (prop.type === "number") {
    return prop.number == null ? "" : String(prop.number);
  }
  if (prop.type === "date") {
    return prop.date?.start || "";
  }
  if (prop.type === "checkbox") {
    return prop.checkbox ? "true" : "false";
  }
  return "";
}

function numberValue(prop) {
  if (!prop) {
    return null;
  }
  if (prop.type === "number") {
    return prop.number;
  }
  const text = richText(prop);
  if (!text) {
    return null;
  }
  const numeric = Number(text);
  return Number.isFinite(numeric) ? numeric : null;
}

function titleProp(value) {
  return {
    title: value ? [{ text: { content: String(value) } }] : [],
  };
}

function richTextProp(value) {
  return {
    rich_text: value ? [{ text: { content: String(value) } }] : [],
  };
}

function selectProp(value) {
  return {
    select: value ? { name: String(value) } : null,
  };
}

function urlProp(value) {
  return { url: value || null };
}

function numberProp(value) {
  return { number: value == null ? null : Number(value) };
}

function dateProp(value) {
  return value ? { date: { start: String(value) } } : { date: null };
}

function checkboxProp(value) {
  return { checkbox: Boolean(value) };
}

function signalTitle(page) {
  return titleText(pickProperty(page.properties || {}, ["signal title", "title", "name"]));
}

function ideaTitle(page) {
  return titleText(pickProperty(page.properties || {}, ["idea title", "title", "name"]));
}

function projectTitle(page) {
  return titleText(pickProperty(page.properties || {}, ["project name", "title", "name"]));
}

function ideaMatches(page, ideaId) {
  const normalizedTarget = normalizeId(ideaId);
  if (!normalizedTarget) {
    return false;
  }
  return normalizeId(page.id) === normalizedTarget;
}

function projectMatches(page, projectId) {
  const normalizedTarget = normalizeId(projectId);
  if (!normalizedTarget) {
    return false;
  }
  return normalizeId(page.id) === normalizedTarget;
}

async function listAll(databaseAliasOrId, pageSize = 100) {
  const results = [];
  let startCursor = null;
  do {
    const payload = { page_size: pageSize };
    if (startCursor) {
      payload.start_cursor = startCursor;
    }
    const response = await queryDatabase(databaseAliasOrId, payload);
    results.push(...(response.results || []));
    startCursor = response.has_more ? response.next_cursor : null;
  } while (startCursor);
  return results;
}

async function findIdeaPage(ideaId) {
  const pages = await listAll("ideas");
  return pages.find((page) => ideaMatches(page, ideaId)) || null;
}

async function findIdeaPages(ideaIds) {
  const wanted = new Set((ideaIds || []).map(normalizeId).filter(Boolean));
  if (wanted.size === 0) {
    return [];
  }
  const pages = await listAll("ideas");
  return pages.filter((page) => wanted.has(normalizeId(page.id)));
}

async function findProjectPage(projectId) {
  const pages = await listAll("projects");
  return pages.find((page) => projectMatches(page, projectId)) || null;
}

async function findProjectBySourceIdea(ideaId) {
  const normalizedIdeaId = normalizeId(ideaId);
  if (!normalizedIdeaId) {
    return null;
  }
  const pages = await listAll("projects");
  return (
    pages.find((page) => {
      const sourceIdea = richText(pickProperty(page.properties || {}, ["source idea"]));
      return normalizeId(sourceIdea) === normalizedIdeaId;
    }) || null
  );
}

async function findRunPage(runDate) {
  const response = await queryDatabase("runs", {
    page_size: 5,
    filter: {
      property: "Run Date",
      date: {
        equals: runDate,
      },
    },
  });
  return response.results?.[0] || null;
}

async function loadCronJobs() {
  try {
    const raw = await fs.readFile(CRON_JOBS_FILE, "utf8");
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed.jobs) ? parsed.jobs : [];
  } catch {
    return [];
  }
}

async function searchNotion(query, filter) {
  const results = [];
  let startCursor = null;
  do {
    const body = { page_size: 100 };
    if (query) {
      body.query = query;
    }
    if (filter) {
      body.filter = filter;
    }
    if (startCursor) {
      body.start_cursor = startCursor;
    }
    const response = await notionRequest("/search", { method: "POST", body });
    results.push(...(response.results || []));
    startCursor = response.has_more ? response.next_cursor : null;
  } while (startCursor);
  return results;
}

function notionObjectTitle(entry) {
  if (!entry) {
    return "";
  }
  if (entry.object === "database") {
    return (entry.title || []).map((item) => item.plain_text || "").join("").trim();
  }
  if (entry.object === "page") {
    return titleText(pickProperty(entry.properties || {}, ["title", "name"]));
  }
  return "";
}

function findHpdCron(jobs, sessionKey) {
  return (
    jobs.find((job) => {
      if (!job || job.enabled === false) {
        return false;
      }
      if (job.agentId !== "hpd-lab") {
        return false;
      }
      if ((job.sessionKey || job.payload?.sessionKey || job.route?.sessionKey) !== sessionKey) {
        return false;
      }
      const name = String(job.name || "");
      return name.startsWith("hpd-start-");
    }) || null
  );
}

function simplifySignal(page) {
  return {
    page_id: page.id,
    title: signalTitle(page),
    source: richText(pickProperty(page.properties || {}, ["source"])),
    url: richText(pickProperty(page.properties || {}, ["url"])),
    summary: richText(pickProperty(page.properties || {}, ["summary"])),
    why_it_matters: richText(pickProperty(page.properties || {}, ["why it matters"])),
    bucket: richText(pickProperty(page.properties || {}, ["bucket"])),
    status: richText(pickProperty(page.properties || {}, ["status"])),
    program_id: richText(pickProperty(page.properties || {}, ["program id"])),
    archive_bucket: richText(pickProperty(page.properties || {}, ["archive bucket"])),
  };
}

function simplifyIdea(page) {
  return {
    page_id: page.id,
    idea_id: normalizeId(page.id),
    title: ideaTitle(page),
    lane: numberValue(pickProperty(page.properties || {}, ["lane"])),
    one_liner: richText(pickProperty(page.properties || {}, ["one liner"])),
    why_now: richText(pickProperty(page.properties || {}, ["why now"])),
    premium_angle: richText(pickProperty(page.properties || {}, ["premium angle"])),
    wow_moment: richText(pickProperty(page.properties || {}, ["wow moment"])),
    manufacturability_note: richText(
      pickProperty(page.properties || {}, ["manufacturability note"])
    ),
    linked_signals: richText(pickProperty(page.properties || {}, ["linked signals"])),
    ip_risk_note: richText(pickProperty(page.properties || {}, ["ip risk note"])),
    materials: richText(pickProperty(page.properties || {}, ["materials"])),
    interactivity: richText(pickProperty(page.properties || {}, ["interactivity"])),
    score_total: numberValue(pickProperty(page.properties || {}, ["score total"])),
    approval_state: richText(pickProperty(page.properties || {}, ["approval state"])),
    rank: numberValue(pickProperty(page.properties || {}, ["rank"])),
    kill_reason: richText(pickProperty(page.properties || {}, ["kill reason"])),
    owner_decision: richText(pickProperty(page.properties || {}, ["owner decision"])),
    batch_date: richText(pickProperty(page.properties || {}, ["batch date"])),
    url: page.url,
  };
}

function simplifyProject(page) {
  return {
    page_id: page.id,
    project_id: normalizeId(page.id),
    title: projectTitle(page),
    status: richText(pickProperty(page.properties || {}, ["status"])),
    source_idea: richText(pickProperty(page.properties || {}, ["source idea"])),
    brief: richText(pickProperty(page.properties || {}, ["brief"])),
    cost_estimate: richText(pickProperty(page.properties || {}, ["cost estimate"])),
    bom: richText(pickProperty(page.properties || {}, ["bom"])),
    assembly_plan: richText(pickProperty(page.properties || {}, ["assembly plan"])),
    render_prompt: richText(pickProperty(page.properties || {}, ["render prompt"])),
    render_image: richText(pickProperty(page.properties || {}, ["render image"])),
    software_spec: richText(pickProperty(page.properties || {}, ["software spec"])),
    tester_report: richText(pickProperty(page.properties || {}, ["tester report"])),
    artifact_manifest: richText(pickProperty(page.properties || {}, ["artifact manifest"])),
    completion_summary: richText(pickProperty(page.properties || {}, ["completion summary"])),
    cad_step_path: richText(pickProperty(page.properties || {}, ["cad step path"])),
    cad_stl_paths: richText(pickProperty(page.properties || {}, ["cad stl paths"])),
    assembly_doc_path: richText(pickProperty(page.properties || {}, ["assembly doc path"])),
    source_code_path: richText(pickProperty(page.properties || {}, ["source code path"])),
    firmware_build_path: richText(pickProperty(page.properties || {}, ["firmware build path"])),
    project_session_key: richText(
      pickProperty(page.properties || {}, ["project session key"])
    ),
    telegram_thread_ref: richText(
      pickProperty(page.properties || {}, ["telegram thread ref"])
    ),
    lobster_ready: richText(pickProperty(page.properties || {}, ["lobster ready"])),
    url: page.url,
  };
}

async function runOpenClaw(args) {
  return new Promise((resolve, reject) => {
    const child = spawn("openclaw", args, {
      env: process.env,
      stdio: ["ignore", "pipe", "pipe"],
    });
    let stdout = "";
    let stderr = "";
    child.stdout.on("data", (chunk) => {
      stdout += chunk;
    });
    child.stderr.on("data", (chunk) => {
      stderr += chunk;
    });
    child.on("close", (code) => {
      if (code === 0) {
        resolve({ stdout, stderr });
        return;
      }
      reject(new Error(stderr.trim() || stdout.trim() || `openclaw failed (${code})`));
    });
  });
}

async function writeSignals(file) {
  const payload = await readJsonArg(file);
  const signals = Array.isArray(payload) ? payload : payload.signals || [];
  const created = [];
  const skipped = [];

  for (const signal of signals) {
    if (!signal.title) {
      skipped.push({ reason: "missing_title", signal });
      continue;
    }
    if (signal.url) {
      const dedupe = await queryDatabase("research", {
        page_size: 1,
        filter: {
          property: "URL",
          url: {
            equals: signal.url,
          },
        },
      });
      if ((dedupe.results || []).length > 0) {
        skipped.push({ reason: "duplicate_url", title: signal.title, url: signal.url });
        continue;
      }
    }
    const page = await createPage("research", {
      properties: {
        "Signal Title": titleProp(signal.title),
        Source: richTextProp(signal.source),
        URL: urlProp(signal.url),
        Summary: richTextProp(signal.summary || signal.short_summary),
        "Why It Matters": richTextProp(signal.why_it_matters || signal.whyItMatters),
        Bucket: selectProp(signal.bucket),
        "Program ID": richTextProp(signal.program_id || signal.programId),
        Status: selectProp(signal.status || "inbox"),
        "Captured At": dateProp(signal.captured_at || currentDate()),
        Evidence: richTextProp(signal.evidence),
      },
    });
    created.push({ page_id: page.id, title: signal.title, url: page.url });
  }

  console.log(JSON.stringify({ ok: true, created, skipped }, null, 2));
}

async function listSignals(bucket, status = "inbox") {
  const filters = [];
  if (status) {
    filters.push({
      property: "Status",
      select: { equals: status },
    });
  }
  if (bucket) {
    filters.push({
      property: "Bucket",
      select: { equals: bucket },
    });
  }
  const body = {
    page_size: 100,
    sorts: [{ timestamp: "last_edited_time", direction: "descending" }],
  };
  if (filters.length === 1) {
    body.filter = filters[0];
  } else if (filters.length > 1) {
    body.filter = { and: filters };
  }
  const response = await queryDatabase("research", body);
  console.log(JSON.stringify({ ok: true, items: (response.results || []).map(simplifySignal) }, null, 2));
}

async function applySignalReviews(file) {
  const payload = await readJsonArg(file);
  const reviews = Array.isArray(payload) ? payload : payload.reviews || [];
  const updated = [];

  for (const review of reviews) {
    if (!review.page_id) {
      continue;
    }
    await updatePage(review.page_id, {
      properties: {
        Status: selectProp(review.status),
        "Librarian Note": richTextProp(review.librarian_note),
        "Duplicate Of": richTextProp(review.duplicate_of),
        "Retry Count": numberProp(review.retry_count),
        "Archive Bucket": selectProp(review.archive_bucket),
      },
    });
    updated.push(review.page_id);
  }

  console.log(JSON.stringify({ ok: true, updated_count: updated.length, updated }, null, 2));
}

async function listArchivedSignals(bucket) {
  const filters = [
    {
      property: "Status",
      select: { equals: "archived" },
    },
  ];
  if (bucket) {
    filters.push({
      property: "Bucket",
      select: { equals: bucket },
    });
  }
  const response = await queryDatabase("research", {
    page_size: 100,
    filter: filters.length === 1 ? filters[0] : { and: filters },
  });
  console.log(JSON.stringify({ ok: true, items: (response.results || []).map(simplifySignal) }, null, 2));
}

async function writeIdeas(file) {
  const payload = await readJsonArg(file);
  const ideas = Array.isArray(payload) ? payload : payload.ideas || [];
  const batchDate = payload.batch_date || currentDate();
  const created = [];

  for (const idea of ideas) {
    if (!idea.title) {
      continue;
    }
    const page = await createPage("ideas", {
      properties: {
        "Idea Title": titleProp(idea.title),
        Lane: numberProp(idea.lane),
        "One Liner": richTextProp(idea.one_liner),
        "Why Now": richTextProp(idea.why_now),
        "Premium Angle": richTextProp(idea.premium_angle),
        "Wow Moment": richTextProp(idea.wow_moment),
        "Manufacturability Note": richTextProp(idea.manufacturability_note),
        "Linked Signals": richTextProp(
          Array.isArray(idea.linked_signals) ? idea.linked_signals.join(", ") : idea.linked_signals
        ),
        "IP Risk Note": richTextProp(idea.ip_risk_note),
        Materials: richTextProp(idea.materials),
        Interactivity: selectProp(idea.interactivity || "none"),
        "Approval State": selectProp("draft"),
        "Owner Decision": selectProp("pending"),
        "Batch Date": dateProp(idea.batch_date || batchDate),
      },
    });
    created.push({ page_id: page.id, idea_id: normalizeId(page.id), title: idea.title, url: page.url });
  }

  console.log(JSON.stringify({ ok: true, batch_date: batchDate, created }, null, 2));
}

async function listIdeas(date = currentDate()) {
  const response = await queryDatabase("ideas", {
    page_size: 100,
    filter: {
      property: "Batch Date",
      date: { equals: date },
    },
  });
  console.log(JSON.stringify({ ok: true, items: (response.results || []).map(simplifyIdea) }, null, 2));
}

async function upsertRunRecord(payload) {
  const runDate = payload.date || currentDate();
  const existing = await findRunPage(runDate);
  const properties = {
    "Run Name": titleProp(payload.run_name || `Nightly Run ${runDate}`),
    "Run Date": dateProp(runDate),
    Summary: richTextProp(payload.summary),
    "Run Status": selectProp(payload.run_status || "complete"),
    Signals: numberProp(payload.signals),
    "Archived Cards": numberProp(payload.archived_cards),
    "Generated Ideas": numberProp(payload.generated_ideas),
    Shortlisted: numberProp(payload.shortlisted),
    "Telegram Message ID": richTextProp(payload.telegram_message_id),
    "Retry Count": numberProp(payload.retry_count),
  };

  if (existing) {
    const updated = await updatePage(existing.id, { properties });
    return { mode: "updated", page_id: updated.id, url: updated.url };
  }

  const created = await createPage("runs", { properties });
  return { mode: "created", page_id: created.id, url: created.url };
}

async function applyEvaluations(file) {
  const payload = await readJsonArg(file);
  const evaluations = payload.evaluations || [];
  const updated = [];
  const batchDate = payload.date || currentDate();
  const shortlistedCount =
    payload.shortlisted ??
    evaluations.filter((evaluation) =>
      String(evaluation.approval_state || "")
        .toLowerCase()
        .includes("shortlist")
    ).length;
  const generatedIdeas = payload.generated_ideas ?? evaluations.length;
  const summary =
    payload.summary ||
    `${generatedIdeas} ideas scored, ${shortlistedCount} shortlisted for the morning report.`;

  for (const evaluation of evaluations) {
    const page = await findIdeaPage(evaluation.idea_id || evaluation.page_id);
    if (!page) {
      continue;
    }
    await updatePage(page.id, {
      properties: {
        "Score Total": numberProp(evaluation.total_score),
        "Approval State": selectProp(evaluation.approval_state),
        Rank: numberProp(evaluation.shortlist_rank),
        "Kill Reason": richTextProp(evaluation.kill_reason),
        "Rubric Breakdown": richTextProp(
          typeof evaluation.rubric_breakdown === "string"
            ? evaluation.rubric_breakdown
            : JSON.stringify(evaluation.rubric_breakdown || {})
        ),
        "Batch Date": dateProp(evaluation.batch_date || batchDate),
      },
    });
    updated.push(page.id);
  }

  const runRecord = await upsertRunRecord({
    ...payload,
    date: batchDate,
    generated_ideas: generatedIdeas,
    shortlisted: shortlistedCount,
    summary,
  });
  console.log(
    JSON.stringify(
      { ok: true, updated_count: updated.length, updated, run_record: runRecord },
      null,
      2
    )
  );
}

async function handleApproval(action, ideaId) {
  if (!["approve", "reject", "later"].includes(action)) {
    throw new Error(`unsupported approval action: ${action}`);
  }

  const ideaPage = await findIdeaPage(ideaId);
  if (!ideaPage) {
    throw new Error(`idea not found: ${ideaId}`);
  }

  const idea = simplifyIdea(ideaPage);
  const ownerDecision = action === "approve" ? "approve" : action === "reject" ? "reject" : "later";
  const approvalState = action === "approve" ? "approved" : action === "reject" ? "rejected" : "later";
  const ideaKey = normalizeId(ideaPage.id);
  const existingProject = await findProjectBySourceIdea(ideaKey);
  const alreadySameDecision =
    normalizeName(idea.owner_decision) === normalizeName(ownerDecision) &&
    (action !== "approve" || Boolean(existingProject));

  if (!alreadySameDecision) {
    await updatePage(ideaPage.id, {
      properties: {
        "Owner Decision": selectProp(ownerDecision),
        "Approval State": selectProp(approvalState),
      },
    });
  }

  if (action !== "approve") {
    console.log(
      JSON.stringify(
        {
          ok: true,
          action,
          already_processed: alreadySameDecision,
          idea_id: ideaKey,
          page_id: ideaPage.id,
        },
        null,
        2
      )
    );
    return;
  }

  let projectPage = existingProject;
  let projectCreated = false;
  if (!projectPage) {
    projectPage = await createPage("projects", {
      properties: {
        "Project Name": titleProp(idea.title),
        Status: selectProp("queued"),
        "Source Idea": richTextProp(ideaKey),
        Brief: richTextProp([idea.one_liner, idea.why_now].filter(Boolean).join("\n\n")),
        "Lobster Ready": checkboxProp(true),
      },
    });
    projectCreated = true;
  }

  const projectKey = normalizeId(projectPage.id);
  const sessionKey = `project:${projectKey}`;
  const projectSummary = simplifyProject(projectPage);
  if (projectCreated || normalizeId(projectSummary.project_session_key) !== normalizeId(sessionKey)) {
    await updatePage(projectPage.id, {
      properties: {
        Status: selectProp(projectSummary.status || "queued"),
        "Project Session Key": richTextProp(sessionKey),
      },
    });
  }

  // Her proje kendi klasörüne gider: /Users/dellymac/.openclaw/projects/<projectKey-prefix>/
  const projectShortId = projectKey.slice(0, 8);
  const projectDir = `/Users/dellymac/.openclaw/projects/${projectShortId}`;

  const message =
    `Run Program: approved-project pack phase. Follow hpd-pipeline and notion-pipeline skills. TÜM metin çıktıları Türkçe olmalıdır (BOM, CAD, STL, OpenSCAD gibi teknik terimler İngilizce kalabilir). ` +
    `\n\nÖNEMLİ — Dosya konumları: Tüm proje çıktıları (pack.json, render.png, design.scad) şu klasöre kaydedilecek: ${projectDir}/ — workspace-hpd-lab'a proje dosyası YAZMA. ` +
    `\n\nAdım 1 — Klasörü oluştur ve projeyi al: \`mkdir -p ${projectDir}\` ardından \`node /Users/dellymac/.openclaw/skills/notion-pipeline/scripts/factory_ops.mjs get-project ${projectKey}\` çalıştır. ` +
    `\n\nAdım 2 — Proje paketi oluştur: ${projectDir}/pack.json dosyasına yaz. Tüm alanlar Türkçe: brief, cost_estimate (TL ve USD), bom, assembly_plan, render_prompt (İngilizce kalabilir), software_spec, tester_report, artifact_manifest, completion_summary. ` +
    `\n\nAdım 3 — Görsel üret: \`node /Users/dellymac/.openclaw/workspace-hpd-lab/generate-render.mjs "<render_prompt>" ${projectDir}/render.png\` komutunu çalıştır. Bu script gemini-3-pro-image-preview ve gemini-3.1-flash-image-preview modellerini sırayla dener. Başarılıysa render_image alanını dosya yoluyla güncelle. ` +
    `\n\nAdım 4 — OpenSCAD taslağı: ${projectDir}/design.scad dosyasına parametrik OpenSCAD taslağı yaz. Temel geometri ve boyutlar yeterli. ` +
    `\n\nAdım 5 — Notion'a yaz: \`node /Users/dellymac/.openclaw/skills/notion-pipeline/scripts/factory_ops.mjs update-project-pack ${projectKey} ${projectDir}/pack.json\` çalıştır. ` +
    `\n\nAdım 6 — Telegram: \`openclaw message send --channel telegram --target 1565027149 --message "✅ Proje tamamlandı: <proje adı>\\n\\n<2-3 cümle Türkçe özet>\\n\\nÜretilenler:\\n• <liste>\\n\\nKlasor: ${projectDir}\\n\\nNotion: <URL>"\`. Gerçek proje adı ve Notion URL kullan.`;

  const jobs = await loadCronJobs();
  let cronJob = findHpdCron(jobs, sessionKey);
  let cronCreated = false;
  if (!cronJob) {
    const cronName = `hpd-start-${projectKey.slice(0, 8)}`;
    const result = await runOpenClaw([
      "cron",
      "add",
      "--name",
      cronName,
      "--at",
      "1m",
      "--agent",
      "hpd-lab",
      "--session",
      "isolated",
      "--session-key",
      sessionKey,
      "--delete-after-run",
      "--no-deliver",
      "--model",
      "openai-codex/gpt-5.4",
      "--thinking",
      "high",
      "--timeout-seconds",
      "1800",
      "--json",
      "--message",
      message,
    ]);
    cronJob = parseJsonMaybe(result.stdout);
    cronCreated = true;
  }

  console.log(
    JSON.stringify(
      {
        ok: true,
        action,
        already_processed: alreadySameDecision && !projectCreated && !cronCreated,
        idea_id: ideaKey,
        project_id: projectKey,
        project_page_id: projectPage.id,
        project_created: projectCreated,
        cron_created: cronCreated,
        cron_result: cronJob,
      },
      null,
      2
    )
  );
}

async function recordReportDelivery(file) {
  const payload = await readJsonArg(file);
  const runDate = payload.date || currentDate();
  const messageId = String(payload.telegram_message_id || payload.message_id || "").trim();
  if (!messageId) {
    throw new Error("telegram_message_id is required");
  }

  const updates = {
    run_page_id: null,
    idea_page_ids: [],
  };

  const runPage = await findRunPage(runDate);
  if (runPage) {
    await updatePage(runPage.id, {
      properties: {
        "Telegram Message ID": richTextProp(messageId),
      },
    });
    updates.run_page_id = runPage.id;
  }

  const ideaPages = await findIdeaPages(payload.idea_ids || []);
  for (const page of ideaPages) {
    await updatePage(page.id, {
      properties: {
        "Telegram Message ID": richTextProp(messageId),
      },
    });
    updates.idea_page_ids.push(page.id);
  }

  console.log(
    JSON.stringify(
      {
        ok: true,
        telegram_message_id: messageId,
        date: runDate,
        ...updates,
      },
      null,
      2
    )
  );
}

async function findPage(query) {
  const results = await searchNotion(query, { value: "page", property: "object" });
  console.log(
    JSON.stringify(
      {
        ok: true,
        items: results.map((entry) => ({
          id: entry.id,
          object: entry.object,
          url: entry.url,
          title: notionObjectTitle(entry),
          parent: entry.parent || null,
        })),
      },
      null,
      2
    )
  );
}

async function listPageChildren(pageId) {
  const items = [];
  let startCursor = null;
  do {
    const suffix = startCursor ? `?page_size=100&start_cursor=${encodeURIComponent(startCursor)}` : "?page_size=100";
    const response = await notionRequest(`/blocks/${pageId}/children${suffix}`);
    items.push(...(response.results || []));
    startCursor = response.has_more ? response.next_cursor : null;
  } while (startCursor);

  console.log(
    JSON.stringify(
      {
        ok: true,
        items: items.map((block) => ({
          id: block.id,
          type: block.type,
          text: blockPlainText(block),
          done: isBlockDone(block),
          checked: block.type === "to_do" ? Boolean(block.to_do?.checked) : null,
          has_children: Boolean(block.has_children),
          url: block.url || null,
        })),
      },
      null,
      2
    )
  );
}

async function markBlockDone(blockId) {
  const block = await notionRequest(`/blocks/${blockId}`);
  const text = blockPlainText(block);
  if (!text) {
    throw new Error(`block has no text content: ${blockId}`);
  }

  if (block.type === "to_do") {
    await notionRequest(`/blocks/${blockId}`, {
      method: "PATCH",
      body: {
        to_do: {
          rich_text: richTextArrayForBlock(block).map((item) => ({
            type: item.type || "text",
            text: item.text,
            annotations: {
              ...(item.annotations || {}),
              strikethrough: true,
            },
            plain_text: undefined,
            href: item.href,
          })),
          checked: true,
          color: block.to_do?.color || "default",
        },
      },
    });
  } else if (["paragraph", "bulleted_list_item", "numbered_list_item", "quote"].includes(block.type)) {
    await notionRequest(`/blocks/${blockId}`, {
      method: "PATCH",
      body: {
        [block.type]: {
          rich_text: richTextArrayForBlock(block).map((item) => ({
            type: item.type || "text",
            text: item.text,
            annotations: {
              ...(item.annotations || {}),
              strikethrough: true,
            },
            plain_text: undefined,
            href: item.href,
          })),
          color: block[block.type]?.color || "default",
        },
      },
    });
  } else {
    throw new Error(`unsupported block type for mark-block-done: ${block.type}`);
  }

  console.log(JSON.stringify({ ok: true, block_id: blockId, type: block.type, text }, null, 2));
}

async function getProject(projectId) {
  const page = await findProjectPage(projectId);
  if (!page) {
    throw new Error(`project not found: ${projectId}`);
  }
  console.log(JSON.stringify({ ok: true, project: simplifyProject(page) }, null, 2));
}

async function updateProjectPack(projectId, file) {
  const page = await findProjectPage(projectId);
  if (!page) {
    throw new Error(`project not found: ${projectId}`);
  }
  const payload = await readJsonArg(file);
  await updatePage(page.id, {
    properties: {
      Status: selectProp(payload.status || "done"),
      Brief: richTextProp(payload.brief),
      "Cost Estimate": richTextProp(payload.cost_estimate),
      BOM: richTextProp(payload.bom),
      "Assembly Plan": richTextProp(payload.assembly_plan),
      "Render Prompt": richTextProp(payload.render_prompt),
      "Render Image": richTextProp(payload.render_image),
      "Software Spec": richTextProp(payload.software_spec),
      "Tester Report": richTextProp(payload.tester_report),
      "Artifact Manifest": richTextProp(payload.artifact_manifest),
      "Completion Summary": richTextProp(payload.completion_summary),
      "CAD STEP Path": richTextProp(payload.cad_step_path),
      "CAD STL Paths": richTextProp(payload.cad_stl_paths),
      "Assembly Doc Path": richTextProp(payload.assembly_doc_path),
      "Source Code Path": richTextProp(payload.source_code_path),
      "Firmware Build Path": richTextProp(payload.firmware_build_path),
      "Project Session Key": richTextProp(payload.project_session_key || `project:${normalizeId(page.id)}`),
      "Telegram Thread Ref": richTextProp(payload.telegram_thread_ref),
      "Lobster Ready": checkboxProp(payload.lobster_ready),
    },
  });
  console.log(JSON.stringify({ ok: true, project_id: normalizeId(page.id), updated: true }, null, 2));
}

async function main() {
  await loadLocalEnv();
  const [command, ...args] = process.argv.slice(2);
  if (!command) {
    usage();
    process.exit(1);
  }

  if (command === "write-signals") {
    await writeSignals(args[0]);
    return;
  }

  if (command === "list-signals") {
    await listSignals(args[0], args[1] || "inbox");
    return;
  }

  if (command === "apply-signal-reviews") {
    await applySignalReviews(args[0]);
    return;
  }

  if (command === "list-archived-signals") {
    await listArchivedSignals(args[0]);
    return;
  }

  if (command === "write-ideas") {
    await writeIdeas(args[0]);
    return;
  }

  if (command === "list-ideas") {
    await listIdeas(args[0] || currentDate());
    return;
  }

  if (command === "apply-evaluations") {
    await applyEvaluations(args[0]);
    return;
  }

  if (command === "handle-approval") {
    await handleApproval(args[0], args[1]);
    return;
  }

  if (command === "record-report-delivery") {
    await recordReportDelivery(args[0]);
    return;
  }

  if (command === "find-page") {
    await findPage(args.join(" "));
    return;
  }

  if (command === "list-page-children") {
    await listPageChildren(args[0]);
    return;
  }

  if (command === "mark-block-done") {
    await markBlockDone(args[0]);
    return;
  }

  if (command === "get-project") {
    await getProject(args[0]);
    return;
  }

  if (command === "update-project-pack") {
    await updateProjectPack(args[0], args[1]);
    return;
  }

  usage();
  process.exit(1);
}

main().catch((error) => {
  console.error(
    JSON.stringify(
      {
        ok: false,
        error: error.message,
        details: error.details || null,
      },
      null,
      2
    )
  );
  process.exit(1);
});
