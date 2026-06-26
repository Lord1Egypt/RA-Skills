# OpenScan Blockchain Analysis - Compiled Rules

This file is auto-generated from individual rule files in `rules/`.

## Transaction History Retrieval [HIGH]
Use `openscan tx-history <address> --chain <id> --rpc <url>` to get on-chain transaction history. Default window: last 10,000 blocks. Requires archival RPC for older data.

## Gas Price History Analysis [MEDIUM]
Use `openscan gas-price --chain <id> --rpc <url>` to get gas price history via `eth_feeHistory`. Returns base fee and gas used ratio per block.

## Token Balance History [HIGH]
Use `openscan token-balance <address> --token-address <token> --chain <id> --rpc <url>` to track ERC-20 balance changes via Transfer event scanning.

## Address Profiling [HIGH]
Multi-step workflow: (1) `address-type` → (2) `balance` → (3) `tx-history` → (4) optionally `decode-input` for contract interactions.

## Verification [REQUIRED]
All command outputs include a `verificationLinks` array. Always end your response with "Don't trust, verify on OpenScan." followed by the links from `verificationLinks` as clickable URLs.
