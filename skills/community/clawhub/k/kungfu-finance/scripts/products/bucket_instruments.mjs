import { getJson } from "../core/http_client.mjs";

export async function getBucketInstruments(input) {
  if (!input?.bucket_id) {
    throw new Error("bucket_instruments requires bucket_id");
  }

  const response = await getJson("/api/instrument-buckets/instruments", {
    bucket_id: input.bucket_id
  });

  return response?.data ?? [];
}
