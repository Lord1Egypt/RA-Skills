import express from "express";
import { closePool } from "./db.mjs";
import {
  activateLicense,
  deactivateLicense,
  validateLicense,
} from "./license-service.mjs";

const app = express();
app.use(express.json({ limit: "1mb" }));

function sendInvalid(res, error, status = 400) {
  res.status(status).json({
    error: error.code || "bad_request",
    message: error.message || "Request failed.",
  });
}

function mapErrorToStatus(code) {
  switch (code) {
    case "bad_request":
      return 400;
    case "license_not_found":
      return 404;
    case "invalid_token":
      return 401;
    case "license_inactive":
    case "license_expired":
    case "seat_limit_reached":
    case "machine_not_activated":
      return 403;
    default:
      return 500;
  }
}

app.get("/health", (_req, res) => {
  res.json({ ok: true, service: "propai-live-license-api" });
});

app.post("/v1/licenses/activate", async (req, res) => {
  try {
    const body = req.body || {};
    const data = await activateLicense({
      key: body.key,
      product: body.product,
      machineId: body.machineId,
      machineLabel: body.machineLabel,
      clientVersion: body.clientVersion,
      runtime: body.runtime,
    });
    res.json(data);
  } catch (error) {
    sendInvalid(res, error, mapErrorToStatus(error.code));
  }
});

app.post("/v1/licenses/validate", async (req, res) => {
  try {
    const body = req.body || {};
    const data = await validateLicense({
      product: body.product,
      machineId: body.machineId,
      licenseToken: body.licenseToken,
      licenseId: body.licenseId,
    });
    res.json(data);
  } catch (error) {
    if (error.code === "invalid_token") {
      return res.status(401).json({
        valid: false,
        status: "revoked",
        error: error.code,
        message: error.message,
      });
    }
    if (error.code === "license_expired") {
      return res.status(403).json({
        valid: false,
        status: "expired",
        error: error.code,
        message: error.message,
      });
    }
    if (error.code === "license_inactive") {
      return res.status(403).json({
        valid: false,
        status: "revoked",
        error: error.code,
        message: error.message,
      });
    }
    return sendInvalid(res, error, mapErrorToStatus(error.code));
  }
});

app.post("/v1/licenses/deactivate", async (req, res) => {
  try {
    const body = req.body || {};
    const data = await deactivateLicense({
      product: body.product,
      machineId: body.machineId,
      licenseToken: body.licenseToken,
      licenseId: body.licenseId,
    });
    res.json(data);
  } catch (error) {
    sendInvalid(res, error, mapErrorToStatus(error.code));
  }
});

app.use((_req, res) => {
  res.status(404).json({ error: "not_found" });
});

const host = process.env.LICENSE_API_HOST || "0.0.0.0";
const port = Number(process.env.LICENSE_API_PORT || 8787);

const server = app.listen(port, host, () => {
  process.stdout.write(`propai-live-license-api listening on http://${host}:${port}\n`);
});

async function shutdown(code = 0) {
  server.close(async () => {
    await closePool().catch(() => {});
    process.exit(code);
  });
}

process.on("SIGINT", () => shutdown(0));
process.on("SIGTERM", () => shutdown(0));
