import react from '@vitejs/plugin-react';
import { defineConfig } from 'vite';

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'dist',
    emptyOutDir: true,
  },
  base: './',
  server: {
    port: 5061,
    proxy: {
      '/ws': {
        target: 'ws://localhost:5070',
        ws: true,
      },
      '/assets': {
        target: 'http://localhost:5070',
      },
      '/api': {
        target: 'http://localhost:5070',
      },
    },
  },
});
