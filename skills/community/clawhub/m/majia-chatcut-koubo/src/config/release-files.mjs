import fs from "node:fs";

export const RELEASE_VERSION = JSON.parse(fs.readFileSync(new URL("../../package.json", import.meta.url), "utf8")).version;
export const LIVE_CANARY_REPORT = `reports/live-canary-v${RELEASE_VERSION}.json`;
