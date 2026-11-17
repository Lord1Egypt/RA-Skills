import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    projects: ['packages/*'],
    // Les tests touchent des DB SQLite sur disque (tmpdir) — pas de parallélisme intra-fichier.
    fileParallelism: true,
  },
})
