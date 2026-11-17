// CLI layer: argument parsing, dispatch, envelope printing, exit codes.
// Providers do the network work; this file never talks to the network itself.

import { parseArgs } from 'node:util';
import { envelope, printEnvelope } from './envelope.js';
import { CliError, CODES, invalidArgument } from './errors.js';
import { createHttpClient } from './http.js';
import { resolveLocation } from './geocode.js';
import { createProvider, PROVIDERS } from './providers/index.js';
import { cartAdd, cartPreview, cartSummary, loadCart, clearCart } from './cart.js';

const USAGE = `lieferando-cli — read-only food-delivery discovery for Germany (JSON output)

Usage:
  lieferando-cli search       --address "…" | --postcode NNNNN [--query TEXT] [--open-now] [--limit N]
  lieferando-cli restaurant   <slug> [--address "…" | --postcode NNNNN]
  lieferando-cli menu         <slug> [--category NAME] [--include-options]
  lieferando-cli item         <slug> <item-id>
  lieferando-cli availability --address "…" | --postcode NNNNN
  lieferando-cli cart add     --restaurant <slug> --item <id> [--variant <id>] [--count N] [--options JSON]
  lieferando-cli cart show
  lieferando-cli cart clear
  lieferando-cli cart preview [--address "…" | --postcode NNNNN]
  lieferando-cli providers

Global flags:
  --provider NAME   (default: lieferando)
  --json            compact single-line JSON (output is always JSON)
  --verbose         redacted request trace on stderr
  --help

Safety: this tool is read-only. It cannot log in, place orders, or pay.
The cart is a local simulation; "cart preview" is local arithmetic.`;

const FLAG_SPEC = {
  address: { type: 'string' },
  postcode: { type: 'string' },
  lat: { type: 'string' },
  lng: { type: 'string' },
  query: { type: 'string' },
  category: { type: 'string' },
  'include-options': { type: 'boolean', default: false },
  'open-now': { type: 'boolean', default: false },
  limit: { type: 'string' },
  restaurant: { type: 'string' },
  item: { type: 'string' },
  variant: { type: 'string' },
  count: { type: 'string' },
  options: { type: 'string' },
  provider: { type: 'string', default: 'lieferando' },
  json: { type: 'boolean', default: false },
  verbose: { type: 'boolean', default: false },
  help: { type: 'boolean', default: false },
};

function parseOptionsJson(raw) {
  if (!raw) return {};
  try {
    const parsed = JSON.parse(raw);
    if (parsed === null || typeof parsed !== 'object' || Array.isArray(parsed)) throw new Error('not an object');
    return parsed;
  } catch {
    throw invalidArgument('--options must be a JSON object like {"<group-id>": ["<option-id>"]}.');
  }
}

export async function run(argv, { fetchImpl, stdout = process.stdout } = {}) {
  let values, positionals;
  try {
    ({ values, positionals } = parseArgs({ args: argv, options: FLAG_SPEC, allowPositionals: true, strict: true }));
  } catch (err) {
    return fail('argv', null, invalidArgument(err.message), false, stdout);
  }

  const [command, ...rest] = positionals;
  const compact = values.json;

  if (values.help || !command) {
    process.stderr.write(USAGE + '\n');
    return values.help ? 0 : 2;
  }

  const providerName = values.provider;
  const http = createHttpClient({ fetchImpl, verbose: values.verbose, provider: providerName });

  try {
    if (command === 'providers') {
      return ok(command, null, { providers: PROVIDERS }, compact, stdout);
    }

    const provider = createProvider(providerName, { http });

    switch (command) {
      case 'search': {
        const loc = await resolveLocation(values, { http });
        const limit = values.limit != null ? Number(values.limit) : 25;
        if (!Number.isInteger(limit) || limit < 0) throw invalidArgument('--limit must be a non-negative integer.');
        const data = await provider.searchRestaurants(loc, {
          query: values.query ?? null,
          limit,
          openNow: values['open-now'],
        });
        return ok(command, providerName, data, compact, stdout);
      }
      case 'restaurant': {
        const slug = rest[0];
        if (!slug) throw invalidArgument('Usage: restaurant <slug>');
        const loc = values.address || values.postcode ? await resolveLocation(values, { http }) : null;
        return ok(command, providerName, await provider.getRestaurant(slug, loc), compact, stdout);
      }
      case 'menu': {
        const slug = rest[0];
        if (!slug) throw invalidArgument('Usage: menu <slug>');
        const data = await provider.getMenu(slug, {
          category: values.category ?? null,
          includeOptions: values['include-options'],
        });
        return ok(command, providerName, data, compact, stdout);
      }
      case 'item': {
        const [slug, itemId] = rest;
        if (!slug || !itemId) throw invalidArgument('Usage: item <slug> <item-id>');
        return ok(command, providerName, await provider.getItem(slug, itemId), compact, stdout);
      }
      case 'availability': {
        const loc = await resolveLocation(values, { http });
        return ok(command, providerName, await provider.availability(loc), compact, stdout);
      }
      case 'cart': {
        const sub = rest[0];
        if (sub === 'add') {
          const data = await cartAdd(provider, {
            restaurant: values.restaurant,
            itemId: values.item,
            variantId: values.variant ?? null,
            count: values.count != null ? Number(values.count) : 1,
            options: parseOptionsJson(values.options),
          });
          return ok('cart add', providerName, data, compact, stdout);
        }
        if (sub === 'show') return ok('cart show', providerName, cartSummary(loadCart()), compact, stdout);
        if (sub === 'clear') {
          clearCart();
          return ok('cart clear', providerName, { simulation: true, cleared: true }, compact, stdout);
        }
        if (sub === 'preview') {
          const loc = values.address || values.postcode ? await resolveLocation(values, { http }) : null;
          return ok('cart preview', providerName, await cartPreview(provider, loc), compact, stdout);
        }
        throw invalidArgument('Usage: cart add|show|clear|preview');
      }
      default:
        throw invalidArgument(`Unknown command "${command}". Run with --help.`);
    }
  } catch (err) {
    if (err instanceof CliError) return fail(command, providerName, err, compact, stdout);
    const wrapped = new CliError(CODES.UPSTREAM_ERROR, `Unexpected failure: ${err?.message ?? 'unknown error'}`, {
      provider: providerName,
      retryable: false,
    });
    return fail(command, providerName, wrapped, compact, stdout);
  }
}

function ok(command, provider, data, compact, stream) {
  printEnvelope(envelope({ command, provider, data }), { compact, stream });
  return 0;
}

function fail(command, provider, cliError, compact, stream) {
  printEnvelope(envelope({ command, provider, data: null, error: cliError.toEnvelopeError() }), { compact, stream });
  return cliError.exitCode ?? 1;
}
