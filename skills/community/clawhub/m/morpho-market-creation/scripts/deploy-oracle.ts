import { findChainByAlias, initializeStaticProvider } from '@api3/dapi-management';
import { getChainAddresses } from '@morpho-org/blue-sdk';
import dotenv from 'dotenv';
import { ethers } from 'ethers';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

dotenv.config();

const ORACLE_FACTORY_ABI = [
  {
    name: "createMorphoChainlinkOracleV2",
    type: "function",
    inputs: [
      { name: "baseVault",                  type: "address" },
      { name: "baseVaultConversionSample",  type: "uint256" },
      { name: "baseFeed1",                  type: "address" },
      { name: "baseFeed2",                  type: "address" },
      { name: "baseTokenDecimals",          type: "uint256" },
      { name: "quoteVault",                 type: "address" },
      { name: "quoteVaultConversionSample", type: "uint256" },
      { name: "quoteFeed1",                 type: "address" },
      { name: "quoteFeed2",                 type: "address" },
      { name: "quoteTokenDecimals",         type: "uint256" },
      { name: "salt",                       type: "bytes32" },
    ],
    outputs: [{ name: "oracle", type: "address" }],
  },
] as const;

const ORACLE_ABI = [
  {
    name: "price",
    type: "function",
    stateMutability: "view",
    inputs: [],
    outputs: [{ name: "", type: "uint256" }],
  },
] as const;

async function main() {
  const chainAlias = process.argv[2];
  if (!chainAlias) {
    console.error('Usage: ts-node scripts/deploy-oracle.ts <chain-alias>');
    process.exit(1);
  }

  const chain = findChainByAlias(chainAlias);
  if (!chain) {
    console.error(`Chain not found: ${chainAlias}`);
    process.exit(1);
  }

  if (!process.env.WALLET_MNEMONIC) {
    console.error('WALLET_MNEMONIC environment variable is required.');
    process.exit(1);
  }

  const ZERO = ethers.ZeroAddress;

  const __dirname = path.dirname(fileURLToPath(import.meta.url));
  const paramsPath = path.resolve(__dirname, '..', 'oracle-params.json');
  const p = JSON.parse(fs.readFileSync(paramsPath, 'utf-8'));

  const params = [
    p.baseVault                    ?? ZERO,
    BigInt(p.baseVaultConversionSample ?? "1"),
    p.baseFeed1                    ?? ZERO,
    p.baseFeed2                    ?? ZERO,
    BigInt(p.baseTokenDecimals     ?? "18"),
    p.quoteVault                   ?? ZERO,
    BigInt(p.quoteVaultConversionSample ?? "1"),
    p.quoteFeed1                   ?? ZERO,
    p.quoteFeed2                   ?? ZERO,
    BigInt(p.quoteTokenDecimals    ?? "18"),
    p.salt                         ?? ethers.ZeroHash,
  ] as const;

  const provider = initializeStaticProvider(chain.alias);
  const wallet = ethers.Wallet.fromPhrase(process.env.WALLET_MNEMONIC).connect(provider);

  const chainAddresses = getChainAddresses(Number(chain.id));
  if (!chainAddresses.chainlinkOracleFactory) {
    console.error(`Morpho ChainlinkOracleV2Factory not found for chain: ${chain.alias}`);
    process.exit(1);
  }

  const factory = new ethers.Contract(chainAddresses.chainlinkOracleFactory, ORACLE_FACTORY_ABI, wallet);

  const oracleAddress: string = await factory.createMorphoChainlinkOracleV2.staticCall(...params);
  console.log(`Oracle will deploy at: ${oracleAddress}`);

  const tx = await factory.createMorphoChainlinkOracleV2(...params);
  console.log(`Tx submitted: ${tx.hash}`);
  await tx.wait();
  console.log(`Oracle deployed at:   ${oracleAddress}`);
}

main();
