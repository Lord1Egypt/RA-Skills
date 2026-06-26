#!/usr/bin/env node
'use strict';

const { spawnSync } = require('child_process');
const fs = require('fs');
const http = require('http');
const https = require('https');
const path = require('path');

const BASE_URL = process.env.OKKIGO_BASE_URL || 'https://go.okki.ai';
const SKILL_VERSION = process.env.OKKIGO_SKILL_VERSION || '1.3.2';
const SKILL_RUNTIME = process.env.OKKIGO_SKILL_RUNTIME || 'unknown';

function resolveApiKey() {
  const resolver = path.join(__dirname, '..', 'resolve-api-key.sh');
  const result = spawnSync('bash', [resolver, '--print'], {
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe']
  });

  if (result.status !== 0) {
    throw new Error(`API key resolver failed: ${(result.stderr || result.stdout || '').trim()}`);
  }

  const key = String(result.stdout || '').trim().split(/\r?\n/)[0];
  if (!key || !key.startsWith('sk-')) {
    throw new Error('No OKKI Go API key resolved.');
  }
  return key;
}

function resolveInstallId() {
  const fromEnv = process.env.OKKIGO_INSTALL_ID || process.env.OKKI_GO_INSTALL_ID;
  if (fromEnv) return firstLine(fromEnv);

  const manifestPath = path.join(__dirname, '..', '.okki-go-manifest.json');
  const manifestId = readJsonInstallId(manifestPath);
  if (manifestId) return manifestId;

  const configHome = process.env.XDG_CONFIG_HOME || path.join(process.env.HOME || '', '.config');
  if (configHome) {
    const installIdPath = path.join(configHome, 'okki-go', 'install-id');
    if (fs.existsSync(installIdPath)) {
      return firstLine(fs.readFileSync(installIdPath, 'utf8'));
    }
  }

  return '';
}

function readJsonInstallId(filePath) {
  if (!fs.existsSync(filePath)) return '';
  try {
    const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));
    const id = data.installId || data.install_id;
    return typeof id === 'string' ? firstLine(id) : '';
  } catch (_) {
    return '';
  }
}

function firstLine(value) {
  return String(value || '').trim().split(/\r?\n/)[0];
}

function authHeaders() {
  const headers = {
    Authorization: `ApiKey ${resolveApiKey()}`,
    'Content-Type': 'application/json',
    'X-Okki-Skill-Version': SKILL_VERSION,
    'X-Okki-Skill-Runtime': SKILL_RUNTIME
  };
  const installId = resolveInstallId();
  if (installId) headers['X-Okki-Install-Id'] = installId;
  return headers;
}

async function getJson(apiPath) {
  return requestJson('GET', apiPath);
}

async function postJson(apiPath, payload) {
  return requestJson('POST', apiPath, payload);
}

async function requestJson(method, apiPath, payload) {
  const result = await requestJsonWithMeta(method, apiPath, payload);
  return result.body;
}

async function postJsonWithMeta(apiPath, payload) {
  return requestJsonWithMeta('POST', apiPath, payload);
}

async function requestJsonWithMeta(method, apiPath, payload) {
  const response = await request(method, `${BASE_URL}${apiPath}`, authHeaders(), payload);
  let body;
  try {
    body = response.body ? JSON.parse(response.body) : null;
  } catch (_) {
    body = response.body;
  }

  if (response.statusCode < 200 || response.statusCode >= 300) {
    const error = new Error(formatApiError(response.statusCode, body));
    error.statusCode = response.statusCode;
    error.body = body;
    throw error;
  }

  return {
    statusCode: response.statusCode,
    body
  };
}

function request(method, urlString, headers, payload) {
  return new Promise((resolve, reject) => {
    const url = new URL(urlString);
    const transport = url.protocol === 'http:' ? http : https;
    const body = payload === undefined ? null : JSON.stringify(payload);
    const requestHeaders = Object.assign({}, headers);
    if (body !== null) {
      requestHeaders['Content-Length'] = Buffer.byteLength(body);
    }

    const req = transport.request({
      method,
      hostname: url.hostname,
      port: url.port || (url.protocol === 'http:' ? 80 : 443),
      path: `${url.pathname}${url.search}`,
      headers: requestHeaders
    }, (res) => {
      const chunks = [];
      res.on('data', (chunk) => chunks.push(chunk));
      res.on('end', () => {
        resolve({
          statusCode: res.statusCode || 0,
          body: Buffer.concat(chunks).toString('utf8')
        });
      });
    });
    req.on('error', reject);
    if (body !== null) req.write(body);
    req.end();
  });
}

function formatApiError(statusCode, body) {
  if (body && typeof body === 'object') {
    return body.detail || body.title || `OKKI Go API returned HTTP ${statusCode}`;
  }
  return body ? String(body) : `OKKI Go API returned HTTP ${statusCode}`;
}

function writeJsonFile(filePath, value) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  fs.writeFileSync(filePath, `${JSON.stringify(value, null, 2)}\n`, { mode: 0o600 });
  try {
    fs.chmodSync(filePath, 0o600);
  } catch (_) {
    // Best effort on platforms that do not support POSIX modes.
  }
}

function readJsonFile(filePath) {
  return JSON.parse(fs.readFileSync(filePath, 'utf8'));
}

function parseJson(source, label) {
  try {
    return JSON.parse(source);
  } catch (error) {
    throw new Error(`Invalid JSON in ${label}: ${error.message}`);
  }
}

module.exports = {
  BASE_URL,
  getJson,
  parseJson,
  postJson,
  postJsonWithMeta,
  readJsonFile,
  requestJson,
  requestJsonWithMeta,
  writeJsonFile
};
