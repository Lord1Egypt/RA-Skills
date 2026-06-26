/** Shared base path / API URL helper for proxy-aware routing */

/** Detect the base path from the page URL (e.g. '/pixel-agents' when proxied) */
export function getBasePath(): string {
  if (import.meta.env.DEV) return '';
  const path = window.location.pathname.replace(/\/+$/, '');
  return path || '';
}

/** Get the API base URL — works both direct and behind a reverse proxy */
export function getApiBase(): string {
  if (import.meta.env.DEV) return 'http://localhost:5070';
  return getBasePath();
}
