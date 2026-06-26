import { requestJson } from "../core/http_client.mjs";

export async function addBucketInstruments(input) {
  if (!input?.bucket_id) {
    throw new Error("bucket_add_instruments requires bucket_id");
  }

  if (!Array.isArray(input.instruments) || input.instruments.length === 0) {
    throw new Error("bucket_add_instruments requires at least one instrument");
  }

  return requestJson("POST", "/api/instrument-buckets/instruments", {
    body: {
      bucket_id: input.bucket_id,
      instruments: input.instruments
    }
  });
}
