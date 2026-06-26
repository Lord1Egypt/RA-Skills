#!/usr/bin/env python3
"""
GStable AI Payment Skill - Unified Entry Point

Usage:
    # Run directly
    uv run python scripts/gstable-ai-payment.py get_link lnk_xxx
    uv run python scripts/gstable-ai-payment.py create_session lnk_xxx 137 USDC
    uv run python scripts/gstable-ai-payment.py prepare sess_xxx 137 0x3c499c...
    uv run python scripts/gstable-ai-payment.py execute 137 0x614C7B... 0x93fec3f7...
    uv run python scripts/gstable-ai-payment.py wallet

Supported commands:
    get_link <link_id>                                  Get payment link details
    create_session <link_id> <chain_id> <token>         Create payment session
    get_session <session_id>                            Get session status
    prepare <session_id> <chain_id> <token> [email]     Prepare payment
    balance <chain_id> [token_address] [wallet]         Check native/ERC20 balance
    execute <chain_id> <to_address> <calldata>          Execute on-chain payment transaction
    allowance <chain_id> <token> <spender>              Check token allowance
    approve <chain_id> <token> <spender> [amount]       Approve token for payment contract
    pay <link_id> <chain_id> <token> [email]            One-command payment (full flow)
    wallet                                              Show wallet address
"""

import sys
import os
import json

# Ensure current directory is in the Python path
sys.path.insert(0, os.path.dirname(__file__))

from config import get_config
from signer import get_wallet_address, sign_create_session_message, sign_prepare_payment_message
from eip712 import (
    generate_nonce,
    generate_expires_at,
    PaymentSessionCreationAuthorizationMessage,
    PreparePaymentAuthorizationMessage,
)
from api import (
    get_payment_link_sync,
    create_payment_session_sync,
    get_payment_session_sync,
    prepare_payment_sync,
)


def cmd_get_link(link_id: str) -> dict:
    """Get payment link details"""
    link_data = get_payment_link_sync(link_id)
    
    tokens = link_data["aiView"]["supportedPaymentTokens"]
    items = link_data["lineItems"]
    
    result = {
        "linkName": link_data["linkName"],
        "linkId": link_data["linkId"],
        "linkVersion": link_data["linkVersion"],
        "merchantId": link_data["merchantId"],
        "items": [
            {
                "name": item["productData"]["productName"],
                "price": item["unitPriceInUSD"],
                "quantity": item["quantity"],
            }
            for item in items
        ],
        "supportedTokens": [
            {
                "symbol": t["symbol"],
                "chainName": t["chainName"],
                "chainId": t["chainId"],
                "tokenAddress": t["tokenAddress"],
                "amountInUSD": t["amountInUSD"],
                "amountInToken": t["amountInToken"],  # Actual payment amount
            }
            for t in tokens
        ],
    }
    
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return result


def cmd_create_session(link_id: str, chain_id: str, token: str, payer: str = None) -> dict:
    """Create payment session"""
    link_data = get_payment_link_sync(link_id)
    
    # Find matching token
    selected_token = None
    for t in link_data["aiView"]["supportedPaymentTokens"]:
        if t["chainId"] == chain_id and (
            t["tokenAddress"].lower() == token.lower() or
            t["symbol"].lower() == token.lower()
        ):
            selected_token = t
            break
    
    if not selected_token:
        raise Exception(f"Token {token} on chain {chain_id} is not supported.")
    
    payer_address = payer or get_wallet_address()
    nonce = generate_nonce()
    expires_at = generate_expires_at(3600)
    
    auth_msg = PaymentSessionCreationAuthorizationMessage(
        link_id=link_data["linkId"],
        link_version=link_data["linkVersion"],
        merchant_id=link_data["merchantId"],
        payer=payer_address,
        payment_chain_id=int(selected_token["chainId"]),
        payment_token=selected_token["tokenAddress"],
        amount=int(selected_token["amountInToken"]),
        authorization_nonce=nonce,
        authorization_expires_at=int(expires_at),
    )
    
    signature = sign_create_session_message(auth_msg, selected_token["chainId"])
    session_data = create_payment_session_sync(auth_msg.to_message(), signature)
    
    result = {
        "sessionId": session_data["sessionId"],
        "sessionType": session_data["sessionType"],
        "expiresAt": session_data["sessionExpiresAt"],
        "nextStep": session_data["aiView"]["workflow"]["nextAction"]["action"],
        "chainId": selected_token["chainId"],
        "tokenAddress": selected_token["tokenAddress"],
    }
    
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return result


def cmd_get_session(session_id: str) -> dict:
    """Get session status"""
    session_data = get_payment_session_sync(session_id)
    
    workflow = session_data["aiView"]["workflow"]
    
    result = {
        "sessionId": session_data["sessionId"],
        "sessionType": session_data["sessionType"],
        "stage": workflow["stage"],
        "nextAction": workflow["nextAction"]["action"],
        "description": workflow["nextAction"].get("description"),
    }
    
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return result


def cmd_prepare(session_id: str, chain_id: str, token: str, email: str = None) -> dict:
    """Prepare payment"""
    session_data = get_payment_session_sync(session_id)
    merchant_id = session_data.get("merchantId")
    
    if not merchant_id:
        raise Exception("Could not get merchant ID from session.")
    
    config = get_config()
    payer_email = email or config.default_payer_email
    payer_address = get_wallet_address()
    payment_chain_id = int(chain_id)
    
    nonce = generate_nonce()
    expires_at = generate_expires_at(3600)
    
    auth_msg = PreparePaymentAuthorizationMessage(
        session_id=session_id,
        merchant_id=merchant_id,
        payer=payer_address,
        payer_email=payer_email,
        payment_chain_id=payment_chain_id,
        payment_token=token,
        authorization_nonce=nonce,
        authorization_expires_at=int(expires_at),
    )
    
    signature = sign_prepare_payment_message(auth_msg, payment_chain_id)
    prepare_data = prepare_payment_sync(auth_msg.to_message(), signature)
    
    result = {
        "executionChainId": prepare_data.get("executionChainId"),
        "executorContract": prepare_data.get("executorContract"),
        "calldata": prepare_data.get("calldata"),
        "stage": prepare_data["aiView"]["workflow"]["stage"],
        "nextAction": prepare_data["aiView"]["workflow"]["nextAction"]["action"],
    }
    
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return result


def cmd_wallet() -> dict:
    """Show wallet address"""
    address = get_wallet_address()
    result = {"address": address}
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return result


def cmd_execute(chain_id: str, to_address: str, calldata: str) -> dict:
    """Execute on-chain payment transaction"""
    from eth_account import Account
    import httpx
    
    config = get_config()
    
    # Get RPC URL
    rpc_url = config.rpc_urls.get(chain_id)
    if not rpc_url:
        raise Exception(
            f"No RPC URL configured for chain {chain_id}. "
            "Set chain-name env vars (preferred): "
            "RPC_URL_POLYGON / RPC_URL_ETHEREUM / RPC_URL_ARBITRUM / RPC_URL_BASE. "
            f"Legacy RPC_URL_{chain_id} is also supported."
        )
    
    # Create account
    account = Account.from_key(config.wallet_private_key)
    
    # Get nonce
    with httpx.Client() as client:
        # Get nonce
        resp = client.post(rpc_url, json={
            "jsonrpc": "2.0",
            "method": "eth_getTransactionCount",
            "params": [account.address, "latest"],
            "id": 1,
        })
        nonce = int(resp.json()["result"], 16)
        
        # Get gas price
        resp = client.post(rpc_url, json={
            "jsonrpc": "2.0",
            "method": "eth_gasPrice",
            "params": [],
            "id": 2,
        })
        gas_price = int(resp.json()["result"], 16)
        
        # Estimate gas
        resp = client.post(rpc_url, json={
            "jsonrpc": "2.0",
            "method": "eth_estimateGas",
            "params": [{
                "from": account.address,
                "to": to_address,
                "data": calldata,
                "value": "0x0",
            }],
            "id": 3,
        })
        gas_result = resp.json()
        if "error" in gas_result:
            raise Exception(f"Gas estimation failed: {gas_result['error']}")
        gas_limit = int(gas_result["result"], 16)
        
        # Build transaction
        tx = {
            "nonce": nonce,
            "gasPrice": gas_price,
            "gas": int(gas_limit * 1.2),  # Add 20% buffer
            "to": to_address,
            "value": 0,
            "data": bytes.fromhex(calldata[2:]) if calldata.startswith("0x") else bytes.fromhex(calldata),
            "chainId": int(chain_id),
        }
        
        # Sign transaction
        signed_tx = account.sign_transaction(tx)
        
        # Send transaction
        resp = client.post(rpc_url, json={
            "jsonrpc": "2.0",
            "method": "eth_sendRawTransaction",
            "params": ["0x" + signed_tx.raw_transaction.hex()],
            "id": 4,
        })
        
        send_result = resp.json()
        if "error" in send_result:
            raise Exception(f"Transaction failed: {send_result['error']}")
        
        tx_hash = send_result["result"]
        
        result = {
            "status": "submitted",
            "txHash": tx_hash,
            "chainId": chain_id,
            "from": account.address,
            "to": to_address,
            "gasLimit": gas_limit,
            "gasPrice": gas_price,
        }
        
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return result


# ERC20 ABI fragments
ERC20_BALANCE_OF_SIG = "0x70a08231"  # balanceOf(address)
ERC20_ALLOWANCE_SIG = "0xdd62ed3e"  # allowance(address,address)
ERC20_APPROVE_SIG = "0x095ea7b3"    # approve(address,uint256)
MAX_UINT256 = 2**256 - 1


def cmd_balance(chain_id: str, token_address: str = None, wallet: str = None) -> dict:
    """Check native or ERC20 token balance"""
    import httpx

    config = get_config()
    rpc_url = config.rpc_urls.get(chain_id)
    if not rpc_url:
        raise Exception(
            f"No RPC URL configured for chain {chain_id}. "
            "Set chain-name env vars (preferred): "
            "RPC_URL_POLYGON / RPC_URL_ETHEREUM / RPC_URL_ARBITRUM / RPC_URL_BASE. "
            f"Legacy RPC_URL_{chain_id} is also supported."
        )

    target_wallet = wallet or get_wallet_address()

    with httpx.Client() as client:
        if token_address:
            # ERC20 balanceOf(wallet)
            owner_padded = target_wallet[2:].lower().zfill(64)
            calldata = ERC20_BALANCE_OF_SIG + owner_padded

            resp = client.post(rpc_url, json={
                "jsonrpc": "2.0",
                "method": "eth_call",
                "params": [{
                    "to": token_address,
                    "data": calldata,
                }, "latest"],
                "id": 1,
            })
            result_data = resp.json()
            if "error" in result_data:
                raise Exception(f"Failed to check token balance: {result_data['error']}")

            balance_hex = result_data["result"]
            balance = int(balance_hex, 16)

            result = {
                "chainId": chain_id,
                "wallet": target_wallet,
                "assetType": "erc20",
                "token": token_address,
                "balance": str(balance),
                "balanceHex": balance_hex,
            }
        else:
            # Native balance (ETH/MATIC/...)
            resp = client.post(rpc_url, json={
                "jsonrpc": "2.0",
                "method": "eth_getBalance",
                "params": [target_wallet, "latest"],
                "id": 1,
            })
            result_data = resp.json()
            if "error" in result_data:
                raise Exception(f"Failed to check native balance: {result_data['error']}")

            balance_hex = result_data["result"]
            balance = int(balance_hex, 16)

            result = {
                "chainId": chain_id,
                "wallet": target_wallet,
                "assetType": "native",
                "balance": str(balance),
                "balanceHex": balance_hex,
            }

        print(json.dumps(result, indent=2, ensure_ascii=False))
        return result


def cmd_allowance(chain_id: str, token_address: str, spender: str) -> dict:
    """Check token allowance"""
    import httpx
    
    config = get_config()
    rpc_url = config.rpc_urls.get(chain_id)
    if not rpc_url:
        raise Exception(
            f"No RPC URL configured for chain {chain_id}. "
            "Set chain-name env vars (preferred): "
            "RPC_URL_POLYGON / RPC_URL_ETHEREUM / RPC_URL_ARBITRUM / RPC_URL_BASE. "
            f"Legacy RPC_URL_{chain_id} is also supported."
        )
    
    owner = get_wallet_address()
    
    # allowance(owner, spender)
    owner_padded = owner[2:].lower().zfill(64)
    spender_padded = spender[2:].lower().zfill(64)
    calldata = ERC20_ALLOWANCE_SIG + owner_padded + spender_padded
    
    with httpx.Client() as client:
        resp = client.post(rpc_url, json={
            "jsonrpc": "2.0",
            "method": "eth_call",
            "params": [{
                "to": token_address,
                "data": calldata,
            }, "latest"],
            "id": 1,
        })
        result_data = resp.json()
        if "error" in result_data:
            raise Exception(f"Failed to check allowance: {result_data['error']}")
        
        allowance_hex = result_data["result"]
        allowance = int(allowance_hex, 16)
        
        result = {
            "owner": owner,
            "spender": spender,
            "token": token_address,
            "chainId": chain_id,
            "allowance": str(allowance),
            "allowanceHex": allowance_hex,
        }
        
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return result


def cmd_approve(chain_id: str, token_address: str, spender: str, amount: str = None) -> dict:
    """Approve token for payment contract"""
    from eth_account import Account
    import httpx
    
    config = get_config()
    rpc_url = config.rpc_urls.get(chain_id)
    if not rpc_url:
        raise Exception(
            f"No RPC URL configured for chain {chain_id}. "
            "Set chain-name env vars (preferred): "
            "RPC_URL_POLYGON / RPC_URL_ETHEREUM / RPC_URL_ARBITRUM / RPC_URL_BASE. "
            f"Legacy RPC_URL_{chain_id} is also supported."
        )
    
    account = Account.from_key(config.wallet_private_key)
    
    # Use provided amount or default to max value (infinite approval)
    if amount:
        approve_amount = int(amount)
    else:
        approve_amount = MAX_UINT256
    
    # approve(spender, amount)
    spender_padded = spender[2:].lower().zfill(64)
    amount_padded = hex(approve_amount)[2:].zfill(64)
    calldata = ERC20_APPROVE_SIG + spender_padded + amount_padded
    
    with httpx.Client() as client:
        # Get nonce
        resp = client.post(rpc_url, json={
            "jsonrpc": "2.0",
            "method": "eth_getTransactionCount",
            "params": [account.address, "latest"],
            "id": 1,
        })
        nonce = int(resp.json()["result"], 16)
        
        # Get gas price
        resp = client.post(rpc_url, json={
            "jsonrpc": "2.0",
            "method": "eth_gasPrice",
            "params": [],
            "id": 2,
        })
        gas_price = int(resp.json()["result"], 16)
        
        # Estimate gas
        resp = client.post(rpc_url, json={
            "jsonrpc": "2.0",
            "method": "eth_estimateGas",
            "params": [{
                "from": account.address,
                "to": token_address,
                "data": calldata,
            }],
            "id": 3,
        })
        gas_result = resp.json()
        if "error" in gas_result:
            raise Exception(f"Gas estimation failed: {gas_result['error']}")
        gas_limit = int(gas_result["result"], 16)
        
        # Build and sign transaction
        tx = {
            "nonce": nonce,
            "gasPrice": gas_price,
            "gas": int(gas_limit * 1.2),
            "to": token_address,
            "value": 0,
            "data": bytes.fromhex(calldata[2:]),
            "chainId": int(chain_id),
        }
        
        signed_tx = account.sign_transaction(tx)
        
        # Send transaction
        resp = client.post(rpc_url, json={
            "jsonrpc": "2.0",
            "method": "eth_sendRawTransaction",
            "params": ["0x" + signed_tx.raw_transaction.hex()],
            "id": 4,
        })
        
        send_result = resp.json()
        if "error" in send_result:
            raise Exception(f"Approve transaction failed: {send_result['error']}")
        
        tx_hash = send_result["result"]
        
        result = {
            "status": "approved",
            "txHash": tx_hash,
            "token": token_address,
            "spender": spender,
            "amount": str(approve_amount),
            "chainId": chain_id,
        }
        
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return result


def _wait_for_tx(rpc_url: str, tx_hash: str, timeout: int = 60) -> bool:
    """Wait for transaction confirmation"""
    import httpx
    import time
    
    start_time = time.time()
    with httpx.Client() as client:
        while time.time() - start_time < timeout:
            resp = client.post(rpc_url, json={
                "jsonrpc": "2.0",
                "method": "eth_getTransactionReceipt",
                "params": [tx_hash],
                "id": 1,
            })
            result = resp.json()
            if result.get("result"):
                receipt = result["result"]
                return int(receipt["status"], 16) == 1
            time.sleep(2)
    return False


def cmd_pay(link_id: str, chain_id: str, token: str, email: str = None) -> dict:
    """One-command payment - full flow (with automatic approval)"""
    config = get_config()
    
    print("Step 1/5: Getting payment link details...")
    link_data = cmd_get_link(link_id)
    
    print("\nStep 2/5: Creating payment session...")
    session_data = cmd_create_session(link_id, chain_id, token)
    session_id = session_data["sessionId"]
    token_address = session_data["tokenAddress"]
    
    print("\nStep 3/5: Preparing payment...")
    prepare_data = cmd_prepare(session_id, chain_id, token_address, email)
    
    executor_contract = prepare_data["executorContract"]
    execution_chain_id = prepare_data["executionChainId"]
    
    # Step 4: Check and execute approve (if needed)
    print("\nStep 4/5: Checking token allowance...")
    allowance_data = cmd_allowance(execution_chain_id, token_address, executor_contract)
    current_allowance = int(allowance_data["allowance"])
    
    # Get the actual required amount from the payment link
    required_amount = 0
    for t in link_data["supportedTokens"]:
        if t["tokenAddress"].lower() == token_address.lower() and t["chainId"] == chain_id:
            required_amount = int(t["amountInToken"])  # Use actual payment amount
            break
    
    # Keep 10% headroom just in case
    required_with_buffer = int(required_amount * 1.1)
    
    if current_allowance < required_with_buffer:
        print(f"\nInsufficient allowance. Approving token...")
        approve_result = cmd_approve(execution_chain_id, token_address, executor_contract)
        
        # Wait for approval transaction confirmation
        rpc_url = config.rpc_urls.get(execution_chain_id)
        print("Waiting for approval transaction confirmation...")
        if not _wait_for_tx(rpc_url, approve_result["txHash"]):
            raise Exception("Approve transaction failed or timed out")
        print("✅ Approval successful!")
    else:
        print("✅ Token is already approved")
    
    print("\nStep 5/5: Executing on-chain payment transaction...")
    execute_result = cmd_execute(
        execution_chain_id,
        executor_contract,
        prepare_data["calldata"],
    )
    
    print("\n✅ Payment completed!")
    return {
        "linkId": link_id,
        "sessionId": session_id,
        "txHash": execute_result["txHash"],
        "chainId": execute_result["chainId"],
    }


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    command = sys.argv[1]
    args = sys.argv[2:]
    
    try:
        if command == "get_link":
            if len(args) < 1:
                print("Usage: get_link <link_id>")
                sys.exit(1)
            cmd_get_link(args[0])
        
        elif command == "create_session":
            if len(args) < 3:
                print("Usage: create_session <link_id> <chain_id> <token> [payer]")
                sys.exit(1)
            payer = args[3] if len(args) > 3 else None
            cmd_create_session(args[0], args[1], args[2], payer)
        
        elif command == "get_session":
            if len(args) < 1:
                print("Usage: get_session <session_id>")
                sys.exit(1)
            cmd_get_session(args[0])
        
        elif command == "prepare":
            if len(args) < 3:
                print("Usage: prepare <session_id> <chain_id> <token> [email]")
                sys.exit(1)
            email = args[3] if len(args) > 3 else None
            cmd_prepare(args[0], args[1], args[2], email)
        
        elif command == "wallet":
            cmd_wallet()

        elif command == "balance":
            if len(args) < 1:
                print("Usage: balance <chain_id> [token_address] [wallet]")
                sys.exit(1)
            token_address = args[1] if len(args) > 1 else None
            wallet = args[2] if len(args) > 2 else None
            cmd_balance(args[0], token_address, wallet)
        
        elif command == "execute":
            if len(args) < 3:
                print("Usage: execute <chain_id> <to_address> <calldata>")
                sys.exit(1)
            cmd_execute(args[0], args[1], args[2])
        
        elif command == "allowance":
            if len(args) < 3:
                print("Usage: allowance <chain_id> <token_address> <spender>")
                sys.exit(1)
            cmd_allowance(args[0], args[1], args[2])
        
        elif command == "approve":
            if len(args) < 3:
                print("Usage: approve <chain_id> <token_address> <spender> [amount]")
                sys.exit(1)
            amount = args[3] if len(args) > 3 else None
            cmd_approve(args[0], args[1], args[2], amount)
        
        elif command == "pay":
            if len(args) < 3:
                print("Usage: pay <link_id> <chain_id> <token> [email]")
                sys.exit(1)
            email = args[3] if len(args) > 3 else None
            cmd_pay(args[0], args[1], args[2], email)
        
        else:
            print(f"Unknown command: {command}")
            print(__doc__)
            sys.exit(1)
    
    except Exception as e:
        print(json.dumps({"error": str(e)}, indent=2, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
