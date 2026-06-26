import { getRuntimeConfig, getWalletAddress } from "./config.js";
import { readStoredAuth } from "./siwe.js";

type ToolHandler = (args: unknown) => Promise<string>;

const get_wallet_info: ToolHandler = async () => {
  try {
    const auth = readStoredAuth();
    if (auth?.walletAddress) {
      return JSON.stringify({
        address: auth.walletAddress,
        source: "local signer / SIWE session (EIP-7702 smart account)",
        gasless: true,
        paymasterNote: "Gas sponsored via Pimlico Paymaster (EIP-7702 + ERC-4337)",
        authPath: "~/.moltx/auth.json",
        walletPath: "~/.moltx/wallet.json",
      });
    }

    const config = getRuntimeConfig();
    if (config.walletAddress) {
      return JSON.stringify({
        address: config.walletAddress,
        source: "runtime walletAddress",
        gasless: false,
        configPath: "~/.moltx/config.json",
      });
    }

    const address = await getWalletAddress();
    return JSON.stringify({
      address,
      source: "local runtime signer (EIP-7702 smart account)",
      gasless: true,
      paymasterNote: "Gas sponsored via Pimlico Paymaster (EIP-7702 + ERC-4337)",
      walletPath: "~/.moltx/wallet.json",
    });
  } catch (error) {
    return JSON.stringify({
      error: (error as Error).message,
      hint: "Run siwe_login to authenticate",
    });
  }
};

export const walletTools: Record<string, ToolHandler> = {
  get_wallet_info,
};
