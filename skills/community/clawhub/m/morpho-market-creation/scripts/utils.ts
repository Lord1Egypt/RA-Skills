import { ethers } from 'ethers';
import { api3Contracts } from "@api3/dapi-management";

type SupportedChain = (typeof api3Contracts.CHAINS)[number];

export function findChainByAlias(alias: string): SupportedChain {
  const chain = api3Contracts.CHAINS.find((c) => c.alias.toLowerCase() === alias.toLowerCase());
  if (!chain) {
    throw new Error(`Chain with alias ${alias} not found in chains exported by @api3/contracts package`);
  }
  return chain;
}

export function initializeStaticProvider(chainAlias: string) {
  const { id: chainId, providers } = findChainByAlias(chainAlias);
  const defaultProvider = providers.find(({ alias }) => alias === 'default');
  if (!defaultProvider) {
    throw new Error(`Missing default provider found for chain '${chainAlias}'`);
  }
  const defaultProviderUrl = defaultProvider.rpcUrl;
  if (!defaultProviderUrl) {
    throw new Error(`Missing RPC URL found for chain '${chainAlias}'`);
  }
  const fetchRequest = new ethers.FetchRequest(defaultProviderUrl);
  fetchRequest.timeout = 15_000;
  const network = new ethers.Network(chainAlias, chainId);
  return new ethers.JsonRpcProvider(fetchRequest, network, { staticNetwork: network });
}