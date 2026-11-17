/* LYGO SMART DISK AGENT portal — local token auth (one-shot friendly) */
const log = document.getElementById("log");
const form = document.getElementById("form");
const msg = document.getElementById("msg");
const healthEl = document.getElementById("health");
const limbOut = document.getElementById("limb-out");
const TOKEN_KEY = "sda_local_token";

function addBubble(text, cls) {
  const d = document.createElement("div");
  d.className = "bubble " + cls;
  d.textContent = text;
  log.appendChild(d);
  log.scrollTop = log.scrollHeight;
}

function getToken() {
  return sessionStorage.getItem(TOKEN_KEY) || "";
}

function setToken(t) {
  if (t) sessionStorage.setItem(TOKEN_KEY, t);
  else sessionStorage.removeItem(TOKEN_KEY);
}

function authHeaders(extra) {
  const h = Object.assign({ "Content-Type": "application/json" }, extra || {});
  const t = getToken();
  if (t) h["X-SDA-Token"] = t;
  return h;
}

function captureTokenFromUrl() {
  const u = new URL(window.location.href);
  const t = u.searchParams.get("t") || u.searchParams.get("token");
  if (t) {
    setToken(t);
    u.searchParams.delete("t");
    u.searchParams.delete("token");
    window.history.replaceState({}, "", u.pathname + u.hash);
  }
}

async function ensureAuth() {
  const r = await fetch("/api/auth", { cache: "no-store", headers: authHeaders() });
  const j = await r.json();
  if (!j.auth_required) return true;
  if (j.authenticated) return true;
  let t = getToken();
  if (!t) {
    t = window.prompt(
      "Local operator token required (from boot console or data/.sda_local_token):",
      ""
    );
    if (t) setToken(t.trim());
  }
  const r2 = await fetch("/api/auth", { cache: "no-store", headers: authHeaders() });
  const j2 = await r2.json();
  if (!j2.authenticated) {
    addBubble("Auth failed — set token from boot console (python agent/smart_disk_agent.py token).", "sys");
    return false;
  }
  return true;
}

async function refreshHealth() {
  try {
    const r = await fetch("/api/health", { cache: "no-store", headers: authHeaders() });
    const j = await r.json();
    const brain = j.brain || "missing";
    healthEl.className = "health " + brain;
    const authBit = j.auth_required
      ? j.authenticated
        ? " · token OK"
        : " · token needed"
      : " · open";
    healthEl.textContent =
      "brain:" +
      brain +
      (j.model ? " · " + j.model : "") +
      " · localhost:9631" +
      authBit +
      " · free " +
      Math.round((j.disk_free_bytes || 0) / 1024) +
      " KB";
  } catch (e) {
    healthEl.className = "health missing";
    healthEl.textContent = "agent offline — run LYGO_SMART_DISK_BOOT.bat";
  }
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const text = msg.value.trim();
  if (!text) return;
  if (!(await ensureAuth())) return;
  addBubble(text, "user");
  msg.value = "";
  try {
    const r = await fetch("/api/chat", {
      method: "POST",
      headers: authHeaders(),
      body: JSON.stringify({ message: text, token: getToken() }),
    });
    const j = await r.json();
    if (r.status === 401) {
      setToken("");
      addBubble("Unauthorized — re-enter local token.", "sys");
      return;
    }
    const reply = j.reply || j.error || JSON.stringify(j);
    addBubble((j.model ? "[" + j.model + "] " : "") + reply, j.ok === false ? "sys" : "bot");
  } catch (err) {
    addBubble("Chat failed — is the agent running?", "sys");
  }
  refreshHealth();
});

document.querySelectorAll("[data-limb]").forEach((btn) => {
  btn.addEventListener("click", async () => {
    const limb = btn.getAttribute("data-limb");
    if (!(await ensureAuth())) return;
    try {
      const r = await fetch("/api/limb", {
        method: "POST",
        headers: authHeaders(),
        body: JSON.stringify({ limb, args: [], token: getToken() }),
      });
      const j = await r.json();
      limbOut.textContent = JSON.stringify(j, null, 2);
    } catch (e) {
      limbOut.textContent = String(e);
    }
  });
});

captureTokenFromUrl();
addBubble(
  "Smart Disk portal ready. Localhost + local operator token (auto from boot URL). Chat memory not on HTTP.",
  "sys"
);
ensureAuth().then(() => refreshHealth());
setInterval(refreshHealth, 15000);
