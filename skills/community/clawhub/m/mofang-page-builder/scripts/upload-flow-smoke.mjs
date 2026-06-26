#!/usr/bin/env node
/**
 * 本地 mock 魔方建站 + 上传接口，用于验证 deploy.mjs 全流程（不上生产）。
 * 用法：node scripts/upload-flow-smoke.mjs
 */
import { createServer } from 'http';
import { spawn } from 'child_process';
import { mkdtempSync, writeFileSync, rmSync } from 'fs';
import { tmpdir } from 'os';
import { dirname, join, resolve } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const SPACE_ID = '00000000-0000-0000-0000-000000000099';
const WEBSITE_ID = '11111111-1111-1111-1111-111111111111';

const server = createServer((req, res) => {
  const host = req.headers.host || '127.0.0.1';
  const u = new URL(req.url || '/', `http://${host}`);

  if (req.method === 'POST' && u.pathname === '/magicflu/jwt') {
    res.writeHead(200, {
      'Content-Type': 'application/json; charset=utf-8',
      'Set-Cookie': 'JSESSIONID=smoke-mock; Path=/',
    });
    res.end(JSON.stringify({ token: 'smoke-jwt-token' }));
    return;
  }

  if (req.method === 'GET' && u.pathname === '/magicflu/service/json/spaces/feed') {
    res.writeHead(200, { 'Content-Type': 'application/json', 'Set-Cookie': 'JSESSIONID=smoke-probe; Path=/' });
    res.end('{}');
    return;
  }

  if (req.method === 'POST' && u.pathname === `/magicflu/service/s/${SPACE_ID}/websites`) {
    let raw = '';
    req.setEncoding('utf8');
    req.on('data', (c) => {
      raw += c;
    });
    req.on('end', () => {
      if (!raw.includes('<website>')) {
        res.writeHead(400);
        res.end('expected website xml');
        return;
      }
      res.writeHead(201, { 'Content-Type': 'text/plain; charset=utf-8' });
      res.end(WEBSITE_ID);
    });
    return;
  }

  if (
    req.method === 'POST' &&
    u.pathname === '/magicflu/html/sites/connectors/jsp/filemanager.jsp' &&
    u.searchParams.get('spaceId') === SPACE_ID
  ) {
    req.on('data', () => {});
    req.on('end', () => {
      res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
      res.end(`<textarea>${JSON.stringify({ Code: 0, Path: '/x/', Name: 'index.html' })}</textarea>`);
    });
    return;
  }

  if (req.method === 'GET' && u.pathname === '/magicflu/html/sites/site.jsp') {
    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
    res.end('<html></html>');
    return;
  }

  res.writeHead(404, { 'Content-Type': 'text/plain' });
  res.end(`not found: ${req.method} ${u.pathname}`);
});

server.listen(0, '127.0.0.1', () => {
  const addr = server.address();
  const port = typeof addr === 'object' && addr ? addr.port : 0;
  const baseUrl = `http://127.0.0.1:${port}`;
  const work = mkdtempSync(join(tmpdir(), 'mofang-upload-smoke-'));
  const indexPath = join(work, 'index.html');
  writeFileSync(indexPath, '<!doctype html><html><body>smoke upload ok</body></html>\n', 'utf8');

  console.log('mock server:', baseUrl);
  const deploy = spawn(
    process.execPath,
    [
      resolve(__dirname, 'deploy.mjs'),
      '--baseUrl',
      baseUrl,
      '--spaceId',
      SPACE_ID,
      '--label',
      'smoke',
      '--shortcut',
      'smoke',
      '--files',
      indexPath,
      '--username',
      'any',
      '--password',
      'any',
    ],
    { stdio: 'inherit', env: { ...process.env, FETCH_TIMEOUT_MS: '10000' } }
  );

  deploy.on('exit', (code) => {
    server.close();
    try {
      rmSync(work, { recursive: true, force: true });
    } catch {
      /* ignore */
    }
    process.exit(code ?? 1);
  });
});
