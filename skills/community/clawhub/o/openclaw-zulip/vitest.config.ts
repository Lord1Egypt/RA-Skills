import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    include: ["src/**/*.test.ts"],
    exclude: [
      // These test files use node:test runner, not vitest
      "src/metadata/command-handler.test.ts",
      "src/metadata/command-parser.test.ts",
      "src/metadata/store.test.ts",
    ],
    environment: "node",
  },
});
