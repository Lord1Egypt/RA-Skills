#!/usr/bin/env node

import { loadLocalEnv, writeEnvFile } from "./local_env.mjs";

function getNotionToken() {
  return process.env.OPENCLAW_NOTION_TOKEN || process.env.NOTION_TOKEN;
}

function getNotionVersion() {
  return process.env.OPENCLAW_NOTION_VERSION || "2022-06-28";
}

async function notionRequest(pathname, { method = "POST", body } = {}) {
  const token = getNotionToken();
  if (!token) {
    throw new Error("OPENCLAW_NOTION_TOKEN is missing");
  }
  const response = await fetch(`https://api.notion.com/v1${pathname}`, {
    method,
    headers: {
      Authorization: `Bearer ${token}`,
      "Notion-Version": getNotionVersion(),
      "Content-Type": "application/json",
    },
    body: body == null ? undefined : JSON.stringify(body),
  });
  const text = await response.text();
  const json = text ? JSON.parse(text) : {};
  if (!response.ok) {
    const error = new Error(`Notion request failed: ${response.status}`);
    error.details = json;
    throw error;
  }
  return json;
}

async function searchObjects(filter) {
  const results = [];
  let startCursor;
  do {
    const payload = { page_size: 100 };
    if (filter) {
      payload.filter = filter;
    }
    if (startCursor) {
      payload.start_cursor = startCursor;
    }
    const response = await notionRequest("/search", { body: payload });
    results.push(...(response.results || []));
    startCursor = response.has_more ? response.next_cursor : null;
  } while (startCursor);
  return results;
}

function text(content) {
  return [{ type: "text", text: { content } }];
}

function selectProperty(options) {
  return {
    select: {
      options: options.map(([name, color]) => ({ name, color })),
    },
  };
}

async function findHomePage() {
  const pages = await searchObjects({ value: "page", property: "object" });
  const workspaceHome = pages.find(
    (page) => page.parent?.type === "workspace" && ((page.properties?.title?.title?.[0]?.plain_text) || (page.properties?.Name?.title?.[0]?.plain_text) || "").trim() === "Home"
  );
  return workspaceHome || pages.find((page) => page.parent?.type === "workspace") || null;
}

function databaseTitle(entry) {
  return (entry.title || []).map((item) => item.plain_text || "").join("").trim();
}

async function findDatabaseByTitle(title) {
  const databases = await searchObjects({ value: "database", property: "object" });
  return databases.find((entry) => databaseTitle(entry) === title) || null;
}

async function ensureDatabase({ title, key, properties, parentPageId }) {
  const existing = await findDatabaseByTitle(title);
  if (existing) {
    return { id: existing.id, url: existing.url, title, created: false, key };
  }
  const created = await notionRequest("/databases", {
    body: {
      parent: {
        type: "page_id",
        page_id: parentPageId,
      },
      title: text(title),
      properties,
    },
  });
  return { id: created.id, url: created.url, title, created: true, key };
}

function schemas(parentPageId) {
  return [
    {
      key: "OPENCLAW_NOTION_DB_RESEARCH_SIGNALS",
      title: "Research Signals",
      parentPageId,
      properties: {
        "Signal Title": { title: {} },
        Source: { rich_text: {} },
        URL: { url: {} },
        Summary: { rich_text: {} },
        "Why It Matters": { rich_text: {} },
        Bucket: selectProperty([
          ["trend", "blue"],
          ["mechanical", "green"],
          ["electronics", "yellow"],
          ["software", "purple"],
          ["infrastructure", "gray"],
        ]),
        "Program ID": { rich_text: {} },
        Status: selectProperty([
          ["inbox", "default"],
          ["archived", "green"],
          ["trash", "red"],
          ["failed", "orange"],
        ]),
        "Captured At": { date: {} },
        Evidence: { rich_text: {} },
        "Duplicate Of": { rich_text: {} },
        "Librarian Note": { rich_text: {} },
        "Retry Count": { number: { format: "number" } },
        "Archive Bucket": selectProperty([
          ["trend-archive", "blue"],
          ["tech-archive", "green"],
          ["infrastructure-archive", "gray"],
        ]),
      },
    },
    {
      key: "OPENCLAW_NOTION_DB_PROJECT_IDEAS",
      title: "Project Ideas",
      parentPageId,
      properties: {
        "Idea Title": { title: {} },
        Lane: { number: { format: "number" } },
        "One Liner": { rich_text: {} },
        "Why Now": { rich_text: {} },
        "Premium Angle": { rich_text: {} },
        "Wow Moment": { rich_text: {} },
        "Manufacturability Note": { rich_text: {} },
        "Linked Signals": { rich_text: {} },
        "IP Risk Note": { rich_text: {} },
        Materials: { rich_text: {} },
        Interactivity: selectProperty([
          ["none", "default"],
          ["interactable", "green"],
          ["non-interactable", "gray"],
        ]),
        "Score Total": { number: { format: "number" } },
        "Approval State": selectProperty([
          ["draft", "default"],
          ["shortlisted", "green"],
          ["rejected", "red"],
          ["approved", "blue"],
          ["later", "yellow"],
        ]),
        Rank: { number: { format: "number" } },
        "Kill Reason": { rich_text: {} },
        "Owner Decision": selectProperty([
          ["pending", "default"],
          ["approve", "green"],
          ["reject", "red"],
          ["later", "yellow"],
        ]),
        "Batch Date": { date: {} },
        "Telegram Message ID": { rich_text: {} },
        "Rubric Breakdown": { rich_text: {} },
      },
    },
    {
      key: "OPENCLAW_NOTION_DB_PROJECTS",
      title: "Projects",
      parentPageId,
      properties: {
        "Project Name": { title: {} },
        Status: selectProperty([
          ["queued", "default"],
          ["planning", "blue"],
          ["design", "purple"],
          ["development", "yellow"],
          ["testing", "orange"],
          ["done", "green"],
          ["blocked", "red"],
        ]),
        "Source Idea": { rich_text: {} },
        Brief: { rich_text: {} },
        "Cost Estimate": { rich_text: {} },
        BOM: { rich_text: {} },
        "Assembly Plan": { rich_text: {} },
        "Render Prompt": { rich_text: {} },
        "Render Image": { rich_text: {} },
        "Software Spec": { rich_text: {} },
        "Tester Report": { rich_text: {} },
        "Project Session Key": { rich_text: {} },
        "Telegram Thread Ref": { rich_text: {} },
        "Lobster Ready": { checkbox: {} },
      },
    },
    {
      key: "OPENCLAW_NOTION_DB_NIGHTLY_RUNS",
      title: "Nightly Runs",
      parentPageId,
      properties: {
        "Run Name": { title: {} },
        "Run Date": { date: {} },
        Summary: { rich_text: {} },
        "Run Status": selectProperty([
          ["queued", "default"],
          ["running", "blue"],
          ["complete", "green"],
          ["blocked", "yellow"],
          ["failed", "red"],
        ]),
        Signals: { number: { format: "number" } },
        "Archived Cards": { number: { format: "number" } },
        "Generated Ideas": { number: { format: "number" } },
        Shortlisted: { number: { format: "number" } },
        "Telegram Message ID": { rich_text: {} },
        "Retry Count": { number: { format: "number" } },
      },
    },
  ];
}

async function main() {
  await loadLocalEnv();
  const token = getNotionToken();
  if (!token) {
    throw new Error("OPENCLAW_NOTION_TOKEN is missing");
  }

  const homePage = await findHomePage();
  if (!homePage) {
    throw new Error("No accessible parent page found in Notion workspace");
  }

  const databases = [];
  for (const definition of schemas(homePage.id)) {
    databases.push(await ensureDatabase(definition));
  }

  const envUpdates = {
    OPENCLAW_NOTION_TOKEN: token,
    OPENCLAW_NOTION_DB_RESEARCH_SIGNALS: databases.find((item) => item.key === "OPENCLAW_NOTION_DB_RESEARCH_SIGNALS")?.id,
    OPENCLAW_NOTION_DB_PROJECT_IDEAS: databases.find((item) => item.key === "OPENCLAW_NOTION_DB_PROJECT_IDEAS")?.id,
    OPENCLAW_NOTION_DB_PROJECTS: databases.find((item) => item.key === "OPENCLAW_NOTION_DB_PROJECTS")?.id,
    OPENCLAW_NOTION_DB_NIGHTLY_RUNS: databases.find((item) => item.key === "OPENCLAW_NOTION_DB_NIGHTLY_RUNS")?.id,
    OPENCLAW_TELEGRAM_TARGET: process.env.OPENCLAW_TELEGRAM_TARGET || "1565027149",
    OPENCLAW_TIMEZONE: process.env.OPENCLAW_TIMEZONE || "Europe/Istanbul",
  };

  await writeEnvFile(envUpdates);

  console.log(
    JSON.stringify(
      {
        ok: true,
        parentPage: {
          id: homePage.id,
          url: homePage.url,
          title:
            homePage.properties?.title?.title?.[0]?.plain_text ||
            homePage.properties?.Name?.title?.[0]?.plain_text ||
            "Home",
        },
        databases,
      },
      null,
      2
    )
  );
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
