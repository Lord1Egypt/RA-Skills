#!/usr/bin/env node
// Extracts OpenTable's `window.__INITIAL_STATE__` (or the equivalent
// `"__INITIAL_STATE__":{...}` embedded-JSON form) from an SSR HTML page and
// prints the parsed object as JSON on stdout, ready to pipe into `jq`.
//
// Same two marker forms opentable-mcp's src/initial-state.ts looks for —
// OpenTable serves either depending on the page/hydration state. Uses a
// balanced-brace, string-aware walk (a regex can't safely match nested
// JSON), same technique as the shared `extractJsonAfterMarker` helper the
// MCP itself uses.
//
// Usage:
//   fpx get 'https://www.opentable.com/user/dining-dashboard' -p opentable \
//     | node extract-initial-state.mjs | jq '.diningDashboard.upcomingReservations'

const html = await new Promise((resolve, reject) => {
  let data = '';
  process.stdin.setEncoding('utf8');
  process.stdin.on('data', (chunk) => (data += chunk));
  process.stdin.on('end', () => resolve(data));
  process.stdin.on('error', reject);
});

const markers = ['window.__INITIAL_STATE__', '"__INITIAL_STATE__"'];
let markerIdx = -1;
let marker = '';
for (const m of markers) {
  const i = html.indexOf(m);
  if (i !== -1) {
    markerIdx = i;
    marker = m;
    break;
  }
}
if (markerIdx === -1) {
  console.error(
    '__INITIAL_STATE__ marker not found — is this real SSR HTML (not a sign-in redirect or an error page)?'
  );
  process.exit(1);
}

const braceStart = html.indexOf('{', markerIdx + marker.length);
if (braceStart === -1) {
  console.error('no { found after the __INITIAL_STATE__ marker');
  process.exit(1);
}

let depth = 0;
let inString = false;
let escaped = false;
let end = -1;
for (let i = braceStart; i < html.length; i++) {
  const c = html[i];
  if (inString) {
    if (escaped) escaped = false;
    else if (c === '\\') escaped = true;
    else if (c === '"') inString = false;
    continue;
  }
  if (c === '"') {
    inString = true;
    continue;
  }
  if (c === '{') depth++;
  else if (c === '}') {
    depth--;
    if (depth === 0) {
      end = i + 1;
      break;
    }
  }
}
if (end === -1) {
  console.error('unbalanced braces after __INITIAL_STATE__ — HTML may be truncated');
  process.exit(1);
}

const jsonText = html.slice(braceStart, end);
try {
  const state = JSON.parse(jsonText);
  process.stdout.write(JSON.stringify(state));
} catch (e) {
  console.error(`JSON.parse failed: ${e.message}`);
  process.exit(1);
}
