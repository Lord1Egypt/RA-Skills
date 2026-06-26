#!/usr/bin/env node
// Binance Cross Margin API client
import { signedRequest, parseArgs, die, out } from "./lib.ts";

const commands: Record<string, (args: Record<string, string | true>) => Promise<void>> = {
  "asset-info": async (args) => {
    if (typeof args.asset !== "string") die("Missing --asset");
    const data: any[] = await signedRequest("GET", "/sapi/v1/margin/allAssets", { asset: args.asset });
    const found = data.find((a) => a.assetName === args.asset);
    if (!found) die(`Asset ${args.asset} not found in margin assets`);
    out({
      asset: found.assetName,
      borrowable: found.isBorrowable,
      mortgageable: found.isMortgageable,
      minBorrow: found.userMinBorrow,
      minRepay: found.userMinRepay,
    });
  },

  "max-borrowable": async (args) => {
    if (typeof args.asset !== "string") die("Missing --asset");
    out(await signedRequest("GET", "/sapi/v1/margin/maxBorrowable", { asset: args.asset }));
  },

  "interest-rate": async (args) => {
    if (typeof args.assets !== "string") die("Missing --assets (comma-separated)");
    out(await signedRequest("GET", "/sapi/v1/margin/next-hourly-interest-rate", {
      assets: args.assets,
      isIsolated: "FALSE",
    }));
  },

  borrow: async (args) => {
    if (typeof args.asset !== "string") die("Missing --asset");
    if (typeof args.amount !== "string") die("Missing --amount");
    out(await signedRequest("POST", "/sapi/v1/margin/borrow-repay", {
      asset: args.asset,
      amount: args.amount,
      type: "BORROW",
      isIsolated: "FALSE",
    }));
  },

  repay: async (args) => {
    if (typeof args.asset !== "string") die("Missing --asset");
    if (typeof args.amount !== "string") die("Missing --amount");
    out(await signedRequest("POST", "/sapi/v1/margin/borrow-repay", {
      asset: args.asset,
      amount: args.amount,
      type: "REPAY",
      isIsolated: "FALSE",
    }));
  },

  account: async () => {
    const data = await signedRequest("GET", "/sapi/v1/margin/account");
    out({
      marginLevel: data.marginLevel,
      collateralMarginLevel: data.collateralMarginLevel,
      totalAssetOfBtc: data.totalAssetOfBtc,
      totalLiabilityOfBtc: data.totalLiabilityOfBtc,
      totalNetAssetOfBtc: data.totalNetAssetOfBtc,
      totalCollateralValueInUSDT: data.TotalCollateralValueInUSDT,
      borrowEnabled: data.borrowEnabled,
      assets: (data.userAssets || [])
        .filter((a: any) => parseFloat(a.borrowed) > 0 || parseFloat(a.free) > 0)
        .map((a: any) => ({
          asset: a.asset,
          free: a.free,
          borrowed: a.borrowed,
          interest: a.interest,
          netAsset: a.netAsset,
        })),
    });
  },

  history: async (args) => {
    const type = typeof args.type === "string" ? args.type : "BORROW";
    const limit = typeof args.limit === "string" ? args.limit : "10";
    const startTime = Date.now() - 30 * 24 * 60 * 60 * 1000; // 30 days ago
    const params: Record<string, string | number> = { type, size: limit, startTime };
    if (typeof args.asset === "string") params.asset = args.asset;
    out(await signedRequest("GET", "/sapi/v1/margin/borrow-repay", params));
  },
};

import { main } from "./lib.ts";
main(async () => {
  const [cmd, ...rest] = process.argv.slice(2);
  if (!cmd || !commands[cmd]) die(`Usage: margin-api.ts <command>\nCommands: ${Object.keys(commands).join(", ")}`);
  await commands[cmd](parseArgs(rest));
});
