/**
 * OurGroceries — log POST JSON bodies from the web app (insertItem, setItemCrossedOff, etc.)
 *
 * HOW TO USE
 * 1. Open https://www.ourgroceries.com/your-lists (or any OurGroceries page that talks to /your-lists).
 * 2. Open DevTools → Console.
 * 3. If Chrome blocks paste: type `allow pasting` on the console prompt first, or use Sources → Snippets
 *    (paste there, save, Run).
 * 4. Paste this entire file and press Enter once.
 * 5. Use the app normally; each matching POST body is printed. For getItemCategory / insertItem / insertItems,
 *    a second line `[og-monitor] EXPORT …` contains JSON.stringify of the full body (easy copy for sharing).
 *
 * OPTIONAL: only log specific commands (comma-separated), e.g. insertItem
 *   localStorage.setItem('ogMonitorCommands', 'insertItem,insertItems');
 * To log everything again:
 *   localStorage.removeItem('ogMonitorCommands');
 *
 * To disable monitoring, refresh the page (hooks are not persisted).
 */
(function () {
  if (window.__ogMonitorInstalled) {
    console.warn('[og-monitor] already installed; refresh the page to reinstall');
    return;
  }
  window.__ogMonitorInstalled = true;

  const HOST = 'ourgroceries.com';
  /** Also log one-line JSON for these (collapsed groups hide fields in some exports). */
  const EXPORT_COMMANDS = new Set(['getItemCategory', 'insertItem', 'insertItems']);

  function allowedCommands() {
    const raw = localStorage.getItem('ogMonitorCommands');
    if (!raw || !raw.trim()) return null;
    return new Set(
      raw
        .split(',')
        .map((s) => s.trim())
        .filter(Boolean),
    );
  }

  function shouldLogUrl(url) {
    try {
      const u = typeof url === 'string' ? new URL(url, location.origin) : new URL(url.href);
      return u.hostname.endsWith(HOST) && u.pathname.startsWith('/your-lists');
    } catch {
      return false;
    }
  }

  function maybeLogBody(url, bodyText) {
    if (!bodyText || typeof bodyText !== 'string') return;
    let data;
    try {
      data = JSON.parse(bodyText);
    } catch {
      return;
    }
    const filter = allowedCommands();
    if (filter && data.command && !filter.has(data.command)) return;

    console.groupCollapsed(`[og-monitor] POST ${data.command || '(no command)'}`, url);
    console.log(data);
    console.groupEnd();

    if (data.command && EXPORT_COMMANDS.has(data.command)) {
      console.log(`[og-monitor] EXPORT ${data.command}`, JSON.stringify(data));
    }
  }

  const origOpen = XMLHttpRequest.prototype.open;
  XMLHttpRequest.prototype.open = function (method, url, ...rest) {
    this.__ogMethod = method;
    this.__ogUrl = url;
    return origOpen.call(this, method, url, ...rest);
  };

  const origSend = XMLHttpRequest.prototype.send;
  XMLHttpRequest.prototype.send = function (body) {
    const method = (this.__ogMethod || '').toUpperCase();
    const url = this.__ogUrl;
    if (method === 'POST' && shouldLogUrl(url) && body != null) {
      const text = typeof body === 'string' ? body : null;
      if (text) maybeLogBody(url, text);
    }
    return origSend.call(this, body);
  };

  const origFetch = window.fetch;
  window.fetch = function (input, init) {
    const url = typeof input === 'string' ? input : input && input.url;
    const method = (init && init.method) || (typeof input !== 'string' && input && input.method) || 'GET';
    if (method.toUpperCase() === 'POST' && shouldLogUrl(url) && init && init.body != null) {
      const body = init.body;
      if (typeof body === 'string') maybeLogBody(url, body);
    }
    return origFetch.apply(this, arguments);
  };

  console.info(
    '[og-monitor] active — POST JSON to /your-lists* is logged. ' +
      'Optional: localStorage.setItem("ogMonitorCommands","insertItem")',
  );
})();
