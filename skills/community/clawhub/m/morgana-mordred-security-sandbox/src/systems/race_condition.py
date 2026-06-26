#!/usr/bin/env python3
"""
RACE CONDITION — For Morgana Testing
Intentional vulnerability: Time-of-check to time-of-use (TOCTOU)
"""

import time
import threading
from datetime import datetime

# Simulated bank account
ACCOUNTS = {
    "alice": {"balance": 1000.00, " overdraft_allowed": False},
    "bob": {"balance": 500.00, "overdraft_allowed": True},
}

TRANSACTION_LOG = []

def check_balance(account):
    """Check balance without locking - RACE CONDITION"""
    if account in ACCOUNTS:
        return {"success": True, "balance": ACCOUNTS[account]["balance"]}
    return {"success": False, "error": "Account not found"}

def transfer_funds(from_account, to_account, amount):
    """
    VULNERABILITY: TOCTOU race condition!
    Checks balance, then transfers - but balance could change between check and transfer
    """
    # Step 1: Check balance (NO LOCK!)
    if from_account not in ACCOUNTS:
        return {"success": False, "error": "Source account not found"}
    if to_account not in ACCOUNTS:
        return {"success": False, "error": "Destination account not found"}
    
    current_balance = ACCOUNTS[from_account]["balance"]
    
    # Step 2: Simulate processing time (makes race window bigger)
    time.sleep(0.1)  # 100ms window for race condition
    
    # Step 3: Transfer (NO DOUBLE-CHECK!)
    if current_balance >= amount:
        ACCOUNTS[from_account]["balance"] -= amount
        ACCOUNTS[to_account]["balance"] += amount
        TRANSACTION_LOG.append({
            "from": from_account,
            "to": to_account,
            "amount": amount,
            "timestamp": datetime.now().isoformat(),
            "status": "COMPLETED"
        })
        return {"success": True, "new_balance": ACCOUNTS[from_account]["balance"]}
    else:
        return {"success": False, "error": "Insufficient funds"}

def withdraw(account, amount):
    """
    VULNERABILITY: No atomic operation!
    Could withdraw more than balance in concurrent requests
    """
    if account not in ACCOUNTS:
        return {"success": False, "error": "Account not found"}
    
    # Check balance
    if ACCOUNTS[account]["balance"] >= amount:
        # Simulate processing
        time.sleep(0.05)
        # Withdraw
        ACCOUNTS[account]["balance"] -= amount
        return {"success": True, "new_balance": ACCOUNTS[account]["balance"]}
    
    return {"success": False, "error": "Insufficient funds"}

def get_transaction_log():
    """No access control - anyone can see all transactions"""
    return {"success": True, "transactions": TRANSACTION_LOG}

def exploit_race_condition():
    """
    Morgana can exploit: Start 2 threads that both check balance simultaneously
    Both see enough balance, both withdraw, account goes negative
    """
    print("=== Race Condition Exploit ===")
    print(f"Initial balance: {ACCOUNTS['alice']['balance']}")
    
    # Reset account
    ACCOUNTS['alice']['balance'] = 1000.00
    
    # Two simultaneous withdrawals of 900 each
    results = []
    
    def withdraw_900():
        result = withdraw("alice", 900)
        results.append(result)
    
    t1 = threading.Thread(target=withdraw_900)
    t2 = threading.Thread(target=withdraw_900)
    
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    
    print(f"Final balance: {ACCOUNTS['alice']['balance']}")
    print(f"Results: {results}")
    print(f"Expected: -800 or -900 (if overdraft) or error")
    print(f"VULNERABILITY: Both withdrawals succeeded!" if ACCOUNTS['alice']['balance'] < 0 else "Race condition not triggered")

if __name__ == "__main__":
    exploit_race_condition()
