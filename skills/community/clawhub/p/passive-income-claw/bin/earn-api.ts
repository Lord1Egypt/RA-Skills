#!/usr/bin/env node
// Binance Simple Earn API client
import { signedRequest, parseArgs, die, out } from "./lib.ts";

const commands: Record<string, (args: Record<string, string | true>) => Promise<void>> = {
  "list-flexible": async (args) => {
    const params: Record<string, string> = {};
    if (typeof args.asset === "string") params.asset = args.asset;
    if (typeof args.size === "string") params.size = args.size;
    if (typeof args.page === "string") params.current = args.page;
    out(await signedRequest("GET", "/sapi/v1/simple-earn/flexible/list", params));
  },

  "list-locked": async (args) => {
    const params: Record<string, string> = {};
    if (typeof args.asset === "string") params.asset = args.asset;
    if (typeof args.size === "string") params.size = args.size;
    if (typeof args.page === "string") params.current = args.page;
    out(await signedRequest("GET", "/sapi/v1/simple-earn/locked/list", params));
  },

  "subscribe-flexible": async (args) => {
    if (typeof args.productId !== "string") die("Missing --productId");
    if (typeof args.amount !== "string") die("Missing --amount");
    out(await signedRequest("POST", "/sapi/v1/simple-earn/flexible/subscribe", {
      productId: args.productId,
      amount: args.amount,
    }));
  },

  "redeem-flexible": async (args) => {
    if (typeof args.productId !== "string") die("Missing --productId");
    const params: Record<string, string> = { productId: args.productId };
    if (args.all === true) params.redeemAll = "true";
    else if (typeof args.amount === "string") params.amount = args.amount;
    else die("Missing --amount or --all");
    out(await signedRequest("POST", "/sapi/v1/simple-earn/flexible/redeem", params));
  },

  "subscribe-locked": async (args) => {
    if (typeof args.projectId !== "string") die("Missing --projectId");
    if (typeof args.amount !== "string") die("Missing --amount");
    out(await signedRequest("POST", "/sapi/v1/simple-earn/locked/subscribe", {
      projectId: args.projectId,
      amount: args.amount,
    }));
  },

  "redeem-locked": async (args) => {
    if (typeof args.positionId !== "string") die("Missing --positionId");
    out(await signedRequest("POST", "/sapi/v1/simple-earn/locked/redeem", {
      positionId: args.positionId,
    }));
  },

  positions: async (args) => {
    if (typeof args.type !== "string" || !["flexible", "locked"].includes(args.type))
      die("Missing or invalid --type (flexible|locked)");
    const params: Record<string, string> = {};
    if (typeof args.asset === "string") params.asset = args.asset;
    out(await signedRequest("GET", `/sapi/v1/simple-earn/${args.type}/position`, params));
  },

  account: async () => {
    out(await signedRequest("GET", "/sapi/v1/simple-earn/account"));
  },

  balance: async () => {
    const data = await signedRequest("GET", "/api/v3/account");
    const assets = (data.balances || [])
      .filter((b: any) => parseFloat(b.free) > 0 || parseFloat(b.locked) > 0)
      .map((b: any) => ({
        asset: b.asset,
        free: b.free,
        locked: b.locked,
        total: (parseFloat(b.free) + parseFloat(b.locked)).toString(),
      }));
    out({ assets });
  },
};

import { main } from "./lib.ts";
main(async () => {
  const [cmd, ...rest] = process.argv.slice(2);
  if (!cmd || !commands[cmd]) die(`Usage: earn-api.ts <command>\nCommands: ${Object.keys(commands).join(", ")}`);
  await commands[cmd](parseArgs(rest));
});
