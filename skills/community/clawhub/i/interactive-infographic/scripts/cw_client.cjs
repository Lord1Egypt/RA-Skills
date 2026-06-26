const fs = require("fs");
const path = require("path");
const crypto = require("crypto");
const http = require("http");
const https = require("https");
const { URL } = require("url");

class CWClient {
  constructor() {
    const baseUrl = "https://pptx.chenxitech.site";
    this.baseUrl = baseUrl ? baseUrl.replace(/\/+$/, "") : "";
    this.timeoutMs = 3000000;
    this.apiKey = this.loadApiKey();
    this.editorProtocol = process.env.CONTEXTWEAVE_EDITOR_PROTOCOL || "trae";
  }

  loadApiKey() {
    const key = process.env.CONTEXTWEAVE_MCP_API_KEY;
    return key || "94a05d02-9ade-4d9d-9f39-88734d9e34b4";
  }

  validateBaseUrl() {
    if (!this.baseUrl) {
      return this.error(
        "MISSING_API_URL",
        "Missing API URL",
        true,
        "内部错误: 基础URL缺失"
      );
    }
    let parsed;
    try {
      parsed = new URL(this.baseUrl);
    } catch (error) {
      return this.error("INVALID_API_URL", "Invalid API URL format", true, "内部错误: 基础URL格式错误");
    }
    if (!["http:", "https:"].includes(parsed.protocol)) {
      return this.error("INVALID_API_URL", "Unsupported API URL protocol", true, "仅支持 http 或 https");
    }
    const allowlist = ["api.contextweave.site", "contextweave.site", "pptx.chenxitech.site", "bpjwmsdb.com"];
    const host = parsed.hostname.toLowerCase();
    const trusted = allowlist.some((allowed) => host === allowed || host.endsWith(`.${allowed}`));
    if (!trusted) {
      return this.error(
        "UNTRUSTED_API_HOST",
        "Untrusted API host",
        true,
        "请使用官方域名"
      );
    }
    return null;
  }

  headers() {
    const headers = { "X-Request-ID": this.createRequestId(), "Content-Type": "application/json" };
    if (this.apiKey) {
      headers["X-API-Key"] = this.apiKey;
    }
    return headers;
  }

  createRequestId() {
    return crypto.randomBytes(16).toString("hex");
  }

  validateSafePath(targetPath) {
    if (!targetPath || typeof targetPath !== "string") {
      return this.error("INVALID_PATH", "Path is empty or invalid");
    }
    if (!path.isAbsolute(targetPath)) {
      return this.error("INPUT_FILE_NOT_ABSOLUTE", `Path must be absolute: ${targetPath}`);
    }
    const normalized = path.resolve(targetPath);
    const cwd = process.cwd();
    const relative = path.relative(cwd, normalized);
    if (relative === '..' || relative.startsWith('..' + path.sep) || path.isAbsolute(relative)) {
      return this.error("PATH_TRAVERSAL_DETECTED", "Path must be strictly within the current working directory");
    }
    return null;
  }

  error(code, message, recoverable = false, recoveryHint = null) {
    const result = { status: "error", error: { code, message } };
    if (recoverable) {
      result.error.recoverable = true;
    }
    if (recoveryHint) {
      result.error.recovery_hint = recoveryHint;
    }
    return result;
  }

  async request(endpoint, payload) {
    const baseUrlError = this.validateBaseUrl();
    if (baseUrlError) {
      return baseUrlError;
    }
    const body = { ...payload };
    if (this.editorProtocol) {
      body.editor_protocol = this.editorProtocol;
    }

    try {
      const response = await this.postJson(`${this.baseUrl}${endpoint}`, body);
      if (response.statusCode === 402) {
        return this.error("PAYMENT_REQUIRED", "Insufficient credits", true, "请充值后重试");
      }
      if (response.statusCode === 403) {
        return this.error("AUTH_ERROR", "Invalid API key or missing key", true, "请检查 CONTEXTWEAVE_MCP_API_KEY");
      }
      if (response.statusCode < 200 || response.statusCode >= 300) {
        throw new Error(`${response.statusCode} ${response.statusMessage || "Request failed"}`);
      }
      return JSON.parse(response.body || "{}");
    } catch (error) {
      return this.error("API_ERROR", String(error.message || error), true, "请检查网络或后端服务状态后重试");
    }
  }

  postJson(urlString, body) {
    const parsed = new URL(urlString);
    const payload = JSON.stringify(body);
    const options = {
      method: "POST",
      hostname: parsed.hostname,
      port: parsed.port || (parsed.protocol === "https:" ? 443 : 80),
      path: `${parsed.pathname}${parsed.search}`,
      headers: {
        ...this.headers(),
        "Content-Length": Buffer.byteLength(payload),
      },
    };
    const transport = parsed.protocol === "https:" ? https : http;
    return new Promise((resolve, reject) => {
      const req = transport.request(options, (res) => {
        const chunks = [];
        res.on("data", (chunk) => chunks.push(chunk));
        res.on("end", () => {
          resolve({
            statusCode: res.statusCode || 0,
            statusMessage: res.statusMessage || "",
            body: Buffer.concat(chunks).toString("utf8"),
          });
        });
      });
      req.setTimeout(this.timeoutMs, () => {
        req.destroy(new Error("timeout"));
      });
      req.on("error", reject);
      req.write(payload);
      req.end();
    });
  }

  async runGeneration({ userRequest, inputFile = null, sessionId = null, mode = "3", inputSequence = null }) {
    const payload = {
      mode,
      input_sequence: inputSequence,
      export_svg: true,
      export_pptx: false,
      session_id: sessionId,
      test_file: null,
    };
    if (inputFile) {
      const pathError = this.validateSafePath(inputFile);
      if (pathError) {
        return pathError;
      }
      if (!fs.existsSync(inputFile)) {
        return this.error("FILE_NOT_FOUND", `File not found: ${inputFile}`);
      }
      try {
        const content = fs.readFileSync(inputFile, "utf8");
        let reqText = content.trim();
        let cwText = "";
        if (content.includes("# CW")) {
          const parts = content.split("# CW");
          const reqPart = parts[0];
          const cwPart = parts.slice(1).join("# CW");
          const afterFence = cwPart.split("```cw")[1];
          if (afterFence && afterFence.includes("```")) {
            cwText = afterFence.split("```")[0].trim();
          } else {
            cwText = cwPart.trim();
          }
          if (reqPart.includes("# Request")) {
            reqText = reqPart.split("# Request")[1].trim();
          } else {
            reqText = reqPart.trim();
          }
        }
        payload.user_request = reqText;
        payload.initial_cw_code = cwText;
      } catch (error) {
        return this.error("READ_ERROR", `Failed to read input file: ${String(error.message || error)}`);
      }
    } else {
      payload.user_request = userRequest;
    }
    return this.request("/run", payload);
  }

  async exportSessionAsset(sessionId, formatName) {
    return this.request("/export-session", { session_id: sessionId, format: formatName });
  }

  async importCode(target = "ContextWeave") {
    const pathError = this.validateSafePath(target);
    if (pathError) {
      return pathError;
    }
    const targetPath = path.resolve(target);
    if (!fs.existsSync(targetPath)) {
      return this.error("PATH_NOT_FOUND", `Path not found: ${targetPath}`);
    }
    
    let cwFile = targetPath;
    const stats = fs.statSync(targetPath);
    if (stats.isDirectory()) {
      cwFile = path.join(targetPath, "diagram.cw");
      if (!fs.existsSync(cwFile)) {
        return this.error("FILE_NOT_FOUND", `diagram.cw not found in directory: ${targetPath}`);
      }
    }
    
    let content;
    try {
      content = fs.readFileSync(cwFile, "utf8");
    } catch (error) {
      return this.error("READ_ERROR", String(error.message || error));
    }
    return this.request("/session/import", { cw_code: content, source_name: cwFile });
  }

  async exportCode(sessionId, target = "ContextWeave") {
    const pathError = this.validateSafePath(target);
    if (pathError) {
      return pathError;
    }
    const result = await this.request("/session/export", { session_id: sessionId });
    if (result.status === "error") {
      return result;
    }
    const cwCode = result.cw_code;
    const targetPath = path.resolve(target);
    try {
      fs.mkdirSync(targetPath, { recursive: true });
    } catch (error) {
      return this.error("CREATE_DIR_ERROR", String(error.message || error));
    }
    const targetFile = path.join(targetPath, "diagram.cw");
    try {
      fs.writeFileSync(targetFile, cwCode || "", "utf8");
    } catch (error) {
      return this.error("WRITE_ERROR", String(error.message || error));
    }
    return { status: "ok", file_path: targetFile, session_id: sessionId };
  }
}

function printJson(data) {
  process.stdout.write(`${JSON.stringify(data, null, 2)}\n`);
}

module.exports = {
  CWClient,
  printJson,
};
