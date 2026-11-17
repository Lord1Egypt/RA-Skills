#!/usr/bin/env node
/**
 * pw-browser — Playwright-based browser automation CLI.
 * Uses a simple daemon (HTTP server) to keep the browser alive across commands.
 *
 * Usage:
 *   node pw-browser.js daemon            — start daemon (keeps browser alive)
 *   node pw-browser.js <command> [args]  — execute command against running daemon
 */

const http = require('http');
const fs = require('fs');
const path = require('path');
const os = require('os');
const vm = require('vm');
const crypto = require('crypto');

// ---- Config ----
const STATE_DIR = path.join(os.homedir(), '.pw-browser');
// Daemon listen port. Override with PW_BROWSER_PORT. On startup we probe the
// port: if a daemon already answers /health there we exit (don't double-start);
// if the port is occupied by something else we auto-increment until free.
let DAEMON_PORT = Number(process.env.PW_BROWSER_PORT) || 19223;
const DAEMON_HOST = '127.0.0.1';

let JSON_OUTPUT = false;

// SECURITY: STATE_DIR holds the daemon auth token and (optionally) exported
// session credentials. Create it 0700 and best-effort tighten it if it already
// exists with looser bits, so other local users cannot enumerate or read it.
// (POSIX only — on Windows the mode argument is ignored by the OS; ACL
// inheritance from the user profile dir applies instead.)
function ensureDir() {
  if (!fs.existsSync(STATE_DIR)) fs.mkdirSync(STATE_DIR, { recursive: true, mode: 0o700 });
  try { fs.chmodSync(STATE_DIR, 0o700); } catch (_) {}
}

// SECURITY: write a file that contains secrets (auth token / session cookies /
// localStorage dumps) with owner-only permissions. writeFileSync's `mode` only
// applies when the file is CREATED, so an explicit chmod follows to also fix
// pre-existing files that were written by an older version as 0644.
function writeSecretFile(fp, data) {
  fs.writeFileSync(fp, data, { mode: 0o600 });
  try { fs.chmodSync(fp, 0o600); } catch (_) {}
}

// SECURITY: turn an attacker-controlled download filename into a safe
// in-directory target, or report traversal. The "suggested filename" of a
// download is chosen by the WEB PAGE being automated, not by the operator — a
// malicious site can return "../../.bashrc" and, when `dest` is a directory,
// path.join would write the file OUTSIDE the intended directory (e.g.
// overwriting a dotfile in $HOME). We strip every path component down to a bare
// basename and then assert the resolved target still lives inside dest.
// Module-scoped (not inside runDaemon) so it can be unit-tested without a
// browser. Returns { path } or { error }.
function safeDownloadTarget(dest, suggested) {
  const base = path.basename(suggested || '');
  const resolvedDest = path.resolve(dest);
  if (base === '') {
    return { error: { kind: 'PathTraversal', message: 'Refusing to save download: the suggested filename is empty, which would escape the destination directory.' } };
  }
  const target = path.join(resolvedDest, base);
  const resolvedTarget = path.resolve(target);
  if (resolvedTarget !== resolvedDest && !resolvedTarget.startsWith(resolvedDest + path.sep)) {
    return { error: { kind: 'PathTraversal', message: `Refusing to save download: filename "${suggested}" escapes the destination directory.` } };
  }
  return { path: target };
}

// SECURITY: constant-time token comparison so a local attacker probing the
// daemon cannot mine the 48-hex-char auth token via timing differences. The
// raw `provided !== daemonToken` short-circuits and leaks length/position —
// negligible against a 24-byte random token, but free to get right.
function timingSafeToken(provided, expected) {
  const a = Buffer.from(String(provided));
  const b = Buffer.from(String(expected));
  if (a.length !== b.length) return false;
  return crypto.timingSafeEqual(a, b);
}

// ===================== DAEMON MODE =====================
async function runDaemon() {
  const { chromium } = require('playwright-core');

  ensureDir();
  console.log(`[daemon] Starting pw-browser daemon on ${DAEMON_HOST}:${DAEMON_PORT}`);

  let browser = null;
  let context = null;
  let page = null;

  // Daemon lifecycle — idle auto-exit so a browser/Chrome window never lingers
  // after the caller is done. Configurable via PW_BROWSER_IDLE_MS (0 disables).
  // inFlight guards against exiting mid-command.
  let lastActivity = Date.now();
  let inFlight = 0;
  const IDLE_MS = (() => {
    const v = Number(process.env.PW_BROWSER_IDLE_MS);
    return Number.isFinite(v) && v > 0 ? v : 15 * 60 * 1000; // default 15 min
  })();

  // Snapshot size cap: a full querySelectorAll('*') over a very large DOM
  // (tens of thousands of nodes) can be slow / memory-heavy. Cap the number of
  // collected interactive elements; once exceeded we stop collecting and flag
  // `truncated` so a caller can re-narrow (e.g. by interacting) instead of
  // OOM-ing on a giant page. Tune via PW_BROWSER_SNAP_LIMIT (0 = no cap, but
  // that still walks the whole tree).
  const SNAP_LIMIT = (() => {
    const v = Number(process.env.PW_BROWSER_SNAP_LIMIT);
    if (v === 0) return Number.MAX_SAFE_INTEGER; // 0 explicitly disables the cap
    return Number.isFinite(v) && v > 0 ? v : 3000;
  })();
  if (process.argv[2] === 'daemon') console.error(`[daemon] Snapshot cap SNAP_LIMIT=${SNAP_LIMIT} (PW_BROWSER_SNAP_LIMIT)`);

  // SECURITY: per-daemon random token + optional safe mode.
  // The token is generated once at daemon start and written to daemon.json
  // (readable only by the local user). Every command route except /health
  // must present it, closing the "unauthenticated HTTP daemon = RCE surface" gap.
  const SAFE_MODE = process.env.PW_BROWSER_SAFE_MODE === '1' || process.env.PW_BROWSER_SAFE_MODE === 'true';
  const daemonToken = crypto.randomBytes(24).toString('hex');

  // SECURITY: cookies/storage export/import move live session credentials
  // (auth cookies, bearer/session tokens, CSRF tokens) to/from the filesystem.
  // These paths are confined to STATE_DIR so a caller cannot silently scatter
  // secrets across the disk or load attacker-planted state from arbitrary paths.
  //
  // PRIVILEGE SEPARATION (v1.3.8): the confinement must NOT be waivable by the
  // party it constrains. Previously `--unsafe` alone lifted it — but --unsafe is
  // supplied by the *caller* (possibly an untrusted/compromised agent), so the
  // guard could be disabled by the very actor it was meant to contain. That is a
  // privilege-escalation path, not a guard. Escaping confinement now requires
  // BOTH:
  //   1. the operator starting the daemon with
  //      PW_BROWSER_ALLOW_UNSAFE_CRED_PATH=1   (process env — a caller sending
  //      HTTP commands cannot set it), and
  //   2. the caller explicitly passing --unsafe (intent, not authority).
  // Without (1), --unsafe is rejected outright. Every credential-path access is
  // logged to the daemon's stderr as an audit trail.
  const ALLOW_UNSAFE_CRED_PATH = process.env.PW_BROWSER_ALLOW_UNSAFE_CRED_PATH === '1' ||
    process.env.PW_BROWSER_ALLOW_UNSAFE_CRED_PATH === 'true';
  if (process.argv[2] === 'daemon' && ALLOW_UNSAFE_CRED_PATH) {
    console.error('[daemon] WARNING: PW_BROWSER_ALLOW_UNSAFE_CRED_PATH=1 — callers may read/write credential files OUTSIDE ' + STATE_DIR + ' via --unsafe. Only enable this for trusted, non-agent-driven use.');
  }
  const CRED_WARNING = 'SECURITY: this file holds live session credentials (cookies / auth tokens). Treat it like a password — never commit, upload, or share it; delete it when done; restore only on your own machine and for the same site. The file is written 0600 (owner-only) on POSIX.';

  // SECURITY (v1.3.9): operator-level kill switch for credential PERSISTENCE.
  // Docs long advised "don't persist credentials to disk in automated flows",
  // but that was advice only — any caller could still `cookies export`. This
  // makes it enforceable and, crucially, finer-grained than SAFE_MODE:
  //   SAFE_MODE=1                -> ALL cookies/storage subcommands blocked
  //   PW_BROWSER_CRED_PERSIST=off-> only export/import blocked; list/get/set/
  //                                 clear still work (in-memory session use)
  // Rationale: the rogue-agent risk is dominated by session state reaching the
  // filesystem, where it survives the daemon and becomes a reusable identity.
  // Blocking just that keeps normal automation usable while removing the
  // privilege-persistence primitive. Env-gated, so a caller cannot lift it.
  const CRED_PERSIST = !(/^(off|0|false|no)$/i).test(String(process.env.PW_BROWSER_CRED_PERSIST || ''));
  if (process.argv[2] === 'daemon' && !CRED_PERSIST) {
    console.error('[daemon] PW_BROWSER_CRED_PERSIST=off — cookies/storage export & import are DISABLED (no credential persistence to disk). In-memory list/get/set/clear remain available.');
  }
  function credPersistBlocked(kind) {
    return { ok: false, error: { kind: 'CredentialPersistenceDisabled', message: `${kind} is disabled: the operator started this daemon with PW_BROWSER_CRED_PERSIST=off, which forbids writing session credentials to disk or restoring them from disk. In-memory cookies/storage commands still work.` } };
  }

  // Resolve symlinks on the deepest existing ancestor, so a symlink planted
  // inside STATE_DIR (e.g. ~/.pw-browser/out -> /tmp) cannot be used to escape
  // the confinement check. Non-existent leaf segments are appended verbatim.
  function realpathish(p) {
    let cur = path.resolve(p);
    const tail = [];
    for (;;) {
      try { return path.join(fs.realpathSync(cur), ...tail.slice().reverse()); } catch (_) {}
      const parent = path.dirname(cur);
      if (parent === cur) return path.resolve(p);
      tail.push(path.basename(cur));
      cur = parent;
    }
  }

  function resolveCredPath(raw, defaultName, params, op) {
    const target = raw || path.join(STATE_DIR, defaultName);
    const root = realpathish(STATE_DIR);
    const abs = realpathish(target);
    const inside = abs === root || abs.startsWith(root + path.sep);
    const wantsUnsafe = params.unsafe === 'true' || params.unsafe === true;
    const label = op || 'access';

    if (inside) {
      console.error(`[daemon] AUDIT credential ${label}: ${abs}`);
      return { path: abs };
    }
    if (!wantsUnsafe) {
      console.error(`[daemon] AUDIT credential ${label} DENIED (outside state dir): ${abs}`);
      return {
        error: {
          kind: 'CredentialPathConfined',
          message: `Refusing to ${label} credentials at a path outside ${root}. This file would hold live session secrets. Keep credential files inside the state directory; if an operator has explicitly enabled PW_BROWSER_ALLOW_UNSAFE_CRED_PATH=1 on the daemon, --unsafe may be used to override.`,
        },
      };
    }
    if (!ALLOW_UNSAFE_CRED_PATH) {
      console.error(`[daemon] AUDIT credential ${label} DENIED (--unsafe not permitted by operator): ${abs}`);
      return {
        error: {
          kind: 'UnsafeOverrideNotPermitted',
          message: `--unsafe cannot lift credential path confinement: the override is operator-controlled, not caller-controlled. The daemon was started without PW_BROWSER_ALLOW_UNSAFE_CRED_PATH=1, so credential files must stay inside ${root}. Restart the daemon with that variable set only if you (a human operator) intend to allow secrets to be written outside the state directory.`,
        },
      };
    }
    console.error(`[daemon] AUDIT credential ${label} OUTSIDE state dir (operator-enabled via PW_BROWSER_ALLOW_UNSAFE_CRED_PATH): ${abs}`);
    return { path: abs, escapedConfinement: true };
  }

  async function ensurePage() {
    if (page && !page.isClosed()) return page;
    if (!browser || !browser.isConnected()) {
      const launchOpts = { headless: false, channel: undefined, executablePath: undefined };

      // Priority: system Chrome/Edge > ms-playwright Chromium
      const channelCandidates = ['chrome', 'msedge'];

      // Platform-specific browser path candidates
      const plat = process.platform;
      let pathCandidates;
      if (plat === 'win32') {
        pathCandidates = [
          'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
          'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',
          'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
          'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe',
          path.join(os.homedir(), 'AppData', 'Local', 'ms-playwright', 'chromium-1228', 'chrome-win64', 'chrome.exe'),
          path.join(os.homedir(), 'AppData', 'Local', 'ms-playwright', 'chromium-1226', 'chrome-win64', 'chrome.exe'),
        ];
      } else if (plat === 'darwin') {
        pathCandidates = [
          '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
          '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
          '/Applications/Chromium.app/Contents/MacOS/Chromium',
          path.join(os.homedir(), 'Library', 'Caches', 'ms-playwright', 'chromium-1228', 'chrome-mac', 'Chromium.app', 'Contents', 'MacOS', 'Chromium'),
          path.join(os.homedir(), 'Library', 'Caches', 'ms-playwright', 'chromium-1226', 'chrome-mac', 'Chromium.app', 'Contents', 'MacOS', 'Chromium'),
        ];
      } else {
        // Linux / other Unix
        pathCandidates = [
          '/usr/bin/google-chrome',
          '/usr/bin/google-chrome-stable',
          '/usr/bin/microsoft-edge',
          '/usr/bin/microsoft-edge-stable',
          '/usr/bin/chromium-browser',
          '/usr/bin/chromium',
          '/snap/bin/chromium',
          path.join(os.homedir(), '.cache', 'ms-playwright', 'chromium-1228', 'chrome-linux', 'chrome'),
          path.join(os.homedir(), '.cache', 'ms-playwright', 'chromium-1226', 'chrome-linux', 'chrome'),
        ];
      }

      let launched = false;

      // Try Playwright channel first (uses system Chrome/Edge discovery)
      for (const ch of channelCandidates) {
        try {
          console.error(`[daemon] Trying channel: ${ch}`);
          browser = await chromium.launch({ headless: false, channel: ch });
          console.error(`[daemon] Launched via channel: ${ch}`);
          launched = true;
          break;
        } catch (e) {
          console.error(`[daemon] Channel ${ch} failed: ${e.message.split('\n')[0]}`);
        }
      }

      // Fallback: explicit path
      if (!launched) {
        for (const p of pathCandidates) {
          if (fs.existsSync(p)) {
            try {
              console.error(`[daemon] Trying path: ${p}`);
              browser = await chromium.launch({ headless: false, executablePath: p });
              console.error(`[daemon] Launched: ${p}`);
              launched = true;
              break;
            } catch (e) {
              console.error(`[daemon] Path ${p} failed: ${e.message.split('\n')[0]}`);
            }
          }
        }
      }

      if (!launched) {
        throw new Error('No browser available. Install Chrome/Edge or run: npx playwright install chromium');
      }
      context = await browser.newContext();
    }
    const pages = context.pages().filter(p => !p.isClosed());
    page = pages[0] || await context.newPage();
    return page;
  }

  // Snapshot helpers — stable refs across snaps (improvement A)
  let refSeq = 0;                 // monotonic ref allocator (never reused)
  const refByKey = new Map();     // stableKey -> ref  (persists across snaps)
  const keyLastSeen = new Map();  // stableKey -> last-seen ts (GC bookkeeping, A)
  const refMap = new Map();       // ref -> element info (rebuilt each snap)
  let cachedSnap = null;          // Last snapshot result, used by click/fill etc.
  let cachedHashes = new Set();   // branch_path_hash set of last snap (change detection, C)
  const opHistory = [];           // operation history (improvement D)

  // Stable key for an element: semantic identity when text/placeholder/aria is
  // present, otherwise fall back to its branch-path hash (position in the tree).
  // This mirrors browser-use's selector_map + branch_path_hash idea: the same
  // logical element keeps the same ref across snaps.
  function semKeyOf(el) {
    const text = el.text || '';
    const ph = el.placeholder || '';
    const al = el.ariaLabel || '';
    if (text || ph || al) return `t:${el.tag}|${text}|${ph}|${al}`;
    return `p:${el.tag}|${el.branchPathHash}`;
  }

  // stableKey = semantic identity + occurrence index. The index disambiguates
  // same-named elements (e.g. two "提交" buttons) so each keeps its own ref,
  // while identical structure still maps to the same ref across snaps.
  function stableKeyFor(el, occ = 1) { return `${semKeyOf(el)}#${occ}`; }

  function allocRef(el, occ = 1) {
    const key = stableKeyFor(el, occ);
    if (refByKey.has(key)) { keyLastSeen.set(key, Date.now()); return refByKey.get(key); }
    const ref = `e${++refSeq}`;
    refByKey.set(key, ref);
    keyLastSeen.set(key, Date.now());
    return ref;
  }

  async function buildSnapshot(p) {
    refMap.clear();
    const data = await p.evaluate(({ limit: SNAP_LIMIT }) => {
      if (typeof SNAP_LIMIT !== 'number' || !isFinite(SNAP_LIMIT)) { SNAP_LIMIT = 3000; }
      function xpathOf(el) {
        if (!el || el.nodeType !== 1) return '';
        let path = ''; let node = el;
        while (node && node.nodeType === 1 && node.nodeName.toLowerCase() !== 'html') {
          let idx = 1; let sib = node.previousElementSibling;
          while (sib) { if (sib.nodeName === node.nodeName) idx++; sib = sib.previousElementSibling; }
          path = `/${node.nodeName.toLowerCase()}[${idx}]${path}`;
          node = node.parentElement;
        }
        return `/html${path}`;
      }
      const hashStr = (s) => {
        let h = 0;
        for (let i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) >>> 0;
        return h.toString(16).padStart(8, '0');
      };
      // CSS path that pierces open shadow roots via ' >>> ' (Playwright syntax)
      // only at shadow boundaries; plain ' > ' elsewhere. The iframe boundary is
      // tracked separately in frameChain and handled by frameLocator.
      function cssPathInDoc(el) {
        const segs = [];
        let node = el;
        while (node && node.nodeType === 1) {
          const root = node.getRootNode();
          let idx = 1; let sib = node.previousElementSibling;
          while (sib) { if (sib.nodeName === node.nodeName) idx++; sib = sib.previousElementSibling; }
          const step = `${node.nodeName.toLowerCase()}:nth-of-type(${idx})`;
          if (root.nodeType === 11 && root.host) {
            segs.unshift({ step, pierce: true });
            node = root.host;
          } else {
            segs.unshift({ step, pierce: false });
            if (node.parentElement) node = node.parentElement; else break;
          }
        }
        let out = segs[0].step;
        for (let i = 1; i < segs.length; i++) out += (segs[i].pierce ? ' >>> ' : ' > ') + segs[i].step;
        return out;
      }
      function iframeSel(f, idx) {
        if (f.id) return `iframe#${CSS.escape(f.id)}`;
        if (f.name) return `iframe[name="${f.name}"]`;
        return `iframe >> nth=${idx}`;
      }
      const sel = 'button, a, input, textarea, select, [role="button"], [role="link"], [role="textbox"], [role="checkbox"], [role="combobox"], [role="tab"], [role="menuitem"], [contenteditable="true"]';
      const out = [];
      let truncated = false;
      function walk(root, frameChain, inShadow) {
        if (truncated) return;
        // Walk EVERY element (not just interactive ones): an interactive element
        // can live inside the shadow root of a non-interactive host, so we must
        // recurse into shadow roots of all elements, and collect those matching sel.
        const all = root.querySelectorAll('*');
        for (let i = 0; i < all.length; i++) {
          if (out.length >= SNAP_LIMIT) { truncated = true; return; }
          const el = all[i];
          if (el.matches(sel)) {
            const rect = el.getBoundingClientRect();
            if (rect.width > 0 && rect.height > 0) {
              const tag = el.tagName.toLowerCase();
              const text = (el.textContent || el.value || el.placeholder || '').trim().slice(0, 80);
              const xpath = xpathOf(el);
              out.push({
                tag, text, id: el.id || '', type: el.type || '', placeholder: el.placeholder || '',
                ariaLabel: el.getAttribute('aria-label') || '', xpath,
                branchPathHash: hashStr(xpath),
                frameChain, inShadow: !!inShadow, cssPath: cssPathInDoc(el),
                rect: { x: Math.round(rect.x), y: Math.round(rect.y), w: Math.round(rect.width), h: Math.round(rect.height) }
              });
            }
          }
          // Recurse into shadow DOM (open roots only; closed roots are skipped)
          if (el.shadowRoot) walk(el.shadowRoot, frameChain, true);
        }
        if (truncated) return;
        // Recurse into same-origin iframes (cross-origin throws → skip)
        root.querySelectorAll('iframe').forEach((f, idx) => {
          try {
            const fd = f.contentDocument;
            if (fd && fd.documentElement) {
              walk(fd, frameChain.concat([{ sel: iframeSel(f, idx) }]), false);
            }
          } catch (_) { /* cross-origin iframe — not accessible */ }
        });
      }
      walk(document, [], false);
      return { elements: out, truncated };
    }, { limit: SNAP_LIMIT });
    const domElements = data.elements;
    const truncated = data.truncated;

    const lines = [];
    lines.push(`- Snapshot @ ${new Date().toISOString()}`);
    lines.push(`  url: ${p.url()}`);
    lines.push(`  title: ${await p.title()}`);
    if (truncated) {
      lines.push(`  ⚠ snapshot truncated: only the first ${SNAP_LIMIT} interactive elements were captured (the page has more). Raise PW_BROWSER_SNAP_LIMIT to capture more, or interact to narrow the page.`);
    }

    const seenHashes = new Set();
    const occCount = {};
    domElements.forEach((el) => {
      const sk = semKeyOf(el);
      occCount[sk] = (occCount[sk] || 0) + 1;
      const occ = occCount[sk];
      const ref = allocRef(el, occ);
      keyLastSeen.set(stableKeyFor(el, occ), Date.now());
      seenHashes.add(el.branchPathHash);
      const label = el.text || el.placeholder || el.ariaLabel || el.type || el.tag;
      lines.push(`  [${ref}] ${el.tag} ${label}${el.type ? ' type=' + el.type : ''}${el.placeholder ? ' placeholder="' + el.placeholder + '"' : ''}`);
      refMap.set(ref, {
        role: el.tag, name: label, tag: el.tag, text: el.text, type: el.type, placeholder: el.placeholder,
        ariaLabel: el.ariaLabel, id: el.id, xpath: el.xpath, branchPathHash: el.branchPathHash, rect: el.rect,
        frameChain: el.frameChain, inShadow: el.inShadow, cssPath: el.cssPath
      });
    });

    // GC stale keys not seen for 5 min (keeps refByKey bounded)
    const now = Date.now();
    for (const [k, t] of keyLastSeen) { if (now - t > 300000) { refByKey.delete(k); keyLastSeen.delete(k); } }

    cachedHashes = seenHashes;
    const result = { text: lines.join('\n'), refMap: new Map(refMap), truncated };
    cachedSnap = result;  // Cache for click/fill findElement
    return result;
  }

  // Serialize a snapshot for JSON: the internal refMap is a Map (used by
  // findElement); convert it to a plain object so structured/AI consumers get
  // real per-ref data instead of an empty `{}`.
  function serializeSnap(snap) {
    const refObj = {};
    for (const [k, v] of snap.refMap) refObj[k] = v;
    return { text: snap.text, refMap: refObj, truncated: !!snap.truncated };
  }

  // (flattenAXTree removed — snapshot now uses a DOM registry with stable refs)

  // Locate an element via Playwright. For shadow-DOM / iframe elements this
  // uses the stored cssPath with FrameLocator chaining; for main-document
  // elements it is equivalent to p.locator('css=...').
  async function resolveLocator(p, info) {
    if (info.frameChain && info.frameChain.length) {
      let loc = p.frameLocator(info.frameChain[0].sel);
      for (let i = 1; i < info.frameChain.length; i++) loc = loc.frameLocator(info.frameChain[i].sel);
      return loc.locator(`css=${info.cssPath}`);
    }
    return p.locator(`css=${info.cssPath}`);
  }

  // Shared "find element or return a structured not-found error" used by both
  // the command switch and executeSingle — removes duplicated find+null checks.
  // Always carries an explicit `ok` flag so /act result entries are uniform
  // (both command routes and act consumers can rely on `result.ok`).
  async function resolveRef(p, ref) {
    const el = await findElement(p, ref);
    if (!el) return { ok: false, error: { kind: 'ElementNotFound', message: `Element ${ref} not found` } };
    return { el };
  }

  // Element finder — uses last cached snapshot (from explicit `snap` command)
  async function findElement(p, ref) {
    if (!cachedSnap) await buildSnapshot(p);
    const info = cachedSnap.refMap.get(ref);
    if (!info) return null;

    // Strategy 0b (NEW): CSS path that pierces open shadow roots (' >>> ') and,
    // via frameLocator, reaches into same-origin iframes. This addresses
    // elements the main-document xpath (Strategy 0) cannot reach.
    if (info.cssPath) {
      try {
        const loc = await resolveLocator(p, info);
        if (await loc.count() > 0) return loc.first();
      } catch (e) { /* fall through to other strategies */ }
    }

    // Strategy 0: precise xpath from the snapshot registry. Main-document
    // elements only (xpath cannot cross shadow/iframe boundaries).
    if (info.xpath && !info.inShadow && (!info.frameChain || info.frameChain.length === 0)) {
      try {
        const loc = p.locator(`xpath=${info.xpath}`);
        if (await loc.count() > 0) return loc.first();
      } catch (e) { /* fall through to semantic strategies */ }
    }

    // Map AX roles to Playwright roles
    const roleMap = {
      'textarea': 'textbox',
      'textbox': 'textbox',
      'button': 'button',
      'link': 'link',
      'img': 'img',
      'heading': 'heading',
      'checkbox': 'checkbox',
      'combobox': 'combobox',
      'listbox': 'listbox',
      'option': 'option',
      'tab': 'tab',
      'menuitem': 'menuitem',
      'a': 'link',
      'input': 'textbox',
      'select': 'combobox',
    };
    const pwRole = roleMap[info.role] || info.role;

    // Strategy 1+2: getByRole — try with name first (if available and short),
    // then fall back to role-only. Merged into a single query to avoid the
    // double Playwright locator construction when name is absent or long.
    if (pwRole && pwRole !== 'unknown' && pwRole !== 'generic') {
      try {
        const hasName = info.name && info.name.length < 100;
        const loc = hasName ? p.getByRole(pwRole, { name: info.name }) : p.getByRole(pwRole);
        const count = await loc.count();
        if (count > 0) return loc.first();
      } catch (e) { /* ignore */ }
    }

    // Strategy 3: getByText
    if (info.name) {
      try {
        const loc = p.getByText(info.name, { exact: true });
        const count = await loc.count();
        if (count > 0) return loc.first();
      } catch (e) { /* ignore */ }
    }

    // Strategy 4: CSS attribute selectors for form inputs (handles type=search etc.)
    if (info.tag === 'input' || info.tag === 'textarea' || info.role === 'textbox') {
      try {
        const selectors = ['input[type="search"]', 'input[type="text"]', 'input[type="email"]',
          'input[type="url"]', 'input[type="tel"]', 'input:not([type])',
          '[role="searchbox"]', 'textarea', '[role="textbox"]'];
        for (const sel of selectors) {
          try {
            const loc = p.locator(sel);
            const count = await loc.count();
            if (count > 0) {
              const el = loc.first();
              if (await el.isVisible().catch(() => false)) return el;
            }
          } catch (_) { /* next */ }
        }
      } catch (e) { /* ignore */ }
    }

    // Strategy 5: placeholder text (for inputs)
    if (info.name) {
      try {
        const loc = p.locator(`[placeholder*="${info.name}"], [aria-label*="${info.name}"]`).first();
        if (await loc.count() > 0) return loc;
      } catch (e) { /* ignore */ }
    }

    // Strategy 6: label association (for form inputs paired with labels)
    if (info.name && (info.tag === 'input' || info.tag === 'textarea' || info.role === 'textbox')) {
      try {
        const loc = p.getByLabel(info.name, { exact: false }).first();
        if (await loc.count() > 0) return loc;
      } catch (e) { /* ignore */ }
    }

    // Strategy 7: tag-based fallback (last resort for non-input elements like button, a, div)
    if (info.tag && info.tag !== 'input' && info.tag !== 'textarea') {
      try {
        const loc = p.locator(info.tag).first();
        const count = await loc.count();
        if (count > 0) return loc;
      } catch (e) { /* ignore */ }
    }

    // Strategy 8: plain text match (last resort)
    if (info.name) {
      try {
        const loc = p.getByText(info.name);
        const count = await loc.count();
        if (count > 0) return loc.first();
      } catch (e) { /* ignore */ }
    }

    return null;
  }

  // Execute a single action object (used by /act and as the shared impl).
  async function executeSingle(p, a) {
    const action = (a.action || '').toLowerCase();
    const ref = a.ref;
    try {
      switch (action) {
        case 'click': {
        const r = await resolveRef(p, ref);
        if (r.error) return r;
        const el = r.el;
          await el.click({ timeout: 10000 });
          return { ok: true, ref };
        }
        case 'fill': {
        const r = await resolveRef(p, ref);
        if (r.error) return r;
        const el = r.el;
          await el.fill(a.text || '', { timeout: 10000 });
          return { ok: true, ref, filled: a.text };
        }
        case 'type': await p.keyboard.type(a.text || ''); return { ok: true, typed: a.text };
        case 'press': await p.keyboard.press(a.key || 'Enter'); return { ok: true, pressed: a.key };
        case 'hover': {
        const r = await resolveRef(p, ref);
        if (r.error) return r;
        const el = r.el;
          await el.hover({ timeout: 5000 });
          return { ok: true, ref };
        }
        case 'select': {
        const r = await resolveRef(p, ref);
        if (r.error) return r;
        const el = r.el;
          await el.selectOption(a.option || '');
          return { ok: true, ref, selected: a.option };
        }
        case 'check': {
        const r = await resolveRef(p, ref);
        if (r.error) return r;
        const el = r.el;
          await el.check();
          return { ok: true, ref };
        }
        case 'uncheck': {
        const r = await resolveRef(p, ref);
        if (r.error) return r;
        const el = r.el;
          await el.uncheck();
          return { ok: true, ref };
        }
        case 'upload': {
          const r = await resolveRef(p, ref);
          if (r.error) return r;
          const el = r.el;
          const files = Array.isArray(a.files) ? a.files : (a.files ? String(a.files).split(',').map(s => s.trim()).filter(Boolean) : []);
          await el.setInputFiles(files);
          return { ok: true, ref, uploaded: files };
        }
        case 'drag': {
          const rs = await resolveRef(p, a.ref);
          if (rs.error) return rs;
          const rt = await resolveRef(p, a.target);
          if (rt.error) return rt;
          await rs.el.dragTo(rt.el, { timeout: 10000 });
          return { ok: true, from: a.ref, to: a.target };
        }
        case 'goto': {
          try {
            await p.goto(a.url, { waitUntil: 'domcontentloaded', timeout: Number(a.timeout) || 60000 });
            await p.waitForLoadState('load', { timeout: 15000 }).catch(() => {});
            return { ok: true, afterUrl: p.url(), title: await p.title() };
          } catch (e) { return { ok: false, error: { kind: 'NavigationTimeout', message: e.message } }; }
        }
        case 'screenshot': {
          const fp = a.path || path.join(STATE_DIR, `screenshot-${Date.now()}.png`);
          await p.screenshot({ path: fp, fullPage: a.full === true || a.full === 'true' });
          return { ok: true, path: fp };
        }
        case 'download': {
          return await doDownload(p, { ref, dest: a.path, timeout: a.timeout });
        }
        default:
          return { ok: false, error: { kind: 'UnknownAction', message: a.action } };
      }
    } catch (e) {
      return { ok: false, error: { kind: 'ActionError', message: e.message } };
    }
  }

  // Diagnose a failed action: is the ref still present? any similar refs now?
  function diagnose(a, snap) {
    const ref = a.ref;
    if (!ref) return 'no ref provided for action ' + a.action;
    if (snap.refMap.has(ref)) return `ref ${ref} still present but action failed (maybe not visible / not actionable)`;
    const similar = [];
    for (const [r, info] of snap.refMap) {
      if (info.tag === a.tag || (info.name && a.text && info.name.includes(String(a.text)))) similar.push(r);
    }
    return `ref ${ref} no longer present. Similar refs now: ${similar.slice(0, 6).join(', ') || 'none'}`;
  }

  // Shared download helper: optionally click <ref> to trigger a download, wait
  // for the page 'download' event, then saveAs to dest. Used by both the
  // /download route and the 'download' act action.
  async function doDownload(p, opts) {
    const dest = opts.dest || process.cwd();
    const timeout = Number(opts.timeout) || 30000;
    const dlPromise = new Promise((resolve, reject) => {
      const onDl = (dl) => { cleanup(); resolve(dl); };
      const timer = setTimeout(() => { cleanup(); reject(new Error(`download timeout: no download started within ${timeout}ms`)); }, timeout);
      function cleanup() { try { p.off('download', onDl); } catch (e) {} clearTimeout(timer); }
      p.on('download', onDl);
    });
    if (opts.ref) {
      const r = await resolveRef(p, opts.ref);
      if (r.error) return r;
      await r.el.click({ timeout: 10000 });
    }
    try {
      const dl = await dlPromise;
      const suggested = dl.suggestedFilename() || `download-${Date.now()}`;
      let safe;
      // Only when dest is an existing DIRECTORY do we let the (attacker-chosen)
      // suggested filename participate — and then it is forced to a bare
      // basename inside dest. When dest is an explicit file path, use it as-is.
      let isDir = false;
      try { isDir = fs.existsSync(dest) && fs.statSync(dest).isDirectory(); } catch (_) {}
      if (isDir) safe = safeDownloadTarget(dest, suggested);
      else safe = { path: dest };
      if (safe.error) return { ok: false, error: safe.error };
      await dl.saveAs(safe.path);
      return { ok: true, savedPath: safe.path, suggestedFilename: suggested };
    } catch (e) {
      return { ok: false, error: { kind: 'DownloadError', message: e.message } };
    }
  }

  // Route handler
  const server = http.createServer(async (req, res) => {
    const url = new URL(req.url, `http://${DAEMON_HOST}`);
    const cmd = url.pathname.slice(1);
    const params = Object.fromEntries(url.searchParams);

    // SECURITY: require token for every route except /health.
    // The token is a random 24-byte hex generated at daemon start and stored
    // in daemon.json (local-user-only). This closes the "unauthenticated
    // HTTP daemon = RCE surface" gap: a malicious local page/process cannot
    // drive the browser without the token.
    if (cmd !== 'health') {
      // Auth: prefer Authorization: Bearer <token> header; fall back to the
      // ?token= query param for backwards compatibility with older clients.
      let provided = null;
      const auth = req.headers['authorization'] || req.headers['Authorization'] || '';
      const m = String(auth).match(/^Bearer\s+(.+)$/i);
      if (m) provided = m[1];
      else provided = url.searchParams.get('token');
      if (!provided || !timingSafeToken(provided, daemonToken)) {
        res.writeHead(403, { 'Content-Type': 'application/json' });
        return res.end(JSON.stringify({ ok: false, error: { kind: 'AuthError', message: 'Missing or invalid token' } }));
      }
    }

    function json(obj) {
      // D: record operation history (skip health pings; filter auth token)
      if (cmd !== 'health') {
        try {
          const { token, ...safe } = params;
          opHistory.push({ ts: Date.now(), cmd, params: safe, ok: obj.ok, elapsedMs: obj.elapsedMs });
          if (opHistory.length > 500) opHistory.shift();
        } catch (e) { /* non-fatal */ }
      }
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify(obj));
    }

    function bad(msg) {
      res.writeHead(400);
      res.end(JSON.stringify({ ok: false, error: { message: msg } }));
    }

    inFlight++;
    lastActivity = Date.now();
    try {
      const p = await ensurePage();
      const t0 = Date.now();

      switch (cmd) {
        case 'health': return json({ ok: true });
        case 'init': {
          return json({ ok: true, pageUrl: p.url(), pageTitle: await p.title(), elapsedMs: Date.now() - t0 });
        }
        case 'open': case 'goto': {
          const targetUrl = params.url;
          if (!targetUrl) return bad('Missing url param');
          try {
            await p.goto(targetUrl, { waitUntil: 'domcontentloaded', timeout: Number(params.timeout) || 60000 });
            await p.waitForLoadState('load', { timeout: 15000 }).catch(() => {});
            json({ ok: true, afterUrl: p.url(), title: await p.title(), elapsedMs: Date.now() - t0 });
          } catch (e) {
            json({ ok: false, error: { kind: 'NavigationTimeout', message: e.message }, elapsedMs: Date.now() - t0 });
          }
          break;
        }
        case 'snap': {
          const snap = await buildSnapshot(p);
          json({ ok: true, truncated: snap.truncated, data: { ...serializeSnap(snap), url: p.url(), title: await p.title() }, elapsedMs: Date.now() - t0 });
          break;
        }
        case 'click': {
        const r = await resolveRef(p, params.ref);
        if (r.error) return json({ ok: false, error: r.error });
        const el = r.el;
          await el.click({ timeout: 10000 });
          json({ ok: true, ref: params.ref, clicked: true, elapsedMs: Date.now() - t0 });
          break;
        }
        case 'fill': {
        const r = await resolveRef(p, params.ref);
        if (r.error) return json({ ok: false, error: r.error });
        const el = r.el;
          await el.fill(params.text || '', { timeout: 10000 });
          json({ ok: true, ref: params.ref, filled: params.text, elapsedMs: Date.now() - t0 });
          break;
        }
        case 'type': {
          await p.keyboard.type(params.text || '');
          json({ ok: true, typed: params.text, elapsedMs: Date.now() - t0 });
          break;
        }
        case 'press': {
          await p.keyboard.press(params.key || 'Enter');
          json({ ok: true, pressed: params.key, elapsedMs: Date.now() - t0 });
          break;
        }
        case 'hover': {
        const r = await resolveRef(p, params.ref);
        if (r.error) return json({ ok: false, error: r.error });
        const el = r.el;
          await el.hover({ timeout: 5000 });
          json({ ok: true, ref: params.ref, hovered: true, elapsedMs: Date.now() - t0 });
          break;
        }
        case 'select': {
        const r = await resolveRef(p, params.ref);
        if (r.error) return json({ ok: false, error: r.error });
        const el = r.el;
          await el.selectOption(params.option || '');
          json({ ok: true, ref: params.ref, selected: params.option, elapsedMs: Date.now() - t0 });
          break;
        }
        case 'check': {
        const r = await resolveRef(p, params.ref);
        if (r.error) return json({ ok: false, error: r.error });
        const el = r.el;
          await el.check();
          json({ ok: true, ref: params.ref, checked: true, elapsedMs: Date.now() - t0 });
          break;
        }
        case 'uncheck': {
        const r = await resolveRef(p, params.ref);
        if (r.error) return json({ ok: false, error: r.error });
        const el = r.el;
          await el.uncheck();
          json({ ok: true, ref: params.ref, unchecked: true, elapsedMs: Date.now() - t0 });
          break;
        }
        case 'upload': {
          const r = await resolveRef(p, params.ref);
          if (r.error) return json({ ok: false, error: r.error });
          const files = (params.files || '').split(',').map(s => s.trim()).filter(Boolean);
          await r.el.setInputFiles(files);
          json({ ok: true, ref: params.ref, uploaded: files, elapsedMs: Date.now() - t0 });
          break;
        }
        case 'drag': {
          const rs = await resolveRef(p, params.ref);
          if (rs.error) return json({ ok: false, error: rs.error });
          const rt = await resolveRef(p, params.target);
          if (rt.error) return json({ ok: false, error: rt.error });
          await rs.el.dragTo(rt.el, { timeout: 10000 });
          json({ ok: true, from: params.ref, to: params.target, elapsedMs: Date.now() - t0 });
          break;
        }
        case 'go-back': {
          await p.goBack();
          json({ ok: true, afterUrl: p.url(), elapsedMs: Date.now() - t0 });
          break;
        }
        case 'go-forward': {
          await p.goForward();
          json({ ok: true, afterUrl: p.url(), elapsedMs: Date.now() - t0 });
          break;
        }
        case 'reload': {
          await p.reload();
          json({ ok: true, afterUrl: p.url(), elapsedMs: Date.now() - t0 });
          break;
        }
        case 'wait-for': {
          const target = params.target;
          const timeout = Number(params.timeout) || 10000;
          try {
            if (target.startsWith('url:')) {
              await p.waitForURL(target.slice(4), { timeout });
            } else if (target.startsWith('text=')) {
              await p.getByText(target.slice(5)).first().waitFor({ timeout });
            } else if (target.startsWith('state:')) {
              await p.waitForLoadState(target.slice(6), { timeout });
            } else {
              await p.waitForSelector(target, { timeout });
            }
            json({ ok: true, target, matched: true, elapsedMs: Date.now() - t0 });
          } catch (e) {
            json({ ok: false, error: { kind: 'WaitTimeout', message: e.message }, elapsedMs: Date.now() - t0 });
          }
          break;
        }
        case 'screenshot': {
          const filePath = params.path || path.join(STATE_DIR, `screenshot-${Date.now()}.png`);
          if (params.annotate === 'true') {
            // B: draw ref-aligned numbered boxes over interactive elements, then capture
            if (!cachedSnap) await buildSnapshot(p);
            const entries = [...cachedSnap.refMap.entries()];
            await p.evaluate((ents) => {
              document.querySelectorAll('.__pw_anno').forEach(n => n.remove());
              const byXpath = (xp) => { try { return document.evaluate(xp, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue; } catch { return null; } };
              for (const [ref, info] of ents) {
                // xpath only resolves main-document elements; skip shadow/iframe
                // ones here (they are still listed in the text snap for targeting).
                if (info.inShadow || (info.frameChain && info.frameChain.length)) continue;
                const el = byXpath(info.xpath);
                if (!el) continue;
                const r = el.getBoundingClientRect();
                if (r.width === 0 || r.height === 0) continue;
                const box = document.createElement('div');
                box.className = '__pw_anno';
                box.style.cssText = `position:fixed;left:${r.left}px;top:${r.top}px;width:${r.width}px;height:${r.height}px;border:2px solid #ff3b30;background:rgba(255,59,48,0.10);z-index:2147483647;pointer-events:none;box-sizing:border-box;`;
                const label = document.createElement('div');
                label.className = '__pw_anno';
                label.textContent = ref;
                label.style.cssText = `position:fixed;left:${r.left}px;top:${Math.max(0, r.top - 14)}px;background:#ff3b30;color:#fff;font:11px/14px monospace;padding:0 3px;z-index:2147483647;pointer-events:none;`;
                document.body.appendChild(box);
                document.body.appendChild(label);
              }
            }, entries);
            await p.screenshot({ path: filePath });
            await p.evaluate(() => document.querySelectorAll('.__pw_anno').forEach(n => n.remove()));
            json({ ok: true, path: filePath, annotated: entries.length, elapsedMs: Date.now() - t0 });
          } else if (params.ref) {
            const el = await findElement(p, params.ref);
            if (!el) return json({ ok: false, error: { kind: 'ElementNotFound', message: `Element ${params.ref} not found` } });
            await el.screenshot({ path: filePath });
            json({ ok: true, path: filePath, elapsedMs: Date.now() - t0 });
          } else {
            await p.screenshot({ path: filePath, fullPage: true });
            json({ ok: true, path: filePath, elapsedMs: Date.now() - t0 });
          }
          break;
        }
        case 'mousewheel': {
          await p.mouse.wheel(Number(params.dx) || 0, Number(params.dy) || 0);
          json({ ok: true, scrolled: { dx: Number(params.dx), dy: Number(params.dy) }, elapsedMs: Date.now() - t0 });
          break;
        }
        case 'eval': {
          if (SAFE_MODE) {
            return json({ ok: false, error: { kind: 'Disabled', message: 'eval is disabled in safe mode (PW_BROWSER_SAFE_MODE=1)' } });
          }
          const expr = params.expr;
          console.error(`[daemon] eval executed (ref=${params.ref || 'page'}, len=${expr.length})`);
          //
          // EXECUTION SEMANTICS (explicit, do not rely on closures):
          //   Playwright serializes the callback to a STRING and evaluates it
          //   inside the browser. Node-scope variables are NOT captured — any
          //   identifier the callback closes over is `undefined` in the page.
          //   Therefore `expr` MUST be passed as an explicit argument and
          //   `eval`-ed there (direct eval, so the arrow function's own scope
          //   — including `el` — is visible to the expression).
          //   - no ref : `p.evaluate(expr)` — Playwright treats a string as a
          //              page-level expression. `this`/scope = page global.
          //   - with ref: expression runs with `el` bound to the resolved
          //              ElementHandle's DOM node. e.g. `el.textContent`.
          //   Return values must be JSON-serializable by Playwright; DOM nodes
          //   and circular structures cannot cross the bridge and will error.
          //
          // SECURITY: this is FULL page-context code execution — NOT a sandbox.
          //   It cannot reach Node APIs (require/fs/process), i.e. it does not
          //   escape to the HOST. But inside the page it can read
          //   document.cookie / localStorage / sessionStorage, issue
          //   credentialed fetch()/XMLHttpRequest as the logged-in user, and
          //   drive arbitrary DOM actions. Same risk class as run-code.
          //   Gated only by daemon token auth; PW_BROWSER_SAFE_MODE=1 disables it.
          //
          const serializeEvalResult = (v) => {
            if (typeof v === 'string') return v;
            try {
              const s = JSON.stringify(v);
              return s === undefined ? String(v) : s;
            } catch {
              return String(v);
            }
          };
          if (params.ref) {
            const el = await findElement(p, params.ref);
            if (!el) return json({ ok: false, error: { kind: 'ElementNotFound', message: `Element ${params.ref} not found` } });
            // `expr` passed as an argument (2nd param of evaluate), NOT captured
            // by closure. `__pwExpr` is deliberately obscure to avoid shadowing
            // identifiers the user expression might use; `el` is the documented binding.
            const r = await el.evaluate((el, __pwExpr) => eval(__pwExpr), expr);
            json({ ok: true, result: serializeEvalResult(r), scope: 'element', elapsedMs: Date.now() - t0 });
          } else {
            const r = await p.evaluate(expr);
            json({ ok: true, result: serializeEvalResult(r), scope: 'page', elapsedMs: Date.now() - t0 });
          }
          break;
        }
        case 'run-code': {
          if (SAFE_MODE) {
            return json({ ok: false, error: { kind: 'Disabled', message: 'run-code is disabled in safe mode (PW_BROWSER_SAFE_MODE=1)' } });
          }
          const codeStr = params.code;
          console.error(`[daemon] run-code executed (len=${codeStr.length})`);
          // SECURITY: run user code inside a restricted VM context.
          // The sandbox is created with Object.create(null) so it has NO
          // prototype chain — `this.constructor` is undefined, which blocks
          // the classic escape `this.constructor.constructor('return process')()`.
          // Standard JS globals (Object/Array/JSON/Function/Promise/...) are
          // provided natively by the vm context; host Node APIs (process/
          // require/fs/child_process) are NOT present, so user code CANNOT
          // directly touch the HOST OS / filesystem / process.
          //
          // IMPORTANT — the sandbox isolates the HOST, NOT the BROWSER SESSION.
          // The injected `page` object below is a FULL-POWER browser authority:
          // it can navigate to ANY origin, read page DOM / cookies / localStorage,
          // interact with ALREADY-AUTHENTICATED sessions, trigger file
          // downloads/uploads, and issue CREDENTIALED requests — i.e. it can
          // exfiltrate secrets or act as the logged-in user. "Cannot reach the
          // host" does NOT mean "cannot do harm". Treat run-code as equivalent
          // to handing the user's browser to the code.
          // Therefore: NEVER enable run-code where untrusted input can reach it.
          // Safe-mode (PW_BROWSER_SAFE_MODE=1) disables this command entirely;
          // outside safe-mode, restrict it to trusted, user-visible local
          // environments only. Token auth gates NETWORK reachability, not
          // capability — it is defense-in-depth, not a sandbox boundary.
          const sandbox = Object.create(null);
          sandbox.page = p;
          sandbox.console = console;
          sandbox.setTimeout = setTimeout;
          sandbox.clearTimeout = clearTimeout;
          sandbox.setInterval = setInterval;
          sandbox.clearInterval = clearInterval;
          sandbox.queueMicrotask = queueMicrotask;
          vm.createContext(sandbox);
          let compiledScript;
          try {
            compiledScript = new vm.Script(`(async () => { ${codeStr} })()`);
          } catch (e) {
            return json({ ok: false, error: { kind: 'SyntaxError', message: e.message }, elapsedMs: Date.now() - t0 });
          }
          try {
            const runPromise = compiledScript.runInContext(sandbox);
            const timeoutMs = 120000;
            const timeoutPromise = new Promise((_, rej) => {
              const t = setTimeout(() => rej(new Error(`run-code exceeded ${timeoutMs}ms`)), timeoutMs);
              runPromise.finally(() => clearTimeout(t));
            });
            const r = await Promise.race([runPromise, timeoutPromise]);
            const text = typeof r === 'string' ? r : JSON.stringify(r, null, 2);
            json({ ok: true, result: text, elapsedMs: Date.now() - t0 });
          } catch (e) {
            json({ ok: false, error: { kind: 'RunCodeError', message: e.message, stack: e.stack } });
          }
          break;
        }
        case 'tab': {
          const sub = params.sub;
          const pages = context.pages();
          if (sub === 'list') {
            const tabs = await Promise.all(pages.map(async (pg, i) => ({
              index: i, url: pg.url(), title: await pg.title().catch(() => '')
            })));
            json({ ok: true, tabs, elapsedMs: Date.now() - t0 });
          } else if (sub === 'select') {
            const idx = Number(params.idx);
            if (idx < 0 || idx >= pages.length) return json({ ok: false, error: { kind: 'InvalidTab', message: `Tab ${idx} out of range` } });
            page = pages[idx];
            await page.bringToFront();
            json({ ok: true, selected: idx, url: page.url(), elapsedMs: Date.now() - t0 });
          } else if (sub === 'close') {
            const idx = Number(params.idx);
            if (idx < 0 || idx >= pages.length) return json({ ok: false, error: { kind: 'InvalidTab', message: `Tab ${idx} out of range` } });
            if (pages.length <= 1) return json({ ok: false, error: { kind: 'LastTab', message: 'Cannot close last tab' } });
            await pages[idx].close();
            page = context.pages()[0];
            json({ ok: true, closed: idx, elapsedMs: Date.now() - t0 });
          } else {
            bad(`Unknown tab subcommand: ${sub}`);
          }
          break;
        }
        case 'sleep': {
          const sec = Number(params.seconds) || 1;
          await new Promise(r => setTimeout(r, sec * 1000));
          json({ ok: true, slept: sec, elapsedMs: Date.now() - t0 });
          break;
        }
        case 'close': {
          if (params.all === 'true') {
            json({ ok: true, closed: 'all', elapsedMs: Date.now() - t0 });
            safeCloseBrowser().then(() => { try { server.close(); } catch (e) {} process.exit(0); });
            break;
          } else {
            if (context.pages().length > 1) {
              await page.close();
              page = context.pages()[0];
            }
            json({ ok: true, closed: 'page', elapsedMs: Date.now() - t0 });
          }
          break;
        }
        case 'dialog-accept': {
          p.once('dialog', async d => { if (params.text) await d.accept(params.text); else await d.accept(); });
          json({ ok: true, elapsedMs: Date.now() - t0 });
          break;
        }
        case 'dialog-dismiss': {
          p.once('dialog', async d => { await d.dismiss(); });
          json({ ok: true, elapsedMs: Date.now() - t0 });
          break;
        }
        case 'recover': {
          if (browser) { await browser.close().catch(() => {}); browser = null; context = null; page = null; }
          await ensurePage();
          json({ ok: true, recovered: true, pageUrl: p.url(), elapsedMs: Date.now() - t0 });
          break;
        }
        case 'shutdown': {
          json({ ok: true, shutdown: true });
          gracefulExit();
          break;
        }
        case 'act': {
          let actions;
          try { actions = JSON.parse(params.actions); } catch (e) { return bad('actions must be a JSON array'); }
          if (!Array.isArray(actions)) return bad('actions must be a JSON array');
          const results = [];
          let interrupted = false;
          let snapAfter = null;
          await buildSnapshot(p); // baseline
          let prevHashes = cachedHashes;
          for (let i = 0; i < actions.length; i++) {
            const a = actions[i];
            const r = await executeSingle(p, a);
            results.push({ index: i, action: a, result: r });
            if (!r.ok) {
              const ds = await buildSnapshot(p);
              results.push({ index: i, diagnosis: diagnose(a, ds) });
              break;
            }
            // C: after each action, detect DOM change. If new elements appeared
            // OR existing elements disappeared/changed, the remaining actions were
            // planned for the old page — stop and return a fresh snapshot so the
            // agent can re-plan (mirrors browser-use's multi_act interruption).
            const post = await buildSnapshot(p);
            const postHashes = new Set([...post.refMap.values()].map(v => v.branchPathHash));
            const appeared = [...postHashes].some(h => !prevHashes.has(h));
            const disappeared = [...prevHashes].some(h => !postHashes.has(h));
            if (appeared || disappeared) {
              interrupted = true;
              snapAfter = post;
              results.push({ index: i, message: 'DOM changed after action, stopped sequence; re-snap provided' });
              break;
            }
            prevHashes = cachedHashes; // advance baseline for the next action
          }
          const finalSnap = snapAfter || await buildSnapshot(p);
          json({ ok: true, results, interrupted, snap: serializeSnap(finalSnap) });
          break;
        }
        case 'history': {
          if (params.clear === 'true') { opHistory.length = 0; return json({ ok: true, cleared: true }); }
          const limit = Number(params.limit) || 50;
          json({ ok: true, count: opHistory.length, history: opHistory.slice(-limit) });
          break;
        }
        case 'download': {
          const dr = await doDownload(p, { ref: params.ref, dest: params.path, timeout: params.timeout });
          return json({ ...dr, elapsedMs: Date.now() - t0 });
        }
        case 'cookies': {
          if (SAFE_MODE) {
            return json({ ok: false, error: { kind: 'Disabled', message: 'cookies commands are disabled in safe mode (PW_BROWSER_SAFE_MODE=1): they read/write live session credentials' } });
          }
          const sub = params.sub;
          try {
            if (sub === 'list') {
              const cookies = await context.cookies();
              return json({ ok: true, count: cookies.length, cookies, elapsedMs: Date.now() - t0 });
            } else if (sub === 'export') {
              if (!CRED_PERSIST) return json({ ...credPersistBlocked('cookies export'), elapsedMs: Date.now() - t0 });
              const rp = resolveCredPath(params.path, 'cookies.json', params, 'export');
              if (rp.error) return json({ ok: false, error: rp.error, elapsedMs: Date.now() - t0 });
              const cookies = await context.cookies();
              writeSecretFile(rp.path, JSON.stringify(cookies, null, 2));
              return json({ ok: true, exported: rp.path, count: cookies.length, confined: !rp.escapedConfinement, warning: CRED_WARNING, elapsedMs: Date.now() - t0 });
            } else if (sub === 'import') {
              if (!CRED_PERSIST) return json({ ...credPersistBlocked('cookies import'), elapsedMs: Date.now() - t0 });
              const fp = params.file;
              if (!fp) return bad('cookies import requires a <file> argument');
              const rp = resolveCredPath(fp, 'cookies.json', params, 'import');
              if (rp.error) return json({ ok: false, error: rp.error, elapsedMs: Date.now() - t0 });
              const cookies = JSON.parse(fs.readFileSync(rp.path, 'utf8'));
              await context.addCookies(Array.isArray(cookies) ? cookies : [cookies]);
              return json({ ok: true, imported: rp.path, count: Array.isArray(cookies) ? cookies.length : 1, confined: !rp.escapedConfinement, warning: CRED_WARNING, elapsedMs: Date.now() - t0 });
            } else if (sub === 'clear') {
              await context.clearCookies();
              return json({ ok: true, cleared: true, elapsedMs: Date.now() - t0 });
            } else if (sub === 'set') {
              const name = params.name, value = params.value || '';
              if (!name) return bad('cookies set requires <name>');
              let domain = params.domain;
              if (!domain) { try { domain = new URL(p.url()).hostname; } catch (e) { return bad('cookies set needs --domain (no current page URL)'); } }
              await context.addCookies([{ name, value, domain, path: params.cpath || '/', sameSite: 'Lax' }]);
              return json({ ok: true, set: name, domain, elapsedMs: Date.now() - t0 });
            } else {
              return bad(`Unknown cookies subcommand: ${sub}`);
            }
          } catch (e) {
            return json({ ok: false, error: { kind: 'CookieError', message: e.message }, elapsedMs: Date.now() - t0 });
          }
        }
        case 'storage': {
          if (SAFE_MODE) {
            return json({ ok: false, error: { kind: 'Disabled', message: 'storage commands are disabled in safe mode (PW_BROWSER_SAFE_MODE=1): they read/write localStorage which may hold session tokens' } });
          }
          const sub = params.sub;
          try {
            if (sub === 'get') {
              const key = params.key;
              const val = await p.evaluate((k) => {
                if (k) return localStorage.getItem(k);
                const o = {}; for (let i = 0; i < localStorage.length; i++) { const key = localStorage.key(i); o[key] = localStorage.getItem(key); } return o;
              }, key);
              return json({ ok: true, key: key || null, value: val, elapsedMs: Date.now() - t0 });
            } else if (sub === 'set') {
              const key = params.key, value = params.value || '';
              if (!key) return bad('storage set requires <key> <value>');
              await p.evaluate(({ k, v }) => localStorage.setItem(k, v), { k: key, v: value });
              return json({ ok: true, set: key, elapsedMs: Date.now() - t0 });
            } else if (sub === 'clear') {
              await p.evaluate(() => localStorage.clear());
              return json({ ok: true, cleared: true, elapsedMs: Date.now() - t0 });
            } else if (sub === 'export') {
              if (!CRED_PERSIST) return json({ ...credPersistBlocked('storage export'), elapsedMs: Date.now() - t0 });
              const rp = resolveCredPath(params.path, 'localStorage.json', params, 'export');
              if (rp.error) return json({ ok: false, error: rp.error, elapsedMs: Date.now() - t0 });
              const obj = await p.evaluate(() => { const o = {}; for (let i = 0; i < localStorage.length; i++) { const k = localStorage.key(i); o[k] = localStorage.getItem(k); } return o; });
              writeSecretFile(rp.path, JSON.stringify(obj, null, 2));
              return json({ ok: true, exported: rp.path, count: Object.keys(obj).length, confined: !rp.escapedConfinement, warning: CRED_WARNING, elapsedMs: Date.now() - t0 });
            } else if (sub === 'import') {
              if (!CRED_PERSIST) return json({ ...credPersistBlocked('storage import'), elapsedMs: Date.now() - t0 });
              const fp = params.file;
              if (!fp) return bad('storage import requires a <file> argument');
              const rp = resolveCredPath(fp, 'localStorage.json', params, 'import');
              if (rp.error) return json({ ok: false, error: rp.error, elapsedMs: Date.now() - t0 });
              const obj = JSON.parse(fs.readFileSync(rp.path, 'utf8'));
              await p.evaluate((o) => { for (const [k, v] of Object.entries(o)) localStorage.setItem(k, v); }, obj);
              return json({ ok: true, imported: rp.path, count: Object.keys(obj).length, confined: !rp.escapedConfinement, warning: CRED_WARNING, elapsedMs: Date.now() - t0 });
            } else {
              return bad(`Unknown storage subcommand: ${sub}`);
            }
          } catch (e) {
            return json({ ok: false, error: { kind: 'StorageError', message: e.message }, elapsedMs: Date.now() - t0 });
          }
        }
        default:
          bad(`Unknown command: ${cmd}`);
      }
    } catch (e) {
      res.writeHead(500);
      res.end(JSON.stringify({ ok: false, error: { kind: 'InternalError', message: e.message }, elapsedMs: 0 }));
    } finally {
      inFlight = Math.max(0, inFlight - 1);
      lastActivity = Date.now();
    }
  });

  // ---- Daemon startup: port config + conflict avoidance ----
  function isPortAlive(port) {
    return new Promise((resolve) => {
      const req = http.get({ host: DAEMON_HOST, port, path: '/health', timeout: 1500 }, (res) => { res.resume(); resolve(res.statusCode === 200); });
      req.on('error', () => resolve(false));
      req.on('timeout', () => { req.destroy(); resolve(false); });
    });
  }
  function startListening(port, depth) {
    if (depth > 100) { console.error('[daemon] Could not find a free port after 100 attempts'); process.exit(1); }
    // SECURITY: check if a daemon is already alive on this port BEFORE binding,
    // so two simultaneous starts don't both claim to be the "new" daemon.
    // If the port is free, bind and on success record it. If bind fails (rare
    // TOCTOU race where another process grabbed the port between checks),
    // increment and try again.
    isPortAlive(port).then((alive) => {
      if (alive) {
        console.error(`[daemon] A daemon is already running on ${DAEMON_HOST}:${port} (see daemon.json). Exiting to avoid a second instance.`);
        process.exit(0);
      }
      server.once('error', (e) => {
        if (e.code === 'EADDRINUSE') {
          console.error(`[daemon] Port ${port} in use (TOCTOU race), trying ${port + 1}`);
          startListening(port + 1, depth + 1);
        } else { console.error(`[daemon] Listen error: ${e.message}`); process.exit(1); }
      });
      server.listen(port, DAEMON_HOST, () => {
        DAEMON_PORT = port;
        console.log(`[daemon] Listening on ${DAEMON_HOST}:${port}`);
        // SECURITY: daemon.json carries the auth token that authorises eval /
        // run-code / credential access. Written 0600 — a 0644 token file would
        // let any other local user take over the browser session.
        writeSecretFile(path.join(STATE_DIR, 'daemon.json'), JSON.stringify({ host: DAEMON_HOST, port, pid: process.pid, token: daemonToken }));
      });
    });
  }
  startListening(DAEMON_PORT, 0);

  // Robust browser close that never hangs the shutdown path.
  async function safeCloseBrowser() {
    if (!browser) return;
    await Promise.race([
      browser.close().catch(() => {}),
      new Promise(r => setTimeout(r, 5000)),
    ]);
    browser = null; context = null; page = null;
  }

  // Flush-then-exit: close the server and exit. Never blocks on browser.close()
  // (raced with a timeout) so a stuck browser can't keep the daemon alive.
  function gracefulExit() {
    try { server.close(); } catch (e) {}
    const finish = () => process.exit(0);
    safeCloseBrowser().then(finish).catch(finish);
    setTimeout(finish, 6000); // hard safety net
  }

  // Idle auto-exit: if no command has been handled for IDLE_MS, close the
  // browser and exit so Chrome doesn't linger. Only fires when idle
  // (inFlight === 0), so long-running commands are never interrupted.
  setInterval(() => {
    if (inFlight === 0 && Date.now() - lastActivity > IDLE_MS) {
      console.error(`[daemon] Idle ${Math.round(IDLE_MS / 1000)}s, auto-exiting`);
      gracefulExit();
    }
  }, 30 * 1000);

  // Global error handlers to prevent daemon crash
  process.on('uncaughtException', (err) => {
    console.error(`[daemon] uncaughtException: ${err.message}`);
  });
  process.on('unhandledRejection', (reason) => {
    console.error(`[daemon] unhandledRejection: ${reason?.message || reason}`);
  });

  // Graceful shutdown
  process.on('SIGINT', async () => { if (browser) await browser.close(); process.exit(0); });
  process.on('SIGTERM', async () => { if (browser) await browser.close(); process.exit(0); });
}

// ===================== CLIENT MODE =====================
async function runClient() {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    console.log(`Usage: node pw-browser.js <command> [args...] [--json]`);
    console.log(`       node pw-browser.js daemon`);
    console.log(`Commands: init, open, snap, click, fill, type, press, hover, select, check, uncheck,`);
    console.log(`          upload, drag, download, goto, go-back, go-forward, reload, wait-for, screenshot, mousewheel,`);
    console.log(`          eval, run-code, act, tab, sleep, close, recover, history, cookies, storage,`);
    console.log(`          dialog-accept [text], dialog-dismiss, shutdown`);
    console.log(`Env (daemon): PW_BROWSER_SAFE_MODE=1 disables eval/run-code AND all cookies/storage commands`);
    console.log(`              PW_BROWSER_CRED_PERSIST=off disables cookies/storage export+import (no credentials on disk)`);
    console.log(`              PW_BROWSER_ALLOW_UNSAFE_CRED_PATH=1 lets --unsafe move credential files outside ~/.pw-browser`);
    console.log(`              PW_BROWSER_IDLE_MS (default 900000, 0 = never), PW_BROWSER_SNAP_LIMIT (default 3000)`);
    process.exit(1);
  }

  const jsonIdx = args.indexOf('--json');
  JSON_OUTPUT = jsonIdx !== -1;
  if (JSON_OUTPUT) args.splice(jsonIdx, 1);

  const cmd = args[0];
  const rest = args.slice(1);

  // Parse opts
  function parseOpts(r) {
    const opts = {};
    const positional = [];
    for (let i = 0; i < r.length; i++) {
      if (r[i].startsWith('--')) {
        const key = r[i].slice(2);
        const val = r[i + 1] && !r[i + 1].startsWith('--') ? r[++i] : 'true';
        opts[key] = val;
      } else {
        positional.push(r[i]);
      }
    }
    return { opts, positional };
  }

  const { opts, positional } = parseOpts(rest);

  // Check daemon
  const daemonFile = path.join(STATE_DIR, 'daemon.json');
  let daemonHost = DAEMON_HOST;
  let daemonPort = DAEMON_PORT;
  if (fs.existsSync(daemonFile)) {
    const d = JSON.parse(fs.readFileSync(daemonFile, 'utf8'));
    daemonHost = d.host;
    daemonPort = d.port;
  }

  // Health check
  async function ensureDaemon() {
    return new Promise((resolve) => {
      const req = http.get(`http://${daemonHost}:${daemonPort}/health`, (res) => {
        resolve(res.statusCode === 200);
      });
      req.on('error', () => resolve(false));
      req.setTimeout(2000, () => { req.destroy(); resolve(false); });
    });
  }

  function callDaemon(path, queryParams = {}) {
    return new Promise((resolve, reject) => {
      const qp = { ...queryParams };
      // Attach the daemon auth token (from daemon.json) via Authorization header.
      // Header transport avoids leaking the token into URLs / logs / history.
      let authHeader = null;
      try {
        const d = JSON.parse(fs.readFileSync(daemonFile, 'utf8'));
        if (d.token) authHeader = `Bearer ${d.token}`;
      } catch {}
      const qs = Object.entries(qp)
        .filter(([, v]) => v !== undefined && v !== null)
        .map(([k, v]) => `${encodeURIComponent(k)}=${encodeURIComponent(v)}`)
        .join('&');
      const fullPath = qs ? `${path}?${qs}` : path;
      const headers = {};
      if (authHeader) headers['Authorization'] = authHeader;
      const req = http.get({ host: daemonHost, port: daemonPort, path: fullPath, headers }, (res) => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => {
          try { resolve(JSON.parse(data)); }
          catch { resolve({ ok: false, error: { message: data } }); }
        });
      });
      let settled = false;
      function settle(v) { if (!settled) { settled = true; resolve(v); } }
      req.on('error', (e) => { settle(reject(e)); });
      req.setTimeout(120000, () => { req.destroy(); settle(reject(new Error('Client request timeout (120s)'))); });
      req.on('end', () => {
        try { settle(resolve(JSON.parse(data))); }
        catch { settle(resolve({ ok: false, error: { message: data } })); }
      });
    });
  }

  // Map CLI args to daemon query params
  async function execute() {
    if (!fs.existsSync(daemonFile)) {
      console.error('Daemon not running. Start it: node pw-browser.js daemon &');
      process.exit(1);
    }

    switch (cmd) {
      case 'init': return callDaemon('/init');
      case 'open': case 'goto': return callDaemon('/open', { url: positional[0], timeout: opts.timeout });
      case 'snap': return callDaemon('/snap');
      case 'click': return callDaemon('/click', { ref: positional[0] });
      case 'fill': return callDaemon('/fill', { ref: positional[0], text: positional.slice(1).join(' ') });
      case 'type': return callDaemon('/type', { text: positional.join(' ') });
      case 'press': return callDaemon('/press', { key: positional[0] });
      case 'hover': return callDaemon('/hover', { ref: positional[0] });
      case 'select': return callDaemon('/select', { ref: positional[0], option: positional[1] });
      case 'check': return callDaemon('/check', { ref: positional[0] });
      case 'uncheck': return callDaemon('/uncheck', { ref: positional[0] });
      case 'upload': return callDaemon('/upload', { ref: positional[0], files: positional.slice(1).join(',') });
      case 'drag': return callDaemon('/drag', { ref: positional[0], target: positional[1] });
      case 'go-back': return callDaemon('/go-back');
      case 'go-forward': return callDaemon('/go-forward');
      case 'reload': return callDaemon('/reload');
      case 'wait-for': return callDaemon('/wait-for', { target: positional[0], timeout: opts.timeout });
      case 'screenshot': return callDaemon('/screenshot', { ref: positional[0], path: opts.path, annotate: opts.annotate });
      case 'mousewheel': return callDaemon('/mousewheel', { dx: positional[0], dy: positional[1] });
      case 'eval': return callDaemon('/eval', { expr: positional[0], ref: positional[1] });
      case 'run-code': return callDaemon('/run-code', { code: positional.join(' ') });
      case 'tab': {
        const sub = positional[0];
        if (sub === 'list') return callDaemon('/tab', { sub: 'list' });
        if (sub === 'select') return callDaemon('/tab', { sub: 'select', idx: positional[1] });
        if (sub === 'close') return callDaemon('/tab', { sub: 'close', idx: positional[1] });
        return { ok: false, error: { message: `Unknown tab subcommand: ${sub}` } };
      }
      case 'sleep': return callDaemon('/sleep', { seconds: positional[0] });
      case 'close': return callDaemon('/close', { all: opts.all });
      case 'dialog-accept': return callDaemon('/dialog-accept', { text: positional[0] });
      case 'dialog-dismiss': return callDaemon('/dialog-dismiss');
      case 'recover': return callDaemon('/recover');
      case 'act': return callDaemon('/act', { actions: positional.join(' ') });
      case 'history': return callDaemon('/history', { clear: opts.clear, limit: opts.limit });
      case 'download': return callDaemon('/download', { ref: positional[0], path: opts.path, timeout: opts.timeout });
      case 'cookies': {
        const sub = positional[0];
        if (sub === 'list') return callDaemon('/cookies', { sub: 'list' });
        if (sub === 'export') return callDaemon('/cookies', { sub: 'export', path: opts.path, unsafe: opts.unsafe });
        if (sub === 'import') return callDaemon('/cookies', { sub: 'import', file: positional[1] || opts.file, unsafe: opts.unsafe });
        if (sub === 'clear') return callDaemon('/cookies', { sub: 'clear' });
        if (sub === 'set') return callDaemon('/cookies', { sub: 'set', name: positional[1], value: positional.slice(2).join(' '), domain: opts.domain, cpath: opts.path });
        return { ok: false, error: { message: `Unknown cookies subcommand: ${sub}` } };
      }
      case 'storage': {
        const sub = positional[0];
        if (sub === 'get') return callDaemon('/storage', { sub: 'get', key: positional[1] });
        if (sub === 'set') return callDaemon('/storage', { sub: 'set', key: positional[1], value: positional.slice(2).join(' ') });
        if (sub === 'clear') return callDaemon('/storage', { sub: 'clear' });
        if (sub === 'export') return callDaemon('/storage', { sub: 'export', path: opts.path, unsafe: opts.unsafe });
        if (sub === 'import') return callDaemon('/storage', { sub: 'import', file: positional[1] || opts.file, unsafe: opts.unsafe });
        return { ok: false, error: { message: `Unknown storage subcommand: ${sub}` } };
      }
      case 'shutdown': return callDaemon('/shutdown');
      default: return { ok: false, error: { message: `Unknown command: ${cmd}` } };
    }
  }

  const result = await execute();
  if (JSON_OUTPUT) {
    console.log(JSON.stringify(result));
    process.exit(result.ok ? 0 : 1);
  } else {
    if (result.ok) {
      const d = result.data;
      if (typeof d === 'string') console.log(d);
      else if (d && d.text) console.log(d.text);
      else if (result.tabs) {
        result.tabs.forEach(t => console.log(`[${t.index}] ${t.title} — ${t.url}`));
      } else {
        console.log(JSON.stringify(result, null, 2));
      }
    } else {
      console.error(`ERROR [${result.error?.kind || 'unknown'}]: ${result.error?.message}`);
      process.exit(1);
    }
  }
}

// ---- Entry ----
// Guard with require.main === module so the file can be `require`d by unit
// tests (which only want the exported helpers) without triggering runClient().
if (require.main === module) {
  if (process.argv[2] === 'daemon') {
    runDaemon();
  } else {
    runClient();
  }
}

// Export pure helpers for unit testing. Only relevant when the module is
// `require`d (not executed as the CLI) — see the require.main guard above.
if (require.main !== module) {
  module.exports = { safeDownloadTarget, timingSafeToken };
}
