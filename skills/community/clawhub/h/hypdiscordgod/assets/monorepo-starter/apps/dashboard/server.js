import http from 'node:http';

const html = `<!doctype html><html><body style="font-family:sans-serif;padding:24px"><h1>Dashboard Starter</h1><p>This monorepo dashboard is wired to the API service shape.</p><ul><li><a href="http://localhost:3000/health">API health</a></li><li><a href="http://localhost:3000/dashboard/guilds">Guild list</a></li></ul></body></html>`;

http.createServer((_req, res) => {
  res.writeHead(200, { 'content-type': 'text/html; charset=utf-8' });
  res.end(html);
}).listen(5173, () => console.log('monorepo dashboard listening on 5173'));
