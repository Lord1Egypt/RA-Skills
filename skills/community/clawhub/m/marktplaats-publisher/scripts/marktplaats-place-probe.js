#!/usr/bin/env node
import { execFileSync } from 'node:child_process';
import { readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import process from 'node:process';

const USER_AGENTS = {
  safari: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_7_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.15',
  chrome: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_7_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
};

function parseArgs(argv) {
  const out = {
    browser: true,
    browserFetch: false,
    json: false,
    save: null,
    url: null,
    cookie: null,
    cookieFile: null,
    header: [],
    bodyLimit: 12000,
    userAgent: 'safari',
    help: false,
    selfTest: false,
  };

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === '--browser') {
      out.browser = true;
      out.browserFetch = false;
    } else if (arg === '--browser-fetch') {
      out.browser = true;
      out.browserFetch = true;
    } else if (arg === '--curl') {
      out.browser = false;
      out.browserFetch = false;
    } else if (arg === '--json') {
      out.json = true;
    } else if (arg === '--help' || arg === '-h') {
      out.help = true;
    } else if (arg === '--save') {
      out.save = argv[++i];
    } else if (arg === '--url') {
      out.url = argv[++i];
    } else if (arg === '--cookie') {
      out.cookie = argv[++i];
    } else if (arg === '--cookie-file') {
      out.cookieFile = argv[++i];
    } else if (arg === '--header') {
      out.header.push(argv[++i]);
    } else if (arg === '--body-limit') {
      out.bodyLimit = Math.max(0, Number(argv[++i] ?? 12000));
    } else if (arg === '--user-agent') {
      out.userAgent = argv[++i] ?? 'safari';
    } else if (arg === '--self-test') {
      out.selfTest = true;
    } else {
      throw new Error(`Unknown argument: ${arg}`);
    }
  }

  return out;
}

function resolveUserAgent(userAgent) {
  if (!userAgent || userAgent === 'safari') return USER_AGENTS.safari;
  if (userAgent === 'chrome') return USER_AGENTS.chrome;
  return userAgent;
}

function loadCookieFile(pathname) {
  if (!pathname) return null;
  const content = readFileSync(resolve(pathname), 'utf8').trim();
  if (!content) return null;
  if (content.includes('=') && content.includes(';')) return content;
  const lines = content.split(/\r?\n/).map((line) => line.trim()).filter(Boolean);
  const cookieLine = lines.find((line) => !line.startsWith('#') && line.includes('\t'));
  if (!cookieLine) return content;
  const parts = cookieLine.split('\t');
  const name = parts.at(-2);
  const value = parts.at(-1);
  return `${name}=${value}`;
}

function isSensitiveField(name) {
  return /(?:xsrf|token|auth|cookie|signature|tmsid|sellername|postcode|email|phone|telephone|address|street)/i.test(String(name || ''));
}

function redactValue(name, value) {
  if (!isSensitiveField(name)) return value ?? '';
  return value ? '[redacted]' : '';
}

function normalizeInputs(inputs) {
  return (Array.isArray(inputs) ? inputs : []).map((input) => ({
    name: input?.name ?? '',
    type: input?.type ?? '',
    value: redactValue(input?.name, input?.value ?? ''),
    checked: Boolean(input?.checked),
    disabled: Boolean(input?.disabled),
    options: Array.isArray(input?.options)
      ? input.options.map((option) => ({
          value: option?.value ?? '',
          text: option?.text ?? '',
          selected: Boolean(option?.selected),
        }))
      : undefined,
  }));
}

function buildFieldMap(inputs) {
  const map = {};
  for (const input of inputs) {
    if (!input.name) continue;
    const value = input.type === 'checkbox' || input.type === 'radio'
      ? input.checked
      : input.value;
    if (Object.hasOwn(map, input.name)) {
      if (Array.isArray(map[input.name])) {
        map[input.name].push(value);
      } else {
        map[input.name] = [map[input.name], value];
      }
    } else {
      map[input.name] = value;
    }
  }
  return map;
}

function normalizeSnapshot(snapshot) {
  const forms = (Array.isArray(snapshot?.forms) ? snapshot.forms : []).map((form) => {
    const inputs = normalizeInputs(form?.inputs);
    return {
      action: form?.action ?? '',
      method: form?.method ?? '',
      id: form?.id ?? '',
      className: form?.className ?? '',
      inputs,
      fieldMap: buildFieldMap(inputs),
    };
  });

  const form = forms[0] ?? null;
  const fieldMap = form?.fieldMap ?? {};

  return {
    source: snapshot?.source ?? 'browser-dom',
    title: snapshot?.title ?? '',
    url: snapshot?.url ?? '',
    forms,
    form: form
      ? {
          action: form.action,
          method: form.method,
          id: form.id,
          className: form.className,
          fields: form.inputs,
        }
      : null,
    fieldMap,
    placeAction: form?.action ?? '',
    hasXsrfToken: Boolean(fieldMap['xsrf.token']),
    selectedBundle: fieldMap.selectedBundle ?? null,
    category: {
      l1: fieldMap.l1 ?? null,
      l2: fieldMap.l2 ?? null,
      bucket: fieldMap.bucket ?? null,
      l2CategoryFullName: fieldMap.l2CategoryFullName ?? null,
    },
    price: {
      typeValue: fieldMap['price.typeValue'] ?? null,
      value: fieldMap['price.value'] ?? null,
      biddingEnabled: fieldMap['price.biddingEnabled'] ?? null,
    },
    deliveryMethod: fieldMap.deliveryMethod ?? null,
    condition: fieldMap['singleSelectAttribute[condition]'] ?? null,
    contactInformation: {
      hasSellerName: Boolean(fieldMap['contactInformation.sellerName']),
      hasPostCode: Boolean(fieldMap['contactInformation.postCode']),
    },
    upload: {
      imageIds: fieldMap['images.ids'] ?? null,
      hasFileInput: form?.inputs.some((input) => input.type === 'file') ?? false,
    },
    shipping: {
      shippingMethods: Array.isArray(fieldMap.shippingMethod) ? fieldMap.shippingMethod : fieldMap.shippingMethod ? [fieldMap.shippingMethod] : [],
      packageSize: fieldMap.packageSize ?? null,
      provider: fieldMap['shippingDetails.provider'] ?? null,
      price: fieldMap['shippingDetails.price'] ?? null,
    },
    raw: {
      source: snapshot?.source ?? 'browser-dom',
      title: snapshot?.title ?? '',
      url: snapshot?.url ?? '',
      forms,
    },
  };
}

function safariProbe() {
  const js = String.raw`
    JSON.stringify((() => {
      const collectInputs = (root) => Array.from(root.querySelectorAll('input, textarea, select')).map((el) => {
        const record = {
          name: el.name || '',
          type: el.type || el.tagName.toLowerCase(),
          value: 'value' in el ? el.value : '',
          checked: Boolean(el.checked),
          disabled: Boolean(el.disabled),
        };
        if (el.tagName === 'SELECT') {
          record.options = Array.from(el.options).map((opt) => ({
            value: opt.value,
            text: opt.text,
            selected: Boolean(opt.selected),
          }));
        }
        return record;
      });

      return {
        source: 'safari-dom',
        title: document.title,
        url: location.href,
        forms: Array.from(document.forms).map((form) => ({
          action: form.action,
          method: form.method,
          id: form.id,
          className: form.className,
          inputs: collectInputs(form),
        })),
      };
    })());
  `;

  const applescript = `tell application "Safari"
    set probeResult to do JavaScript ${JSON.stringify(js)} in front document
    return probeResult
  end tell`;

  const raw = execFileSync('osascript', ['-e', applescript], { encoding: 'utf8' }).trim();
  return JSON.parse(raw);
}

function safariFetchProbe(options) {
  const targetUrl = options.url ?? '';
  const js = String.raw`
    JSON.stringify((() => {
      const target = TARGET_URL || location.href;
      const xhr = new XMLHttpRequest();
      xhr.open('GET', target, false);
      xhr.withCredentials = true;
      xhr.setRequestHeader('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8');
      xhr.send();

      const parser = new DOMParser();
      const doc = parser.parseFromString(xhr.responseText, 'text/html');
      const collectInputs = (root) => Array.from(root.querySelectorAll('input, textarea, select')).map((el) => {
        const record = {
          name: el.name || '',
          type: el.type || el.tagName.toLowerCase(),
          value: 'value' in el ? el.value : '',
          checked: Boolean(el.checked),
          disabled: Boolean(el.disabled),
        };
        if (el.tagName === 'SELECT') {
          record.options = Array.from(el.options).map((opt) => ({
            value: opt.value,
            text: opt.text,
            selected: Boolean(opt.selected),
          }));
        }
        return record;
      });

      return {
        source: 'safari-fetch',
        title: doc.title,
        url: xhr.responseURL || target,
        status: xhr.status,
        ok: xhr.status >= 200 && xhr.status < 300,
        isLoginRedirect: /\/identity\/v2\/login\b/.test(xhr.responseURL || '') || /Inloggen op uw account/i.test(xhr.responseText),
        bodyLength: xhr.responseText.length,
        requestHeaders: {
          'user-agent': navigator.userAgent,
          accept: 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
          credentials: 'include',
        },
        forms: Array.from(doc.forms).map((form) => ({
          action: form.action,
          method: form.method,
          id: form.id,
          className: form.className,
          inputs: collectInputs(form),
        })),
      };
    })());
  `.replace('TARGET_URL', JSON.stringify(targetUrl));

  const applescript = `tell application "Safari"
    set probeResult to do JavaScript ${JSON.stringify(js)} in front document
    return probeResult
  end tell`;

  const raw = execFileSync('osascript', ['-e', applescript], { encoding: 'utf8' }).trim();
  return JSON.parse(raw);
}

async function curlProbe(options) {
  if (!options.url) {
    throw new Error('curl mode requires --url');
  }

  const userAgent = resolveUserAgent(options.userAgent);
  const headers = new Headers({
    'User-Agent': userAgent,
    Accept: 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    ...Object.fromEntries(options.header.map((value) => {
      const idx = value.indexOf(':');
      if (idx === -1) return [value, ''];
      return [value.slice(0, idx).trim(), value.slice(idx + 1).trim()];
    })),
  });

  const cookie = options.cookie ?? loadCookieFile(options.cookieFile);
  if (cookie) {
    headers.set('Cookie', cookie);
  }

  const response = await fetch(options.url, {
    redirect: 'follow',
    headers,
  });
  const body = await response.text();
  const isLoginRedirect = /\/identity\/v2\/login\b/.test(response.url) || /Inloggen op uw account/i.test(body);
  const bodyLimit = Number.isFinite(options.bodyLimit) ? options.bodyLimit : 12000;
  const bodyPreview = bodyLimit === 0 ? '' : body.slice(0, bodyLimit);
  return {
    source: 'curl',
    url: response.url,
    status: response.status,
    ok: response.ok,
    isLoginRedirect,
    requestHeaders: {
      'user-agent': userAgent,
      accept: headers.get('Accept'),
    },
    headers: Object.fromEntries(response.headers.entries()),
    body: bodyPreview,
    bodyTruncated: bodyPreview.length < body.length,
    bodyLength: body.length,
  };
}

function printHelp() {
  console.log(`Usage:
  marktplaats-place-probe [--browser] [--json] [--save PATH]
  marktplaats-place-probe --browser-fetch [--url URL] [--json] [--save PATH]
  marktplaats-place-probe --curl --url URL [--cookie STRING | --cookie-file PATH] [--header NAME:VALUE]

Options:
  --browser            Read the live place page from the active Safari tab (default)
  --browser-fetch      Fetch a same-origin page inside Safari with its logged-in session
  --curl               Fetch the given URL with fetch/curl-style headers
  --url URL            URL to fetch in curl mode
  --cookie STRING       Raw Cookie header for curl mode
  --cookie-file PATH    File with a raw Cookie header or Netscape cookie export
  --header NAME:VALUE   Extra request header (repeatable)
  --user-agent VALUE    "safari", "chrome", or a custom UA string (default safari)
  --body-limit N       Max body chars to keep in curl mode (default 12000)
  --json               Emit JSON only
  --save PATH          Write the JSON snapshot to a file
  --self-test          Run a deterministic normalizer test
  -h, --help           Show this help
`);
}

function selfTest() {
  const sample = {
    source: 'safari-dom',
    title: '≥ Marktplaats - De plek om nieuwe en tweedehands spullen te kopen en verkopen',
    url: 'https://www.marktplaats.nl/plaats/31/1453?bucketId=12&title=Neomounts%20FPMA-W500%20monitor%2Ftv%20wandbeugel',
    forms: [
      {
        action: 'https://www.marktplaats.nl/plaats/ads',
        method: 'post',
        id: 'syi-form',
        className: '',
        inputs: [
          { name: 'images.ids', type: 'hidden', value: '', checked: false },
          { name: 'title_nl-NL', type: 'text', value: 'Neomounts FPMA-W500 monitor/tv wandbeugel', checked: false },
          { name: 'xsrf.token', type: 'hidden', value: 'fixture-sensitive-value', checked: false },
          { name: 'l1', type: 'hidden', value: '31', checked: false },
          { name: 'l2', type: 'hidden', value: '1453', checked: false },
          { name: 'bucket', type: 'hidden', value: '12', checked: false },
          { name: 'l2CategoryFullName', type: 'hidden', value: 'Televisiebeugels', checked: false },
          { name: 'selectedBundle', type: 'hidden', value: '', checked: false },
          { name: 'deliveryMethod', type: 'radio', value: 'Ophalen of Verzenden', checked: true },
          { name: 'shippingMethod', type: 'checkbox', value: 'postnl', checked: true },
        ],
      },
    ],
  };
  const normalized = normalizeSnapshot(sample);
  if (normalized.placeAction !== 'https://www.marktplaats.nl/plaats/ads') {
    throw new Error('self-test failed: placeAction');
  }
  if (normalized.category.l2 !== '1453' || normalized.category.bucket !== '12') {
    throw new Error('self-test failed: category');
  }
  if (normalized.hasXsrfToken !== true) {
    throw new Error('self-test failed: xsrf token');
  }
  if (normalized.fieldMap['xsrf.token'] !== '[redacted]') {
    throw new Error('self-test failed: xsrf redaction');
  }
  if (normalized.upload.hasFileInput !== false) {
    throw new Error('self-test failed: upload');
  }
  console.log('self-test ok');
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    printHelp();
    return;
  }
  if (args.selfTest) {
    selfTest();
    return;
  }

  let result;
  if (args.browserFetch) {
    result = normalizeSnapshot(safariFetchProbe(args));
  } else if (args.browser) {
    result = normalizeSnapshot(safariProbe());
  } else {
    result = await curlProbe(args);
  }

  if (args.save) {
    writeFileSync(resolve(args.save), `${JSON.stringify(result, null, 2)}\n`);
  }

  if (args.json || args.save) {
    console.log(JSON.stringify(result, null, 2));
    return;
  }

  console.log(`source: ${result.source}`);
  console.log(`title: ${result.title}`);
  console.log(`url: ${result.url}`);
  if (result.placeAction) console.log(`form action: ${result.placeAction}`);
  if (result.hasXsrfToken) console.log('xsrf token: [redacted]');
  if (result.isLoginRedirect) console.log('login redirect: yes');
  if (result.category?.l1 || result.category?.l2 || result.category?.bucket) {
    console.log(`category: l1=${result.category.l1} l2=${result.category.l2} bucket=${result.category.bucket}`);
  }
  if (result.selectedBundle != null) console.log(`selected bundle: ${result.selectedBundle || '(empty)'}`);
  if (result.upload?.hasFileInput != null) console.log(`upload file input: ${result.upload.hasFileInput ? 'yes' : 'no'}`);
  if (result.form?.fields?.length) console.log(`fields: ${result.form.fields.length}`);
}

main().catch((error) => {
  console.error(error?.stack || error?.message || String(error));
  process.exitCode = 1;
});
