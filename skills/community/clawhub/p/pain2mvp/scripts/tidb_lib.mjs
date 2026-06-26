import fs from "node:fs/promises";
import { stdin as input } from "node:process";
import { connect } from "@tidbcloud/serverless";

export const REQUIRED_URL_PARAM = "sslaccept";
export const REQUIRED_URL_VALUE = "strict";

export const OPPORTUNITY_TABLE_SQL = `
CREATE TABLE IF NOT EXISTS opportunity_snapshots (
  opportunity_id VARCHAR(64) PRIMARY KEY,
  run_id VARCHAR(64) NOT NULL,
  \`rank\` INT NOT NULL,
  title VARCHAR(255) NOT NULL,
  affected_user TEXT NOT NULL,
  job_to_be_done TEXT NOT NULL,
  pain_statement TEXT NOT NULL,
  score_total INT NOT NULL,
  score_breakdown_json JSON NOT NULL,
  confidence VARCHAR(16) NOT NULL,
  confidence_reason TEXT NOT NULL,
  pain_cluster_key VARCHAR(128) NOT NULL,
  supporting_evidence_json JSON NOT NULL,
  contradictions_json JSON NOT NULL,
  query_scope_json JSON NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY uniq_run_rank (run_id, \`rank\`),
  KEY idx_run_created (run_id, created_at),
  KEY idx_cluster (pain_cluster_key)
)`;

export const PRDS_TABLE_SQL = `
CREATE TABLE IF NOT EXISTS prds (
  prd_id VARCHAR(64) PRIMARY KEY,
  run_id VARCHAR(64) NOT NULL,
  opportunity_id VARCHAR(64) NOT NULL,
  title VARCHAR(255) NOT NULL,
  status VARCHAR(32) NOT NULL,
  target_user TEXT NOT NULL,
  goal TEXT NOT NULL,
  structured_prd_json JSON NOT NULL,
  markdown_snapshot LONGTEXT NOT NULL,
  source_evidence_json JSON NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  KEY idx_prds_run_created (run_id, created_at),
  KEY idx_prds_opp_created (opportunity_id, created_at)
)`;

export const AGENT_MEMORY_TABLE_SQL = `
CREATE TABLE IF NOT EXISTS agent_memory (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  source_url TEXT NOT NULL,
  source_type VARCHAR(128) NOT NULL,
  author_handle VARCHAR(255) NOT NULL,
  community_or_site VARCHAR(255) NOT NULL,
  published_at VARCHAR(128) NOT NULL,
  snippet TEXT NOT NULL,
  pain_cluster_id VARCHAR(128) NOT NULL,
  engagement_signals JSON NOT NULL,
  retrieval_timestamp VARCHAR(128) NOT NULL,
  traceability_status VARCHAR(128) NOT NULL,
  KEY idx_agent_memory_cluster (pain_cluster_id)
)`;


const OPPORTUNITY_FIELDS = [
  "opportunity_id",
  "run_id",
  "rank",
  "title",
  "affected_user",
  "job_to_be_done",
  "pain_statement",
  "score_total",
  "score_breakdown_json",
  "confidence",
  "confidence_reason",
  "pain_cluster_key",
  "supporting_evidence_json",
  "contradictions_json",
  "query_scope_json",
];

const PRD_FIELDS = [
  "prd_id",
  "run_id",
  "opportunity_id",
  "title",
  "status",
  "target_user",
  "goal",
  "structured_prd_json",
  "markdown_snapshot",
  "source_evidence_json",
];

const EVIDENCE_FIELDS = [
  "source_url",
  "source_type",
  "author_handle",
  "community_or_site",
  "published_at",
  "snippet",
  "pain_cluster_id",
  "engagement_signals",
  "retrieval_timestamp",
  "traceability_status",
];

const EVIDENCE_BATCH_FIELDS = ["run_id", "evidence_rows"];
const OPPORTUNITY_BATCH_FIELDS = ["run_id", "opportunities"];

export function fail(message, details) {
  const error = new Error(message);
  if (details !== undefined) {
    error.details = details;
  }
  throw error;
}

export function parseTidbUrl(urlString) {
  if (!urlString) {
    fail("Missing TIDB_DATABASE_URL");
  }

  let url;
  try {
    url = new URL(urlString);
  } catch {
    fail("Invalid TIDB_DATABASE_URL");
  }

  if (url.protocol !== "mysql:") {
    fail("TIDB_DATABASE_URL must use the mysql:// scheme");
  }

  const databaseName = url.pathname.replace(/^\//, "");
  if (!databaseName) {
    fail("TIDB_DATABASE_URL must include a database name");
  }

  const sslAccept = url.searchParams.get(REQUIRED_URL_PARAM);
  if (sslAccept !== REQUIRED_URL_VALUE) {
    fail("TIDB_DATABASE_URL must include ?sslaccept=strict");
  }

  return {
    urlString,
    databaseName,
  };
}

export function getConnection(urlString = process.env.TIDB_DATABASE_URL) {
  const { urlString: normalizedUrl } = parseTidbUrl(urlString);
  return connect({ url: normalizedUrl });
}

export async function ensureTables(conn) {
  await conn.execute(OPPORTUNITY_TABLE_SQL);
  await conn.execute(PRDS_TABLE_SQL);
  await conn.execute(AGENT_MEMORY_TABLE_SQL);
}

export function parseJsonArgument(raw, label = "input") {
  if (raw === undefined || raw === null || raw === "") {
    return {};
  }

  if (typeof raw !== "string") {
    return raw;
  }

  try {
    return JSON.parse(raw);
  } catch {
    fail(`Invalid JSON in ${label}`);
  }
}

export async function readCommandInput(argv) {
  const fileIndex = argv.indexOf("--input-file");
  if (fileIndex !== -1) {
    const filePath = argv[fileIndex + 1];
    if (!filePath) {
      fail("Missing value for --input-file");
    }
    const content = await fs.readFile(filePath, "utf8");
    return parseJsonArgument(content, "--input-file");
  }

  if (!input.isTTY) {
    const chunks = [];
    for await (const chunk of input) {
      chunks.push(chunk);
    }
    const content = Buffer.concat(chunks).toString("utf8").trim();
    return parseJsonArgument(content, "stdin");
  }

  return {};
}

export function requireFields(payload, fields, label) {
  for (const field of fields) {
    if (payload[field] === undefined || payload[field] === null || payload[field] === "") {
      fail(`Missing required field ${field} for ${label}`);
    }
  }
}

export function normalizeJsonField(value, fieldName) {
  if (typeof value === "string") {
    try {
      JSON.parse(value);
      return value;
    } catch {
      fail(`Field ${fieldName} must be valid JSON`);
    }
  }

  return JSON.stringify(value ?? null);
}

export function normalizeEvidenceRow(payload) {
  requireFields(payload, EVIDENCE_FIELDS, "save-evidence");
  return {
    ...payload,
    engagement_signals: normalizeJsonField(payload.engagement_signals, "engagement_signals"),
  };
}

export function normalizeEvidenceBatchPayload(payload) {
  requireFields(payload, EVIDENCE_BATCH_FIELDS, "save-evidence-batch");
  if (!Array.isArray(payload.evidence_rows) || payload.evidence_rows.length === 0) {
    fail("save-evidence-batch requires a non-empty evidence_rows array");
  }

  return {
    run_id: payload.run_id,
    evidence_rows: payload.evidence_rows.map((row) => normalizeEvidenceRow(row)),
  };
}

export function normalizeOpportunitySnapshot(payload) {
  requireFields(payload, OPPORTUNITY_FIELDS, "save-opportunity");
  return {
    ...payload,
    rank: Number(payload.rank),
    score_total: Number(payload.score_total),
    score_breakdown_json: normalizeJsonField(payload.score_breakdown_json, "score_breakdown_json"),
    supporting_evidence_json: normalizeJsonField(payload.supporting_evidence_json, "supporting_evidence_json"),
    contradictions_json: normalizeJsonField(payload.contradictions_json, "contradictions_json"),
    query_scope_json: normalizeJsonField(payload.query_scope_json, "query_scope_json"),
  };
}

export function normalizeOpportunityBatchPayload(payload) {
  requireFields(payload, OPPORTUNITY_BATCH_FIELDS, "save-opportunity-batch");
  if (!Array.isArray(payload.opportunities) || payload.opportunities.length === 0) {
    fail("save-opportunity-batch requires a non-empty opportunities array");
  }

  return {
    run_id: payload.run_id,
    opportunities: payload.opportunities.map((row) => normalizeOpportunitySnapshot(row)),
  };
}

export function normalizePrdRecord(payload) {
  requireFields(payload, PRD_FIELDS, "save-prd");
  return {
    ...payload,
    structured_prd_json: normalizeJsonField(payload.structured_prd_json, "structured_prd_json"),
    source_evidence_json: normalizeJsonField(payload.source_evidence_json, "source_evidence_json"),
  };
}

async function insertEvidenceRow(conn, row) {
  await conn.execute(
    `INSERT INTO agent_memory (
      source_url,
      source_type,
      author_handle,
      community_or_site,
      published_at,
      snippet,
      pain_cluster_id,
      engagement_signals,
      retrieval_timestamp,
      traceability_status
    ) VALUES (?, ?, ?, ?, ?, ?, ?, CAST(? AS JSON), ?, ?)`,
    [
      row.source_url,
      row.source_type,
      row.author_handle,
      row.community_or_site,
      row.published_at,
      row.snippet,
      row.pain_cluster_id,
      row.engagement_signals,
      row.retrieval_timestamp,
      row.traceability_status,
    ],
  );
}

export async function saveEvidence(conn, payload) {
  const row = normalizeEvidenceRow(payload);
  await insertEvidenceRow(conn, row);

  return {
    ok: true,
    command: "save-evidence",
    pain_cluster_id: row.pain_cluster_id,
    source_url: row.source_url,
  };
}

export async function saveEvidenceBatch(conn, payload) {
  const batch = normalizeEvidenceBatchPayload(payload);
  for (const row of batch.evidence_rows) {
    await insertEvidenceRow(conn, row);
  }

  return {
    ok: true,
    command: "save-evidence-batch",
    run_id: batch.run_id,
    saved_count: batch.evidence_rows.length,
  };
}

async function upsertOpportunityRow(conn, row) {
  await conn.execute(
    `INSERT INTO opportunity_snapshots (
      opportunity_id,
      run_id,
      \`rank\`,
      title,
      affected_user,
      job_to_be_done,
      pain_statement,
      score_total,
      score_breakdown_json,
      confidence,
      confidence_reason,
      pain_cluster_key,
      supporting_evidence_json,
      contradictions_json,
      query_scope_json
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, CAST(? AS JSON), ?, ?, ?, CAST(? AS JSON), CAST(? AS JSON), CAST(? AS JSON))
    ON DUPLICATE KEY UPDATE
      run_id = VALUES(run_id),
      \`rank\` = VALUES(\`rank\`),
      title = VALUES(title),
      affected_user = VALUES(affected_user),
      job_to_be_done = VALUES(job_to_be_done),
      pain_statement = VALUES(pain_statement),
      score_total = VALUES(score_total),
      score_breakdown_json = VALUES(score_breakdown_json),
      confidence = VALUES(confidence),
      confidence_reason = VALUES(confidence_reason),
      pain_cluster_key = VALUES(pain_cluster_key),
      supporting_evidence_json = VALUES(supporting_evidence_json),
      contradictions_json = VALUES(contradictions_json),
      query_scope_json = VALUES(query_scope_json)`,
    [
      row.opportunity_id,
      row.run_id,
      row.rank,
      row.title,
      row.affected_user,
      row.job_to_be_done,
      row.pain_statement,
      row.score_total,
      row.score_breakdown_json,
      row.confidence,
      row.confidence_reason,
      row.pain_cluster_key,
      row.supporting_evidence_json,
      row.contradictions_json,
      row.query_scope_json,
    ],
  );
}

export async function saveOpportunity(conn, payload) {
  const row = normalizeOpportunitySnapshot(payload);
  await upsertOpportunityRow(conn, row);

  return {
    ok: true,
    command: "save-opportunity",
    run_id: row.run_id,
    opportunity_id: row.opportunity_id,
  };
}

export async function saveOpportunityBatch(conn, payload) {
  const batch = normalizeOpportunityBatchPayload(payload);
  for (const row of batch.opportunities) {
    await upsertOpportunityRow(conn, row);
  }

  return {
    ok: true,
    command: "save-opportunity-batch",
    run_id: batch.run_id,
    saved_count: batch.opportunities.length,
  };
}

export async function getOpportunity(conn, payload) {
  let sql;
  let params;

  if (payload.opportunity_id) {
    sql = `SELECT * FROM opportunity_snapshots WHERE opportunity_id = ? LIMIT 1`;
    params = [payload.opportunity_id];
  } else if (payload.run_id && payload.rank !== undefined) {
    sql = `SELECT * FROM opportunity_snapshots WHERE run_id = ? AND \`rank\` = ? LIMIT 1`;
    params = [payload.run_id, Number(payload.rank)];
  } else {
    fail("get-opportunity requires opportunity_id or run_id and rank");
  }

  const rows = await conn.execute(sql, params);
  if (!rows.length) {
    fail("Opportunity not found");
  }
  return rows[0];
}

export async function savePrd(conn, payload) {
  const row = normalizePrdRecord(payload);
  await conn.execute(
    `INSERT INTO prds (
      prd_id,
      run_id,
      opportunity_id,
      title,
      status,
      target_user,
      goal,
      structured_prd_json,
      markdown_snapshot,
      source_evidence_json
    ) VALUES (?, ?, ?, ?, ?, ?, ?, CAST(? AS JSON), ?, CAST(? AS JSON))
    ON DUPLICATE KEY UPDATE
      run_id = VALUES(run_id),
      opportunity_id = VALUES(opportunity_id),
      title = VALUES(title),
      status = VALUES(status),
      target_user = VALUES(target_user),
      goal = VALUES(goal),
      structured_prd_json = VALUES(structured_prd_json),
      markdown_snapshot = VALUES(markdown_snapshot),
      source_evidence_json = VALUES(source_evidence_json)`,
    [
      row.prd_id,
      row.run_id,
      row.opportunity_id,
      row.title,
      row.status,
      row.target_user,
      row.goal,
      row.structured_prd_json,
      row.markdown_snapshot,
      row.source_evidence_json,
    ],
  );

  return {
    ok: true,
    command: "save-prd",
    prd_id: row.prd_id,
    opportunity_id: row.opportunity_id,
    run_id: row.run_id,
  };
}

export async function getPrd(conn, payload) {
  let sql;
  let params = [];

  if (payload.prd_id) {
    sql = `SELECT * FROM prds WHERE prd_id = ? LIMIT 1`;
    params = [payload.prd_id];
  } else if (payload.opportunity_id) {
    sql = `SELECT * FROM prds WHERE opportunity_id = ? ORDER BY updated_at DESC LIMIT 1`;
    params = [payload.opportunity_id];
  } else if (payload.run_id) {
    sql = `SELECT * FROM prds WHERE run_id = ? ORDER BY updated_at DESC LIMIT 1`;
    params = [payload.run_id];
  } else if (payload.latest === true || Object.keys(payload).length === 0) {
    sql = `SELECT * FROM prds ORDER BY updated_at DESC LIMIT 1`;
  } else {
    fail("get-prd requires prd_id, opportunity_id, run_id, or latest=true");
  }

  const rows = await conn.execute(sql, params);
  if (!rows.length) {
    fail("PRD not found");
  }
  return rows[0];
}

export async function listRuns(conn) {
  const rows = await conn.execute(
    `SELECT run_id, COUNT(*) AS opportunity_count, MAX(created_at) AS last_created_at
     FROM opportunity_snapshots
     GROUP BY run_id
     ORDER BY last_created_at DESC`,
  );
  return rows;
}

export async function dispatchCommand(conn, command, payload) {
  switch (command) {
    case "save-evidence":
      return saveEvidence(conn, payload);
    case "save-evidence-batch":
      return saveEvidenceBatch(conn, payload);
    case "save-opportunity":
      return saveOpportunity(conn, payload);
    case "save-opportunity-batch":
      return saveOpportunityBatch(conn, payload);
    case "get-opportunity":
      return getOpportunity(conn, payload);
    case "save-prd":
      return savePrd(conn, payload);
    case "get-prd":
      return getPrd(conn, payload);
    case "list-runs":
      return listRuns(conn);
    default:
      fail(`Unsupported command: ${command}`);
  }
}

export function printJson(value) {
  process.stdout.write(`${JSON.stringify(value, null, 2)}\n`);
}

export function printError(error) {
  const payload = {
    ok: false,
    error: error.message,
  };
  if (error.details !== undefined) {
    payload.details = error.details;
  }
  process.stderr.write(`${JSON.stringify(payload)}\n`);
}
