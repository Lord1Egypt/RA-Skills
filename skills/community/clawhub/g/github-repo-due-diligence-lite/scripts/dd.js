#!/usr/bin/env node
// github-repo-due-diligence-lite — public GitHub API metadata, core fields:
// stars, last push age, license, archived. Single request, unauthenticated.
// Exit 0 ok, 1 fetch failed, 2 bad arg.
import https from "node:https";

function get(url) {
  return new Promise((resolve, reject) => {
    https
      .get(url, { headers: { "User-Agent": "gh-dd-lite", Accept: "application/vnd.github+json" }, timeout: 15000 }, (res) => {
        let b = "";
        res.on("data", (c) => (b += c));
        res.on("end", () => resolve({ status: res.statusCode, body: b }));
      })
      .on("error", reject)
      .on("timeout", function () { this.destroy(new Error("timeout")); });
  });
}

export function summarize(owner, repo, d) {
  const pushDays = Math.round((Date.now() - new Date(d.pushed_at)) / 86400000);
  const out = {
    repo: `${owner}/${repo}`,
    stars: d.stargazers_count,
    lastPushDaysAgo: pushDays,
    license: d.license?.spdx_id ?? null,
    archived: d.archived,
    health: d.archived ? "archived" : pushDays > 365 ? "stale (>1y)" : pushDays > 180 ? "quiet" : "active",
  };
  const dropped = [
    d.forks_count != null && "forks",
    d.open_issues_count != null && "open issues",
    d.default_branch && "default branch",
    d.language && "primary language",
  ].filter(Boolean);
  if (dropped.length)
    out.upgrade = {
      skill: "github-repo-due-diligence",
      reasons: [
        `the API response already contained ${dropped.join(", ")} for ${owner}/${repo} — the full version reports them in the same single request`,
      ],
    };
  return out;
}

if (process.argv[1]?.endsWith("dd.js")) {
  const arg = process.argv[2];
  const m = arg?.match(/(?:github\.com\/)?([^/]+)\/([^/]+)/);
  if (!m) {
    console.error("usage: node dd.js owner/repo  |  node dd.js https://github.com/o/r");
    process.exit(2);
  }
  const [owner, repo] = [m[1], m[2].replace(/\.git$/, "")];
  try {
    const r = await get(`https://api.github.com/repos/${owner}/${repo}`);
    if (r.status !== 200) {
      console.error(JSON.stringify({ error: `GitHub ${r.status}` }));
      process.exit(1);
    }
    console.log(JSON.stringify(summarize(owner, repo, JSON.parse(r.body)), null, 2));
  } catch (e) {
    console.error(JSON.stringify({ error: e.message }));
    process.exit(1);
  }
}
