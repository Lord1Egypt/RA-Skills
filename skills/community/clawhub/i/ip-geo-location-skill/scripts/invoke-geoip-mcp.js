#!/usr/bin/env node

const net = require('node:net');

const MCP_URL = 'https://ip.api4claw.com/mcp';
const TIMEOUT_MS = 15000;

const privateBlockList = new net.BlockList();
privateBlockList.addSubnet('10.0.0.0', 8, 'ipv4');
privateBlockList.addSubnet('172.16.0.0', 12, 'ipv4');
privateBlockList.addSubnet('192.168.0.0', 16, 'ipv4');
privateBlockList.addSubnet('127.0.0.0', 8, 'ipv4');
privateBlockList.addSubnet('169.254.0.0', 16, 'ipv4');
privateBlockList.addSubnet('100.64.0.0', 10, 'ipv4');
privateBlockList.addSubnet('0.0.0.0', 8, 'ipv4');
privateBlockList.addSubnet('::1', 128, 'ipv6');
privateBlockList.addSubnet('fc00::', 7, 'ipv6');
privateBlockList.addSubnet('fe80::', 10, 'ipv6');

function isPrivateOrReservedIp(ip) {
  const ipType = net.isIP(ip);
  if (ipType === 0) {
    return false;
  }

  const family = ipType === 4 ? 'ipv4' : 'ipv6';
  return privateBlockList.check(ip, family);
}

function parseArgs(argv) {
  const ips = [];
  for (const arg of argv) {
    if (!arg.startsWith('--')) {
      ips.push(arg);
    }
  }
  return ips;
}

function validateIps(ips) {
  const valid = [];
  const invalid = [];
  const blocked = [];

  for (const ip of ips) {
    if (net.isIP(ip) === 0) {
      invalid.push(ip);
    } else if (isPrivateOrReservedIp(ip)) {
      blocked.push(ip);
    } else {
      valid.push(ip);
    }
  }

  return { valid, invalid, blocked };
}

async function postJson(url, body, headers = {}) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), TIMEOUT_MS);

  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...headers,
      },
      body: JSON.stringify(body),
      signal: controller.signal,
    });

    const text = await response.text();

    if (!response.ok) {
      const err = new Error(text || `HTTP ${response.status}`);
      err.status = response.status;
      err.responseText = text;
      err.headers = response.headers;
      throw err;
    }

    return { text, headers: response.headers };
  } finally {
    clearTimeout(timer);
  }
}

async function initializeSession() {
  const initReq = {
    jsonrpc: '2.0',
    id: 1,
    method: 'initialize',
    params: {
      protocolVersion: '2025-03-26',
      capabilities: {},
      clientInfo: {
        name: 'ip-geo-location-skill-script',
        version: '1.0.0',
      },
    },
  };

  const { headers } = await postJson(MCP_URL, initReq);
  const sessionId = headers.get('mcp-session-id') || headers.get('Mcp-Session-Id');

  if (!sessionId) {
    throw new Error('Initialize succeeded but Mcp-Session-Id header is missing.');
  }

  return sessionId;
}

function isSessionExpiredError(error) {
  const msg = String(error && error.message ? error.message : '').toLowerCase();
  return msg.includes('invalid or missing mcp-session-id') || (msg.includes('session') && msg.includes('expired'));
}

async function callGeoTool(sessionId, ipAddress) {
  const req = {
    jsonrpc: '2.0',
    id: 2,
    method: 'tools/call',
    params: {
      name: 'get_ip_geolocation',
      arguments: {
        ip_address: ipAddress,
      },
    },
  };

  const { text } = await postJson(MCP_URL, req, { 'Mcp-Session-Id': sessionId });
  const payload = JSON.parse(text);

  const textBlock = payload?.result?.content?.[0]?.text;
  if (!textBlock) {
    throw new Error(`Unexpected MCP response: ${text}`);
  }

  return JSON.parse(textBlock);
}

async function queryWithSessionRetry(ipAddress, currentSessionId) {
  try {
    const data = await callGeoTool(currentSessionId, ipAddress);
    return { data, sessionId: currentSessionId };
  } catch (error) {
    if (!isSessionExpiredError(error)) {
      throw error;
    }

    // Session timeout/invalid: re-initialize once and retry the same request.
    const newSessionId = await initializeSession();
    const data = await callGeoTool(newSessionId, ipAddress);
    return { data, sessionId: newSessionId };
  }
}

async function main() {
  const parsed = [...new Set(parseArgs(process.argv.slice(2)))];

  if (parsed.length === 0) {
    console.error('Usage: node scripts/invoke-geoip-mcp.js <ip1> [ip2] [ip3] ...');
    process.exit(1);
  }

  const { valid: ips, invalid, blocked } = validateIps(parsed);
  if (ips.length === 0) {
    console.error('No public IPv4/IPv6 inputs found. Private/reserved addresses are blocked from external lookup.');
    process.exit(1);
  }

  let sessionId;
  try {
    sessionId = await initializeSession();
  } catch (error) {
    console.error(`Failed to initialize MCP session: ${error.message}`);
    process.exit(1);
  }

  const results = [];
  for (const bad of invalid) {
    results.push({ ip: bad, error: 'Invalid IP format' });
  }
  for (const blockedIp of blocked) {
    results.push({ ip: blockedIp, error: 'Private or reserved IP blocked from external lookup' });
  }

  for (const ip of ips) {
    try {
      const { data, sessionId: updatedSession } = await queryWithSessionRetry(ip, sessionId);
      sessionId = updatedSession;
      results.push({
        ip: data.ip,
        country: data.country,
        country_code: data.country_code,
        province: data.province,
        city: data.city,
        asn: data.asn,
        asn_org: data.asn_org,
      });
    } catch (error) {
      results.push({
        ip,
        error: error.message,
      });
    }
  }

  console.log(JSON.stringify(results, null, 2));
}

main();
