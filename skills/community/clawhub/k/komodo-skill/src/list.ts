/**
 * List Komodo resources with detailed info.
 *
 * Usage:
 *   bun run scripts/list.ts <type>
 *
 * Types:
 *   servers | stacks | deployments | builds | repos | procedures | actions
 *
 * Examples:
 *   bun run scripts/list.ts servers
 *   bun run scripts/list.ts stacks
 *   bun run scripts/list.ts deployments
 */
import { komodo } from "../openclaw.ts";

const TYPES = ["servers", "stacks", "deployments", "builds", "repos", "procedures", "actions"] as const;
type ListType = (typeof TYPES)[number];

const type = process.argv[2] as ListType | undefined;

if (!type || !TYPES.includes(type)) {
  console.error("Usage: bun run scripts/list.ts <type>");
  console.error("Types:", TYPES.join(" | "));
  process.exit(1);
}

const SEP = "─".repeat(72);

// ── Servers ──────────────────────────────────────────────────────────────────

async function listServers() {
  const servers = await komodo.read("ListServers", {});
  if (servers.length === 0) { console.log("No servers found."); return; }

  const stats = await Promise.all(
    servers.map(async (s) => {
      if (s.info.state !== "Ok") return null;
      try { return await komodo.read("GetSystemStats", { server: s.name }); }
      catch { return null; }
    })
  );

  console.log(`\nServers (${servers.length})\n${SEP}`);
  for (let i = 0; i < servers.length; i++) {
    const s = servers[i]!;
    const st = stats[i];
    const stateLabel =
      s.info.state === "Ok"       ? "● Ok"       :
      s.info.state === "NotOk"    ? "✖ NotOk"    :
                                    "○ Disabled";
    const region  = s.info.region  ? ` [${s.info.region}]`            : "";
    const version = s.info.version ? `  periphery ${s.info.version}`  : "";

    console.log(`${s.name}${region}`);
    console.log(`  ID      : ${s.id}`);
    console.log(`  State   : ${stateLabel}${version}`);
    console.log(`  Address : ${s.info.address}`);

    if (st) {
      const memPerc = ((st.mem_used_gb / st.mem_total_gb) * 100).toFixed(1);
      const diskSummary = st.disks.map((d) => {
        const perc = ((d.used_gb / d.total_gb) * 100).toFixed(1);
        return `${d.mount} ${d.used_gb.toFixed(1)}/${d.total_gb.toFixed(1)} GB (${perc}%)`;
      }).join("  |  ");
      console.log(`  CPU     : ${st.cpu_perc.toFixed(1)}%`);
      console.log(`  Memory  : ${st.mem_used_gb.toFixed(2)}/${st.mem_total_gb.toFixed(2)} GB (${memPerc}%)`);
      console.log(`  Disk    : ${diskSummary}`);
      if (st.load_average) {
        const la = st.load_average;
        console.log(`  Load    : ${la.one.toFixed(2)}  ${la.five.toFixed(2)}  ${la.fifteen.toFixed(2)}  (1m 5m 15m)`);
      }
    }
    console.log(SEP);
  }
}

// ── Stacks ───────────────────────────────────────────────────────────────────

async function listStacks() {
  const stacks = await komodo.read("ListStacks", {});
  if (stacks.length === 0) { console.log("No stacks found."); return; }

  console.log(`\nStacks (${stacks.length})\n${SEP}`);
  for (const s of stacks) {
    const state = s.info.state;
    const stateLabel =
      state === "running"   ? "● running"   :
      state === "stopped"   ? "○ stopped"   :
      state === "paused"    ? "⏸ paused"    :
      state === "deploying" ? "↻ deploying" :
      state === "dead"      ? "✖ dead"      :
                              `  ${state}`;

    const source =
      s.info.repo          ? `${s.info.git_provider}/${s.info.repo}@${s.info.branch}` :
      s.info.file_contents ? "inline file contents" :
      s.info.files_on_host ? "files on host"        : "—";

    const hashLine =
      s.info.deployed_hash && s.info.latest_hash
        ? `deployed=${s.info.deployed_hash}  latest=${s.info.latest_hash}` +
          (s.info.deployed_hash !== s.info.latest_hash ? "  ⚠ update available" : "")
        : s.info.deployed_hash ? `deployed=${s.info.deployed_hash}` : null;

    const services = s.info.services.length
      ? s.info.services.map((sv) =>
          `    • ${sv.service}  image=${sv.image}${sv.update_available ? " [update available]" : ""}`
        ).join("\n")
      : "    (no services)";

    console.log(`${s.name}`);
    console.log(`  ID      : ${s.id}`);
    console.log(`  State   : ${stateLabel}${s.info.status ? `  (${s.info.status})` : ""}`);
    console.log(`  Source  : ${source}`);
    if (hashLine) console.log(`  Commits : ${hashLine}`);
    if (s.info.missing_files.length) console.log(`  ⚠ Missing files: ${s.info.missing_files.join(", ")}`);
    console.log(`  Services:`);
    console.log(services);
    console.log(SEP);
  }
}

// ── Deployments ──────────────────────────────────────────────────────────────

async function listDeployments() {
  const deployments = await komodo.read("ListDeployments", {});
  if (deployments.length === 0) { console.log("No deployments found."); return; }

  console.log(`\nDeployments (${deployments.length})\n${SEP}`);
  for (const d of deployments) {
    const state = d.info.state;
    const stateLabel =
      state === "running"      ? "● running"      :
      state === "exited"       ? "○ exited"       :
      state === "not_deployed" ? "○ not deployed" :
      state === "restarting"   ? "↻ restarting"   :
      state === "paused"       ? "⏸ paused"       :
      state === "dead"         ? "✖ dead"         :
                                 `  ${state}`;

    console.log(`${d.name}`);
    console.log(`  ID      : ${d.id}`);
    console.log(`  State   : ${stateLabel}${d.info.status ? `  (${d.info.status})` : ""}`);
    console.log(`  Image   : ${d.info.image}${d.info.update_available ? "  ⚠ image update available" : ""}`);
    if (d.info.build_id) console.log(`  Build   : ${d.info.build_id}`);
    console.log(SEP);
  }
}

// ── Builds ───────────────────────────────────────────────────────────────────

async function listBuilds() {
  const builds = await komodo.read("ListBuilds", {});
  if (builds.length === 0) { console.log("No builds found."); return; }

  console.log(`\nBuilds (${builds.length})\n${SEP}`);
  for (const b of builds) {
    const state = b.info.state;
    const stateLabel =
      state === "Ok"       ? "● Ok"       :
      state === "Failed"   ? "✖ Failed"   :
      state === "Building" ? "↻ Building" :
                             `  ${state}`;

    const version   = `${b.info.version.major}.${b.info.version.minor}.${b.info.version.patch}`;
    const lastBuilt = b.info.last_built_at ? new Date(b.info.last_built_at).toLocaleString() : "never";
    const source    =
      b.info.repo                ? `${b.info.git_provider}/${b.info.repo}@${b.info.branch}` :
      b.info.dockerfile_contents ? "inline dockerfile" :
      b.info.files_on_host       ? "files on host"     : "—";
    const hashLine =
      b.info.built_hash && b.info.latest_hash
        ? `built=${b.info.built_hash}  latest=${b.info.latest_hash}` +
          (b.info.built_hash !== b.info.latest_hash ? "  ⚠ new commits" : "")
        : b.info.built_hash ? `built=${b.info.built_hash}` : null;

    console.log(`${b.name}`);
    console.log(`  ID        : ${b.id}`);
    console.log(`  State     : ${stateLabel}`);
    console.log(`  Version   : ${version}`);
    console.log(`  Last built: ${lastBuilt}`);
    console.log(`  Source    : ${source}`);
    if (hashLine) console.log(`  Commits   : ${hashLine}`);
    if (b.info.image_registry_domain) console.log(`  Registry  : ${b.info.image_registry_domain}`);
    console.log(SEP);
  }
}

// ── Repos ─────────────────────────────────────────────────────────────────────

async function listRepos() {
  const repos = await komodo.read("ListRepos", {});
  if (repos.length === 0) { console.log("No repos found."); return; }

  console.log(`\nRepos (${repos.length})\n${SEP}`);
  for (const r of repos) {
    const state = r.info.state;
    const stateLabel =
      state === "Ok"       ? "● Ok"       :
      state === "Failed"   ? "✖ Failed"   :
      state === "Cloning"  ? "↻ Cloning"  :
      state === "Pulling"  ? "↻ Pulling"  :
      state === "Building" ? "↻ Building" :
                             `  ${state}`;

    const lastPulled = r.info.last_pulled_at ? new Date(r.info.last_pulled_at).toLocaleString() : "never";
    const lastBuilt  = r.info.last_built_at  ? new Date(r.info.last_built_at).toLocaleString()  : "never";
    const hashLine   = [
      r.info.cloned_hash ? `cloned=${r.info.cloned_hash}` : null,
      r.info.built_hash  ? `built=${r.info.built_hash}`   : null,
      r.info.latest_hash ? `latest=${r.info.latest_hash}` : null,
    ].filter(Boolean).join("  ");

    console.log(`${r.name}`);
    console.log(`  ID         : ${r.id}`);
    console.log(`  State      : ${stateLabel}`);
    console.log(`  Source     : ${r.info.git_provider}/${r.info.repo}@${r.info.branch}`);
    console.log(`  Last pulled: ${lastPulled}`);
    console.log(`  Last built : ${lastBuilt}`);
    if (hashLine) console.log(`  Commits    : ${hashLine}`);
    if (r.info.cloned_message) console.log(`  Message    : ${r.info.cloned_message}`);
    console.log(SEP);
  }
}

// ── Procedures ────────────────────────────────────────────────────────────────

async function listProcedures() {
  const procedures = await komodo.read("ListProcedures", {});
  if (procedures.length === 0) { console.log("No procedures found."); return; }

  console.log(`\nProcedures (${procedures.length})\n${SEP}`);
  for (const p of procedures) {
    const state = p.info.state;
    const stateLabel =
      state === "Ok"      ? "● Ok"      :
      state === "Failed"  ? "✖ Failed"  :
      state === "Running" ? "↻ Running" :
                            `  ${state}`;

    const lastRun = p.info.last_run_at        ? new Date(p.info.last_run_at).toLocaleString()        : "never";
    const nextRun = p.info.next_scheduled_run ? new Date(p.info.next_scheduled_run).toLocaleString() : null;

    console.log(`${p.name}`);
    console.log(`  ID      : ${p.id}`);
    console.log(`  State   : ${stateLabel}`);
    console.log(`  Stages  : ${p.info.stages}`);
    console.log(`  Last run: ${lastRun}`);
    if (nextRun) console.log(`  Next run: ${nextRun}`);
    if (p.info.schedule_error) console.log(`  ⚠ Schedule error: ${p.info.schedule_error}`);
    console.log(SEP);
  }
}

// ── Actions ───────────────────────────────────────────────────────────────────

async function listActions() {
  const actions = await komodo.read("ListActions", {});
  if (actions.length === 0) { console.log("No actions found."); return; }

  console.log(`\nActions (${actions.length})\n${SEP}`);
  for (const a of actions) {
    const state = a.info.state;
    const stateLabel =
      state === "Ok"      ? "● Ok"      :
      state === "Failed"  ? "✖ Failed"  :
      state === "Running" ? "↻ Running" :
                            `  ${state}`;

    const lastRun = a.info.last_run_at        ? new Date(a.info.last_run_at).toLocaleString()        : "never";
    const nextRun = a.info.next_scheduled_run ? new Date(a.info.next_scheduled_run).toLocaleString() : null;

    console.log(`${a.name}`);
    console.log(`  ID      : ${a.id}`);
    console.log(`  State   : ${stateLabel}`);
    console.log(`  Last run: ${lastRun}`);
    if (nextRun) console.log(`  Next run: ${nextRun}`);
    if (a.info.schedule_error) console.log(`  ⚠ Schedule error: ${a.info.schedule_error}`);
    console.log(SEP);
  }
}

// ── Dispatch ──────────────────────────────────────────────────────────────────

switch (type) {
  case "servers":     await listServers();     break;
  case "stacks":      await listStacks();      break;
  case "deployments": await listDeployments(); break;
  case "builds":      await listBuilds();      break;
  case "repos":       await listRepos();       break;
  case "procedures":  await listProcedures();  break;
  case "actions":     await listActions();     break;
}
