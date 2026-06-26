import { getJson } from "../core/http_client.mjs";

export async function getBucketList() {
  const response = await getJson("/api/instrument-buckets/buckets");
  return response?.data ?? [];
}
