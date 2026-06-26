# Token Prices

Query current prices for ADA and INDY tokens.

## MCP Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `get_ada_price` | Get the current ADA price in USD | None |
| `get_indy_price` | Get the current INDY token price in ADA and USD | None |

## Examples

### Get ADA/USD price

Use `get_ada_price` to retrieve the current Cardano ADA price in USD. This is useful for converting ADA-denominated values to USD or providing price context for Cardano-native assets.

```
User: "What is the current price of ADA?"
Tool: get_ada_price
Response: Returns the current ADA price in USD (e.g., $0.45).
```

```
User: "How much is 1000 ADA worth in dollars?"
Tool: get_ada_price
Response: Returns ADA/USD price. Multiply by the amount to get the USD value.
```

### Get INDY price in ADA and USD

Use `get_indy_price` to retrieve the current INDY governance token price. This returns the price in both ADA and USD, which is useful since INDY primarily trades against ADA on Cardano DEXes.

```
User: "What's the INDY token price?"
Tool: get_indy_price
Response: Returns INDY price in both ADA (e.g., 2.15 ADA) and USD (e.g., $0.97).
```

```
User: "How much is INDY worth in ADA?"
Tool: get_indy_price
Response: Returns the INDY/ADA pair price along with the USD equivalent.
```

### Price source information

- **ADA price** is sourced from market aggregators and reflects the current ADA/USD trading price across major exchanges.
- **INDY price** is derived from Cardano DEX liquidity pools (primarily Minswap and SundaeSwap) where INDY/ADA pairs trade. The USD price is calculated by combining the INDY/ADA rate with the current ADA/USD price.

### Historical price context

The `get_ada_price` and `get_indy_price` tools return current spot prices only. They do not provide historical data or price charts. For price trend analysis, query the price at different times or combine with external data sources. These tools are best suited for:
- Real-time portfolio valuation
- Converting between ADA, INDY, and USD
- Displaying current market conditions alongside protocol data
