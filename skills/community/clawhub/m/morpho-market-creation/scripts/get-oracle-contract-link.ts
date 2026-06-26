import { findChainByAlias } from '@api3/dapi-management';
import { getChainAddresses } from '@morpho-org/blue-sdk';

function main() {
  const chainAlias = process.argv[2];

  if (!chainAlias) {
    console.error('Usage: ts-node scripts/get-oracle-contract-link.ts <chain-alias>');
    process.exit(1);
  }

  const chain = findChainByAlias(chainAlias);
  if (!chain) {
    console.error(`Chain not found: ${chainAlias}`);
    process.exit(1);
  }

  const targetChainId = Number(chain.id);
  const blockExplorerUrl = chain.blockExplorerUrl;
  const chainAddresses = getChainAddresses(targetChainId);

  if (!chainAddresses.chainlinkOracleFactory) {
    console.error(`Morpho ChainlinkOracleV2Factory not found for chain: ${chain.alias}`);
    process.exit(1);
  }

  console.log(`${blockExplorerUrl}address/${chainAddresses.chainlinkOracleFactory}#writeContract`);
}

main();