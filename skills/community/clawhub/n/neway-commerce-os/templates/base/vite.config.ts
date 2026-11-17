import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// `static/` is the public dir, so bundled demo images resolve as `/images/<file>.jpg`
// and are copied into `dist/images/` on build.
export default defineConfig({
  plugins: [react()],
  publicDir: "static",
  server: {
    port: 5173,
  },
});
