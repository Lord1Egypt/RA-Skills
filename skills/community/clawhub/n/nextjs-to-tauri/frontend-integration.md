# Frontend integration templates

Add only the pieces you need. JS deps (the plugins pull in `@tauri-apps/api` transitively — you don't need it as a direct dep):

```bash
yarn add @tauri-apps/plugin-opener@^2 @tauri-apps/plugin-updater@^2
```

All of this **no-ops outside a Tauri webview**, so it's safe to ship in the same bundle to the web. Rename the storage keys (`<app>_*`) per project.

---

## `utils/externalLink.ts` — Tauri detection + system-browser links

A plain `.ts` (no JSX). `isTauriRuntime` is **synchronous** so click handlers can branch without awaiting (gotcha #4). Opening uses `@tauri-apps/plugin-opener` — the dedicated Tauri 2 plugin for opening URLs (the shell plugin is for spawning processes).

```ts
declare global {
  interface Window {
    __TAURI__?: unknown;
    __TAURI_INTERNALS__?: unknown;
  }
}

// Detect via runtime globals/UA only — NEVER by importing @tauri-apps/api (it loads
// fine in a browser; invoke only throws at call time). Sync so click handlers can use it.
export const isTauriRuntime = (): boolean => {
  if (typeof window === "undefined") return false;
  if (window.__TAURI_INTERNALS__) return true; // v2
  if (window.__TAURI__) return true; // v1
  if (typeof navigator !== "undefined" && navigator.userAgent.includes("Tauri")) return true;
  return false;
};

export const isTauri = async (): Promise<boolean> => isTauriRuntime();

export const openExternalLink = async (url: string) => {
  if (isTauriRuntime()) {
    try {
      const { openUrl } = await import("@tauri-apps/plugin-opener");
      await openUrl(url);
      return;
    } catch (e) {
      console.error("opener failed:", e);
    }
  }
  window.open(url, "_blank", "noopener,noreferrer");
};
```

> Don't bother writing an `<ExternalLink>` wrapper component — you'd have to find and convert every link. The global click delegate below catches them all (gotcha #10).

---

## `utils/updater.ts` — check + download (defer install)

```ts
"use client";
import { isTauri } from "./externalLink";

export interface UpdateCheckResult {
  hasUpdate: boolean;
  version?: string;
  downloaded?: boolean;
  install?: () => Promise<void>;
  error?: string;
}

export const checkForUpdates = async (): Promise<UpdateCheckResult> => {
  if (!(await isTauri())) return { hasUpdate: false, error: "Not in Tauri" };
  try {
    const { check } = await import("@tauri-apps/plugin-updater");
    const update = await check();
    if (!update) return { hasUpdate: false };
    await update.download(); // auto-download, install on confirm
    return { hasUpdate: true, version: update.version, downloaded: true, install: () => update.install() };
  } catch (error) {
    return { hasUpdate: false, error: String(error) };
  }
};
```

---

## `hooks/useAutoUpdate.ts` — startup + interval check, confirm-to-install, skip-version

```ts
"use client";
import { useEffect, useRef, useCallback } from "react";
import { message, Modal } from "antd"; // swap for your UI lib's dialog/toast
import { checkForUpdates, UpdateCheckResult } from "@/app/utils/updater";
import { isTauri } from "@/app/utils/externalLink";

const SKIPPED_KEY = "<app>_skipped_version";

export const useAutoUpdate = ({ startupDelay = 3000, checkInterval = 24 * 60 * 60 * 1000 } = {}) => {
  const checkedStartup = useRef(false);
  const lastCheck = useRef(0);

  const confirm = useCallback((r: UpdateCheckResult) => {
    Modal.confirm({
      title: "Update Available",
      content: `Version ${r.version} downloaded. Install now and restart?`,
      okText: "Install Now",
      cancelText: "Skip This Version",
      onOk: () => r.install?.(),
      onCancel: () => { try { localStorage.setItem(SKIPPED_KEY, r.version!); } catch {} },
    });
  }, []);

  const run = useCallback(async () => {
    if (!(await isTauri())) return;
    const now = Date.now();
    if (now - lastCheck.current < 60 * 60 * 1000) return; // throttle 1h
    lastCheck.current = now;
    const r = await checkForUpdates();
    if (r.hasUpdate && r.downloaded && r.version) {
      let skipped = ""; try { skipped = localStorage.getItem(SKIPPED_KEY) || ""; } catch {}
      if (skipped === r.version) return;
      confirm(r);
    }
  }, [confirm]);

  useEffect(() => {
    if (checkedStartup.current) return;
    const t = setTimeout(() => { checkedStartup.current = true; run(); }, startupDelay);
    return () => clearTimeout(t);
  }, [run, startupDelay]);

  useEffect(() => {
    const id = setInterval(run, checkInterval);
    return () => clearInterval(id);
  }, [run, checkInterval]);
};
```

---

## next-intl i18n — switching, and (optionally) remembering the language

**Switch locales with plain soft navigation (`router.push`).** It's client-side RSC
routing that never touches the webview's asset protocol, so it just works in Tauri —
exactly as on the web. **Do NOT hard-navigate** (`window.location`) for a switch: a hard
reload remounts the `[locale]` layout subtree, which resets `useRef` guards and re-fires
any startup redirect — the bounce that makes switching look broken (gotcha #11).

Remembering the language across launches is **optional**. If you add it, two rules keep
the launch-time redirect from fighting the switcher:

1. The "redirect once per session" guard must be a **MODULE-LEVEL variable, not a
   `useRef`** — a locale switch remounts the hook's host, resetting a ref and re-running
   the redirect every switch.
2. Persist the preference in the **switcher** (explicit user action), NOT in a navigation
   effect — an effect races the startup redirect and can save the entry locale over the
   saved one.

`hooks/useLanguagePreference.ts` (self-contained; Tauri-only so the web build is untouched):

```ts
"use client";
import { useEffect } from "react";
import { usePathname, useRouter } from "next/navigation";
import { isTauriRuntime } from "@/app/utils/externalLink";

const KEY = "<app>_preferred_language";
export const setPreferredLanguage = (l: string) => { try { localStorage.setItem(KEY, l); } catch {} };
const read = () => { try { return localStorage.getItem(KEY); } catch { return null; } };
const localeOf = (p: string) => p.match(/^\/([a-z]{2}(-[a-z]+)?)/i)?.[1] ?? null;
const systemLocale = () => {
  const s = (typeof navigator !== "undefined" && navigator.language) || "en";
  if (s.startsWith("zh")) return /TW|HK|Hant/i.test(s) ? "zh-hant" : "zh";
  return s.split("-")[0];
};

// MODULE-level, not a ref: survives the [locale] layout remount a switch triggers, so
// the redirect runs exactly once per app launch and never bounces a switch (gotcha #11).
let sessionRedirectDone = false;

export function useLanguagePreference(valid: string[]) {
  const pathname = usePathname();
  const router = useRouter();
  useEffect(() => {
    if (sessionRedirectDone || !isTauriRuntime()) return;
    const cur = localeOf(pathname);
    if (!cur) return;
    sessionRedirectDone = true;
    let pref = read();
    if (!pref) { const s = systemLocale(); if (valid.includes(s)) { pref = s; setPreferredLanguage(s); } } // first run → system
    if (pref && valid.includes(pref) && pref !== cur) {
      router.replace(pathname.replace(/^\/[a-z]{2}(-[a-z]+)?/i, `/${pref}`)); // SOFT redirect, once
    }
  }, [pathname, router, valid]);
}
```

**Language switcher** — plain soft nav, and save the choice here (not in an effect):

```ts
import { setPreferredLanguage } from "@/app/hooks/useLanguagePreference";
import { isTauriRuntime } from "@/app/utils/externalLink";

const onPick = (locale: string) => {
  if (isTauriRuntime()) setPreferredLanguage(locale);      // remember the explicit choice
  const next = pathname.replace(/^\/[a-z]{2}(-[a-z]+)?/, `/${locale}`);
  router.push(`${next}${window.location.search}${window.location.hash}`); // SOFT nav — works in Tauri
};
```

> Skip the whole hook if you don't need cross-launch memory — plain `router.push` in the
> switcher is all switching itself requires.

---

## Mount point — one client component inside your providers

Render inside `NextIntlClientProvider` (for `useLocale`/router) and your UI lib's context provider (antd `<App>` for `message`/`Modal`). A server-component layout can render this client child directly. This also installs the **global external-link interceptor** (gotcha #10): one capture-phase delegate sends every external link to the system browser — no per-link wrapping.

```tsx
"use client";
import { useEffect } from "react";
import { useAutoUpdate } from "@/app/hooks/useAutoUpdate";
import { useLanguagePreference } from "@/app/hooks/useLanguagePreference";
import { isTauriRuntime, openExternalLink } from "@/app/utils/externalLink";
import { routing } from "@/i18n/routing";

export default function TauriIntegration() {
  useAutoUpdate();
  useLanguagePreference([...routing.locales]);

  useEffect(() => {
    if (!isTauriRuntime()) return;
    const onClick = (e: MouseEvent) => {
      if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
      const href = (e.target as Element | null)?.closest?.("a")?.getAttribute("href");
      if (!href) return;
      let url: URL;
      try { url = new URL(href, window.location.href); } catch { return; }
      const external = (url.protocol === "http:" || url.protocol === "https:") && url.origin !== window.location.origin;
      if (!external && url.protocol !== "mailto:" && url.protocol !== "tel:") return; // internal → let the router handle it
      e.preventDefault();
      e.stopPropagation();
      openExternalLink(url.href);
    };
    document.addEventListener("click", onClick, true); // capture phase
    return () => document.removeEventListener("click", onClick, true);
  }, []);

  return null;
}
```
