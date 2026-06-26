import crypto from "node:crypto";
import { query, withTransaction } from "./db.mjs";

const ACTIVE_STATUSES = new Set(["active", "trial", "grace"]);

function serviceError(code, message) {
  const error = new Error(message || code);
  error.code = code;
  return error;
}

function nowIso() {
  return new Date().toISOString();
}

function hashText(value) {
  return crypto.createHash("sha256").update(value).digest("hex");
}

function generateToken() {
  const random = crypto.randomBytes(24).toString("base64url");
  return `plt_${random}`;
}

function parseHours(value, fallback) {
  const num = Number(value);
  return Number.isFinite(num) && num >= 0 ? num : fallback;
}

function isExpired(expiresAt) {
  if (!expiresAt) {
    return false;
  }
  const ms = Date.parse(expiresAt);
  return Number.isFinite(ms) && Date.now() > ms;
}

async function getEntitlements(client, licenseId) {
  const result = await client.query(
    "SELECT name FROM entitlements WHERE license_id = $1 ORDER BY name ASC",
    [licenseId],
  );
  return result.rows.map((row) => String(row.name).toLowerCase());
}

async function logAudit(client, licenseId, eventType, payload) {
  await client.query(
    `
      INSERT INTO license_audit_log (license_id, event_type, payload_json)
      VALUES ($1, $2, $3::jsonb)
    `,
    [licenseId || null, eventType, JSON.stringify(payload || {})],
  );
}

function normalizeLicenseRow(row) {
  return {
    id: row.id,
    productSlug: row.product_slug,
    plan: row.plan,
    status: String(row.status || "").toLowerCase(),
    seatLimit: Number(row.seat_limit || 0),
    expiresAt: row.expires_at ? new Date(row.expires_at).toISOString() : null,
  };
}

function ensureLicenseActive(license) {
  if (!ACTIVE_STATUSES.has(license.status)) {
    throw serviceError("license_inactive", `License status '${license.status}' is not active.`);
  }
  if (isExpired(license.expiresAt)) {
    throw serviceError("license_expired", "License has expired.");
  }
}

function responseEnvelope(license, entitlements) {
  return {
    licenseId: license.id,
    status: license.status,
    plan: license.plan,
    entitlements,
    expiresAt: license.expiresAt,
    offlineGraceHours: parseHours(process.env.OFFLINE_GRACE_HOURS, 72),
    nextCheckHours: parseHours(process.env.NEXT_CHECK_HOURS, 6),
  };
}

export async function activateLicense({
  key,
  product,
  machineId,
  machineLabel,
  clientVersion,
  runtime,
}) {
  if (!key || !product || !machineId) {
    throw serviceError("bad_request", "key, product, and machineId are required.");
  }

  return withTransaction(async (client) => {
    const keyHash = hashText(key);
    const licenseResult = await client.query(
      `
        SELECT id, product_slug, plan, status, seat_limit, expires_at
        FROM licenses
        WHERE license_key_hash = $1 AND product_slug = $2
        LIMIT 1
      `,
      [keyHash, product],
    );
    if (licenseResult.rowCount === 0) {
      await logAudit(client, null, "activate_failed", { product, machineId, reason: "license_not_found" });
      throw serviceError("license_not_found", "License key is invalid.");
    }

    const license = normalizeLicenseRow(licenseResult.rows[0]);
    ensureLicenseActive(license);

    const existingActivation = await client.query(
      `
        SELECT id
        FROM activations
        WHERE license_id = $1 AND machine_id = $2
        LIMIT 1
      `,
      [license.id, machineId],
    );

    if (existingActivation.rowCount === 0) {
      const activeSeats = await client.query(
        `
          SELECT COUNT(*)::int AS count
          FROM activations
          WHERE license_id = $1 AND revoked_at IS NULL
        `,
        [license.id],
      );
      const activeSeatCount = Number(activeSeats.rows[0].count || 0);
      if (activeSeatCount >= license.seatLimit) {
        await logAudit(client, license.id, "activate_failed", {
          reason: "seat_limit_reached",
          machineId,
          activeSeatCount,
          seatLimit: license.seatLimit,
        });
        throw serviceError("seat_limit_reached", "Seat limit reached for this license.");
      }
    }

    await client.query(
      `
        INSERT INTO activations (license_id, machine_id, machine_label, last_seen_at, revoked_at)
        VALUES ($1, $2, $3, NOW(), NULL)
        ON CONFLICT (license_id, machine_id)
        DO UPDATE SET
          machine_label = EXCLUDED.machine_label,
          last_seen_at = NOW(),
          revoked_at = NULL
      `,
      [license.id, machineId, machineLabel || null],
    );

    await client.query(
      "UPDATE license_tokens SET revoked_at = NOW() WHERE license_id = $1 AND revoked_at IS NULL",
      [license.id],
    );

    const licenseToken = generateToken();
    const tokenHash = hashText(licenseToken);
    await client.query(
      "INSERT INTO license_tokens (license_id, token_hash) VALUES ($1, $2)",
      [license.id, tokenHash],
    );

    const entitlements = await getEntitlements(client, license.id);
    await logAudit(client, license.id, "activate", {
      product,
      machineId,
      machineLabel: machineLabel || null,
      clientVersion: clientVersion || null,
      runtime: runtime || null,
      at: nowIso(),
    });

    return {
      ...responseEnvelope(license, entitlements),
      licenseToken,
    };
  });
}

async function resolveLicenseByToken(client, token) {
  if (!token) {
    throw serviceError("invalid_token", "licenseToken is required.");
  }
  const tokenHash = hashText(token);
  const result = await client.query(
    `
      SELECT l.id, l.product_slug, l.plan, l.status, l.seat_limit, l.expires_at
      FROM license_tokens t
      INNER JOIN licenses l ON l.id = t.license_id
      WHERE t.token_hash = $1 AND t.revoked_at IS NULL
      LIMIT 1
    `,
    [tokenHash],
  );
  if (result.rowCount === 0) {
    throw serviceError("invalid_token", "licenseToken is invalid or revoked.");
  }
  return normalizeLicenseRow(result.rows[0]);
}

export async function validateLicense({
  product,
  machineId,
  licenseToken,
  licenseId,
}) {
  if (!product || !machineId || !licenseToken) {
    throw serviceError("bad_request", "product, machineId, and licenseToken are required.");
  }

  return withTransaction(async (client) => {
    const license = await resolveLicenseByToken(client, licenseToken);
    if (license.productSlug !== product) {
      throw serviceError("invalid_token", "Token product does not match request.");
    }
    if (licenseId && license.id !== licenseId) {
      throw serviceError("invalid_token", "licenseId does not match token.");
    }
    ensureLicenseActive(license);

    const activation = await client.query(
      `
        SELECT id
        FROM activations
        WHERE license_id = $1 AND machine_id = $2 AND revoked_at IS NULL
        LIMIT 1
      `,
      [license.id, machineId],
    );
    if (activation.rowCount === 0) {
      throw serviceError("machine_not_activated", "Machine is not activated for this license.");
    }

    await client.query(
      `
        UPDATE activations
        SET last_seen_at = NOW()
        WHERE license_id = $1 AND machine_id = $2
      `,
      [license.id, machineId],
    );

    const entitlements = await getEntitlements(client, license.id);
    await logAudit(client, license.id, "validate", { product, machineId, at: nowIso() });

    return {
      valid: true,
      ...responseEnvelope(license, entitlements),
    };
  });
}

export async function deactivateLicense({
  product,
  machineId,
  licenseToken,
  licenseId,
}) {
  if (!product || !machineId || !licenseToken) {
    throw serviceError("bad_request", "product, machineId, and licenseToken are required.");
  }

  return withTransaction(async (client) => {
    const license = await resolveLicenseByToken(client, licenseToken);
    if (license.productSlug !== product) {
      throw serviceError("invalid_token", "Token product does not match request.");
    }
    if (licenseId && license.id !== licenseId) {
      throw serviceError("invalid_token", "licenseId does not match token.");
    }

    await client.query(
      `
        UPDATE activations
        SET revoked_at = NOW(), last_seen_at = NOW()
        WHERE license_id = $1 AND machine_id = $2 AND revoked_at IS NULL
      `,
      [license.id, machineId],
    );
    await client.query(
      `
        UPDATE license_tokens
        SET revoked_at = NOW()
        WHERE token_hash = $1 AND revoked_at IS NULL
      `,
      [hashText(licenseToken)],
    );

    await logAudit(client, license.id, "deactivate", { product, machineId, at: nowIso() });
    return { ok: true };
  });
}
