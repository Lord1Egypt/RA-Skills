import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: false,
    environment: 'node',
    include: ['tests/**/*.test.js'],
    // Some of our modules still use CommonJS require()
    // This helps with compatibility
    deps: {
      inline: ['ethers'],
    },
  },
});