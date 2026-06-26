// Check for kungfu-finance skill updates on ClawHub registry.
// Makes ONE GET request to ClawHub (public, no auth, no secrets sent).
// Does NOT write any files. Does NOT spawn subprocesses.
// Local version is read from package.json via a separate utility.
import { getLocalSkillVersion } from "./update_version_reader.mjs";

const CLAWHUB_API = "https://wry-manatee-359.convex.site";
const CLAWHUB_FALLBACK = "https://clawhub.ai";
const SKILL_SLUG = "kungfu-finance";

function compareSemver(a, b) {
  const pa = a.split(".").map(Number);
  const pb = b.split(".").map(Number);
  for (let i = 0; i < 3; i++) {
    if ((pa[i] || 0) < (pb[i] || 0)) return -1;
    if ((pa[i] || 0) > (pb[i] || 0)) return 1;
  }
  return 0;
}

async function tryFetch(baseUrl) {
  const url = `${baseUrl}/api/v1/skills/${SKILL_SLUG}`;
  const res = await fetch(url, {
    headers: { Accept: "application/json" },
    signal: AbortSignal.timeout(15000)
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`${res.status}: ${text.slice(0, 200)}`);
  }
  return res.json();
}

async function fetchLatestVersion() {
  let data;
  try {
    data = await tryFetch(CLAWHUB_API);
  } catch {
    data = await tryFetch(CLAWHUB_FALLBACK);
  }
  const ver = data?.latestVersion?.version;
  if (!ver) throw new Error("ClawHub response missing latestVersion.version");
  return {
    version: ver,
    created_at: data.latestVersion.createdAt || null,
    changelog: data.latestVersion.changelog || null
  };
}

export async function runCheckUpdateFlow() {
  const localVersion = getLocalSkillVersion();
  if (!localVersion) {
    return {
      update_available: false,
      error: "Cannot determine local version — package.json not found"
    };
  }

  let remote;
  try {
    remote = await fetchLatestVersion();
  } catch (err) {
    return {
      update_available: false,
      local_version: localVersion,
      error: `Failed to check ClawHub: ${err.message}`
    };
  }

  const cmp = compareSemver(localVersion, remote.version);

  if (cmp >= 0) {
    return {
      update_available: false,
      local_version: localVersion,
      remote_version: remote.version,
      message: cmp === 0
        ? "Already up to date."
        : `Local version (${localVersion}) is ahead of registry (${remote.version}).`
    };
  }

  return {
    update_available: true,
    local_version: localVersion,
    remote_version: remote.version,
    changelog: remote.changelog,
    update_command: `clawhub update ${SKILL_SLUG}`,
    message: `Update available: ${localVersion} → ${remote.version}`
  };
}
