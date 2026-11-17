import { DEFAULT_EVENT_LIMIT } from "./constants.mjs";
import {
  ClientValidationError,
  CorrespondenceError,
  UnknownOutcomeError,
  fallbackCode,
  fallbackMessage,
} from "./errors.mjs";
import { collectSecrets, redactString } from "./redact.mjs";
import { readBoundedJson, validResponse } from "./response.mjs";
import {
  assertBodySize,
  validateEventPost,
  validateEventQuery,
  validateGrantCreate,
  validateId,
  validateIdempotencyKey,
  validateProjectCreate,
} from "./validate.mjs";

function bytesToBase64Url(bytes) {
  let binary = "";
  for (const byte of bytes) binary += String.fromCharCode(byte);
  const base64 = btoa(binary);
  return base64.replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/g, "");
}

export function createIdempotencyKey() {
  const bytes = new Uint8Array(32);
  if (!globalThis.crypto?.getRandomValues) {
    throw new ClientValidationError({ message: "a cryptographic RNG is required to mint an Idempotency-Key" });
  }
  globalThis.crypto.getRandomValues(bytes);
  return bytesToBase64Url(bytes);
}

function isLoopbackHost(hostname) {
  const host = String(hostname || "")
    .toLowerCase()
    .replace(/^\[|\]$/g, "");
  return host === "localhost" || host === "127.0.0.1" || host === "::1";
}

export function assertCorrespondenceOrigin(baseUrl) {
  if (!baseUrl) {
    throw new ClientValidationError({ message: "baseUrl is required" });
  }
  let parsed;
  try {
    parsed = new URL(baseUrl);
  } catch {
    throw new ClientValidationError({ message: "baseUrl must be a valid URL" });
  }
  if (parsed.protocol === "http:") {
    if (!isLoopbackHost(parsed.hostname)) {
      throw new ClientValidationError({ message: "HTTP is allowed only for localhost closed-pilot origins" });
    }
  } else if (parsed.protocol !== "https:") {
    throw new ClientValidationError({ message: "baseUrl must use HTTPS" });
  }
  if (parsed.username || parsed.password) {
    throw new ClientValidationError({ message: "baseUrl must not contain credentials" });
  }
  if (parsed.search || parsed.hash) {
    throw new ClientValidationError({ message: "baseUrl must not contain a query or fragment" });
  }
  return `${parsed.origin}${parsed.pathname.replace(/\/$/, "")}`;
}

export class CorrespondenceClient {
  #baseUrl;
  #fetch;
  #token;
  #timeoutMs;
  #maxResponseBytes;
  #disposed = false;
  #disposeController = new AbortController();

  constructor({ baseUrl, fetch: fetchImpl, token, timeoutMs = 15_000, maxResponseBytes = 8 * 1024 * 1024 } = {}) {
    this.#baseUrl = assertCorrespondenceOrigin(baseUrl);
    if (
      !Number.isSafeInteger(timeoutMs) ||
      timeoutMs < 1 ||
      timeoutMs > 300_000 ||
      !Number.isSafeInteger(maxResponseBytes) ||
      maxResponseBytes < 1 ||
      maxResponseBytes > 64 * 1024 * 1024
    ) {
      throw new ClientValidationError({ message: "invalid transport bounds" });
    }
    this.#timeoutMs = timeoutMs;
    this.#maxResponseBytes = maxResponseBytes;
    if (typeof fetchImpl !== "function") {
      throw new ClientValidationError({
        message: "fetch is required; inject ordinary fetch or a test-only transport",
      });
    }
    this.#fetch = fetchImpl;
    this.#token = token ?? null;
  }

  get baseUrl() {
    return this.#baseUrl;
  }

  get disposed() {
    return this.#disposed;
  }

  dispose() {
    if (this.#disposed) return;
    this.#disposed = true;
    this.#token = null;
    this.#disposeController.abort();
  }

  async createProject({ idempotencyKey, token, ...body } = {}) {
    const key = this.#requireIdempotencyKey(idempotencyKey);
    const validated = validateProjectCreate(body);
    return this.#mutate("POST", "/v1/projects", {
      body: validated,
      token,
      idempotencyKey: key,
      success: [200, 201],
      validate: (payload) => validResponse("createProject", payload),
      map: (status, payload) => ({
        project: payload.project,
        ownerToken: payload.ownerToken,
        idempotencyKey: key,
        status,
        replayed: status === 200,
      }),
    });
  }

  async getProject({ projectId, token } = {}) {
    const id = validateId(projectId, "projectId");
    return this.#read("GET", `/v1/projects/${encodeURIComponent(id)}`, {
      token,
      success: [200],
      validate: (payload) => validResponse("getProject", payload, { projectId: id }),
      map: (_status, payload) => ({ project: payload.project }),
    });
  }

  async createGrant({ projectId, token, ...body } = {}) {
    const id = validateId(projectId, "projectId");
    const validated = validateGrantCreate(body);
    return this.#mutate("POST", `/v1/projects/${encodeURIComponent(id)}/grants`, {
      body: validated,
      token,
      success: [201],
      validate: (payload) => validResponse("createGrant", payload, { role: validated.role }),
      map: (_status, payload) => ({
        grantId: payload.grantId,
        token: payload.token,
        role: payload.role,
        expiresAt: payload.expiresAt ?? null,
      }),
    });
  }

  async revokeGrant({ projectId, grantId, token } = {}) {
    const id = validateId(projectId, "projectId");
    const grant = validateId(grantId, "grantId");
    return this.#mutate("DELETE", `/v1/projects/${encodeURIComponent(id)}/grants/${encodeURIComponent(grant)}`, {
      token,
      success: [204],
      map: () => ({ status: 204 }),
    });
  }

  async postEvent({ projectId, idempotencyKey, token, ...body } = {}) {
    const id = validateId(projectId, "projectId");
    const key = this.#requireIdempotencyKey(idempotencyKey);
    const validated = validateEventPost(body);
    return this.#mutate("POST", `/v1/projects/${encodeURIComponent(id)}/events`, {
      body: validated,
      token,
      idempotencyKey: key,
      success: [200, 201],
      validate: (payload) => validResponse("postEvent", payload, { projectId: id }),
      map: (status, payload) => ({
        event: payload.event,
        project: payload.project,
        idempotencyKey: key,
        status,
        replayed: status === 200,
      }),
    });
  }

  async listEvents({ projectId, after, limit, token } = {}) {
    const id = validateId(projectId, "projectId");
    const query = validateEventQuery({ after, limit });
    const search = new URLSearchParams();
    if (query.after) search.set("after", query.after);
    if (query.limit != null) search.set("limit", String(query.limit));
    const suffix = search.toString() ? `?${search.toString()}` : "";
    return this.#read("GET", `/v1/projects/${encodeURIComponent(id)}/events${suffix}`, {
      token,
      success: [200],
      validate: (payload) => validResponse("listEvents", payload, { projectId: id, limit: query.limit }),
      map: (_status, payload) => ({
        events: payload.events,
        nextCursor: payload.nextCursor ?? null,
        limit: query.limit ?? DEFAULT_EVENT_LIMIT,
      }),
    });
  }

  #requireIdempotencyKey(value) {
    if (value == null) {
      throw new ClientValidationError({
        message: "Idempotency-Key is required for mutations; reuse it to reconcile unknown results",
      });
    }
    return validateIdempotencyKey(value);
  }

  #resolveToken(token) {
    const resolved = token === undefined ? this.#token : token;
    if (!resolved) {
      throw new ClientValidationError({
        status: 401,
        code: "invalid_grant",
        message: "a bearer token is required",
      });
    }
    if (typeof resolved !== "string") {
      throw new ClientValidationError({ message: "token must be a string" });
    }
    return resolved;
  }

  async #read(method, path, options) {
    return this.#request(method, path, { ...options, mutation: false });
  }

  async #mutate(method, path, options) {
    return this.#request(method, path, { ...options, mutation: true });
  }

  async #request(method, path, { body, token, idempotencyKey, success, map, validate, mutation }) {
    if (this.#disposed || this.#disposeController.signal.aborted) {
      throw new CorrespondenceError({
        status: null,
        code: "unavailable",
        message: "request failed or its response could not be read safely",
      });
    }
    const accepted = Array.isArray(success) ? success : mutation ? [200, 201] : [200];
    const resolvedToken = this.#resolveToken(token);
    const secrets = collectSecrets(resolvedToken, this.#token);
    if (body !== undefined) assertBodySize(body);
    const url = `${this.#baseUrl}${path}`;
    this.#assertSafeUrl(url, secrets);

    const headers = {
      Accept: "application/json",
      Authorization: `Bearer ${resolvedToken}`,
    };
    let encodedBody;
    if (body !== undefined) {
      headers["Content-Type"] = "application/json";
      encodedBody = JSON.stringify(body);
    }
    if (idempotencyKey) headers["Idempotency-Key"] = idempotencyKey;

    const controller = new AbortController();
    const onDispose = () => controller.abort();
    this.#disposeController.signal.addEventListener("abort", onDispose, { once: true });
    let timer;
    let response;
    let payload;
    try {
      const deadline = new Promise((_, reject) => {
        timer = setTimeout(() => {
          controller.abort();
          reject(new Error("request timed out"));
        }, this.#timeoutMs);
      });
      await Promise.race([
        deadline,
        (async () => {
          response = await this.#fetch(url, {
            method,
            headers,
            body: encodedBody,
            redirect: "manual",
            signal: controller.signal,
          });
          if (
            controller.signal.aborted ||
            this.#disposed ||
            response.redirected ||
            (response.status >= 300 && response.status < 400) ||
            (response.url && response.url !== url)
          ) {
            void response.body?.cancel?.().catch(() => {});
            throw new Error("unexpected redirect or aborted request");
          }
          if (response.status !== 204) {
            payload = await readBoundedJson(response, this.#maxResponseBytes, controller.signal);
          }
        })(),
      ]);
    } catch {
      controller.abort();
      if (mutation) {
        throw new UnknownOutcomeError({
          idempotencyKey: idempotencyKey ?? null,
          operation: `${method} ${stripQuery(path)}`,
        });
      }
      throw new CorrespondenceError({
        status: null,
        code: "unavailable",
        message: "request failed or its response could not be read safely",
      });
    } finally {
      clearTimeout(timer);
      this.#disposeController.signal.removeEventListener("abort", onDispose);
    }

    const status = response.status;
    if (status === 204 && accepted.includes(204)) {
      return map(status, null);
    }

    if (!accepted.includes(status)) {
      if (mutation && isUnknownMutationStatus(status, payload)) {
        throw new UnknownOutcomeError({
          idempotencyKey: idempotencyKey ?? null,
          operation: `${method} ${stripQuery(path)}`,
        });
      }
      throw errorFromPayload(status, payload, {
        idempotencyKey,
        secrets,
      });
    }

    if (!validate?.(payload)) {
      if (mutation) {
        throw new UnknownOutcomeError({
          idempotencyKey: idempotencyKey ?? null,
          operation: `${method} ${stripQuery(path)}`,
        });
      }
      throw new CorrespondenceError({
        status,
        code: "invalid_response",
        message: "response does not match the correspondence contract",
        idempotencyKey,
      });
    }

    return map(status, payload);
  }

  #assertSafeUrl(url, secrets) {
    const parsed = new URL(url);
    const publicUrl = parsed.toString();
    for (const secret of secrets) {
      if (secret && publicUrl.includes(secret)) {
        throw new ClientValidationError({ message: "refusing to send a credential in the URL" });
      }
    }
    if (parsed.username || parsed.password) {
      throw new ClientValidationError({ message: "refusing to send a credential in the URL" });
    }
  }

  [Symbol.for("nodejs.util.inspect.custom")]() {
    return `CorrespondenceClient { baseUrl: ${this.#baseUrl}, token: [redacted], disposed: ${this.#disposed} }`;
  }
}

function stripQuery(path) {
  const idx = path.indexOf("?");
  return idx === -1 ? path : path.slice(0, idx);
}

function isUnknownMutationStatus(status, payload) {
  if (status >= 200 && status < 300) return true;
  if (status === 500 || status === 502 || status === 504) return true;
  return !(
    [400, 401, 403, 404, 409, 413, 429, 503].includes(status) &&
    typeof payload?.error?.code === "string" &&
    typeof payload?.error?.message === "string"
  );
}

function errorFromPayload(status, payload, { idempotencyKey, secrets }) {
  const error = payload?.error;
  const code = redactString(typeof error?.code === "string" ? error.code : fallbackCode(status), secrets);
  const message = redactString(
    typeof error?.message === "string" ? error.message : fallbackMessage(status),
    secrets,
  );
  return new CorrespondenceError({
    status,
    code,
    message,
    idempotencyKey: idempotencyKey ?? null,
    retryable: false,
  });
}
