#!/usr/bin/env node
/**
 * register-and-mint.mjs — Paratrix Life Registration + SBT Mint (Entry Point)
 *
 * Zero external dependencies: pure Node.js built-in modules only.
 *
 * Modules:
 *   register-and-mint.mjs  — entry point + main flow
 *   bridge.mjs              — BridgeServer + BRIDGE_HTML
 *   api.mjs                 — API client
 */

import { randomBytes } from 'node:crypto';
import { BridgeServer } from './bridge.mjs';
import { createApiClient, ApiError } from './api.mjs';

// ═══════════════════════════════════════════════════════════════
// Config
// ═══════════════════════════════════════════════════════════════

const ENV_CLI = (() => {
  const args = process.argv.slice(2);
  for (const arg of args) {
    const [k, ...v] = arg.split('=');
    if (k === '--env') return v.join('=') || 'testnet';
  }
  return '';
})();
const ENV = ENV_CLI || process.env.KARPAK_ENV || 'mainnet';

const CONFIGS = {
  testnet: {
    apiBase: 'https://devnet-lifestyle-api.karpak.xyz',
    sbtUrl:  'https://devnet.paratrix-sbt.pages.dev',
    chainId: 97,
    rpcUrl:  'https://data-seed-prebsc-1-s1.binance.org:8545/',
    bscscan: 'https://testnet.bscscan.com',
    sbtContract: '0x754F167ae420758F1AA5a2142757E2111b0E2241',
  },
  mainnet: {
    apiBase: 'https://lifestyle-api.karpak.xyz',
    sbtUrl:  'https://sbt.karpak.xyz',
    chainId: 56,
    rpcUrl:  'https://bsc-dataseed.binance.org',
    bscscan: 'https://bscscan.com',
    sbtContract: '0x988b33Ef3b7EE4d36F3118ce4dB67848201081C5',
  },
};

const CFG = CONFIGS[ENV];
if (!CFG) { console.error(`Unknown env: ${ENV}`); process.exit(1); }

const BRIDGE_PORT = parseInt(process.env.BRIDGE_PORT || '0', 10) || (3000 + Math.floor(Math.random() * 1000));

const DEFAULT_NICKNAME    = process.env.KARPAK_NICKNAME || '';
const DEFAULT_IDENTITY    = process.env.KARPAK_IDENTITY || 'IDENTITY_TYPE_HUMAN';
const DEFAULT_TWITTER     = process.env.KARPAK_TWITTER  || '';
const WALLET_ADDRESS      = process.env.KARPAK_WALLET   || '';

// ═══════════════════════════════════════════════════════════════
// Utilities
// ═══════════════════════════════════════════════════════════════

function encodeMintCall(signatureHex) {
  // Keccak-256('mint(bytes)') first 4 bytes — hardcoded because Node.js sha3-256 != Ethereum Keccak-256
  const selector = Buffer.from('7ba0e2e7', 'hex');
  const sig = signatureHex.startsWith('0x') ? signatureHex.slice(2) : signatureHex;
  const sigBytes = Buffer.from(sig, 'hex');
  const sigLen = sigBytes.length;
  const offsetBuf = Buffer.alloc(32);
  offsetBuf.writeUInt32BE(32, 28);
  const lenBuf = Buffer.alloc(32);
  lenBuf.writeUInt32BE(sigLen, 28);
  const padLen = Math.ceil(sigLen / 32) * 32;
  const dataBuf = Buffer.alloc(padLen);
  sigBytes.copy(dataBuf);
  return '0x' + Buffer.concat([selector, offsetBuf, lenBuf, dataBuf]).toString('hex');
}

function genNickname() { return 'paratrix_agent_' + randomBytes(4).toString('hex'); }
function genTwitter()  { return 'paratrix_agent_' + randomBytes(4).toString('hex'); }
function log(emoji, msg) { console.log(`${emoji} ${msg}`); }
function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

// ═══════════════════════════════════════════════════════════════
// Main Flow (Single-Tab, Fully Automatic)
// ═══════════════════════════════════════════════════════════════

async function main() {
  const args = process.argv.slice(2);
  const opts = {};
  for (const arg of args) {
    const [k, ...v] = arg.split('=');
    opts[k.replace(/^--/, '')] = v.join('=') || true;
  }

  const nickname     = opts.nickname    || DEFAULT_NICKNAME    || genNickname();
  const identityType = opts.identity    || DEFAULT_IDENTITY;
  const twitterUser  = opts.twitter     || DEFAULT_TWITTER     || genTwitter();
  const walletAddr   = opts.wallet      || WALLET_ADDRESS;

  log('---', `Environment: ${ENV} | Chain ID: ${CFG.chainId}`);
  log('---', `Nickname: ${nickname} | Identity: ${identityType} | Twitter: @${twitterUser}`);
  if (walletAddr) log('---', `Wallet: ${walletAddr}`);

  const bridge = new BridgeServer(BRIDGE_PORT);
  const api = createApiClient(CFG);

  try {
    // Step 1: Start bridge + open single browser tab + auto-connect wallet
    await bridge.start();
    bridge.openFlow();

    log('[1]', 'Waiting for wallet connection...');
    const connectResult = await bridge.waitForSubmit(60000);
    if (connectResult.error) throw new Error(`Wallet connect failed: ${connectResult.message}`);
    let address = connectResult.address;
    log('OK ', `Wallet address: ${address}`);

    // Step 2: Issue nonce
    log('[2]', 'Requesting nonce...');
    const { nonce, message } = await api.issueNonce(address);
    log('OK ', `Nonce received (message: ${message.length} chars)`);

    // Step 3: Auto-sign (MetaMask popup)
    log('[3]', 'Requesting signature...');
    bridge.pushAction('sign', { message, address });
    const signResult = await bridge.waitForSubmit(120000);
    if (signResult.error) throw new Error(`Signature failed: ${signResult.error} - ${signResult.message}`);
    const signature = signResult.signature;
    if (signResult.address && signResult.address !== address) {
      address = signResult.address;
      log('   ', `Address updated from signature: ${address}`);
    }
    log('OK ', `Signature: ${signature.slice(0, 10)}...`);

    // Step 4: Verify
    log('[4]', 'Verifying signature...');
    const verifyResult = await api.verify(address, signature);
    const { accessToken, accountStatus, user, wallet, hasCredential } = verifyResult;
    log('OK ', `Status: ${accountStatus} | User: ${user?.nickname || '(new)'} | HasCredential: ${hasCredential}`);

    // Step 5: Profile (if needed)
    if (accountStatus === 'ACCOUNT_STATUS_PROFILE_REQUIRED') {
      log('[5]', `Setting profile: nickname="${nickname}", identity=${identityType}`);
      const profileResult = await api.updateProfile(accessToken, nickname, identityType);
      log('OK ', `After profile: ${profileResult.accountStatus}`);
      if (profileResult.accountStatus === 'ACCOUNT_STATUS_ACTIVE') {
        log('OK ', 'Registration complete! Account is ACTIVE.');
        bridge.pushAction('done', { title: 'Registration Complete', message: 'Account is ACTIVE. You can close this page.' });
        return report(address, profileResult, null);
      }
    }

    if (accountStatus === 'ACCOUNT_STATUS_ACTIVE') {
      // Check if user explicitly provided a nickname or twitter to update
      const providedNickname = opts.nickname || DEFAULT_NICKNAME;
      const currentNickname  = user?.nickname || '';
      const isAutoNick       = !opts.nickname && !DEFAULT_NICKNAME; // was auto-generated
      const needUpdateNick   = !isAutoNick && providedNickname && providedNickname !== currentNickname;
      const needMint         = !hasCredential;

      if (needUpdateNick) {
        log('[5]', `Updating profile: nickname="${providedNickname}" (was "${currentNickname}")`);
        try {
          const profileResult = await api.updateProfile(accessToken, providedNickname, identityType);
          log('OK ', `Profile updated: ${profileResult.accountStatus}`);
        } catch (e) {
          log(' ! ', `Profile update skipped: ${e.message}`);
        }
      }

      if (!needMint && !needUpdateNick) {
        log('OK ', 'Account already ACTIVE with credential - nothing to do!');
        bridge.pushAction('done', { title: 'Already Active', message: 'Account is already ACTIVE. You can close this page.' });
        return report(address, { accountStatus, user, wallet, hasCredential }, null);
      }

      if (needMint) {
        log('OK ', 'Account ACTIVE but missing credential - proceeding to mint.');
        // Fall through to Step 6 below
      } else {
        bridge.pushAction('done', { title: 'Profile Updated', message: 'Profile updated. You can close this page.' });
        return report(address, { accountStatus, user, wallet, hasCredential }, null);
      }
    }

    // Step 6: Credential / SBT Mint
    const needMintFlow = accountStatus === 'ACCOUNT_STATUS_PROFILE_REQUIRED' ||
                         accountStatus === 'ACCOUNT_STATUS_CREDENTIAL_REQUIRED' ||
                         (accountStatus === 'ACCOUNT_STATUS_ACTIVE' && !hasCredential);
    if (needMintFlow) {

      const contractAddress = CFG.sbtContract;
      const mintChainId = CFG.chainId;

      log('[6a]', `SBT Contract: ${contractAddress} | Chain: ${mintChainId}`);

      log('[6a]', 'Checking mint status...');
      const { mintEnded } = await api.checkMintStatus();
      if (mintEnded) {
        log(' ! ', 'Mint has ended — cannot mint SBT at this time.');
        bridge.pushAction('done', { title: 'Mint Ended', message: 'Minting is no longer available. You can close this page.' });
        return report(address, { accountStatus, user, wallet, hasCredential }, null);
      }
      log('OK ', 'Mint is still open — proceeding.');

      log('[6b]', `Requesting mint signature (twitter: @${twitterUser})...`);
      const { signature: serverSig, verified } = await api.getMintSignature(
        address, twitterUser, contractAddress, mintChainId
      );
      if (!verified) throw new Error('Mint signature verification failed');
      log('OK  ', `Server signature: ${serverSig.slice(0, 10)}...`);

      const encodedData = encodeMintCall(serverSig);
      log('[6c]', `Encoded call data (${encodedData.length} chars)`);

      log('[6d]', 'Requesting mint transaction...');
      bridge.pushAction('mint', { to: contractAddress, data: encodedData, address });
      const mintResult = await bridge.waitForSubmit(120000);
      if (mintResult.error) throw new Error(`Mint tx failed: ${mintResult.error} - ${mintResult.message}`);
      const txHash = mintResult.txHash;
      log('OK ', `Tx submitted: ${txHash}`);
      log('   ', `${CFG.bscscan}/tx/${txHash}`);

      await api.waitForTx(txHash);

      log('[6e]', 'Verifying credential...');
      await sleep(2000);
      const credResult = await api.getCredential(accessToken);

      if (credResult.accountStatus === 'ACCOUNT_STATUS_ACTIVE') {
        log('OK ', 'FULLY REGISTERED + SBT MINTED! Account is ACTIVE.');
        bridge.pushAction('done', { title: 'Registration + SBT Mint Complete!', message: 'Tx: ' + txHash.slice(0,10) + '... You can close this page.' });
        return report(address, credResult, txHash);
      } else {
        log(' ! ', `Credential: ${credResult.accountStatus} - may need a moment to propagate`);
        bridge.pushAction('done', { title: 'Processing...', message: 'Transaction submitted. Credential may take a moment. You can close this page.' });
        return report(address, credResult, txHash);
      }
    }

    throw new Error(`Unexpected accountStatus: ${accountStatus}`);

  } catch (e) {
    if (e instanceof ApiError) {
      log('ERR', e.message);
      const detail = typeof e.data === 'object' ? e.data : {};
      if (detail.error === 'INVALID_TOKEN') log('TIP', 'Session token expired - restart with fresh login.');
      else if (detail.error === 'NONCE_MISSING') log('TIP', 'Nonce expired - retry.');
      else if (detail.error === 'INVALID_SIGNATURE') log('TIP', 'Signature mismatch - ensure correct wallet and message.');
    } else {
      log('ERR', e.message);
    }
    try { bridge.pushAction('error', { message: e.message }); } catch(_) {}
    process.exitCode = 1;
  } finally {
    await sleep(2000);
    await bridge.close();
  }
}

function report(address, statusObj, txHash) {
  console.log('');
  console.log('============================================================');
  console.log('  RESULT');
  console.log('============================================================');
  console.log(`  Wallet:     ${address}`);
  console.log(`  Status:     ${statusObj.accountStatus || 'unknown'}`);
  if (statusObj.user?.nickname) console.log(`  Nickname:   ${statusObj.user.nickname}`);
  if (statusObj.hasCredential !== undefined) console.log(`  Credential: ${statusObj.hasCredential}`);
  if (txHash) {
    console.log(`  Tx Hash:    ${txHash}`);
    console.log(`  Explorer:   ${CFG.bscscan}/tx/${txHash}`);
  }
  console.log('============================================================');
}

main().catch(e => { log('ERR', `Unhandled: ${e.message}`); process.exit(1); });
