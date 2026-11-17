import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    // The arg-shape tests pass arbitrary server paths; confinement is exercised
    // explicitly by the tests that narrow GOG_FILE_ROOTS themselves.
    env: {
      GOG_FILE_ROOTS: '/',
    },
    coverage: {
      provider: 'v8',
      include: ['src/**/*.ts'],
      exclude: ['src/index.ts'],
      thresholds: {
        lines: 100,
        functions: 100,
        branches: 100,
        statements: 100,
      },
    },
  },
});
