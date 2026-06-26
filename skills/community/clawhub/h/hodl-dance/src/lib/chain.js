const { ethers } = require('ethers');
const BONDING_CURVE_ABI = require('../abi/BondingCurve.json');

const ERC20_ABI = [
  'function approve(address spender, uint256 amount) returns (bool)',
  'function allowance(address owner, address spender) view returns (uint256)',
  'function balanceOf(address owner) view returns (uint256)',
];

const RPC_URL = process.env.HODL_RPC_URL || 'https://bsc-dataseed.binance.org/';

function getProvider() {
  return new ethers.JsonRpcProvider(RPC_URL);
}

function getWallet() {
  const pk = process.env.HODL_PRIVATE_KEY;
  if (!pk) throw new Error('HODL_PRIVATE_KEY env variable not set');
  return new ethers.Wallet(pk, getProvider());
}

function getCurve(address, signerOrProvider) {
  return new ethers.Contract(address, BONDING_CURVE_ABI, signerOrProvider);
}

function getToken(address, signerOrProvider) {
  return new ethers.Contract(address, ERC20_ABI, signerOrProvider);
}

async function simulateBuy(curveAddress, bnbAmount) {
  const provider = getProvider();
  const curve = getCurve(curveAddress, provider);
  const [r, t] = await Promise.all([curve.r(), curve.t()]);
  const bnbWei = ethers.parseEther(String(bnbAmount));
  const fee    = bnbWei / 100n;
  const bnbNet = bnbWei - fee;
  const newR   = r + bnbNet;
  const newT   = (r * t) / newR;
  const tokensOut = t - newT;
  return { tokensOut, fee, bnbNet };
}

async function simulateSell(curveAddress, tokenAmount) {
  const provider = getProvider();
  const curve = getCurve(curveAddress, provider);
  const [r, t] = await Promise.all([curve.r(), curve.t()]);
  const tokensWei = ethers.parseUnits(String(tokenAmount), 18);
  const newT      = t + tokensWei;
  const newR      = (r * t) / newT;
  const bnbGross  = r - newR;
  const fee       = bnbGross / 100n;
  const bnbOut    = bnbGross - fee;
  return { bnbOut, fee };
}

module.exports = { getProvider, getWallet, getCurve, getToken, simulateBuy, simulateSell };
