#!/usr/bin/env node

import fs from "node:fs/promises";
import { loadLocalEnv } from "./local_env.mjs";

const notionVersion = process.env.OPENCLAW_NOTION_VERSION || "2022-06-28";

function getNotionToken() {
  return process.env.OPENCLAW_NOTION_TOKEN || process.env.NOTION_TOKEN;
}

function getAliasMap() {
  return {
    research: process.env.OPENCLAW_NOTION_DB_RESEARCH_SIGNALS,
    ideas: process.env.OPENCLAW_NOTION_DB_PROJECT_IDEAS,
    projects: process.env.OPENCLAW_NOTION_DB_PROJECTS,
    runs: process.env.OPENCLAW_NOTION_DB_NIGHTLY_RUNS,
  };
}

function getRequiredEnvMap() {
  return {
    OPENCLAW_NOTION_DB_RESEARCH_SIGNALS: process.env.OPENCLAW_NOTION_DB_RESEARCH_SIGNALS,
    OPENCLAW_NOTION_DB_PROJECT_IDEAS: process.env.OPENCLAW_NOTION_DB_PROJECT_IDEAS,
    OPENCLAW_NOTION_DB_PROJECTS: process.env.OPENCLAW_NOTION_DB_PROJECTS,
    OPENCLAW_NOTION_DB_NIGHTLY_RUNS: process.env.OPENCLAW_NOTION_DB_NIGHTLY_RUNS,
  };
}

function usage() {
  console.error(
    "Usage: notion_api.mjs <check-env|query-db|create-page|update-page|append-blocks|retrieve-page> [args...]"
  );
}

function resolveId(value) {
  if (!value) {
    throw new Error("missing id or alias");
  }
  return getAliasMap()[value] || value;
}

async function readJsonArg(file) {
  if (!file) {
    return {};
  }
  const raw = file === "-" ? await readStdin() : await fs.readFile(file, "utf8");
  return raw.trim() ? JSON.parse(raw) : {};
}

async function readStdin() {
  let data = "";
  for await (const chunk of process.stdin) {
    data += chunk;
  }
  return data;
}

async function notionRequest(path, { method = "GET", body } = {}) {
  const notionToken = getNotionToken();
  if (!notionToken) {
    throw new Error("OPENCLAW_NOTION_TOKEN is missing");
  }
  const response = await fetch(`https://api.notion.com/v1${path}`, {
    method,
    headers: {
      Authorization: `Bearer ${notionToken}`,
      "Notion-Version": notionVersion,
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

async function main() {
  await loadLocalEnv();
  const [command, ...args] = process.argv.slice(2);
  if (!command) {
    usage();
    process.exit(1);
  }

  if (command === "check-env") {
    const aliasMap = getAliasMap();
    const requiredEnvMap = getRequiredEnvMap();
    const notionToken = getNotionToken();
    const missing = [];
    if (!notionToken) {
      missing.push("OPENCLAW_NOTION_TOKEN");
    }
    for (const [name, value] of Object.entries(requiredEnvMap)) {
      if (!value) {
        missing.push(name);
      }
    }
    console.log(
      JSON.stringify(
        {
          ok: missing.length === 0,
          missing,
          aliases: aliasMap,
        },
        null,
        2
      )
    );
    return;
  }

  if (command === "query-db") {
    const [database, payloadFile] = args;
    const databaseId = resolveId(database);
    const payload = await readJsonArg(payloadFile);
    const result = await notionRequest(`/databases/${databaseId}/query`, {
      method: "POST",
      body: payload,
    });
    console.log(JSON.stringify(result, null, 2));
    return;
  }

  if (command === "create-page") {
    const [database, payloadFile] = args;
    const databaseId = resolveId(database);
    const payload = await readJsonArg(payloadFile);
    const body = {
      parent: payload.parent || { database_id: databaseId },
      ...payload,
    };
    const result = await notionRequest("/pages", { method: "POST", body });
    console.log(JSON.stringify(result, null, 2));
    return;
  }

  if (command === "update-page") {
    const [pageId, payloadFile] = args;
    const payload = await readJsonArg(payloadFile);
    const result = await notionRequest(`/pages/${pageId}`, {
      method: "PATCH",
      body: payload,
    });
    console.log(JSON.stringify(result, null, 2));
    return;
  }

  if (command === "append-blocks") {
    const [pageId, payloadFile] = args;
    const payload = await readJsonArg(payloadFile);
    const body = Array.isArray(payload) ? { children: payload } : payload;
    const result = await notionRequest(`/blocks/${pageId}/children`, {
      method: "PATCH",
      body,
    });
    console.log(JSON.stringify(result, null, 2));
    return;
  }

  if (command === "retrieve-page") {
    const [pageId] = args;
    const result = await notionRequest(`/pages/${pageId}`);
    console.log(JSON.stringify(result, null, 2));
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
