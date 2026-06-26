#!/bin/bash
# fast-swap.sh
# Builds swap transaction without confirmation
# Usage: ./fast-swap.sh <chain> <tokenIn> <tokenOut> <amount> <sender> <slippageBps>
# Slippage in basis points (100 = 1%). API expects percentage; script converts automatically.
# All progress output goes to stderr; only JSON is printed to stdout for piping.

set -e  # Exit on error

# Configuration
API_BASE="https://open-api.openocean.finance/v4"
NATIVE_TOKEN_ADDRESS="0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"

# Default values: slippage in basis points (100 bps = 1%). API expects percentage (1 = 1%), so we convert.
SLIPPAGE_BPS=${6:-100}
SLIPPAGE_API=$(python3 -c "print(round($SLIPPAGE_BPS / 100, 2))" 2>/dev/null || echo "1")
# Ensure we have a value (default 1 = 1%)
if [ -z "$SLIPPAGE_API" ]; then SLIPPAGE_API=1; fi

# Validate arguments
if [ $# -lt 5 ]; then
    echo "Usage: $0 <chain> <tokenIn> <tokenOut> <amount> <sender> [slippageBps]" >&2
    echo "Example: $0 ethereum ETH USDC 1 0x742d35Cc6634C0532925a3b844Bc9e90F1b6fB28 100" >&2
    exit 1
fi

CHAIN="$1"
TOKEN_IN="$2"
TOKEN_OUT="$3"
AMOUNT="$4"
SENDER="$5"

echo "[*] Building swap: $AMOUNT $TOKEN_IN -> $TOKEN_OUT on $CHAIN" >&2
echo "   Sender: $SENDER" >&2
echo "   Slippage: $SLIPPAGE_BPS bps (= ${SLIPPAGE_API}% for API)" >&2

# Step 1: Resolve token addresses
resolve_token_address() {
    local symbol="$1"
    local chain="$2"
    
    local symbol_lower=$(echo "$symbol" | tr '[:upper:]' '[:lower:]')
    
    case "$symbol_lower" in
        eth|ether|ethereum)
            echo "$NATIVE_TOKEN_ADDRESS"
            echo "18"
            return 0
            ;;
        usdc)
            case "$chain" in
                ethereum|1)
                    echo "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
                    echo "6"
                    ;;
                bsc|56)
                    echo "0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d"
                    echo "18"
                    ;;
                polygon|137)
                    echo "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"
                    echo "6"
                    ;;
                arbitrum|42161)
                    echo "0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8"
                    echo "6"
                    ;;
                *)
                    query_token_api "$symbol" "$chain"
                    ;;
            esac
            return 0
            ;;
        usdt)
            case "$chain" in
                ethereum|1)
                    echo "0xdAC17F958D2ee523a2206206994597C13D831ec7"
                    echo "6"
                    ;;
                bsc|56)
                    echo "0x55d398326f99059fF775485246999027B3197955"
                    echo "18"
                    ;;
                *)
                    query_token_api "$symbol" "$chain"
                    ;;
            esac
            return 0
            ;;
        *)
            query_token_api "$symbol" "$chain"
            ;;
    esac
}

query_token_api() {
    local symbol="$1"
    local chain="$2"
    local symbol_lower
    symbol_lower=$(echo "$symbol" | tr '[:upper:]' '[:lower:]')

    echo "   Querying OpenOcean token API for $symbol on $chain..." >&2
    
    TOKEN_LIST_RESPONSE=$(curl -s "$API_BASE/$chain/tokenList")
    
    if [ $? -ne 0 ]; then
        echo "Failed to query token API" >&2
        exit 1
    fi

    TOKEN_DATA=$(echo "$TOKEN_LIST_RESPONSE" | jq -r --arg symbol "$symbol_lower" '.data[] | select((.symbol | ascii_downcase) == $symbol) | [.address, .decimals] | @tsv' | head -1)

    if [ -z "$TOKEN_DATA" ]; then
        echo "Token $symbol not found on $chain" >&2
        exit 1
    fi
    
    TOKEN_ADDR=$(echo "$TOKEN_DATA" | cut -f1)
    TOKEN_DECIMALS=$(echo "$TOKEN_DATA" | cut -f2)
    
    echo "$TOKEN_ADDR"
    echo "$TOKEN_DECIMALS"
}

echo "   Resolving $TOKEN_IN address..." >&2
TOKEN_IN_DATA=$(resolve_token_address "$TOKEN_IN" "$CHAIN")
TOKEN_IN_ADDR=$(echo "$TOKEN_IN_DATA" | head -1)
TOKEN_IN_DECIMALS=$(echo "$TOKEN_IN_DATA" | tail -1)

echo "   Resolving $TOKEN_OUT address..." >&2
TOKEN_OUT_DATA=$(resolve_token_address "$TOKEN_OUT" "$CHAIN")
TOKEN_OUT_ADDR=$(echo "$TOKEN_OUT_DATA" | head -1)
TOKEN_OUT_DECIMALS=$(echo "$TOKEN_OUT_DATA" | tail -1)

echo "Token addresses resolved:" >&2
echo "   $TOKEN_IN: $TOKEN_IN_ADDR (decimals: $TOKEN_IN_DECIMALS)" >&2
echo "   $TOKEN_OUT: $TOKEN_OUT_ADDR (decimals: $TOKEN_OUT_DECIMALS)" >&2

echo "Fetching gas price..." >&2
GAS_PRICE_RESPONSE=$(curl -s "$API_BASE/$CHAIN/gasPrice")
if [ $? -ne 0 ]; then
    echo "Failed to fetch gas price" >&2
    exit 1
fi

# Per OpenOcean API v4: Ethereum returns data.standard.legacyGasPrice / data.base (wei);
# other EVM chains may return data.standard as a number (wei). All values in wei.
GAS_PRICE=$(echo "$GAS_PRICE_RESPONSE" | jq -r '.data.standard.legacyGasPrice // .data.standard // .data.base')
if [ "$GAS_PRICE" = "null" ] || [ -z "$GAS_PRICE" ]; then
    echo "Could not extract gas price from response" >&2
    exit 1
fi

echo "Gas price: $GAS_PRICE wei" >&2

echo "Converting amount to wei..." >&2
AMOUNT_IN_WEI=$(python3 -c "
amount = $AMOUNT
decimals = $TOKEN_IN_DECIMALS
result = int(amount * (10 ** decimals))
print(result)
")

echo "Amount in wei: $AMOUNT_IN_WEI" >&2

echo "Getting swap quote with calldata..." >&2
SWAP_URL="$API_BASE/$CHAIN/swap?inTokenAddress=$TOKEN_IN_ADDR&outTokenAddress=$TOKEN_OUT_ADDR&amountDecimals=$AMOUNT_IN_WEI&gasPriceDecimals=$GAS_PRICE&slippage=$SLIPPAGE_API&account=$SENDER"

SWAP_RESPONSE=$(curl -s "$SWAP_URL")
if [ $? -ne 0 ]; then
    echo "Failed to call swap API" >&2
    exit 1
fi

RESPONSE_CODE=$(echo "$SWAP_RESPONSE" | jq -r '.code')
if [ "$RESPONSE_CODE" != "200" ]; then
    ERROR_MSG=$(echo "$SWAP_RESPONSE" | jq -r '.message // "Unknown error"')
    echo "API error $RESPONSE_CODE: $ERROR_MSG" >&2
    exit 1
fi

FROM=$(echo "$SWAP_RESPONSE" | jq -r '.data.from')
TO=$(echo "$SWAP_RESPONSE" | jq -r '.data.to')
VALUE=$(echo "$SWAP_RESPONSE" | jq -r '.data.value')
DATA=$(echo "$SWAP_RESPONSE" | jq -r '.data.data')
GAS=$(echo "$SWAP_RESPONSE" | jq -r '.data.estimatedGas')
CHAIN_ID=$(echo "$SWAP_RESPONSE" | jq -r '.data.chainId')
# Use gas price from swap response so the transaction matches the quote (OpenOcean API v4).
SWAP_GAS_PRICE=$(echo "$SWAP_RESPONSE" | jq -r '.data.gasPrice')
if [ -z "$SWAP_GAS_PRICE" ] || [ "$SWAP_GAS_PRICE" = "null" ]; then
    SWAP_GAS_PRICE="$GAS_PRICE"
fi

if [ -z "$DATA" ] || [ "$DATA" = "null" ]; then
    echo "No calldata in response" >&2
    exit 1
fi

# Gas fee in wei = gas limit * gas price (both from swap response). All units per API v4: wei.
GAS_FEE_WEI=$(python3 -c "
gas = int($GAS)
price = int('$SWAP_GAS_PRICE')
print(gas * price)
" 2>/dev/null || echo "0")
GAS_FEE_ETH=$(python3 -c "print(int('$GAS_FEE_WEI') / 1e18)" 2>/dev/null || echo "0")
GAS_PRICE_GWEI=$(python3 -c "print(int('$SWAP_GAS_PRICE') / 1e9)" 2>/dev/null || echo "0")

echo "Swap transaction built successfully" >&2
echo "   From: $FROM | To: $TO | Value: $VALUE wei | Gas: $GAS | Gas price: $SWAP_GAS_PRICE wei ($GAS_PRICE_GWEI Gwei) | Chain: $CHAIN_ID" >&2
echo "   Est. gas fee: $GAS_FEE_ETH ETH ($GAS_FEE_WEI wei)" >&2

# Only JSON to stdout for execute-swap.sh
# gasPrice is in wei (per OpenOcean API v4). gasPriceGwei and gasFeeEth prevent unit confusion downstream.
cat <<EOF
{
  "from": "$FROM",
  "to": "$TO",
  "value": "$VALUE",
  "data": "$DATA",
  "gas": "$GAS",
  "gasPrice": "$SWAP_GAS_PRICE",
  "gasPriceGwei": "$GAS_PRICE_GWEI",
  "gasFeeWei": "$GAS_FEE_WEI",
  "gasFeeEth": "$GAS_FEE_ETH",
  "chainId": "$CHAIN_ID",
  "tokenIn": "$TOKEN_IN",
  "tokenOut": "$TOKEN_OUT",
  "amount": "$AMOUNT",
  "slippage": "$SLIPPAGE_BPS"
}
EOF
