import type { ParsedArgs } from "../../types.js";
import { parseUnits } from "viem";

function parseValue(value: string | undefined): string | undefined {
  if (!value || value === "0") return undefined;
  if (value.startsWith("0x")) return value;
  if (value.includes(".")) {
    const wei = parseUnits(value, 18);
    return "0x" + wei.toString(16);
  }
  return "0x" + BigInt(value).toString(16);
}

function parseGas(value: string | undefined): string | undefined {
  if (!value) return undefined;
  if (value.startsWith("0x")) return value;
  return "0x" + BigInt(value).toString(16);
}

export interface CallTransaction {
  from: string;
  to: string;
  data?: string;
  value?: string;
  gas?: string;
  gasPrice?: string;
}

export function buildCallTransaction(
  from: string,
  to: string,
  args: ParsedArgs
): CallTransaction {
  const tx: CallTransaction = {
    from,
    to,
  };
  if (args.data) {
    tx.data = args.data.startsWith("0x") ? args.data : "0x" + args.data;
  }
  const value = parseValue(args.value);
  if (value) tx.value = value;
  const gas = parseGas(args.gas);
  if (gas) tx.gas = gas;
  const gasPrice = parseGas(args.gasPrice);
  if (gasPrice) tx.gasPrice = gasPrice;
  return tx;
}
