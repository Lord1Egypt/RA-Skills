#!/usr/bin/env node
/**
 * Grizzly SMS CLI — OpenClaw exec. Network: only https://api.grizzlysms.com (official API).
 * API key: scripts/grizzly-env.mjs (no fetch there).
 * Usage: node grizzly-cli.mjs <command> [args...]
 * Commands: get_services | get_countries | get_balance | get_prices | get_wallet | request_number | get_status | set_status
 */

/** Official Grizzly SMS API host only — do not substitute from env (moderation / security scanners). */
const GRIZZLY_API_ORIGIN = 'https://api.grizzlysms.com';

async function requestHandlerApi(params, apiKey) {
  const url = new URL('/stubs/handler_api.php', GRIZZLY_API_ORIGIN + '/');
  url.searchParams.set('api_key', apiKey);
  for (const [k, v] of Object.entries(params)) {
    if (v !== undefined && v !== null) url.searchParams.set(k, v);
  }
  const res = await fetch(url.toString());
  const text = await res.text();
  try {
    return JSON.parse(text);
  } catch {
    return text;
  }
}

async function requestWallet(apiKey) {
  const url = new URL('/public/crypto/wallet', GRIZZLY_API_ORIGIN + '/');
  url.searchParams.set('api_key', apiKey);
  url.searchParams.set('coin', 'usdt');
  url.searchParams.set('network', 'tron');
  const res = await fetch(url.toString());
  const text = await res.text();
  try {
    return JSON.parse(text);
  } catch {
    return { wallet_address: null, error: text };
  }
}

const COMMANDS_NEEDING_KEY = new Set([
  'get_services',
  'get_countries',
  'get_balance',
  'get_wallet',
  'get_prices',
  'request_number',
  'get_status',
  'set_status',
]);

async function main() {
  const [cmd, ...args] = process.argv.slice(2);
  let apiKey = null;
  if (COMMANDS_NEEDING_KEY.has(cmd)) {
    const { readGrizzlySmsApiKey } = await import('./grizzly-env.mjs');
    apiKey = readGrizzlySmsApiKey();
  }
  try {
    switch (cmd) {
      case 'get_services': {
        const data = await requestHandlerApi({ action: 'getServicesList' }, apiKey);
        console.log(JSON.stringify(data, null, 2));
        break;
      }
      case 'get_countries': {
        const data = await requestHandlerApi({ action: 'getCountries' }, apiKey);
        console.log(JSON.stringify(data, null, 2));
        break;
      }
      case 'get_balance': {
        const data = await requestHandlerApi({ action: 'getBalance' }, apiKey);
        console.log(typeof data === 'string' ? data : JSON.stringify(data, null, 2));
        break;
      }
      case 'get_wallet': {
        const data = await requestWallet(apiKey);
        console.log(JSON.stringify(data, null, 2));
        break;
      }
      case 'get_prices': {
        const [country, service] = args;
        const params = { action: 'getPrices' };
        if (country) params.country = country;
        if (service) params.service = service;
        const data = await requestHandlerApi(params, apiKey);
        console.log(JSON.stringify(data, null, 2));
        break;
      }
      case 'request_number': {
        const [service, country] = args;
        if (!service) {
          console.error(JSON.stringify({ error: 'service required (e.g. ub, tg, wa)' }));
          process.exit(1);
        }
        const params = { action: 'getNumber', service };
        if (country) params.country = country;
        const data = await requestHandlerApi(params, apiKey);
        console.log(typeof data === 'string' ? data : JSON.stringify(data, null, 2));
        break;
      }
      case 'get_status': {
        const [activationId] = args;
        if (!activationId) {
          console.error(JSON.stringify({ error: 'activationId required' }));
          process.exit(1);
        }
        const data = await requestHandlerApi({ action: 'getStatus', id: activationId }, apiKey);
        console.log(typeof data === 'string' ? data : JSON.stringify(data, null, 2));
        break;
      }
      case 'set_status': {
        const [activationId, status] = args;
        if (!activationId || !status) {
          console.error(JSON.stringify({ error: 'activationId and status required (status: 6=complete, 8=cancel)' }));
          process.exit(1);
        }
        const data = await requestHandlerApi({ action: 'setStatus', id: activationId, status }, apiKey);
        console.log(typeof data === 'string' ? data : JSON.stringify(data, null, 2));
        break;
      }
      default:
        console.error(JSON.stringify({
          error: 'Unknown command',
          usage: 'grizzly-cli.mjs <get_services|get_countries|get_balance|get_prices|get_wallet|request_number|get_status|set_status> [args...]',
          examples: [
            'node grizzly-cli.mjs get_services',
            'node grizzly-cli.mjs get_balance',
            'node grizzly-cli.mjs get_wallet',
            'node grizzly-cli.mjs request_number ub 73',
            'node grizzly-cli.mjs get_status ACTIVATION_ID',
            'node grizzly-cli.mjs set_status ACTIVATION_ID 6',
          ],
        }));
        process.exit(1);
    }
  } catch (err) {
    console.error(JSON.stringify({ error: err.message }));
    process.exit(1);
  }
}

main();
