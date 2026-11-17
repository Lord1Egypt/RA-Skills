/**
 * Service statique de l'UI web (packages/web/dist) sous /ui/ —
 * même origine que l'API : pas de CORS, pas de découverte de port côté front.
 * Le token admin est passé au navigateur via le fragment (#token=…), jamais
 * loggé ni envoyé en query.
 */
import { existsSync, readFileSync, statSync } from 'node:fs'
import { extname, join, normalize, resolve } from 'node:path'
import type { ServerResponse } from 'node:http'

const MIME: Record<string, string> = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.json': 'application/json',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.ico': 'image/x-icon',
  '.map': 'application/json',
  '.woff2': 'font/woff2',
  '.webp': 'image/webp',
}

/** Localise le dist de l'UI : option explicite > @memoria/web/dist résolu localement. */
export function findUiDist(explicit?: string): string | null {
  const candidates = [
    explicit,
    // monorepo (dev) et installation npm (dist embarqué)
    new URL('../../web/dist', import.meta.url).pathname,
    new URL('../web-dist', import.meta.url).pathname,
  ].filter((p): p is string => Boolean(p))
  for (const c of candidates) {
    if (existsSync(join(c, 'index.html'))) return c
  }
  return null
}

/** Sert /ui/* depuis distDir. Retourne false si le chemin ne nous concerne pas. */
export function serveUi(pathname: string, distDir: string, res: ServerResponse): boolean {
  if (pathname === '/' || pathname === '/ui') {
    res.writeHead(302, { location: '/ui/' })
    res.end()
    return true
  }
  if (!pathname.startsWith('/ui/')) return false

  const rel = pathname.slice('/ui/'.length) || 'index.html'
  // garde anti-traversée : le chemin résolu doit rester dans distDir
  const filePath = resolve(distDir, normalize(rel))
  if (!filePath.startsWith(resolve(distDir))) {
    res.writeHead(403).end()
    return true
  }
  const target = existsSync(filePath) && statSync(filePath).isFile() ? filePath : join(distDir, 'index.html')
  const body = readFileSync(target)
  res.writeHead(200, {
    'content-type': MIME[extname(target)] ?? 'application/octet-stream',
    'content-length': body.length,
    'cache-control': 'no-store',
  })
  res.end(body)
  return true
}
