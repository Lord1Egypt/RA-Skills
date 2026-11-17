// KPN — Korea Judgment Verification: minimal reference handler.
//
// Least privilege by design:
//   • HTTPS outbound to persona-mcp-server.onrender.com ONLY.
//   • No shell, no filesystem writes, no environment variables, no secrets, no credentials.
//   • No dynamic eval / obfuscation. Does exactly what SKILL.md describes: submit a Korea
//     question, poll for the human-verified verdict, return it. Never acts on the user's behalf.
//
// Usage: askKPN("your Korea-related question") -> { verdict, raw }

const API = "https://persona-mcp-server.onrender.com";

/**
 * Submit a Korea-judgment question and wait for the verified verdict (async ~10–15 min).
 * @param {string} question  Korea-specific matter to judge (>= 5 chars).
 * @param {object} [opts]    { title?, classificationOnly?, wallet?, pollMs?, timeoutMs? }
 * @returns {Promise<{status:string, verdict?:object, ref?:string, message?:string}>}
 */
export async function askKPN(question, opts = {}) {
  const q = String(question ?? "").trim();
  if (q.length < 5) return { status: "error", message: "question must be >= 5 characters" };

  // Step 1 — submit.
  const submit = await fetch(`${API}/ai/advisory?src=clawhub`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      question: q,
      ...(opts.title ? { title: String(opts.title).slice(0, 300) } : {}),
      ...(opts.classificationOnly ? { classification_only: true } : {}),
      ...(/^0x[0-9a-fA-F]{40}$/.test(opts.wallet || "") ? { wallet: opts.wallet } : {}),
    }),
  });
  const started = await submit.json().catch(() => ({}));
  if (submit.status === 400) return { status: "error", message: started.error || "bad_request" };
  if (submit.status === 429) return { status: "rate_limited", message: "daily free limit reached — try later" };
  if (!submit.ok || !started.status_url) return { status: "error", message: `submit failed (${submit.status})` };

  // Step 2 — poll status_url until the verdict is ready (HTTP 200).
  const statusUrl = started.status_url;               // already carries the access token
  const pollMs = Math.max(15000, Number(opts.pollMs) || 45000);
  const deadline = Date.now() + (Math.max(60000, Number(opts.timeoutMs) || 20 * 60 * 1000));
  while (Date.now() < deadline) {
    await new Promise((r) => setTimeout(r, pollMs));
    const r = await fetch(statusUrl, { headers: { Accept: "application/json" } });
    if (r.status === 200) {
      const verdict = await r.json().catch(() => ({}));
      // Step 3 — return the verdict as-is. The caller must present it honestly and NOT override a HOLD.
      return { status: "done", ref: started.ref_code, verdict };
    }
    // 202 => still generating; keep polling.
  }
  return { status: "timeout", ref: started.ref_code, message: "verdict not ready yet — retry status_url later" };
}

/** Optional: register a contact to be notified when paid tiers resume (all fields optional). */
export async function notifyMeWhenPaidResumes({ agentName, operator, webhookUrl, email, wallet } = {}) {
  const r = await fetch(`${API}/ai/contact?src=clawhub`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ agent_name: agentName, operator, webhook_url: webhookUrl, email, wallet }),
  });
  return r.json().catch(() => ({}));
}
