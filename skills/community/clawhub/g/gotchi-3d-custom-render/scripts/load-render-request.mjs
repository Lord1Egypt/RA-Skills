#!/usr/bin/env node

import fs from "node:fs";

export function loadRenderRequest(inputJsonPath) {
  return JSON.parse(fs.readFileSync(inputJsonPath, "utf8"));
}
