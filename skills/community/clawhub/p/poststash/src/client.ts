const BASE = "https://poststash.com/api";

export async function poststashFetch(path: string, init: RequestInit = {}): Promise<unknown> {
  const apiKey = process.env.POSTSTASH_API_KEY;
  if (!apiKey) {
    throw new Error("POSTSTASH_API_KEY environment variable is not set");
  }

  const res = await fetch(`${BASE}${path}`, {
    ...init,
    headers: {
      Authorization: `Bearer ${apiKey}`,
      "Content-Type": "application/json",
      ...init.headers,
    },
  });

  const json = await res.json();
  if (!res.ok) {
    throw new Error((json as { error?: string }).error ?? `HTTP ${res.status}`);
  }
  return json;
}
