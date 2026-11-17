// Only public GET requests. Timeouts cover headers AND response bodies.
export async function readPublic(url, { timeoutMs = 15000, html = false } = {}) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const requestOptions = {
      method: "GET",
      headers: { accept: html ? "text/html" : "application/json" },
      signal: controller.signal,
      redirect: "manual",
    };
    let response = await fetch(url, requestOptions);
    // Cloudflare serves existing .html report links through an extensionless
    // canonical URL. Permit that one exact same-origin rewrite, no other hop.
    if (html && [301, 302, 303, 307, 308].includes(response.status)) {
      const original = new URL(url);
      const location = response.headers.get("location");
      const canonical = location ? new URL(location, original) : null;
      await response.body?.cancel();
      if (!canonical || canonical.origin !== original.origin || canonical.username || canonical.password ||
          canonical.search || canonical.hash || !original.pathname.endsWith(".html") ||
          canonical.pathname !== original.pathname.slice(0, -5)) {
        throw new Error("Unapproved report redirect");
      }
      response = await fetch(canonical, requestOptions);
    }
    if (!response.ok) throw new Error("HTTP " + response.status);
    const type = response.headers.get("content-type") || "";
    if (!type.includes(html ? "text/html" : "application/json")) throw new Error("Unexpected content type: " + type);
    const reader = response.body.getReader();
    const chunks = [];
    let length = 0;
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      length += value.byteLength;
      if (length > 5 * 1024 * 1024) {
        await reader.cancel();
        throw new Error("Response exceeds 5 MiB; narrow the query.");
      }
      chunks.push(value);
    }
    const text = Buffer.concat(chunks).toString("utf8");
    if (html) return text;
    const data = JSON.parse(text);
    if (data === null || typeof data !== "object" || Array.isArray(data)) throw new Error("Invalid API object");
    if (data.error) throw new Error("API reported an error");
    return data;
  } catch (error) {
    if (controller.signal.aborted) throw new Error("Request timed out after " + timeoutMs + " ms");
    throw new Error("Public source unavailable (" + new URL(url).origin + "): " + error.message);
  } finally {
    clearTimeout(timer);
  }
}

export async function requestJson(base, path, params = {}, options = {}) {
  const url = new URL(path, base + "/");
  for (const [key, value] of Object.entries(params)) {
    if (Array.isArray(value)) value.forEach((item) => url.searchParams.append(key, item));
    else if (value !== undefined && value !== "") url.searchParams.set(key, value);
  }
  return readPublic(url, options);
}
