import { defineConfig, type PluginOption } from 'vite'
import react from '@vitejs/plugin-react'

// base relative : l'UI est servie par le daemon sous /ui/, pas à la racine.
export default defineConfig({
  base: './',
  // Cast : la racine du monorepo hoiste vite 8 (vitest) alors que ce package
  // utilise vite 7 — les types Plugin divergent, le runtime est compatible.
  plugins: [react() as unknown as PluginOption],
  build: {
    outDir: 'dist',
    emptyOutDir: true,
  },
})
