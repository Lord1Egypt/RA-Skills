import { KomodoClient } from "komodo_client";

const url = process.env.KOMODO_URL;
const key = process.env.KOMODO_API_KEY;
const secret = process.env.KOMODO_API_SECRET;

if (!url) throw new Error("Missing env: KOMODO_URL");
if (!key) throw new Error("Missing env: KOMODO_API_KEY");
if (!secret) throw new Error("Missing env: KOMODO_API_SECRET");

export const komodo = KomodoClient(url, {
  type: "api-key",
  params: { key, secret },
});
