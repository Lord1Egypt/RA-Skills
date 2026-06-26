import { findChainByAlias, initializeStaticProvider } from '@api3/dapi-management';
import { getChainAddresses } from '@morpho-org/blue-sdk';
import dotenv from 'dotenv';
import { ethers } from 'ethers';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

dotenv.config();

const MORPHO_ABI = [
  {
    name: "createMarket",
    type: "function",
    inputs: [
      {
        name: "marketParams",
        type: "tuple",
        components: [
          { name: "loanToken",       type: "address" },
          { name: "collateralToken", type: "address" },
          { name: "oracle",          type: "address" },
          { name: "irm",             type: "address" },
          { name: "lltv",            type: "uint256" },
        ],
      },
    ],
    outputs: [],
  },
] as const;

async function main() {
  const chainAlias = process.argv[2];
  if (!chainAlias) {
    console.error('Usage: ts-node scripts/create-market.ts <chain-alias>');
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

  const __dirname = path.dirname(fileURLToPath(import.meta.url));
  const paramsPath = path.resolve(__dirname, '..', 'market-params.json');
  const p = JSON.parse(fs.readFileSync(paramsPath, 'utf-8'));

  const marketParams = {
    loanToken:       p.loanToken,
    collateralToken: p.collateralToken,
    oracle:          p.oracle,
    irm:             p.irm,
    lltv:            BigInt(Math.round(p.lltv * 1e16)),
  };

  const provider = initializeStaticProvider(chain.alias);
  const wallet = ethers.Wallet.fromPhrase(process.env.WALLET_MNEMONIC).connect(provider);

  const chainAddresses = getChainAddresses(Number(chain.id));
  if (!chainAddresses.morpho) {
    console.error(`Morpho Blue contract not found for chain: ${chain.alias}`);
    process.exit(1);
  }

  const marketId = ethers.keccak256(
    ethers.AbiCoder.defaultAbiCoder().encode(
      ['(address,address,address,address,uint256)'],
      [[marketParams.loanToken, marketParams.collateralToken, marketParams.oracle, marketParams.irm, marketParams.lltv]]
    )
  );
  console.log(`Market ID: ${marketId}`);

  const morpho = new ethers.Contract(chainAddresses.morpho, MORPHO_ABI, wallet);

  const tx = await morpho.createMarket(marketParams);
  console.log(`Tx submitted: ${tx.hash}`);
  await tx.wait();
  console.log(`Market created: ${marketId}`);
}

main();
