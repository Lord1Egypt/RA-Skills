import { defineConfig } from 'vite';

export default defineConfig({
  server: {
    proxy: {
      '/auth': 'http://localhost:3000',
      '/dashboard': 'http://localhost:3000'
    }
  }
});
