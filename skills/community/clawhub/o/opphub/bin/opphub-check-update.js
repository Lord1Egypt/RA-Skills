#!/usr/bin/env node
// opphub-check-update.js · v4.0.1.5
// status: implemented (远端版本比对)
//
// 用途: 检查 skill 自身是否有新版本 (供 plugin 调用)
//   - 本输出 不直接 console.log 推 IM (plugin 负责)
//   - 返回 JSON 结构 ({ ok, status, local, remote, commits, ... }) 供 plugin 渲染后 推 IM

import { exec } from "node:child_process";
import { promisify } from "node:util";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";
import { existsSync, readFileSync } from "node:fs";
const execp = promisify(exec);
const __skillDir = dirname(fileURLToPath(import.meta.url));

//   - 默认 mode=json: 返回 JSON 给 plugin 拿去渲染 + 推 IM
//   - mode=notify: 老 cron 路径保留 (可以兼容), console.log 一行
function out(obj, mode = "json") {
  const status = obj?.status ?? "ok";
  if (mode === "notify") {
    if (status === "upgrade_available") {
      // 兼容老 cron
      console.log(`🆕 opphub skill v${obj.remote} (当前 v${obj.local})`);
      console.log(`升级: ${obj.upgrade_cmd ?? "clawhub install opphub"}`);
      if (obj.local && obj.remote) {
        console.log(`变更: https://github.com/mtty-ai/opphub-skill/compare/v${obj.local}...v${obj.remote}`);
      }
    } else if (obj.ok === false) {
      console.log(`⚠️ check-update 异常: ${obj.error ?? "unknown"}`);
    }
  } else {
    // mode=json 默认: plugin 从stdout 走一行 JSON 拿
    if (obj.ok === false) {
      // 异常也是 stdout (plugin 不走 stderr, 一行 JSON 拿总状)
      console.log(JSON.stringify({ ...obj, status: "error" }));
    } else {
      console.log(JSON.stringify(obj));
    }
  }
}

async function getLocalVersion() {
  // openclaw skills info --json 不返 version, 直接读 SKILL.md frontmatter
  // skill 安装路径可能在多个位置, 按优先级探测
  const candidates = [
    process.env.OPPHUB_SKILL_DIR,
    join(__skillDir, ".."),  // bin/ 的上一级
    join(process.env.HOME || "", ".openclaw/skills/opphub"),
  ].filter(Boolean);
  for (const dir of candidates) {
    const md = join(dir, "SKILL.md");
    if (process.env.OPPHUB_DEBUG) console.error(`[debug] try: ${dir}/SKILL.md`);
    if (existsSync(md)) {
      try {
        const content = readFileSync(md, "utf8");
        const m = content.match(/^---\n([\s\S]*?)\n---/);
        if (m) {
          const fm = m[1];
          const vMatch = fm.match(/^version:\s*["']?([^"'\n]+?)["']?\s*$/m);
          if (process.env.OPPHUB_DEBUG) console.error(`[debug] vMatch=${JSON.stringify(vMatch)}`);
          if (vMatch) return vMatch[1].trim();
        }
      } catch (e) {
        if (process.env.OPPHUB_DEBUG) console.error(`[debug] err: ${e.message}`);
      }
    }
  }
  return null;
}

async function getRemoteVersion() {
  try {
    const { stdout } = await execp(
      "gh release view --repo mtty-ai/opphub-skill --json tagName -q .tagName 2>/dev/null"
    );
    const v = stdout.trim().replace(/^v/, "");
    if (v) return v;
  } catch {}
  try {
    const { stdout } = await execp(
      "gh api repos/mtty-ai/opphub-skill/contents/_meta.json --jq .content 2>/dev/null"
    );
    const decoded = Buffer.from(stdout.trim(), "base64").toString("utf8");
    const meta = JSON.parse(decoded);
    return meta.version ?? null;
  } catch {
    return null;
  }
}

// 去 "v" 前缀 (gh release tag 返 "v4.0.1", _meta.json 返 "4.0.1")
function stripPrefix(v) {
  return String(v).replace(/^v/, "");
}

function compareSemver(a, b) {
  // 用 字符串数组比, 只要 主.次.补丁 都同名, 就 localeCompare 预发布部分
  const mainA = stripPrefix(a);
  const mainB = stripPrefix(b);
  if (mainA !== mainB) {
    const na = mainA.split(".").map((x) => parseInt(x, 10) || 0);
    const nb = mainB.split(".").map((x) => parseInt(x, 10) || 0);
    for (let i = 0; i < Math.max(na.length, nb.length); i++) {
      if (na[i] !== nb[i]) return na[i] - nb[i];
    }
  }
  // 主版本同 → 预发布标签 (alpha.x) 拿 X 比
  const preA = (a.split("-")[1] ?? "999").match(/\d+/)?.[0] ?? "999";
  const preB = (b.split("-")[1] ?? "999").match(/\d+/)?.[0] ?? "999";
  return parseInt(preA, 10) - parseInt(preB, 10);
}

async function main() {
  //   cli 用法: `node opphub-check-update.js [--mode=notify|json]` [--kind=skill|plugin]
  //   --mode=notify (旧, cron 场景)  --mode=json (默认, plugin 场景)
  //   --kind=skill 查 skill, --kind=plugin 查 plugin (拿 不同仓的 SKILL.md / openclaw.plugin.json)
  const args = process.argv.slice(2);
  const opts = Object.fromEntries(args.filter(a => a.startsWith("--")).map(a => {
    const [k, v] = a.replace("--", "").split("=");
    return [k, v ?? "true"];
  }));

  const kind = opts.kind ?? "skill";
  // 现在仅 本文件处理 skill (plugin 仓里有自己 的 check-update.ts)
  // plugin 仓调本脚本 是为了查 skill
  // --kind=plugin 暂作未实现 (plugin 仓提供同 API)
  if (kind !== "skill") {
    out({ ok: false, status: "invalid_kind", reason: "仅 skill 本仓查, 请在 plugin 仓 调 plugin/check-update.ts" }, opts.mode);
    return;
  }

  const local = await getLocalVersion();
  const remote = await getRemoteVersion();
  if (process.env.OPPHUB_DEBUG) {
    console.error(`[debug] local=${JSON.stringify(local)} remote=${JSON.stringify(remote)}`);
  }

  if (!local) {
    out({ ok: true, status: "unknown", reason: "local version 不可读, 静默" }, opts.mode);
    return;
  }
  if (!remote) {
    out({ ok: true, status: "unknown", reason: "remote version 不可读, 静默", local }, opts.mode);
    return;
  }

  const cmp = compareSemver(local, remote);
  if (cmp < 0) {
    // 仅返 plugin 需要的 fields: local/remote/upgrade_cmd/repo/source
    out({
      ok: true,
      status: "upgrade_available",
      kind: "skill",
      local,
      remote,
      upgrade_cmd: "clawhub install opphub",
      repo: "mtty-ai/opphub-skill",
      source: "github_release_or_meta",
      diff_url: `https://github.com/mtty-ai/opphub-skill/compare/v${local}...v${remote}`,
    }, opts.mode);
    return;
  }

  out({ ok: true, status: "up_to_date", kind: "skill", local, remote }, opts.mode);
}

main().catch((e) => {
  out({ ok: false, status: "error", error: e?.message ?? String(e) });
  process.exit(0); // 不返非0, 让 cron 标记为 ok
});
