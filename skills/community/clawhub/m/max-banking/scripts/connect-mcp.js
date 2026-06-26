#!/usr/bin/env node
/**
 * Pareamento via MCP — chama a tool pairing_exchange no MCP (como o chat faria).
 * Uso: node connect-mcp.js <pairing_code> <mcp_url> [env]
 *   MCP_URL: ex. https://xxx.ngrok-free.app/mcp
 *   env: prod | homolog | local (inferido da URL se omitido)
 *
 * O MCP deve ter BANKING_API_URL configurado e a tool pairing_exchange.
 * Salva agent_key e session.json em ~/.openclaw/secrets/maxbank/.
 */

const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');
const os = require('os');

const PAIRING_CODE = process.argv[2]?.trim();
const MCP_URL = process.argv[3]?.trim();
const ENV_ARG = process.argv[4]?.trim();

const SECRETS_DIR = path.join(os.homedir(), '.openclaw', 'secrets', 'maxbank');
const AGENT_KEY_FILE = path.join(SECRETS_DIR, 'agent_key');
const SESSION_FILE = path.join(SECRETS_DIR, 'session.json');

function fail(msg) {
  console.error('pairing (MCP):', msg);
  process.exit(1);
}

if (!PAIRING_CODE) {
  fail('pairing_code obrigatório. Uso: node connect-mcp.js ABCD-EF12 https://xxx.ngrok-free.app/mcp');
}
if (!MCP_URL) {
  fail('MCP_URL obrigatório (2º argumento). Ex: node connect-mcp.js ABCD-EF12 https://xxx.ngrok-free.app/mcp');
}

// MCP JSON-RPC: tools/call
const rpcRequest = {
  jsonrpc: '2.0',
  id: 1,
  method: 'tools/call',
  params: {
    name: 'pairing_exchange',
    arguments: { pairing_code: PAIRING_CODE },
  },
};

const url = new URL(MCP_URL.replace(/\/$/, ''));
const body = JSON.stringify(rpcRequest);

const req = (url.protocol === 'https:' ? https : http).request(
  url.toString(),
  {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json, text/event-stream',
    },
  },
  (res) => {
    let data = '';
    res.on('data', (c) => (data += c));
    res.on('end', () => {
      if (res.statusCode !== 200) {
        fail(`MCP retornou status ${res.statusCode}: ${data.slice(0, 200)}`);
      }
      let rpc;
      try {
        // MCP pode retornar NDJSON (uma linha por mensagem)
        const lines = data.trim().split('\n').filter((l) => l.startsWith('data:') || (!l.startsWith('data:') && l.trim()));
        const jsonStr = lines.length > 0
          ? (lines[lines.length - 1].replace(/^data:\s*/, '').trim())
          : data;
        rpc = JSON.parse(jsonStr);
      } catch {
        fail('resposta MCP inválida: ' + data.slice(0, 200));
      }
      if (rpc.error) {
        fail(rpc.error.message || JSON.stringify(rpc.error));
      }
      // MCP pode retornar array (batch) ou objeto único
      let rpcResult = rpc.result;
      if (Array.isArray(rpcResult)) {
        rpcResult = rpcResult.find((r) => r && !r.error) || rpcResult[rpcResult.length - 1];
      }
      const result = rpcResult;
      if (!result) {
        fail('result não retornado');
      }
      // Erro da tool (ex: CONFIG_ERROR, EXCHANGE_FAILED)
      if (result.isError && result.content && result.content[0]) {
        const errText = result.content[0].text || JSON.stringify(result.content[0]);
        let errObj;
        try { errObj = JSON.parse(errText); } catch { errObj = { message: errText }; }
        fail(errObj.message || errText);
      }
      // Extrai exchange_result de várias estruturas possíveis do MCP
      function extractExchange(obj) {
        if (!obj) return null;
        if (obj.agent_key) return obj;
        if (obj.exchange_result && obj.exchange_result.agent_key) return obj.exchange_result;
        if (obj.structuredContent) return extractExchange(obj.structuredContent);
        if (obj.content && obj.content[0]) {
          const raw = obj.content[0].text;
          if (typeof raw === 'string') {
            try { return extractExchange(JSON.parse(raw)); } catch { return null; }
          }
        }
        return null;
      }
      const exchangeResult = extractExchange(result);
      if (!exchangeResult || !exchangeResult.agent_key) {
        fail('agent_key não retornado pela tool. Verifique se o MCP possui a tool pairing_exchange configurada.');
      }
      const phoneNumber = exchangeResult.phone_number || null;
      try {
        fs.mkdirSync(SECRETS_DIR, { mode: 0o700, recursive: true });
        fs.chmodSync(path.join(os.homedir(), '.openclaw', 'secrets'), 0o700);
        fs.writeFileSync(AGENT_KEY_FILE, exchangeResult.agent_key.trim(), { mode: 0o600 });
        const baseUrl = (exchangeResult.config?.mcp_base_url || '').trim() || url.origin;
        const env = ENV_ARG || (baseUrl.includes('homolog') ? 'homolog' : baseUrl.includes('ngrok') ? 'local' : 'prod');
        const session = {
          environment: env,
          account_id: exchangeResult.account_id,
          phone_number: phoneNumber,
          mcp_base_url: baseUrl,
          scopes: exchangeResult.scopes || ['balance:read'],
          operator_id: exchangeResult.operator_id,
          agent_id: exchangeResult.agent_id,
          paired_at: new Date().toISOString(),
        };
        fs.writeFileSync(SESSION_FILE, JSON.stringify(session, null, 2), { mode: 0o600 });
      } catch (e) {
        fail(e.message);
      }
      const phone = phoneNumber || exchangeResult.account_id;
      console.log('SETUP_OK');
      console.log('PHONE=' + phone);
      console.log('ENV=' + (ENV_ARG || 'local'));
    });
  }
);
req.on('error', (e) => fail(e.message));
req.write(body);
req.end();
