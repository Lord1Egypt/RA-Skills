# Sandbox & Testing (Base Sepolia)

This guide covers how to test the PayNode payment flow in a safe environment using the Base Sepolia Testnet.

## 1. Prerequisites

- Your wallet must have **Base Sepolia ETH** for gas.
- You must have **MockUSDC** on the testnet.

## 2. Mint Test Tokens

If your testnet wallet is low on USDC, run the minting script to receive **1,000 MockUSDC**:

```bash
# Execute from the skill root
bun run mint-test-tokens --json
```

Alternatively, you can mint manually via [Basescan Sepolia](https://sepolia.basescan.org/address/0x109AEddD656Ed2761d1e210E179329105039c784#writeContract).

## 3. Test Merchant: Doodle Wall (PoM)

The **Doodle Wall** is a live testnet merchant where you can "leave your mark" by completing a 0.01 USDC payment.

### API Specifications

| Method   | Description                                                                              | Input                                                                                                                                                                                | Output                                                                                                                                                                                                                                |
| :------- | :--------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **POST** | **Handshake**: Get payment parameters.<br>**Verification**: Verify on-chain transaction. | **Query**: `network` ("testnet") <br> **Header**: `x-paynode-receipt` (Optional), `x-paynode-order-id` (Required for verification) <br> **Body**: `agent_name` (Optional) | **402 (Payment Required)**: Returns headers (`x-paynode-*`) with contract, merchant, amount, token, order ID, etc.<br>**200 (Success)**: Returns JSON object with `status: "SUCCESS"`.<br>**400/500 (Error)**: Returns error message. |

- **Basic URL**: `https://paynode.dev/api/pom`
- **Method**: `POST`
- **Query Parameter**: `network=testnet`
- **Request Body (JSON)**:
  - `agent_name`: (String, Optional) The name you want to display on the leaderboard.

### How to Call (Using CLI)

Using our `request` script, it will automatically handle the 402 handshake, perform the payment, and verify the receipt in one go:

```bash
# Handshake + Auto-pay + Verification
bun run request "https://paynode.dev/api/pom?network=testnet" \
    --network testnet \
    -X POST \
    agent_name="My AI Agent" \
    --json
```

- **Web UI**: Visit [paynode.dev/pom?network=testnet](https://paynode.dev/pom?network=testnet) to see your Agent's name on the leaderboard.

## 4. Sandbox Configuration

- **Network**: Base Sepolia (Chain ID: `84532`)
- **Router Address**: `0x24cD8b68aaC209217ff5a6ef1Bf55a59f2c8Ca6F`
- **USDC Address**: `0x109AEddD656Ed2761d1e210E179329105039c784`
- **Merchant Address**: `0x598bF63F5449876efafa7b36b77Deb2070621C0E` (Treasury for demo)
