/**
 * Shared CLOB client initialization.
 * Based on https://github.com/Alchemist-X/pm-PlaceOrder/src/lib/client.ts
 */

import dotenv from "dotenv";
import { resolve, dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
dotenv.config({ path: resolve(__dirname, "..", ".env.aizen") });

import { ClobClient, OrderType, Side } from "@polymarket/clob-client";
import { Wallet } from "ethers";

export const HOST = "https://clob.polymarket.com";
export const CHAIN_ID = 137;

export interface ClientEnv {
  privateKey: string;
  funderAddress: string;
  signatureType: number;
  eoaAddress: string;
}

export function loadEnv(): ClientEnv {
  const privateKey = process.env.PRIVATE_KEY ?? "";
  const funderAddress = process.env.FUNDER_ADDRESS ?? "";
  const signatureType = parseInt(process.env.SIGNATURE_TYPE ?? "1", 10);

  if (!privateKey || !funderAddress) {
    console.log(JSON.stringify({
      error: "Missing PRIVATE_KEY or FUNDER_ADDRESS in .env.aizen",
      status: "config_error",
    }));
    process.exit(1);
  }

  return {
    privateKey,
    funderAddress,
    signatureType,
    eoaAddress: new Wallet(privateKey).address,
  };
}

export async function initClient(env: ClientEnv): Promise<ClobClient> {
  const signer = new Wallet(env.privateKey);
  const temp = new ClobClient(HOST, CHAIN_ID, signer);
  const creds = await temp.createOrDeriveApiKey();
  return new ClobClient(HOST, CHAIN_ID, signer, creds, env.signatureType, env.funderAddress);
}

export { ClobClient, OrderType, Side };
