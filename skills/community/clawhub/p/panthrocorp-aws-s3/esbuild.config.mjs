import { build } from "esbuild";

await build({
  entryPoints: ["src/index.mjs"],
  bundle: true,
  platform: "node",
  target: "node22",
  format: "cjs",
  outfile: "dist/index.cjs",
});
