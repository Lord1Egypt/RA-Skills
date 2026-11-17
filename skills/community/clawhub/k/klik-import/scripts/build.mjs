import * as esbuild from 'esbuild';

await esbuild.build({
  entryPoints: ['src/cli.ts'],
  bundle: true,
  format: 'esm',
  platform: 'node',
  target: 'node18',
  outfile: 'dist/klik-import.mjs',
  banner: { js: '#!/usr/bin/env node' },
  minify: false,
  sourcemap: false,
});

console.log('dist/klik-import.mjs built');
