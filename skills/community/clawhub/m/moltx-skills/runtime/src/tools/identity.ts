import { getWalletAddress } from "./config.js";
import {
  getPublicRuntime,
  getWriteRuntime,
  identityAbi,
  stringifyJson,
  type ToolHandler,
} from "./shared.js";

const DEFAULT_IDENTITY_ADDRESS = "0xb16aA007A5F0C6dE1A69D0D81412BA6d77c685Ab" as `0x${string}`;

/**
 * is_registered — 检查当前钱包是否已在 MoltXIdentity 注册。
 */
const is_registered: ToolHandler = async () => {
  const { publicClient } = getPublicRuntime();
  const wallet = await getWalletAddress();

  const registered = await publicClient.readContract({
    address: DEFAULT_IDENTITY_ADDRESS,
    abi: identityAbi,
    functionName: "isRegistered",
    args: [wallet],
  });

  return stringifyJson({
    tool: "is_registered",
    walletAddress: wallet,
    registered,
  });
};

/**
 * register_identity — 在 MoltXIdentity 注册当前钱包。
 *
 * 注册是参与协议的前置条件：createTask 和 acceptTask 都会检查 isRegistered。
 * 幂等安全：如果已注册会 revert AlreadyRegistered，调用前建议先用 is_registered 检查。
 */
const register_identity: ToolHandler = async () => {
  const { publicClient } = getPublicRuntime();
  const { walletClient, account } = await getWriteRuntime();
  const wallet = await getWalletAddress();

  // Check first to give a clear message
  const already = await publicClient.readContract({
    address: DEFAULT_IDENTITY_ADDRESS,
    abi: identityAbi,
    functionName: "isRegistered",
    args: [wallet],
  });

  if (already) {
    return stringifyJson({
      tool: "register_identity",
      walletAddress: wallet,
      alreadyRegistered: true,
      hint: "Wallet is already registered, no action taken",
    });
  }

  const hash = await walletClient.writeContract({
    address: DEFAULT_IDENTITY_ADDRESS,
    abi: identityAbi,
    functionName: "register",
    args: [],
    account,
    chain: publicClient.chain,
  });

  const receipt = await publicClient.waitForTransactionReceipt({ hash });

  return stringifyJson({
    tool: "register_identity",
    walletAddress: wallet,
    txHash: hash,
    status: receipt.status,
  });
};

export const identityTools: Record<string, ToolHandler> = {
  is_registered,
  register_identity,
};
