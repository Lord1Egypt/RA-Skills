import { defineConfig } from "tsup";

export default defineConfig({
  entry: {
    index: "./src/index.ts",
    cli: "./src/cli.ts",
    "mcp-server": "./src/mcp-server.ts",
    types: "./src/types.ts",
    "openclaw-plugin": "./openclaw-plugin.mts",
  },
  clean: true,
  dts: true,
  format: ["esm", "cjs"],
  target: "node18",
  sourcemap: false,
  splitting: false,
  shims: false,
  outDir: "dist",
  bundle: true,
  esbuildOptions(options, context) {
    if (context.format === "esm") {
      options.banner = {
        js: 'import { createRequire as __createRequire } from "node:module"; const require = __createRequire(import.meta.url);',
      };
    }
  },
  outExtension({ format }) {
    return {
      js: format === "esm" ? ".mjs" : ".cjs",
    };
  },
});
