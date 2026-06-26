"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.requestText = requestText;
const http_1 = __importDefault(require("http"));
const https_1 = __importDefault(require("https"));
const url_1 = require("url");
async function requestText(rawUrl, options = {}) {
    const { method = "GET", headers = {}, body, timeoutMs = 15000, insecure = false, maxRedirects = 5, } = options;
    const target = new url_1.URL(rawUrl);
    const isHttps = target.protocol === "https:";
    const transport = isHttps ? https_1.default : http_1.default;
    const requestHeaders = { ...headers };
    const hasContentLength = Object.keys(requestHeaders).some((key) => key.toLowerCase() === "content-length");
    if (body !== undefined && !hasContentLength) {
        requestHeaders["Content-Length"] = String(Buffer.byteLength(body, "utf-8"));
    }
    return await new Promise((resolve, reject) => {
        const request = transport.request({
            protocol: target.protocol,
            hostname: target.hostname,
            port: target.port || undefined,
            path: `${target.pathname}${target.search}`,
            method,
            headers: requestHeaders,
            agent: isHttps && insecure ? new https_1.default.Agent({ rejectUnauthorized: false }) : undefined,
        }, async (response) => {
            const chunks = [];
            response.on("data", (chunk) => {
                chunks.push(Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk));
            });
            response.on("end", async () => {
                const statusCode = response.statusCode || 0;
                const responseBody = Buffer.concat(chunks).toString("utf-8");
                const location = response.headers.location;
                if (location &&
                    [301, 302, 303, 307, 308].includes(statusCode) &&
                    maxRedirects > 0) {
                    try {
                        const nextUrl = new url_1.URL(location, target).toString();
                        const redirected = await requestText(nextUrl, {
                            method: statusCode === 303 ? "GET" : method,
                            headers: requestHeaders,
                            body: statusCode === 303 ? undefined : body,
                            timeoutMs,
                            insecure,
                            maxRedirects: maxRedirects - 1,
                        });
                        resolve(redirected);
                    }
                    catch (error) {
                        reject(error);
                    }
                    return;
                }
                resolve({
                    statusCode,
                    headers: response.headers,
                    body: responseBody,
                });
            });
        });
        request.on("error", reject);
        request.setTimeout(timeoutMs, () => {
            request.destroy(new Error(`request timeout after ${timeoutMs}ms`));
        });
        if (body !== undefined) {
            request.write(body);
        }
        request.end();
    });
}
