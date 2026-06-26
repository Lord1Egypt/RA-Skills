---
name: morpho-market-creation
description: Deploys Morpho markets backed by API3 oracles.
metadata:
  version: 0.1.0
  clawdis:
    requires:
      bins:
        - ts-node
        - pnpm
      env:
        - WALLET_MNEMONIC
    primaryEnv: WALLET_MNEMONIC
---

# Morpho Market Creation

## Variables

| Variable | Description |
|---|---|
| `CHAIN_NAME` | Human-readable chain name (e.g. `Ethereum`) |
| `CHAIN_ALIAS` | Chain alias from the chain list (e.g. `ethereum`) |
| `CHAIN_ID` | Numeric chain ID (e.g. `1`) |
| `COLLATERAL_TOKEN` | Collateral asset symbol (e.g. `ETH`, `USDC`) |
| `LOAN_TOKEN` | Loan asset symbol (e.g. `DAI`, `USDT`) |
| `COLLATERAL_PROXY_ADDRESS` | Api3ReaderProxyV1 address for the collateral/USD feed — starts with `0x`, exactly 42 characters |
| `LOAN_PROXY_ADDRESS` | Api3ReaderProxyV1 address for the loan/USD feed — starts with `0x`, exactly 42 characters |

---

# Rules
- **NEVER** read .env files or ask for secrets such as WALLET_MNEMONIC.
- **ALWAYS** use the `exec` tool to run commands. Never use Bash or shell directly.
- **ALWAYS** run scripts in skill's directory, which is referenced as `{baseDir}` variable and name is given in this file's name field at top. Prefix every command with `cd {baseDir} &&` to ensure it runs from the correct directory.
- **ALWAYS** substitute actual variable values into every `exec` command before running it.
- **ALWAYS** after asking any question, stop and wait for the user's response. Do not assume a response or continue until the user has replied.
- **ALWAYS** complete the current phase fully before moving to the next. Never skip a phase or assume it is already done.
- Treat affirmative responses as approval (e.g. "yes", "sure", "ok", "go ahead", "yep"). Treat negative responses as rejection (e.g. "no", "nope", "cancel", "stop"). If intent is unclear, ask once more before acting.
- **NEVER** wrap URLs in markdown formatting (backticks, asterisks, brackets, etc.) or add trailing punctuation when sharing them with the user — share the raw URL as plain text so it stays clickable and isn't corrupted with extra characters.
- **ALWAYS** lowercase `<CHAIN_ALIAS>` and the token symbol (`<COLLATERAL_TOKEN>` / `<LOAN_TOKEN>`) when substituting them into market.api3.org URL paths (e.g. `https://market.api3.org/ethereum/eth-usd/integrate`), even if the confirmed values are stored/displayed with different casing.

## Phase 0: Introduction

- Introduce the skill: you will walk the user through deploying a Morpho Market backed by Api3 oracles, step by step. You will ask for approval before installing packages and before executing transactions.
- Ask if they are ready to begin and wait for an affirmative response before continuing.

---

## Phase 1: Package Installation

### Part 1.1

- **You must always run this step. Do not skip it, even if you think packages are already installed.**
- Inform the user that before any scripts can run, the required packages must be installed. Show them the list:
  - `@api3/dapi-management`
  - `@morpho-org/blue-sdk`
  - `dotenv`
  - `ethers`
- Ask for approval to run `pnpm install`. Wait for an affirmative response. Once approved, run the command regardless of whether packages may already be installed:
```
exec command="cd {baseDir} && pnpm install"
```
- If the output contains `[ERR_PNPM_IGNORED_BUILDS] Ignored build scripts: unrs-resolver...`, this is expected and not a real failure — the ignored build script is not needed for this skill. Treat it as success and continue.
- If the command fails for any other reason, inform the user and ask what to do. This step cannot be skipped.

---

## Phase 2: Collect and Validate Parameters

### Part 2.1
- Ask the user in a single message for: the chain they want to deploy on, the collateral token symbol, and the loan token symbol. Wait for all three answers before continuing.

### Part 2.2
- Run `get-dapis.ts` and `get-chains.ts` to fetch the list of available feeds and supported chains:
```
exec command="cd {baseDir} && ts-node {baseDir}/scripts/get-dapis.ts"
exec command="cd {baseDir} && ts-node {baseDir}/scripts/get-chains.ts"
```
- If script fails, let user know about the problem and ask what to do. This data is necessary for validating their input, so skipping is not an option.

### Part 2.3
- Validate `CHAIN_ALIAS`:
  - Search the output of `get-chains.ts` — first by `alias` field (case-insensitive), then by `name` field.
  - Match found: set `CHAIN_ALIAS`, `CHAIN_NAME`, `CHAIN_ID` and confirm the matched values with the user. If they say no, ask them to re-enter the chain and repeat.
  - No match: tell the user and ask them to re-enter the chain name or alias.

- Validate feeds:
  - Search the output of `get-dapis.ts` for `<COLLATERAL_TOKEN>/USD` and `<LOAN_TOKEN>/USD` (case-insensitive).
  - Both found: keep `COLLATERAL_TOKEN` and `LOAN_TOKEN` as bare token symbols only, and show the user the matched feed names (`<COLLATERAL_TOKEN>/USD` and `<LOAN_TOKEN>/USD`) for confirmation.
  - Either missing: tell the user which feed was not found, ask for a different token symbol, and repeat for the missing feed.

### Part 2.4
- Show the user all confirmed parameters:
  - Chain: `<CHAIN_NAME>` (`<CHAIN_ALIAS>`, ID: `<CHAIN_ID>`)
  - Collateral Token: `<COLLATERAL_TOKEN>`
  - Loan Token: `<LOAN_TOKEN>`
  - Matched Feeds: `<COLLATERAL_TOKEN>/USD`, `<LOAN_TOKEN>/USD`
- Ask the user to confirm that they want to proceed. If yes, proceed to Phase 3. If no, ask the user what they want to do.

---

## Phase 3: Test Oracle

### Part 3.1
- Warn the user that the found Api3 data feeds must be active on Api3 Market. Ask if they want to continue. If no, ask the user what they want to do.

### Part 3.2
- Ask the user to open https://market.api3.org/<CHAIN_ALIAS>/<COLLATERAL_TOKEN>-usd/integrate, copy the **Api3ReaderProxyV1 address**, and share it here.
  - Validate: must start with `0x` and be exactly 42 characters. If invalid, tell the user and ask them to re-enter.
  - Set `COLLATERAL_PROXY_ADDRESS` to the validated value.
- Run `read-data-feed.ts` to verify the collateral feed is active:
```
exec command="cd {baseDir} && ts-node {baseDir}/scripts/read-data-feed.ts <COLLATERAL_PROXY_ADDRESS> <CHAIN_ALIAS>"
```
- If the script fails, let user know about the problem and ask what to do.
- Show the value and timestamp from the output and ask the user if it looks correct. If no, ask them to recheck the URL and re-enter the address, then repeat.

- Ask the user to open https://market.api3.org/<CHAIN_ALIAS>/<LOAN_TOKEN>-usd/integrate, copy the **Api3ReaderProxyV1 address**, and share it here.
  - Validate: must start with `0x` and be exactly 42 characters. If invalid, tell the user and ask them to re-enter.
  - Set `LOAN_PROXY_ADDRESS` to the validated value.
- Run `read-data-feed.ts` to verify the loan feed is active:
```
exec command="cd {baseDir} && ts-node {baseDir}/scripts/read-data-feed.ts <LOAN_PROXY_ADDRESS> <CHAIN_ALIAS>"
```
- If the script fails, let user know about the problem and ask what to do.
- Show the value and timestamp from the output and ask the user if it looks correct. If no, ask them to recheck the URL and re-enter the address, then repeat.

### Part 3.3
- Direct the user to open https://oracles.morpho.dev/oracle-tester and select `<CHAIN_NAME>` as the chain. Ask them to select the collateral and loan assets from the dropdowns — they should confirm those contract addresses match the intended assets. Then paste `<COLLATERAL_PROXY_ADDRESS>` into **Base Feed1** and `<LOAN_PROXY_ADDRESS>` into **Quote Feed1**. Wait for confirmation before continuing.
- Ask the user to click **Run Oracle Tests** and report whether all tests passed.
  - If any failed: ask them to recheck the feed addresses from the integration URLs, correct them on the tester, and retry. Wait until all tests pass.
- Ask the user to click **Generate Safe Payload** to use later if needed. Proceed to Phase 4.

---

## Phase 4: Deploy Oracle

### Part 4.1
- Ask the user how they want to deploy the oracle, offering three options:
  - **Option 1 — Gnosis Safe** — upload the payload JSON to Safe{Wallet}
  - **Option 2 — Etherscan** — execute via Etherscan
  - **Option 3 — Script** — deploy on their behalf using a script
- Wait for the user to choose an option before continuing.

### Part 4.2 — Option 1: Gnosis Safe
- Instruct the user to download the generated payload JSON, then open Safe{Wallet}, click **New Transaction**, select **Transaction Builder**, upload the downloaded payload JSON, and follow the prompts to submit the transaction.
- Proceed to Phase 5.

### Part 4.2 — Option 2: Etherscan
- Run `get-oracle-contract-link.ts` to get the correct Etherscan URL:
```
exec command="cd {baseDir} && ts-node {baseDir}/scripts/get-oracle-contract-link.ts <CHAIN_ALIAS>"
```
- If the script fails, let user know about the problem and ask what to do.
- Instruct the user to open the provided Etherscan URL, connect their wallet, find the `createMorphoChainlinkOracleV2` function and fill in the parameters exactly as shown in the Morpho Oracle Tester.
- Proceed to Phase 5.

### Part 4.2 — Option 3: Script
- Ask the user to open `{baseDir}/oracle-params.json` and fill in the oracle constructor parameters using the values from the Morpho Oracle Tester: set `baseFeed1` to `<COLLATERAL_PROXY_ADDRESS>` and `quoteFeed1` to `<LOAN_PROXY_ADDRESS>`, and fill in the remaining fields (decimals, vaults, salt) to match. Also ask them to set `WALLET_MNEMONIC` in the `.env` file. Wait for confirmation.
- Ask for approval to run `deploy-oracle.ts`. Wait for an affirmative response, then run:
```
exec command="cd {baseDir} && ts-node {baseDir}/scripts/deploy-oracle.ts <CHAIN_ALIAS>"
```
- If the script fails, let user know about the problem and ask what to do.
- Show the user: transaction hash and deployed oracle address.
- Proceed to Phase 5.

---

## Phase 5: Create Market

### Part 5.1
- Ask the user to open `{baseDir}/market-params.json` and fill in the market parameters:
  - `loanToken` — contract address of the loan token (e.g. can be found at /tokens path of block explorer)
  - `collateralToken` — contract address of the collateral token (e.g. can be found at /tokens path of block explorer)
  - `oracle` — the oracle address deployed in Phase 4
  - `irm` — governance-approved Interest Rate Model address for `<CHAIN_NAME>` (tell the user to check https://docs.morpho.org/get-started/resources/addresses/#morpho-blue Adaptive Curve IRM model address)
  - `lltv` — liquidation LTV as a percentage number; suggested to be one of the governance-approved values: `0`, `38.5`, `62.5`, `77`, `86`, `91.5`, `94.5`, `96.5`, `98`
- Ask them to confirm `WALLET_MNEMONIC` is still set in the `.env` file. Wait for confirmation.

### Part 5.2
- Ask for approval to run `create-market.ts`. Wait for an affirmative response, then run:
```
exec command="cd {baseDir} && ts-node {baseDir}/scripts/create-market.ts <CHAIN_ALIAS>"
```
- If the script fails, let user know about the problem and ask what to do.
- Show the user the transaction hash and the market ID from the output.
