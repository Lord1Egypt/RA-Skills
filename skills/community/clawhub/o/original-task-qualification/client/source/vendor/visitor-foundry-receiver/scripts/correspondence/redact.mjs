const BEARER_RE = /Bearer\s+\S+/gi;
const TOKEN_RE = /\b(?:tok_|neo_(?:own|rdr|wtr)_)[A-Za-z0-9_-]{16,}\b/gi;

export function redactSecrets(value, secrets = []) {
  if (value == null) return value;
  if (typeof value === "string") return redactString(value, secrets);
  if (typeof value !== "object") return value;
  if (Array.isArray(value)) return value.map((item) => redactSecrets(item, secrets));
  const out = {};
  for (const [key, item] of Object.entries(value)) {
    if (isSecretKey(key)) out[key] = "[redacted]";
    else out[key] = redactSecrets(item, secrets);
  }
  return out;
}

export function redactString(text, secrets = []) {
  let out = String(text);
  for (const secret of secrets) {
    if (typeof secret === "string" && secret.length >= 8) {
      out = out.split(secret).join("[redacted]");
    }
  }
  return out.replace(BEARER_RE, "Bearer [redacted]").replace(TOKEN_RE, "[redacted]");
}

export function collectSecrets(...values) {
  return values.filter((value) => typeof value === "string" && value.length >= 8);
}

export function assertNoSecretInPublicValue(value, secrets, label) {
  const serialized = typeof value === "string" ? value : JSON.stringify(value);
  for (const secret of secrets) {
    if (typeof secret === "string" && secret.length >= 8 && serialized.includes(secret)) {
      const error = new Error(`${label} must not contain a credential`);
      error.code = "secret_leak";
      throw error;
    }
  }
  if (/Bearer\s+\S+/i.test(serialized)) {
    const error = new Error(`${label} must not contain a Bearer credential`);
    error.code = "secret_leak";
    throw error;
  }
}

function isSecretKey(key) {
  const normalized = String(key).toLowerCase();
  return (
    normalized === "token" ||
    normalized === "ownertoken" ||
    normalized === "authorization" ||
    normalized === "password" ||
    normalized === "secret" ||
    normalized === "credential"
  );
}
