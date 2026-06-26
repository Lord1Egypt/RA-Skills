#!/usr/bin/env node
/**
 * GitLab API helper for MR code review.
 *
 * Usage:
 *   node gitlab-api.js get-version
 *   node gitlab-api.js list-mrs [--project <path>]
 *   node gitlab-api.js get-changes <project_id> <mr_iid>
 *   node gitlab-api.js get-file <project_id> <branch> <file_path>
 *   node gitlab-api.js post-comment <project_id> <mr_iid> '<json>'
 *   node gitlab-api.js post-note <project_id> <mr_iid> '<text>'
 *
 * Env: GITLAB_URL, GITLAB_TOKEN
 *       These can be set in the OS environment or in {baseDir}/.env
 */

// Load .env from the skill base directory (one level up from scripts/)
const path = require("path");
const fs = require("fs");
const envPath = path.resolve(__dirname, "..", ".env");
if (fs.existsSync(envPath)) {
  for (const line of fs.readFileSync(envPath, "utf8").split("\n")) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#")) continue;
    const eq = trimmed.indexOf("=");
    if (eq === -1) continue;
    const key = trimmed.slice(0, eq).trim();
    const val = trimmed.slice(eq + 1).trim();
    if (!(key in process.env)) process.env[key] = val;
  }
}

const GITLAB_URL = process.env.GITLAB_URL?.replace(/\/+$/, "");
const GITLAB_TOKEN = process.env.GITLAB_TOKEN;

if (!GITLAB_URL || !GITLAB_TOKEN) {
  console.error("Error: GITLAB_URL and GITLAB_TOKEN environment variables are required.");
  process.exit(1);
}

const crypto = require("crypto");
const headers = { "PRIVATE-TOKEN": GITLAB_TOKEN, "Content-Type": "application/json" };

/**
 * Generate GitLab line_code: first 32 chars of SHA256(file_path) + "_" + old_line + "_" + new_line
 */
function generateLineCode(filePath, oldLine, newLine) {
  const hash = crypto.createHash("md5").update(filePath).digest("hex");
  // GitLab format: md5(filepath)_old_line_new_line (all parts present, use 0 for absent)
  const ol = oldLine != null ? oldLine : 0;
  const nl = newLine != null ? newLine : 0;
  return `${hash}_${ol}_${nl}`;
}

async function request(method, apiPath, body) {
  const url = `${GITLAB_URL}/api/v4${apiPath}`;
  const opts = { method, headers };
  if (body) opts.body = JSON.stringify(body);
  const res = await fetch(url, opts);
  const text = await res.text();
  if (!res.ok) {
    console.error(`[gitlab-api] API error [${res.status}]: ${text}`);
    process.exit(1);
  }
  try { return JSON.parse(text); } catch { return text; }
}

// ── Commands ──

async function getVersion() {
  const data = await request("GET", "/version");
  console.log(JSON.stringify({ version: data.version, revision: data.revision }, null, 2));
}

async function listMRs(args) {
  const projectFilter = args.includes("--project")
    ? args[args.indexOf("--project") + 1]
    : null;

  let apiPath = "/merge_requests?state=opened&scope=all&order_by=created_at&sort=asc&per_page=100";
  if (projectFilter) {
    apiPath = `/projects/${encodeURIComponent(projectFilter)}/merge_requests?state=opened&order_by=created_at&sort=asc&per_page=100`;
  }

  const mrs = await request("GET", apiPath);
  if (!mrs.length) {
    console.log("NO_OPEN_MRS");
    return;
  }

  // Output compact JSON array with fields the worker needs
  const result = mrs.map(mr => ({
    project_id: mr.project_id,
    mr_iid: mr.iid,
    title: mr.title,
    author: mr.author?.name,
    source_branch: mr.source_branch,
    target_branch: mr.target_branch,
    web_url: mr.web_url,
    created_at: mr.created_at,
    project_path: mr.references?.full || mr.web_url?.replace(/\/-\/merge_requests\/\d+$/, ""),
  }));

  console.log(JSON.stringify(result, null, 2));
}

async function getChanges(projectId, mrIid) {
  console.log(`[gitlab-api] Fetching MR diff: project ${projectId} !${mrIid}...`);
  const mr = await request("GET",
    `/projects/${encodeURIComponent(projectId)}/merge_requests/${mrIid}/changes`
  );

  const changes = (mr.changes || []).map(c => ({
    old_path: c.old_path,
    new_path: c.new_path,
    new_file: c.new_file,
    renamed_file: c.renamed_file,
    deleted_file: c.deleted_file,
    diff: c.diff,
  }));

  const result = {
    mr_title: mr.title,
    mr_description: mr.description,
    source_branch: mr.source_branch,
    target_branch: mr.target_branch,
    diff_refs: mr.diff_refs,
    changes,
  };

  console.log(JSON.stringify(result, null, 2));
}

async function getFile(projectId, branch, filePath) {
  try {
    const result = await request("GET",
      `/projects/${encodeURIComponent(projectId)}/repository/files/${encodeURIComponent(filePath)}/raw?ref=${encodeURIComponent(branch)}`
    );
    console.log(typeof result === "string" ? result : JSON.stringify(result));
  } catch {
    console.log("[gitlab-api] File not found (this is OK — no custom rules)");
  }
}

let commentCount = 0;

async function postComment(projectId, mrIid, jsonPayload) {
  const payload = JSON.parse(jsonPayload);
  const pos = payload.position || {};
  const position = {
    base_sha: pos.base_sha,
    start_sha: pos.start_sha,
    head_sha: pos.head_sha,
    position_type: "text",
    old_path: pos.old_path || pos.new_path,
    new_path: pos.new_path,
  };
  if (pos.new_line != null) position.new_line = pos.new_line;
  if (pos.old_line != null) position.old_line = pos.old_line;
  // Add line_code for GitLab compatibility (required on some versions)
  position.line_code = generateLineCode(position.new_path, pos.old_line, pos.new_line);
  const body = {
    body: payload.body,
    position,
  };

  const result = await request("POST",
    `/projects/${encodeURIComponent(projectId)}/merge_requests/${mrIid}/discussions`, body
  );
  commentCount++;
  console.log(`[gitlab-api] ✅ Comment #${commentCount} posted (discussion ${result.id})`);
}

async function postNote(projectId, mrIid, text) {
  const result = await request("POST",
    `/projects/${encodeURIComponent(projectId)}/merge_requests/${mrIid}/notes`,
    { body: text }
  );
  console.log(`[gitlab-api] ✅ ${commentCount} comments + summary note posted (note ${result.id})`);
  commentCount = 0;
}

// ── CLI ──

const [, , command, ...args] = process.argv;

const commands = {
  "get-version":  () => getVersion(),
  "list-mrs":     () => listMRs(args),
  "get-changes":  () => getChanges(args[0], args[1]),
  "get-file":     () => getFile(args[0], args[1], args[2]),
  "post-comment": () => {
    if (args[0] === '--file') {
      const payload = fs.readFileSync(args[1], 'utf8');
      return postComment(args[2], args[3], payload);
    }
    return postComment(args[0], args[1], args[2]);
  },
  "post-note":    () => postNote(args[0], args[1], args.slice(2).join(" ")),
};

if (!commands[command]) {
  console.error("Usage: gitlab-api.js <get-version|list-mrs|get-changes|get-file|post-comment|post-note>");
  process.exit(1);
}

commands[command]();
