/**
 * Know Your AI — Shared helpers for skill scripts
 */

/**
 * Validate and sanitize an ID input to prevent GraphQL injection.
 * IDs should only contain alphanumeric characters, hyphens, and underscores.
 * Throws if the input contains unexpected characters.
 */
export function sanitizeId(input, label = "ID") {
  if (!input || typeof input !== "string") {
    throw new Error(`${label} is required and must be a string`);
  }
  const trimmed = input.trim();
  if (!/^[a-zA-Z0-9_-]+$/.test(trimmed)) {
    throw new Error(`Invalid ${label}: "${trimmed}" — must contain only alphanumeric characters, hyphens, and underscores`);
  }
  return trimmed;
}

/**
 * Parse a Know Your AI DSN string into its components.
 * Format: https://kya_xxx:da2-xxx@host/product_id
 */
export function parseDsn(dsn) {
  const url = new URL(dsn);
  const apiKey = url.username;
  const authToken = decodeURIComponent(url.password);
  const host = url.hostname + (url.port ? `:${url.port}` : "");
  const productId = url.pathname.replace(/^\//, "").replace(/\/$/, "");
  if (!apiKey || !authToken || !host || !productId) {
    throw new Error("DSN must contain api_key, auth_token, host, and product_id");
  }
  // Sanitize the productId from the DSN as well
  sanitizeId(productId, "Product ID");
  return { apiKey, authToken, host, productId };
}

/**
 * Execute a GraphQL query against the Know Your AI API.
 * Always use GraphQL variables for parameterized queries — never interpolate
 * user input directly into query strings.
 */
export async function gql(parsed, query, variables = {}) {
  const resp = await fetch(`https://${parsed.host}/graphql`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: parsed.authToken,
    },
    body: JSON.stringify({ query, variables }),
  });

  if (!resp.ok) {
    const text = await resp.text().catch(() => "");
    throw new Error(`API request failed (${resp.status}): ${text.slice(0, 300)}`);
  }

  const data = await resp.json();
  if (data.errors) {
    throw new Error(`GraphQL errors: ${JSON.stringify(data.errors).slice(0, 300)}`);
  }
  return data;
}

/**
 * Require KNOW_YOUR_AI_DSN or exit with a helpful message.
 */
export function requireDsn() {
  const dsn = (process.env.KNOW_YOUR_AI_DSN ?? "").trim();
  if (!dsn) {
    console.error("✖ Missing KNOW_YOUR_AI_DSN environment variable.");
    console.error("  Set it from the Know Your AI dashboard → Settings → API Keys.");
    console.error('  Example: export KNOW_YOUR_AI_DSN="https://kya_xxx:da2-xxx@host/product_id"');
    process.exit(1);
  }
  return dsn;
}

/**
 * Format an error for display.
 */
export function formatError(err) {
  return err instanceof Error ? err.message : String(err);
}
