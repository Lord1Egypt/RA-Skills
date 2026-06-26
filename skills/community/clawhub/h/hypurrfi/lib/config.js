/**
 * HypurrFi Configuration
 * All contract addresses and ABIs for HyperEVM lending
 */

export const CHAIN = {
  id: 999,
  name: 'HyperEVM',
  rpc: 'https://rpc.hyperliquid.xyz/evm',
  explorer: 'https://explorer.hyperliquid.xyz',
  nativeToken: 'HYPE',
  nativeDecimals: 18
};

// Market contract addresses
export const MARKETS = {
  pooled: {
    name: 'Pooled',
    type: 'aave',
    pool: '0xceCcE0EB9DD2Ef7996e01e25DD70e461F918A14b',
    dataProvider: '0x895C799a5bbdCb63B80bEE5BD94E7b9138D977d6',
    wrappedHypeGateway: '0xd1EF87FeFA83154F83541b68BD09185e15463972',
    oracle: '0x9BE2ac1ff80950DCeb816842834930887249d9A8'
  },
  prime: {
    name: 'Prime',
    type: 'euler',
    vault: '0x...', // TODO: Get Prime vault address
    description: 'Lower risk Euler cluster'
  },
  yield: {
    name: 'Yield', 
    type: 'euler',
    vault: '0x...', // TODO: Get Yield vault address
    description: 'Higher risk Euler cluster'
  },
  vault: {
    name: 'Vault',
    type: 'curated',
    manager: 'ClearstarLabs',
    vaults: {
      usdt0: '0x...' // TODO: Get Vault addresses
    }
  }
};

// Token addresses on HyperEVM
export const TOKENS = {
  hype: {
    address: null, // Native token
    symbol: 'HYPE',
    decimals: 18,
    markets: ['pooled', 'prime', 'yield']
  },
  usdt0: {
    address: '0xB8CE59FC3717ada4C02eaDF9682A9e934F625ebb',
    symbol: 'USDT0',
    decimals: 6,
    markets: ['pooled', 'prime', 'yield', 'vault'],
    aTokens: {
      pooled: '0x1Ca7e21B2dAa5Ab2eB9de7cf8f34dCf9c8683007'
    }
  },
  usdc: {
    address: '0x211Cc4DD073734dA055fbF44a2b4667d5E5fE5d2',
    symbol: 'USDC',
    decimals: 6,
    markets: ['pooled']
  },
  usdxl: {
    address: '0xca79db4B49f608eF54a5CB813FbEd3a6387bC645',
    symbol: 'USDXL',
    decimals: 18,
    markets: ['pooled']
  },
  hwhype: {
    address: '0x...', // hwHYPE address
    symbol: 'hwHYPE',
    decimals: 18,
    markets: ['prime', 'yield']
  }
};

export const WALLET_PATH = process.env.HOME + '/.hyperliquid-wallet.json';

// ABI fragments
export const ERC20_ABI = [
  'function name() view returns (string)',
  'function symbol() view returns (string)',
  'function decimals() view returns (uint8)',
  'function balanceOf(address) view returns (uint256)',
  'function allowance(address owner, address spender) view returns (uint256)',
  'function approve(address spender, uint256 amount) returns (bool)',
  'function transfer(address to, uint256 amount) returns (bool)'
];

export const AAVE_POOL_ABI = [
  'function supply(address asset, uint256 amount, address onBehalfOf, uint16 referralCode)',
  'function withdraw(address asset, uint256 amount, address to) returns (uint256)',
  'function borrow(address asset, uint256 amount, uint256 interestRateMode, uint16 referralCode, address onBehalfOf)',
  'function repay(address asset, uint256 amount, uint256 interestRateMode, address onBehalfOf) returns (uint256)',
  'function getUserAccountData(address user) view returns (uint256 totalCollateralBase, uint256 totalDebtBase, uint256 availableBorrowsBase, uint256 currentLiquidationThreshold, uint256 ltv, uint256 healthFactor)'
];

export const DATA_PROVIDER_ABI = [
  'function getReserveTokensAddresses(address asset) view returns (address aTokenAddress, address stableDebtTokenAddress, address variableDebtTokenAddress)',
  'function getUserReserveData(address asset, address user) view returns (uint256 currentATokenBalance, uint256 currentStableDebt, uint256 currentVariableDebt, uint256 principalStableDebt, uint256 scaledVariableDebt, uint256 stableBorrowRate, uint256 liquidityRate, uint40 stableRateLastUpdated, bool usageAsCollateralEnabled)',
  'function getReserveData(address asset) view returns (uint256 unbacked, uint256 accruedToTreasuryScaled, uint256 totalAToken, uint256 totalStableDebt, uint256 totalVariableDebt, uint256 liquidityRate, uint256 variableBorrowRate, uint256 stableBorrowRate, uint256 averageStableBorrowRate, uint256 liquidityIndex, uint256 variableBorrowIndex, uint40 lastUpdateTimestamp)'
];

export const WRAPPED_HYPE_GATEWAY_ABI = [
  'function depositETH(address pool, address onBehalfOf, uint16 referralCode) payable',
  'function withdrawETH(address pool, uint256 amount, address to)',
  'function borrowETH(address pool, uint256 amount, uint256 interestRateMode, uint16 referralCode)',
  'function repayETH(address pool, uint256 amount, uint256 rateMode, address onBehalfOf) payable'
];

// Euler-style vault ABI (for Prime/Yield markets)
export const EULER_VAULT_ABI = [
  'function deposit(uint256 assets, address receiver) returns (uint256)',
  'function withdraw(uint256 assets, address receiver, address owner) returns (uint256)',
  'function balanceOf(address account) view returns (uint256)',
  'function totalAssets() view returns (uint256)',
  'function asset() view returns (address)'
];
