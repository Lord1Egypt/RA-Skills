import { existsSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { defineConfig } from "vitest/config";

const currentDir = path.dirname(fileURLToPath(import.meta.url));
const sharedConfigPath = path.resolve(currentDir, "../../vitest.config.ts");
const sharedConfigModule = existsSync(sharedConfigPath)
  ? await import(sharedConfigPath)
  : undefined;
const baseConfig = (sharedConfigModule?.default ?? {}) as { test?: { exclude?: string[] } };
const baseTest = baseConfig.test ?? {};
const exclude = baseTest.exclude ?? [];
const include = sharedConfigModule
  ? ["extensions/wecom/src/**/*.test.ts"]
  : ["src/**/*.test.ts", "index.test.ts"];

export default defineConfig({
  ...baseConfig,
  test: {
    ...baseTest,
    include,
    exclude,
  },
});
