import { html, nothing } from "lit";

export type AiProviderConnectMode = "oauth" | "token" | "api-key";

export type AiProviderConnectOption = {
  mode: AiProviderConnectMode;
  label: string;
  hint: string;
  /** What auth profile type this stores as */
  profileMode: "oauth" | "token" | "api_key";
};

export type AiProviderStatus = "connected" | "not-connected" | "connecting";

export type ConnectedProfile = {
  profileId: string;
  mode: "api_key" | "oauth" | "token";
  email?: string;
};

export type AiProvider = {
  id: string;
  name: string;
  logo: string;
  color: string;
  description: string;
  connectOptions: AiProviderConnectOption[];
  status: AiProviderStatus;
  profiles: ConnectedProfile[];
};

export type AiProvidersProps = {
  providers: AiProvider[];
  /** provider id → selected connect mode */
  selectedMode: Record<string, AiProviderConnectMode>;
  /** Provider id → paste value (for token/api-key) */
  pasteValues: Record<string, string>;
  /** Which provider's API key input is expanded */
  activeConnect: string | null;
  /** Provider currently running OAuth in browser */
  connectingProvider: string | null;
  /** The OAuth URL to display in the card (replaces popup) */
  oauthUrl: string | null;
  /** Value of the manual redirect URL paste field shown during OAuth */
  oauthRedirectPaste: string;
  message: { kind: "success" | "error"; text: string } | null;
  restartNeeded: boolean;
  onConnect: (id: string) => void;
  onSelectMode: (id: string, mode: AiProviderConnectMode) => void;
  onPasteChange: (id: string, value: string) => void;
  onSave: (id: string) => void;
  onOAuth: (id: string) => void;
  onAnthropicAuto: () => void;
  onRemoveProfile: (profileId: string) => void;
  onCancel: (id: string) => void;
  onOAuthPasteChange: (value: string) => void;
  onSubmitCode: () => void;
  onRestart: () => void;
};

// ─── Badge helpers ────────────────────────────────────────────────────────────

function statusBadge(status: AiProviderStatus, profileCount: number) {
  if (status === "connected") {
    const label = profileCount > 1 ? `${profileCount} profiles` : "Connected";
    return html`<span style="
      display:inline-flex;align-items:center;gap:4px;
      font-size:11px;font-weight:600;padding:2px 8px;
      background:#16a34a1a;color:#16a34a;border:1px solid #16a34a44;border-radius:999px;">
      <span style="width:6px;height:6px;background:#16a34a;border-radius:50%;display:inline-block;"></span>
      ${label}
    </span>`;
  }
  if (status === "connecting") {
    return html`<span style="
      display:inline-flex;align-items:center;gap:4px;
      font-size:11px;font-weight:600;padding:2px 8px;
      background:#f59e0b1a;color:#f59e0b;border:1px solid #f59e0b44;border-radius:999px;">
      ⟳ Connecting…
    </span>`;
  }
  return nothing;
}

function profileModeBadge(mode: "api_key" | "oauth" | "token") {
  const labels: Record<string, string> = { api_key: "API Key", oauth: "OAuth", token: "Subscription" };
  const colors: Record<string, string> = { api_key: "#6366f1", oauth: "#10b981", token: "#f59e0b" };
  const c = colors[mode] ?? "#888";
  return html`<span style="
    font-size:10px;font-weight:600;padding:1px 6px;
    background:${c}1a;color:${c};border:1px solid ${c}44;border-radius:4px;">
    ${labels[mode] ?? mode}
  </span>`;
}

// ─── Provider Card ────────────────────────────────────────────────────────────

function renderProvider(p: AiProvider, props: AiProvidersProps) {
  const isApiKeyExpanded = props.activeConnect === p.id;
  const pasteVal = props.pasteValues[p.id] ?? "";
  const isConnecting = props.connectingProvider === p.id;

  const oauthOption = p.connectOptions.find((o) => o.mode === "oauth");
  const tokenOption = p.connectOptions.find((o) => o.mode === "token");
  const apiKeyOption = p.connectOptions.find((o) => o.mode === "api-key");

  return html`
    <section style="
      border:1px solid var(--border,#30363d);border-radius:12px;
      background:var(--bg-panel,#161b22);overflow:hidden;margin-bottom:16px;
      ${p.status === "connected" ? `border-left:3px solid ${p.color};` : ""}
    ">
      <!-- Card Body -->
      <div style="padding:20px 24px;display:flex;align-items:flex-start;gap:16px;">

        <!-- Logo -->
        <div style="
          width:52px;height:52px;border-radius:12px;flex-shrink:0;
          background:${p.color}1a;border:1px solid ${p.color}33;
          display:flex;align-items:center;justify-content:center;font-size:26px;line-height:1;
        ">${p.logo}</div>

        <!-- Info + actions -->
        <div style="flex:1;min-width:0;">
          <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;">
            <span style="font-size:17px;font-weight:700;color:var(--text);">${p.name}</span>
            ${statusBadge(p.status, p.profiles.length)}
          </div>
          <div style="font-size:13px;color:var(--text-muted);margin-top:4px;margin-bottom:16px;">${p.description}</div>

          <!-- ── Primary action buttons (always visible) ── -->
          ${isConnecting ? html`
            <div style="padding:14px 16px;
              background:var(--bg-surface,#0d1117);border-radius:8px;border:1px solid var(--border,#30363d);">
              <div style="display:flex;align-items:center;gap:12px;">
                <div style="width:18px;height:18px;border:2px solid ${p.color};border-top-color:transparent;
                  border-radius:50%;animation:spin 1s linear infinite;flex-shrink:0;"></div>
                <div style="flex:1;min-width:0;">
                  <div style="font-size:13px;font-weight:600;color:var(--text);">Waiting for sign-in…</div>
                  <div style="font-size:12px;color:var(--text-muted);margin-top:2px;">
                    ${props.oauthUrl
                      ? "Click the link below to open the sign-in page, then return here."
                      : "Preparing sign-in link…"}
                  </div>
                </div>
                <button @click=${() => props.onCancel(p.id)} style="
                  flex-shrink:0;font-size:12px;padding:4px 10px;
                  background:transparent;border:1px solid var(--border,#30363d);
                  color:var(--text-muted);border-radius:6px;cursor:pointer;">
                  Cancel
                </button>
              </div>
              ${props.oauthUrl ? html`
                <div style="margin-top:12px;padding:10px 12px;
                  background:var(--bg-panel,#161b22);border-radius:6px;
                  border:1px solid ${p.color}44;">
                  <div style="font-size:11px;color:var(--text-muted);margin-bottom:6px;font-weight:600;text-transform:uppercase;letter-spacing:.5px;">
                    Sign-in URL
                  </div>
                  <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">
                    <a href="${props.oauthUrl}" target="_blank" rel="noopener noreferrer" style="
                      font-size:12px;color:${p.color};word-break:break-all;
                      text-decoration:none;flex:1;min-width:0;
                      overflow:hidden;text-overflow:ellipsis;white-space:nowrap;
                      display:block;
                    " title="${props.oauthUrl}">
                      ↗ ${props.oauthUrl}
                    </a>
                    <button @click=${() => { void navigator.clipboard.writeText(props.oauthUrl ?? ""); }} style="
                      flex-shrink:0;font-size:11px;padding:3px 8px;
                      background:${p.color}22;border:1px solid ${p.color}44;
                      color:${p.color};border-radius:5px;cursor:pointer;white-space:nowrap;
                    ">
                      Copy
                    </button>
                  </div>
                  <!-- Manual fallback for WSL2 / environments where localhost callback is blocked -->
                  <div style="margin-top:10px;border-top:1px solid var(--border,#30363d);padding-top:10px;">
                    <div style="font-size:11px;color:var(--text-muted);margin-bottom:6px;">
                      If the sign-in page doesn't redirect automatically, paste the full redirect URL here:
                    </div>
                    <div style="display:flex;gap:6px;align-items:stretch;">
                      <input
                        type="text"
                        placeholder="http://localhost:1455/auth/callback?code=..."
                        .value=${props.oauthRedirectPaste}
                        @input=${(e: Event) => props.onOAuthPasteChange((e.target as HTMLInputElement).value)}
                        @keydown=${(e: KeyboardEvent) => { if (e.key === "Enter" && props.oauthRedirectPaste.trim()) props.onSubmitCode(); }}
                        style="flex:1;font-size:12px;padding:6px 10px;
                          background:var(--bg-surface,#0d1117);
                          border:1px solid var(--border,#30363d);border-radius:6px;
                          color:var(--text);outline:none;font-family:monospace;"
                      />
                      <button
                        @click=${() => props.onSubmitCode()}
                        ?disabled=${!props.oauthRedirectPaste.trim()}
                        style="
                          font-size:12px;padding:6px 12px;
                          background:${props.oauthRedirectPaste.trim() ? p.color : "var(--bg-panel,#161b22)"};
                          color:${props.oauthRedirectPaste.trim() ? "#fff" : "var(--text-muted)"};
                          border:1px solid ${props.oauthRedirectPaste.trim() ? p.color : "var(--border,#30363d)"};
                          border-radius:6px;cursor:${props.oauthRedirectPaste.trim() ? "pointer" : "default"};
                          white-space:nowrap;transition:all .15s;
                        ">
                        Submit
                      </button>
                    </div>
                  </div>
                </div>
              ` : nothing}
            </div>
            <style>@keyframes spin { to { transform: rotate(360deg); } }</style>
          ` : html`
            <div style="display:flex;flex-wrap:wrap;gap:8px;align-items:center;">

              ${oauthOption ? html`
                <button style="
                  font-size:13px;font-weight:700;padding:9px 20px;
                  background:${p.color};color:#fff;border:none;border-radius:8px;
                  cursor:pointer;display:inline-flex;align-items:center;gap:7px;
                  box-shadow:0 2px 8px ${p.color}40;
                " @click=${() => props.onOAuth(p.id)}>
                  ↗ Login via OAuth
                </button>
              ` : nothing}

              ${tokenOption ? html`
                <button style="
                  font-size:13px;font-weight:600;padding:9px 20px;
                  background:${oauthOption ? "transparent" : p.color};
                  color:${oauthOption ? "var(--text)" : "#fff"};
                  border:1px solid ${oauthOption ? "var(--border,#30363d)" : "transparent"};
                  border-radius:8px;cursor:pointer;display:inline-flex;align-items:center;gap:7px;
                " @click=${() => props.onConnect(p.id)}>
                  🔑 Connect via Subscription Token
                </button>
              ` : nothing}

              ${apiKeyOption && !tokenOption ? html`
                <button style="
                  font-size:13px;font-weight:600;padding:9px 20px;
                  background:${oauthOption ? "transparent" : p.color};
                  color:${oauthOption ? "var(--text)" : "#fff"};
                  border:1px solid ${oauthOption ? "var(--border,#30363d)" : "transparent"};
                  border-radius:8px;cursor:pointer;
                " @click=${() => props.onConnect(p.id)}>
                  Add API Key
                </button>
              ` : nothing}

              ${apiKeyOption && tokenOption ? html`
                <button style="
                  font-size:12px;font-weight:500;padding:7px 14px;
                  background:transparent;color:var(--text-muted);
                  border:1px solid var(--border,#30363d);border-radius:8px;cursor:pointer;
                " @click=${() => { props.onSelectMode(p.id, "api-key"); props.onConnect(p.id); }}>
                  API Key instead
                </button>
              ` : nothing}

              ${p.status === "connected" ? html`
                <button style="
                  font-size:12px;padding:7px 14px;
                  background:transparent;color:var(--text-muted);
                  border:1px solid var(--border,#30363d);border-radius:8px;cursor:pointer;
                " @click=${() => props.onConnect(p.id)}>
                  ＋ Add Another Profile
                </button>
              ` : nothing}
            </div>
          `}

          <!-- Connected profiles -->
          ${p.profiles.length > 0 ? html`
            <div style="margin-top:14px;display:flex;flex-direction:column;gap:6px;">
              ${p.profiles.map((prof) => html`
                <div style="display:flex;align-items:center;gap:8px;font-size:12px;">
                  ${profileModeBadge(prof.mode)}
                  <span style="color:var(--text-muted);font-family:monospace;">
                    ${prof.email ?? prof.profileId}
                  </span>
                  <button style="
                    background:none;border:none;color:var(--clr-danger,#ef4444);
                    cursor:pointer;font-size:11px;padding:2px 6px;opacity:.7;
                  " @click=${() => { if (confirm("Remove profile " + prof.profileId + "?")) props.onRemoveProfile(prof.profileId); }}>✕ Remove</button>
                </div>
              `)}
            </div>
          ` : nothing}
        </div>
      </div>

      <!-- ── Expanded: token / api-key input ── -->
      ${isApiKeyExpanded ? html`
        <div style="border-top:1px solid var(--border,#30363d);padding:20px 24px;background:var(--bg-surface,#0d1117);">

          <!-- Mode tabs (token vs api-key) — only shown if both exist -->
          ${tokenOption && apiKeyOption ? html`
            <div style="display:flex;gap:4px;margin-bottom:16px;padding:3px;
              background:var(--bg-panel,#161b22);border-radius:8px;width:fit-content;">
              ${[tokenOption, apiKeyOption].map((opt) => {
                const sel = (props.selectedMode[p.id] ?? tokenOption.mode) === opt.mode;
                return html`
                  <button style="
                    font-size:12px;font-weight:600;padding:5px 14px;border:none;border-radius:6px;cursor:pointer;
                    background:${sel ? p.color : "transparent"};
                    color:${sel ? "#fff" : "var(--text-muted)"};transition:all .15s;
                  " @click=${() => props.onSelectMode(p.id, opt.mode)}>
                    ${opt.label}
                  </button>
                `;
              })}
            </div>
          ` : nothing}

          ${(() => {
            const mode = props.selectedMode[p.id] ?? (tokenOption ? "token" : "api-key");
            return html`
              ${mode === "token" ? html`
                <div style="
                  padding:12px;background:var(--bg-panel,#161b22);border-radius:8px;
                  border:1px solid var(--border,#30363d);margin-bottom:14px;
                ">
                  <div style="display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;">
                    <div>
                      <div style="font-size:12px;font-weight:600;color:var(--text);margin-bottom:4px;">How to get your token:</div>
                      <ol style="font-size:12px;color:var(--text-muted);margin:0;padding-left:18px;line-height:2;">
                        <li>Open a terminal and run: <code style="background:var(--bg,#0d1117);padding:1px 5px;border-radius:3px;font-size:11px;">claude setup-token</code></li>
                        <li>Copy the generated <code style="font-size:11px;">sk-ant-oat01-…</code> token</li>
                        <li>Paste it below and click Save</li>
                      </ol>
                    </div>
                    <button
                      @click=${() => props.onAnthropicAuto()}
                      style="
                        flex-shrink:0;font-size:12px;font-weight:600;padding:8px 14px;
                        background:${p.color};color:#fff;border:none;border-radius:8px;
                        cursor:pointer;display:inline-flex;align-items:center;gap:6px;
                        white-space:nowrap;box-shadow:0 2px 8px ${p.color}40;
                      ">
                      ✨ Auto-detect
                    </button>
                  </div>
                  <div style="margin-top:8px;padding-top:8px;border-top:1px solid var(--border,#30363d);
                    font-size:11px;color:var(--text-muted);">
                    If you've already signed into the <code style="font-size:10px;">claude</code> CLI, <strong>Auto-detect</strong> reads the token automatically — no copy-paste needed.
                  </div>
                </div>
              ` : nothing}

              <div style="display:flex;gap:8px;flex-wrap:wrap;align-items:flex-start;">
                <input
                  type="password"
                  style="
                    flex:1;min-width:220px;padding:9px 12px;
                    background:var(--bg-panel,#161b22);border:1px solid var(--border,#30363d);
                    border-radius:8px;color:var(--text);font-size:13px;font-family:monospace;
                  "
                  placeholder=${mode === "token"
                    ? "sk-ant-oat01-…"
                    : p.id === "anthropic" ? "sk-ant-api03-…"
                    : p.id === "openai" ? "sk-proj-…"
                    : "Paste API key…"}
                  .value=${pasteVal}
                  @input=${(e: Event) => props.onPasteChange(p.id, (e.target as HTMLInputElement).value)}
                  @keydown=${(e: KeyboardEvent) => { if (e.key === "Enter" && pasteVal.trim()) props.onSave(p.id); }}
                />
                <button style="
                  font-size:13px;font-weight:600;padding:9px 22px;
                  background:${p.color};color:#fff;border:none;border-radius:8px;cursor:pointer;
                  opacity:${pasteVal.trim() ? "1" : "0.4"};
                "
                  ?disabled=${!pasteVal.trim()}
                  @click=${() => props.onSave(p.id)}>
                  Save
                </button>
                <button style="
                  font-size:13px;padding:9px 14px;
                  background:transparent;border:1px solid var(--border,#30363d);
                  color:var(--text-muted);border-radius:8px;cursor:pointer;
                " @click=${() => props.onCancel(p.id)}>
                  Cancel
                </button>
              </div>
              <div style="margin-top:10px;font-size:11px;color:var(--text-muted);opacity:.8;">
                🔒 Stored encrypted in <code>auth-profiles.json</code> — never sent to or read by the AI.
              </div>
            `;
          })()}
        </div>
      ` : nothing}
    </section>
  `;
}

// ─── Page ─────────────────────────────────────────────────────────────────────

export function renderAiProviders(props: AiProvidersProps) {
  return html`
    <div class="page-body" style="max-width:780px;">
      <div style="margin-bottom:24px;">
        <h2 style="font-size:20px;font-weight:700;color:var(--text);margin:0 0 6px;">OAuth & Provider Login</h2>
        <p style="font-size:13px;color:var(--text-muted);margin:0;line-height:1.6;">
          Connect your AI model providers using OAuth, subscription tokens, or API keys.
          OAuth and subscription logins use your existing plan — no extra charges.
        </p>
      </div>

      ${props.message ? html`
        <div style="
          margin-bottom:16px;padding:10px 14px;border-radius:8px;font-size:13px;
          ${props.message.kind === "error"
            ? "background:#ef44441a;border:1px solid #ef444444;color:#ef4444;"
            : "background:#16a34a1a;border:1px solid #16a34a44;color:#16a34a;"}
        ">${props.message.text}</div>
      ` : nothing}

      ${props.restartNeeded ? html`
        <div style="
          margin-bottom:16px;padding:10px 14px;
          background:#f59e0b18;border:1px solid var(--clr-warning,#f59e0b);
          border-radius:8px;display:flex;align-items:center;justify-content:space-between;gap:10px;
        ">
          <span style="font-size:13px;color:var(--clr-warning,#f59e0b);">
            ⚠ Gateway restart required for changes to take effect.
          </span>
          <button class="btn" style="font-size:12px;padding:4px 12px;background:var(--clr-warning,#f59e0b);color:#000;border:none;font-weight:600;"
            @click=${() => props.onRestart()}>Restart Now</button>
        </div>
      ` : nothing}

      ${props.providers.map((p) => renderProvider(p, props))}

      <div style="margin-top:8px;font-size:12px;color:var(--text-muted);text-align:center;opacity:.7;">
        API keys are stored in the <a href="/apikeys" style="color:var(--text-muted);text-decoration:underline;">🔒 Vault</a>.
        Auth profiles live in <code>auth-profiles.json</code> per-agent.
      </div>
    </div>
  `;
}
