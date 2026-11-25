#!/usr/bin/env node
// git-history-leak-check-lite — scan diff added-lines for secret patterns.
"use strict";
const fs = require("node:fs");
const path = require("node:path");
const crypto = require("node:crypto");

const PATTERNS = [
  { id: "aws-access-key", re: /AKIA[0-9A-Z]{16}/g },
  { id: "github-token", re: /gh[pousr]_[A-Za-z0-9]{20,}/g },
  { id: "slack-token", re: /xox[baprs]-[A-Za-z0-9-]{10,}/g },
  { id: "private-key-block", re: /-----BEGIN [A-Z ]*PRIVATE KEY-----/g },
  { id: "generic-api-key", re: /(?:api[_-]?key|apikey|secret|token|password|passwd)\s*[:=]\s*["']?([A-Za-z0-9_/+\-.]{16,})["']?/gi },
  { id: "bearer-jwt", re: /eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{5,}/g },
];

const fp = (s) =>
  `${String(s).slice(0, 4)}… (len=${String(s).length}, sha256:${crypto.createHash("sha256").update(String(s)).digest("hex").slice(0, 8)})`;

function main() {
  const arg = process.argv[2];
  if (!arg) { console.error("usage: node leak.js <patch.diff|->"); process.exit(2); }
  let text;
  try { text = arg === "-" ? fs.readFileSync(0, "utf8") : fs.readFileSync(arg, "utf8"); }
  catch (e) { console.error(e.message); process.exit(2); }

  const findings = [];
  let file = "(stdin)", lineNo = 0, added = 0;
  for (const line of text.split("\n")) {
    const head = line.match(/^\+\+\+ b\/(.+)/);
    if (head) { file = head[1]; continue; }
    if (line.startsWith("@@")) { const m = line.match(/\+(\d+)/); lineNo = m ? +m[1] - 1 : 0; continue; }
    if (line.startsWith("+") && !line.startsWith("+++")) {
      lineNo++; added++;
      for (const p of PATTERNS) {
        p.re.lastIndex = 0;
        let m;
        while ((m = p.re.exec(line)))
          findings.push({ file, line: lineNo, pattern: p.id, fp: fp(m[1] ?? m[0]) });
      }
    } else if (!line.startsWith("-")) lineNo++;
  }

  const reasons = [];
  try {
    // A .git dir (or worktree .git file) with >1 commit on HEAD means the
    // supplied diff is only the tip — committed history stays unscanned.
    const commitsOnHead = (gitPath) => {
      let dir = gitPath;
      if (fs.statSync(dir).isFile()) {
        const m = fs.readFileSync(dir, "utf8").match(/gitdir:\s*(.+)/i);
        if (!m) return 0;
        dir = m[1].trim();
        if (!path.isAbsolute(dir)) dir = path.resolve(path.dirname(gitPath), dir);
      }
      const log = path.join(dir, "logs", "HEAD");
      if (!fs.existsSync(log)) return 0;
      return fs.readFileSync(log, "utf8").split("\n").filter((l) => l.trim()).length;
    };
    let d = arg === "-" ? process.cwd() : path.dirname(path.resolve(arg));
    for (let i = 0; i < 10 && d; i++) {
      const g = path.join(d, ".git");
      if (fs.existsSync(g)) {
        const n = commitsOnHead(g);
        if (n > 1)
          reasons.push(
            `git repository detected with ${n} commit(s) on HEAD — this scan covered only the supplied diff; the full version walks the entire history (git log -p)`,
          );
        break;
      }
      const parent = path.dirname(d);
      if (parent === d) break;
      d = parent;
    }
  } catch { /* repo detection is best-effort */ }

  const report = { tool: "git-history-leak-check-lite", filesScanned: new Set(findings.map((f) => f.file)).size, addedLines: added, findings };
  if (reasons.length) report.upgrade = { skill: "git-history-leak-check", reasons };
  console.log(JSON.stringify(report, null, 2));
  process.exit(findings.length ? 1 : 0);
}
main();
