#!/usr/bin/env node
/** Upload files to S3-compatible storage for md-web skill. Zero dependencies (Node.js built-in only). */

var crypto = require("node:crypto");
var https = require("node:https");
var fs = require("node:fs");
var path = require("node:path");
var os = require("node:os");

function createPublishHelpers(skillDir, console = globalThis.console) {
  var SERVER_DIR = path.join(skillDir, "docsify-server");
  var JUNK = ["Thumbs.db", "desktop.ini"];
  var DOC_EXTS = [".md", ".markdown", ".txt"];
  var YAML_KEY_LINE = /^[ \t]*(?:["'][^"']+["']|[A-Za-z_][\w.-]*)[ \t]*:(?:[ \t]|$)/;
  function versionIndexHtml(html, version) {
    return html.replace(/(href|src)="(assets\/[^"?]+)"/g, function (_m, attr, asset) {
      return attr + '="assets/' + version + '/' + asset.slice(7) + '"';
    });
  }

  function listServerFiles() {
    var out = [];
    function walk(dir, prefix) {
      var names;
      try {
        names = fs.readdirSync(dir).sort();
      } catch (e) {
        // The viewer files ship with the skill, so a missing directory is a broken
        // install. Say that in the documented error vocabulary instead of letting
        // a raw ENOENT stack escape to the caller.
        throw new Error("the viewer assets are missing from " + dir + " (" + (e.code || e.message) + ") — reinstall the skill");
      }
      names.forEach(function (name) {
        if (name.charAt(0) === "." || JUNK.indexOf(name) !== -1) return;
        var full = path.join(dir, name);
        var key = prefix ? prefix + "/" + name : name;
        if (fs.statSync(full).isDirectory()) walk(full, key);
        else out.push({ full: full, key: key });
      });
    }
    walk(SERVER_DIR, "");
    return out;
  }

  function createViewerDeployment() {
    // Read once: every uploaded byte and the index use the same snapshot even if
    // another process upgrades the installed Skill while setup is in progress.
    var files = listServerFiles().map(function (f) {
      return { key: f.key, payload: fs.readFileSync(f.full) };
    });
    var hash = crypto.createHash("sha256");
    files.forEach(function (f) {
      hash.update(JSON.stringify([f.key, f.payload.length]) + "\n");
      hash.update(f.payload);
    });
    var version = hash.digest("hex");
    var index = files.find(function (f) { return f.key === "index.html"; });
    if (!index) throw new Error("the viewer index.html is missing — reinstall the skill");
    return {
      hash: version,
      index: Buffer.from(versionIndexHtml(index.payload.toString("utf8"), version), "utf8"),
      files: files.filter(function (f) { return f !== index; }).map(function (f) {
        return { key: f.key.indexOf("assets/") === 0 ? "assets/" + version + "/" + f.key.slice(7) : f.key, payload: f.payload };
      }),
    };
  }

  function serverDirHash() {
    return createViewerDeployment().hash;
  }

  function timestamp() {
    var d = new Date();
    var pad = function (n) { return n < 10 ? "0" + n : "" + n; };
    return d.getFullYear() + pad(d.getMonth() + 1) + pad(d.getDate())
      + "-" + pad(d.getHours()) + pad(d.getMinutes()) + pad(d.getSeconds());
  }

  function slugify(base) {
    var s = String(base).normalize("NFKD").replace(/[\u0300-\u036f]/g, "").toLowerCase()
      .replace(/[^a-z0-9._-]+/g, "-").replace(/-{2,}/g, "-").replace(/^[-.]+|[-.]+$/g, "");
    return s.slice(0, 80).replace(/[-.]+$/, "") || "doc";
  }

  function addTimestamp(key) {
    key = path.basename(String(key).replace(/\\/g, "/"));
    var ext = path.extname(key);
    var base = key.slice(0, key.length - ext.length);
    // Strip only an extension we recognise. path.extname() calls everything after the last
    // dot an extension, so "v1.2-release-notes" reported ".2-release-notes" and dropping it
    // shipped the document as "v1.md" — silently truncated, with a 200 on the URL to hide it.
    if (DOC_EXTS.indexOf(ext.toLowerCase()) === -1) base = key;
    var slug = slugify(base);
    if (slug !== base) console.log("  Note: remote key normalized to \"" + slug + "\"");
    // The timestamp only has second resolution and the slug is lossy (every name without
    // ASCII letters or digits collapses to "doc"), so two documents published in the same
    // second could land on the same key: the second PUT would overwrite the first, and the
    // first URL would keep answering 200 with someone else's document. A short random
    // suffix makes every publish land on its own object.
    return timestamp() + "-" + slug + "-" + crypto.randomBytes(2).toString("hex") + ".md";
  }

  function prepareMarkdown(buf) {
    var text = buf.toString("utf-8").replace(/^\uFEFF/, "");
    var m = text.match(/^---[ \t]*\r?\n([\s\S]*?)\r?\n(?:---|\.\.\.)[ \t]*(?:\r?\n|$)/);
    if (m && m[1].split(/\r?\n/).some(function (line) { return YAML_KEY_LINE.test(line); })) {
      text = text.slice(m[0].length).replace(/^\s*\r?\n/, "");
      console.log("  Note: YAML front matter stripped from the published copy");
    }
    if (!text.trim()) throw new Error("document is empty after removing front matter");
    return Buffer.from(text, "utf-8");
  }
  return { versionIndexHtml, listServerFiles, serverDirHash, createViewerDeployment, timestamp, slugify, addTimestamp, prepareMarkdown };
}

// A conservative, dependency-free XML reader for lifecycle read/modify/write.
// Unsupported namespaces/DTDs or malformed input must stop a policy rewrite.
// Keep original slices rather than serializing user-owned rules and settings.
function parseLifecycleConfiguration(xml) {
  if (!xml.trim()) return { opening: '<LifecycleConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">', rules: [], extras: "" };
  var tokens = /<!--([\s\S]*?)-->|<\?[\s\S]*?\?>|<!\[CDATA\[[\s\S]*?\]\]>|<\/?[A-Za-z_][\w.-]*(?:\s+[\w.:-]+\s*=\s*(?:"[^"<>]*"|'[^'<>]*'))*\s*\/?>/g;
  var stack = [], roots = [], cursor = 0, match;
  function invalid() { throw new Error("not a LifecycleConfiguration in a supported, complete XML form; refusing to rewrite the lifecycle configuration"); }
  while ((match = tokens.exec(xml))) {
    var gap = xml.slice(cursor, match.index);
    if (gap.includes("<") || (!stack.length && gap.trim())) invalid();
    cursor = tokens.lastIndex;
    var token = match[0];
    if (token.startsWith("<!--") || token.startsWith("<?")) continue;
    if (token.startsWith("<![CDATA[")) { if (!stack.length) invalid(); continue; }
    var name = /^<\/?([\w.-]+)/.exec(token)[1];
    if (token.startsWith("</")) {
      var node = stack.pop();
      if (!node || node.name !== name || token !== "</" + name + ">") invalid();
      node.end = cursor;
      node.innerEnd = match.index;
    } else {
      var node = {name: name, start: match.index, openEnd: cursor, end: cursor, innerEnd: cursor, children: []};
      if (/\sxmlns\s*=/.test(token) && (!token.includes('xmlns="http://s3.amazonaws.com/doc/2006-03-01/"') && !token.includes("xmlns='http://s3.amazonaws.com/doc/2006-03-01/'"))) invalid();
      if (stack.length) stack[stack.length - 1].children.push(node);
      else roots.push(node);
      if (!token.endsWith("/>")) stack.push(node);
    }
  }
  if (stack.length || xml.slice(cursor).trim() || roots.length !== 1 || roots[0].name !== "LifecycleConfiguration") invalid();
  var root = roots[0];
  var rules = root.children.filter(function (node) { return node.name === "Rule"; });
  var ours = 0, kept = [];
  rules.forEach(function (rule) {
    var ids = rule.children.filter(function (node) { return node.name === "ID"; });
    if (ids.length > 1) invalid();
    var id = ids.length ? xml.slice(ids[0].openEnd, ids[0].innerEnd).trim() : "";
    if (id.includes("<")) invalid();
    id = id.replace(/&#(x[\da-f]+|\d+);|&(amp|lt|gt|quot|apos);/gi, function (_text, number, entity) {
      return number ? String.fromCodePoint(parseInt(number.replace(/^x/i, ""), /^x/i.test(number) ? 16 : 10)) : {amp: "&", lt: "<", gt: ">", quot: '"', apos: "'"}[entity.toLowerCase()];
    });
    if (id === "md-web-auto-expire") {
      var prefixNodes = rule.children.filter(function (node) { return node.name === "Prefix"; });
      var filters = rule.children.filter(function (node) { return node.name === "Filter"; });
      if (filters.length) {
        if (filters.length !== 1 || filters[0].children.length !== 1 || filters[0].children[0].name !== "Prefix") invalid();
        prefixNodes = prefixNodes.concat(filters[0].children);
      }
      if (prefixNodes.length !== 1 || xml.slice(prefixNodes[0].openEnd, prefixNodes[0].innerEnd).trim() !== "md-web/" || ++ours > 1)
        throw new Error("the md-web lifecycle ID is not uniquely scoped to md-web/; refusing to replace it");
    } else kept.push(xml.slice(rule.start, rule.end));
  });
  var extras = "", at = root.openEnd;
  rules.forEach(function (rule) { extras += xml.slice(at, rule.start); at = rule.end; });
  extras += xml.slice(at, root.innerEnd);
  return { opening: xml.slice(root.start, root.openEnd).replace(/\/>$/, ">"), rules: kept, extras: extras.trim(), hadRules: rules.length > 0 };
}

// Create the destination with private permissions before writing any credentials.
// Never copy a permissive source mode or overwrite a concurrent migration.
function migrateConfig(source, destination, io = fs, platform = process.platform) {
  var directory = path.dirname(destination);
  io.mkdirSync(directory, { recursive: true, mode: 0o700 });
  var stat = io.lstatSync(directory);
  if (!stat.isDirectory() || stat.isSymbolicLink()) throw new Error("config directory must be a real directory");
  if (platform !== "win32" && typeof process.getuid === "function" && stat.uid !== process.getuid())
    throw new Error("config directory must belong to the current user");
  if (platform !== "win32") io.chmodSync(directory, 0o700);
  var fd;
  try { fd = io.openSync(destination, "wx", 0o600); }
  catch (error) { if (error.code === "EEXIST") { secureConfigFile(destination, io, platform); return; } throw error; }
  try {
    io.writeFileSync(fd, io.readFileSync(source));
  } catch (error) {
    io.closeSync(fd);
    io.unlinkSync(destination);
    throw error;
  }
  io.closeSync(fd);
}

function secureConfigFile(file, io = fs, platform = process.platform) {
  var stat = io.lstatSync(file);
  if (!stat.isFile() || stat.isSymbolicLink()) throw new Error("config must be a regular file");
  if (platform !== "win32") {
    if (typeof process.getuid === "function" && stat.uid !== process.getuid()) throw new Error("config must belong to the current user");
    io.chmodSync(file, 0o600);
  }
}

module.exports = { createPublishHelpers, parseLifecycleConfiguration, migrateConfig };

// Importing exposes helpers without reading config or starting an upload.
if (require.main === module) {
  var SCRIPT_DIR = __dirname;
  var { createViewerDeployment, addTimestamp, prepareMarkdown } = createPublishHelpers(SCRIPT_DIR, console);

  // Two modes, deliberately separate. Publishing one document only ever writes
  // that one object; provisioning the viewer writes the site's root files and may
  // touch the bucket's lifecycle, so it is an explicit command of its own rather
  // than something an upload does on the side.
  //
  // Argument checks stay at the top for two reasons: loading the config exits when it is
  // missing, so a check below it is unreachable for anyone who has not configured yet; and a
  // run's first act in setup mode is deploying the server files, so validating late meant a
  // typo in the local path cost a full round of uploads before failing with an ENOENT about
  // the file alone.
  var args = process.argv.slice(2);
  var SCRIPT_NAME = path.basename(process.argv[1]);
  // Quoted absolute path for hints the agent will copy verbatim: the skill is rarely the cwd,
  // and skill directories often live under paths with spaces.
  var SCRIPT_CMD = 'node "' + path.resolve(process.argv[1]) + '"';
  var SETUP_FLAG = "--setup";
  var usage = [
    "Usage:",
    "  node " + SCRIPT_NAME + " <local-file> <remote-key>   publish one markdown document",
    "  node " + SCRIPT_NAME + " " + SETUP_FLAG + " --confirm-shared-writes   replace shared viewer files and apply configured retention",
  ].join("\n");

  if (args[0] === "--help" || args[0] === "-h") {
    console.log(usage);
    process.exit(0);
  }
  var isSetup = args[0] === SETUP_FLAG;
  if (isSetup && (args.length !== 2 || args[1] !== "--confirm-shared-writes")) {
    console.log(usage);
    console.error('UPLOAD_FAILED: ' + SETUP_FLAG + ' requires --confirm-shared-writes after authorization to replace shared viewer files and apply configured retention.');
    process.exit(1);
  }
  if (!isSetup) {
    if (args.length !== 2) {
      console.log(usage);
      console.error("UPLOAD_FAILED: expected exactly two arguments (<local-file> <remote-key>), got " + args.length + (args.length ? ": " + args.join(" ") : "."));
      process.exit(1);
    }
    if (args[0].charAt(0) === "-") {
      console.log(usage);
      console.error('UPLOAD_FAILED: "' + args[0] + '" looks like an option; this script takes two positional arguments, plus the single flag ' + SETUP_FLAG + '.');
      process.exit(1);
    }
  }
  var localPath = isSetup ? null : args[0];
  if (!isSetup) {
    var localStat = null;
    try { localStat = fs.statSync(localPath); } catch (e) { /* reported below */ }
    if (!localStat || !localStat.isFile()) {
      console.error("UPLOAD_FAILED: not a readable file: " + localPath);
      process.exit(1);
    }
    if (localStat.size === 0) {
      console.error("UPLOAD_FAILED: file is empty: " + localPath);
      process.exit(1);
    }
  }

  // ── User data dir: upgrade-safe location in home dir ──
  var USER_CONFIG_DIR = path.join(os.homedir(), ".md-web");
  var USER_CONFIG_PATH = path.join(USER_CONFIG_DIR, "config.json");
  var LOCAL_CONFIG_PATH = path.join(SCRIPT_DIR, "config.json");
  var LOCAL_DEPLOYED_FLAG = path.join(SCRIPT_DIR, ".deployed");

  var CONFIG_PATH;
  if (fs.existsSync(USER_CONFIG_PATH)) {
    CONFIG_PATH = USER_CONFIG_PATH;
  } else if (fs.existsSync(LOCAL_CONFIG_PATH)) {
    // Migrate credentials without a world-readable intermediate copy.
    try {
      migrateConfig(LOCAL_CONFIG_PATH, USER_CONFIG_PATH);
      CONFIG_PATH = USER_CONFIG_PATH;
      if (fs.existsSync(LOCAL_DEPLOYED_FLAG)) {
        // This is only a deployment hint; failure must not invalidate credentials.
        try { fs.copyFileSync(LOCAL_DEPLOYED_FLAG, path.join(USER_CONFIG_DIR, ".deployed"), fs.constants.COPYFILE_EXCL); } catch (_) {}
      }
      console.log("Config migrated to: " + USER_CONFIG_PATH);
    } catch (error) {
      console.error("CONFIG_INVALID: secure credential migration failed (" + (error.code || "invalid directory") + "). Fix the private config directory before retrying.");
      process.exit(1);
    }
  } else {
    CONFIG_PATH = USER_CONFIG_PATH;
  }

  // The deployment hint follows the active private config directory.
  var DEPLOYED_FLAG = path.join(path.dirname(CONFIG_PATH), ".deployed");

  // ── Load Configuration ──
  var CONFIG;
  if (fs.existsSync(CONFIG_PATH)) {
    try { secureConfigFile(CONFIG_PATH); }
    catch (error) {
      console.error("CONFIG_INVALID: cannot make the credential file owner-only (" + (error.code || "permission failure") + ").");
      process.exit(1);
    }
  }
  try {
    CONFIG = JSON.parse(fs.readFileSync(CONFIG_PATH, "utf-8"));
  } catch (e) {
    console.error("CONFIG_MISSING: " + CONFIG_PATH);
    console.error("Run this skill once to configure, or create: " + USER_CONFIG_PATH);
    process.exit(1);
  }

  var REQUIRED = ["access_key", "secret_key", "endpoint", "bucket", "public_url"];
  // Credentials may come from the environment instead of the config file, so a user
  // who does not want a long-lived secret at rest never has to write one there.
  // The file wins when both are set, so an existing setup keeps working unchanged.
  if (!CONFIG.access_key && process.env.MD_WEB_ACCESS_KEY) CONFIG.access_key = process.env.MD_WEB_ACCESS_KEY;
  if (!CONFIG.secret_key && process.env.MD_WEB_SECRET_KEY) CONFIG.secret_key = process.env.MD_WEB_SECRET_KEY;
  // config.json holds the bucket secret. Written with the default umask it lands at
  // 0644, i.e. readable by every account on the machine; 0600 is the difference
  // between "only me" and "everyone", and it costs one call. Windows ACLs are not
  // chmod, so this is POSIX-only — the env vars above are the portable answer.
  var missing = REQUIRED.filter(function (k) { return !CONFIG[k]; });
  if (missing.length) {
    console.error("Missing config fields: " + missing.join(", "));
    console.error("Edit: " + CONFIG_PATH);
    process.exit(1);
  }
  // The two most common hand-typed mistakes: pasting the endpoint with its scheme (R2's
  // dashboard shows it as https://...), and a public_url without one. The endpoint's scheme
  // is stripped below, so a pasted one no longer reaches the Host header; what is left to
  // reject is a real path in it ("host/bucket"), which would break the Host header and the
  // signature with an opaque DNS error. A public_url without a scheme yields a link that
  // is not a link.
  CONFIG.endpoint = String(CONFIG.endpoint).trim().replace(/^https?:\/\//i, "").replace(/\/+$/, "");
  CONFIG.public_url = String(CONFIG.public_url).trim().replace(/\/+$/, "");
  if (CONFIG.endpoint.indexOf("/") !== -1) {
    console.error("CONFIG_INVALID: endpoint must be a bare hostname (e.g. ACCOUNT_ID.r2.cloudflarestorage.com), got: " + CONFIG.endpoint);
    process.exit(1);
  }
  // A port is allowed and must be split off: https.request takes the host and the
  // port separately, and handing it "host:port" as the hostname makes Node resolve
  // the literal string (ENOTFOUND host:port). The Host header keeps the port,
  // which is exactly what SigV4 signs.
  var ENDPOINT_HOST = CONFIG.endpoint;
  var ENDPOINT_PORT = null;
  var endpointWithPort = /^([^:]+):(\d{1,5})$/.exec(CONFIG.endpoint);
  if (endpointWithPort) {
    ENDPOINT_HOST = endpointWithPort[1];
    ENDPOINT_PORT = Number(endpointWithPort[2]);
  }
  if (!/^https?:\/\//i.test(CONFIG.public_url)) {
    console.error("CONFIG_INVALID: public_url must start with https:// (e.g. https://pub-XXXX.r2.dev), got: " + CONFIG.public_url);
    process.exit(1);
  }

  var CONTENT_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".md": "text/markdown; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".txt": "text/plain; charset=utf-8",
  };

  // ── HTTPS Agent (connection reuse) ──
  var agent = new https.Agent({ keepAlive: true, maxSockets: 6 });

  // ── S3 Signature V4 ──
  function hmacSha256(key, msg) {
    return crypto.createHmac("sha256", key).update(msg, "utf-8").digest();
  }

  function sha256Hex(data) {
    return crypto.createHash("sha256").update(data).digest("hex");
  }

  var _skCache = {};
  function signingKey(dateStamp) {
    if (_skCache.ds === dateStamp) return _skCache.key;
    var region = CONFIG.region || "auto";
    var k = hmacSha256("AWS4" + CONFIG.secret_key, dateStamp);
    k = hmacSha256(k, region);
    k = hmacSha256(k, "s3");
    k = hmacSha256(k, "aws4_request");
    _skCache = { ds: dateStamp, key: k };
    return k;
  }

  // S3 SigV4 URI encoding: encode all except A-Z a-z 0-9 - . _ ~
  function uriEncode(str) {
    return encodeURIComponent(str).replace(/[!'()*]/g, function (c) {
      return "%" + c.charCodeAt(0).toString(16).toUpperCase();
    });
  }

  function uriEncodePath(p) {
    return p.split("/").map(uriEncode).join("/");
  }

  // Build the SigV4 canonical query string (also reused as the request's ?search).
  // Accepts a string ("lifecycle" → valueless param) or an object ({k: v, ...}).
  // Keys/values are URI-encoded and sorted by encoded key, per the SigV4 spec.
  function canonicalizeQuery(query) {
    if (!query) return "";
    var params = query;
    if (typeof query === "string") { params = {}; params[query] = ""; }
    return Object.keys(params)
      .map(function (k) { return [uriEncode(k), uriEncode(String(params[k]))]; })
      .sort(function (a, b) { return a[0] < b[0] ? -1 : a[0] > b[0] ? 1 : 0; })
      .map(function (p) { return p[0] + "=" + p[1]; })
      .join("&");
  }

  function parseR2Error(xml) {
    var code = (xml.match(/<Code>(.*?)<\/Code>/) || [])[1];
    var msg = (xml.match(/<Message>(.*?)<\/Message>/) || [])[1];
    if (code && msg) return code + ": " + msg;
    if (code) return code;
    return xml.length > 200 ? xml.slice(0, 200) + "..." : xml;
  }

  // ── General S3 Request ──
  // All S3 operations go through this single signing path.
  // extraHeaders: signed AND sent. Content-Length + auth added automatically.
  function s3FetchOnce(method, resourcePath, query, payload, extraHeaders) {
    var region = CONFIG.region || "auto";
    if (typeof payload === "string") payload = Buffer.from(payload, "utf-8");
    if (!payload) payload = Buffer.alloc(0);

    var encodedPath = uriEncodePath(resourcePath);
    var canonicalQS = canonicalizeQuery(query);

    return new Promise(function (resolve, reject) {
      var now = new Date();
      var amzDate = now.toISOString().replace(/[-:]/g, "").replace(/\.\d+Z/, "Z");
      var dateStamp = amzDate.slice(0, 8);
      var payloadHash = sha256Hex(payload);

      // Canonical headers (lowercase keys, sorted)
      var signHdrs = {
        "host": CONFIG.endpoint,
        "x-amz-content-sha256": payloadHash,
        "x-amz-date": amzDate,
      };
      if (extraHeaders) {
        Object.keys(extraHeaders).forEach(function (k) {
          signHdrs[k.toLowerCase()] = extraHeaders[k];
        });
      }

      var sortedKeys = Object.keys(signHdrs).sort();
      var canonicalHeaders = sortedKeys.map(function (k) { return k + ":" + signHdrs[k]; }).join("\n") + "\n";
      var signedHeaders = sortedKeys.join(";");
      var canonicalRequest = method + "\n" + encodedPath + "\n" + canonicalQS + "\n" + canonicalHeaders + "\n" + signedHeaders + "\n" + payloadHash;

      var scope = dateStamp + "/" + region + "/s3/aws4_request";
      var stringToSign = "AWS4-HMAC-SHA256\n" + amzDate + "\n" + scope + "\n" + sha256Hex(canonicalRequest);
      var sig = hmacSha256(signingKey(dateStamp), stringToSign).toString("hex");
      var auth = "AWS4-HMAC-SHA256 Credential=" + CONFIG.access_key + "/" + scope + ", SignedHeaders=" + signedHeaders + ", Signature=" + sig;

      // HTTP request headers (unsigned Content-Length + auth added here)
      var reqHeaders = {
        "x-amz-content-sha256": payloadHash,
        "x-amz-date": amzDate,
        Authorization: auth,
        // Node omits the default port (443) from the Host header it generates, while
        // the signature below covers CONFIG.endpoint including an explicit :443.
        // Send the signed value verbatim so the server and the signature agree.
        Host: CONFIG.endpoint,
      };
      if (payload.length > 0) reqHeaders["Content-Length"] = payload.length;
      if (extraHeaders) {
        Object.keys(extraHeaders).forEach(function (k) {
          reqHeaders[k] = extraHeaders[k];
        });
      }

      var req = https.request(
        {
          hostname: ENDPOINT_HOST,
          port: ENDPOINT_PORT || undefined,
          path: encodedPath + (canonicalQS ? "?" + canonicalQS : ""),
          method: method,
          timeout: 30000,
          agent: agent,
          headers: reqHeaders,
        },
        function (res) {
          // Collect the chunks and decode once. Appending a Buffer to a string decodes each
          // chunk separately, so a multibyte character straddling a chunk boundary turns into
          // mojibake — and R2 echoes the key back in its error XML, where keys are not ASCII.
          var chunks = [];
          res.on("data", function (c) { chunks.push(c); });
          res.on("end", function () {
            var body = Buffer.concat(chunks).toString("utf-8");
            if (res.statusCode >= 200 && res.statusCode < 300) resolve({ status: res.statusCode, body: body, headers: res.headers || {} });
            else {
              var err = new Error("HTTP " + res.statusCode + " — " + parseR2Error(body));
              err.statusCode = res.statusCode;
              reject(err);
            }
          });
        }
      );
      req.on("timeout", function () { req.destroy(new Error("Request timed out")); });
      req.on("error", reject);
      req.end(payload.length > 0 ? payload : undefined);
    });
  }

  // Object writes and reads retry transient failures: throttling (429), 5xx and network
  // errors — notably ECONNRESET on a keep-alive socket the server already closed, which
  // otherwise failed a whole setup run on one stale connection. 4xx answers are final.
  var MAX_ATTEMPTS = 3;
  function isTransient(e) {
    if (e.statusCode) return e.statusCode === 429 || e.statusCode >= 500;
    return true; // no HTTP status: socket/DNS/timeout
  }
  function s3Fetch(method, resourcePath, query, payload, extraHeaders) {
    // Replaying a bucket-wide replacement after a lost response can overwrite a
    // policy edited since our read. Let the operator re-read on the next setup.
    if (query === "lifecycle" && method !== "GET") return s3FetchOnce(method, resourcePath, query, payload, extraHeaders);
    var attempt = 0;
    function tryOnce() {
      attempt++;
      return s3FetchOnce(method, resourcePath, query, payload, extraHeaders).catch(function (e) {
        if (attempt >= MAX_ATTEMPTS || !isTransient(e)) throw e;
        var delay = 500 * Math.pow(2, attempt - 1);
        console.error("  retry " + attempt + "/" + (MAX_ATTEMPTS - 1) + " after " + (e.message || e) + "");
        return new Promise(function (r) { setTimeout(r, delay); }).then(tryOnce);
      });
    }
    return tryOnce();
  }

  // ── File Upload ──
  function getContentType(filePath) {
    return CONTENT_TYPES[path.extname(filePath).toLowerCase()] || "application/octet-stream";
  }

  var CACHE_IMMUTABLE = "public, max-age=31536000, immutable";
  var CACHE_SHORT = "public, max-age=300";

  function cacheControlFor(remoteKey) {
    var ext = path.extname(remoteKey).toLowerCase();
    if (/^assets\/[a-f0-9]{64}\//.test(remoteKey) && (ext === ".js" || ext === ".css")) return CACHE_IMMUTABLE;
    return CACHE_SHORT;
  }

  function putObject(payload, remoteKey, conditions) {
    var ct = getContentType(remoteKey);
    return s3Fetch("PUT", "/" + CONFIG.bucket + "/" + remoteKey, null, payload, {
      "Content-Type": ct,
      "Cache-Control": cacheControlFor(remoteKey),
      ...conditions,
    }).then(function () { console.log("  OK  " + remoteKey); });
  }

  // ── Server Deployment and Lifecycle ──
  // Lifecycle administration is opt-in. It is a bucket-level request and needs an
  // Admin token, while publishing one document only ever needs object writes — so an
  // absent expire_days means this tool never sends one at all, and an object-scoped
  // token is enough. null ("do not touch the bucket") is not the same as
  // expire_days: 0 ("remove this skill's rule, leave every other rule alone").
  function expireDays() {
    var d = CONFIG.expire_days;
    if (d == null || d === "") return null;
    if ((typeof d !== "number" && !(typeof d === "string" && /^\d+$/.test(d))) ||
        !Number.isSafeInteger(Number(d)) || Number(d) < 0) {
      throw new Error("CONFIG_INVALID: expire_days must be a non-negative integer");
    }
    return Number(d);
  }

  // Fingerprints the viewer, not the retention setting: whether the site files in the
  // bucket are the ones in this skill. Leaving expire_days out means editing the
  // expiry does not make a current deployment look unprovisioned.
  var deployment;
  function viewer() {
    if (!deployment) deployment = createViewerDeployment();
    return deployment;
  }
  function deployFingerprint() {
    return CONFIG.endpoint + "/" + CONFIG.bucket + "@" + viewer().hash;
  }

  // ── S3 Lifecycle Rule ──
  var LIFECYCLE_RULE_ID = "md-web-auto-expire";

  // S3 has no per-rule lifecycle API: PUT ?lifecycle replaces the whole
  // configuration. Every write below is therefore a read-modify-write — read what the
  // bucket has, keep the rules that are not ours, then write. Blanking the config and
  // PUTting one rule erased the user's own retention rules, and expire_days: 0 used to
  // DELETE the entire configuration outright; both destroyed policy this skill never
  // owned.
  function readLifecycle() {
    return s3Fetch("GET", "/" + CONFIG.bucket, "lifecycle")
      .then(function (r) { return { xml: r.body, transitionMinimum: r.headers["x-amz-transition-default-minimum-object-size"] }; })
      .catch(function (e) {
        // NoSuchLifecycleConfiguration is the only "there is nothing there" answer.
        // AccessDenied and transport failures must abort instead: writing back a
        // config we failed to read would delete rules we never saw.
        if (/NoSuchLifecycle/i.test(e.message || "")) return { xml: "", transitionMinimum: null };
        throw e;
      });
  }

  // Scoped to md-web's own uploads (the "md-web/" key prefix) — never the viewer
  // files at the bucket root, nor any unrelated object sharing the bucket.
  function expiryRule(days) {
    return '<Rule><ID>' + LIFECYCLE_RULE_ID + '</ID>' +
      '<Filter><Prefix>' + UPLOAD_PREFIX + '</Prefix></Filter>' +
      '<Status>Enabled</Status>' +
      '<Expiration><Days>' + days + '</Days></Expiration>' +
      '</Rule>';
  }

  function writeLifecycle(configuration, method, payload, headers) {
    // The lifecycle API has no atomic per-rule/CAS operation. Detect edits since
    // the initial read, and never blindly retry this bucket-wide replacement.
    return readLifecycle().then(function (current) {
      if (current.xml !== configuration.xml || current.transitionMinimum !== configuration.transitionMinimum)
        throw new Error("lifecycle changed during setup; no policy written — serialize policy administration and retry");
      return s3Fetch(method, "/" + CONFIG.bucket, "lifecycle", payload, headers);
    });
  }

  function putLifecycle(rules, extras, transitionMinimum, opening, configuration) {
    var xml = opening +
      (extras || "") + rules.join("") + '</LifecycleConfiguration>';
    var payload = Buffer.from(xml, "utf-8");
    var md5 = crypto.createHash("md5").update(payload).digest("base64");
    var headers = { "Content-Type": "application/xml", "Content-MD5": md5 };
    if (transitionMinimum) headers["x-amz-transition-default-minimum-object-size"] = transitionMinimum;
    return writeLifecycle(configuration, "PUT", payload, headers);
  }

  function setLifecycleRule() {
    var days = expireDays();
    if (days === null) {
      console.log("  Lifecycle: untouched (set expire_days to let this skill manage it)");
      return Promise.resolve();
    }

    return readLifecycle()
      .then(function (configuration) {
        var existing = configuration.xml;
        var transitionMinimum = configuration.transitionMinimum;
        var parsed = parseLifecycleConfiguration(existing);
        var others = parsed.rules;
        var extras = parsed.extras;
        var wanted = days > 0 ? [expiryRule(days)] : [];

        if (!wanted.length && !others.length) {
          // No md-web rule or user-owned rule remains. The lifecycle document
          // is empty, so DELETE preserves all retained rules. The read above
          // establishes this precondition before any policy write.
          if (!parsed.hadRules) {
            console.log("  Lifecycle: nothing to remove");
            return null;
          }
          // DELETE removes the whole document, including top-level settings that are
          // not rules; keep those by rewriting a configuration with only the extras.
          if (extras) {
            return putLifecycle([], extras, transitionMinimum, parsed.opening, configuration).then(function () {
              console.log("  Lifecycle: no expiry (the md-web rule was removed; other settings preserved)");
            });
          }
          return writeLifecycle(configuration, "DELETE")
            .then(function () { console.log("  Lifecycle: no expiry"); });
        }

        return putLifecycle(wanted.concat(others), extras, transitionMinimum, parsed.opening, configuration).then(function () {
          console.log("  Lifecycle: " + (days > 0 ? days + " days (md-web/ only)" : "no expiry (only the md-web rule was removed)"));
        });
      })
      // Report the failure either way: swallowing it meant a token without lifecycle
      // permission produced no output at all, so the bucket kept whatever rule it had
      // while the config said otherwise.
      .catch(function (e) {
        var msg = e.message || "";
        console.error("  Warning: lifecycle — " + msg +
          (msg.indexOf("AccessDenied") !== -1
            ? " (token needs Admin Read & Write, or set the rule in the Cloudflare Dashboard)"
            : ""));
      });
  }

  function serverDeployed() {
    // A local hint cannot establish remote shared state: another installation may
    // have replaced or removed the entry point since this machine ran setup.
    try {
      if (fs.readFileSync(DEPLOYED_FLAG, "utf-8") === deployFingerprint()) {
        return readViewer().then(function (remote) {
          return remote !== null && remote.body === viewer().index.toString("utf8");
        });
      }
    } catch (_) {}
    return Promise.resolve(false);
  }

  function readViewer() {
    return s3Fetch("GET", "/" + CONFIG.bucket + "/index.html")
      .catch(function (e) {
        if (e.statusCode === 404) return null;
        throw e; // Never treat AccessDenied or a transport failure as absence.
      });
  }

  function deployServer() {
    var files = viewer().files;

    // Parallel upload (work-stealing, 4 concurrent)
    var concurrency = 4;
    var idx = 0;
    function next() {
      if (idx >= files.length) return Promise.resolve();
      var file = files[idx++];
      return putObject(file.payload, file.key).then(next);
    }

    return readViewer().then(function (remote) {
      if (remote && !remote.headers.etag) throw new Error("SETUP_CONFLICT: index.html has no ETag; cannot safely replace it");
      var conditions = remote ? { "If-Match": remote.headers.etag } : { "If-None-Match": "*" };
      var workers = [];
      for (var i = 0; i < Math.min(concurrency, files.length); i++) workers.push(next());
      return Promise.allSettled(workers).then(function (results) {
        var failure = results.find(function (result) { return result.status === "rejected"; });
        if (failure) throw failure.reason;
        // Versioned assets stay available to old pages. Switch the entry point
        // last; its precondition prevents concurrent setups silently clobbering it.
        return putObject(viewer().index, "index.html", conditions).catch(function (e) {
          if (e.statusCode === 409 || e.statusCode === 412)
            throw new Error("SETUP_CONFLICT: index.html changed during setup; inspect the active viewer before retrying");
          throw e;
        });
      });
    })
      .then(function () { return readViewer(); })
      .then(function (remote) {
        if (!remote || remote.body !== viewer().index.toString("utf8"))
          throw new Error("SETUP_CONFLICT: the active viewer differs after setup; no local deployment recorded");
      })
      .then(function () { return setLifecycleRule(); })
      .then(function () {
        try { fs.writeFileSync(DEPLOYED_FLAG, deployFingerprint()); } catch (_) {}
        console.log("Docsify server deployed.\n");
      });
  }

  var UPLOAD_PREFIX = "md-web/";

  // ── Main ──
  // Provisioning and publishing are separate commands on purpose. Publishing used to
  // deploy the whole viewer whenever the fingerprint did not match, so an ordinary
  // publish could rewrite index.html and every asset at the bucket root — shared state
  // every published document depends on — as a side effect of publishing one document.
  // It now refuses and names the one command that provisions it.
  function setup() {
    expireDays(); // Reject malformed retention settings before any writes.
    console.log("Provisioning viewer: index.html + assets at the bucket root, then the lifecycle rule.");
    return deployServer().then(function () {
      console.log("Viewer ready: " + CONFIG.public_url + "/index.html");
    });
  }

  function publish() {
    return serverDeployed().then(function (deployed) {
      if (!deployed) {
        throw new Error("SETUP_REQUIRED: the viewer is not provisioned for this bucket/version yet. Run once: " + SCRIPT_CMD + " " + SETUP_FLAG);
      }
      var key = UPLOAD_PREFIX + addTimestamp(args[1]);
      return putObject(prepareMarkdown(fs.readFileSync(localPath)), key).then(function () {
        var name = key.replace(/\.md$/i, "");
        // The key is percent-encoded on the way in (uriEncodePath in s3Fetch), so it has to be
        // encoded on the way out too: a raw space ends the link the moment anything parses it.
        console.log("\n" + CONFIG.public_url + "/index.html#/" + name.split("/").map(encodeURIComponent).join("/"));
      });
    });
  }

  // setup() reads the viewer directory synchronously, so a missing file throws
  // before any promise exists. Without this wrapper the throw escapes as a raw
  // stack trace and the documented UPLOAD_FAILED contract never appears.
  var completion = Promise.resolve()
    .then(function () {
      return isSetup ? setup() : publish();
    })
    .then(function () {
      agent.destroy();
    })
    .catch(function (e) {
      console.error("UPLOAD_FAILED: " + e.message);
      agent.destroy();
      // Set exitCode instead of process.exit() so the URL/error line is flushed
      // to a piped stdout/stderr before the process exits (process.exit can
      // truncate async pipe writes on Linux/macOS — the skill captures this output).
      process.exitCode = 1;
    });
}
