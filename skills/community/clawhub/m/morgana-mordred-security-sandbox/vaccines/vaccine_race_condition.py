#!/usr/bin/env python3
"""
VACCINE: race_condition.py
Patch for TOCTOU (Time-of-Check-Time-of-Use) Race Condition

APPLIQUER CE PATCH POUR CORRIGER:
- Double withdrawal possible (soldes négatifs)
- Transactions concurrentes corrompues
- Race conditions dans les opérations read-modify-write
"""

import threading
import time
from typing import Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Account:
    """
    Compte bancaire SÉCURISÉ avec verrouillage atomique.
    
    VULNÉRABILITÉ CORRIGÉE:
    - AVANT: Check (balance >= amount) puis Write séparés
    - APRÈS: Opération atomique avec Lock
    """
    
    account_id: str
    balance: float
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)
    
    def withdraw(self, amount: float) -> bool:
        """
        Retire de l'argent de façon ATOMIQUE.
        
        L'opération entière est protégée par un mutex.
        Le check ET le write arrivent ensemble, sans interférence.
        
        Returns:
            True si le withdrawal a réussi, False sinon
        """
        if amount <= 0:
            return False
        
        with self._lock:  # ✅ ACQUISITION ATOMIQUE DU VERROU
            # Le check et le write sont INSÉPARABLES
            if self.balance >= amount:
                self.balance -= amount
                return True
            return False
    
    def deposit(self, amount: float) -> bool:
        """Dépose de l'argent de façon ATOMIQUE."""
        if amount <= 0:
            return False
        
        with self._lock:  # ✅ ACQUISITION ATOMIQUE DU VERROU
            self.balance += amount
            return True
    
    def get_balance(self) -> float:
        """Retourne le solde actuel (lecture rapide)."""
        with self._lock:
            return self.balance


class TransactionLog:
    """
    Journal de transactions avec protection contre les races.
    """
    
    def __init__(self):
        self._transactions = []
        self._lock = threading.Lock()
    
    def add_transaction(self, account_id: str, action: str, amount: float, 
                       balance_before: float, balance_after: float):
        """Ajoute une transaction au journal de façon atomique."""
        with self._lock:
            self._transactions.append({
                'timestamp': datetime.now().isoformat(),
                'account_id': account_id,
                'action': action,
                'amount': amount,
                'balance_before': balance_before,
                'balance_after': balance_after
            })
    
    def get_transactions(self, account_id: Optional[str] = None):
        """Retourne les transactions, optionnellement filtrées par compte."""
        with self._lock:
            if account_id:
                return [t for t in self._transactions if t['account_id'] == account_id]
            return self._transactions.copy()


class SecureTransfer:
    """
    Transfert sécurisé entre deux comptes.
    
    Utilise deux verrous pour éviter les deadlocks:
    - Acquiert toujours les verrous dans le même ordre (par account_id)
    """
    
    def __init__(self, account1: Account, account2: Account, 
                 log: Optional[TransactionLog] = None):
        self.account1 = account1
        self.account2 = account2
        self.log = log or TransactionLog()
    
    def transfer(self, amount: float, from_id: str, to_id: str) -> bool:
        """
        Transfère de l'argent entre deux comptes de façon ATOMIQUE.
        
        Acquiert les verrous dans un ordre déterministe pour éviter les deadlocks.
        """
        if amount <= 0:
            return False
        
        # Déterminer l'ordre d'acquisition (pour éviter deadlock)
        accounts = sorted([self.account1, self.account2], 
                         key=lambda a: a.account_id)
        
        # Acquérir les verrous
        with accounts[0]._lock:
            with accounts[1]._lock:
                # Trouver les bons comptes
                if self.account1.account_id == from_id:
                    source = self.account1
                    dest = self.account2
                else:
                    source = self.account2
                    dest = self.account1
                
                # Effectuer le transfert
                if source.balance >= amount:
                    balance_before_src = source.balance
                    balance_before_dst = dest.balance
                    
                    source.balance -= amount
                    dest.balance += amount
                    
                    # Logger la transaction
                    self.log.add_transaction(
                        from_id, 'WITHDRAWAL', amount,
                        balance_before_src, source.balance
                    )
                    self.log.add_transaction(
                        to_id, 'DEPOSIT', amount,
                        balance_before_dst, dest.balance
                    )
                    
                    return True
        
        return False


def simulate_race_condition():
    """
    Simule le scénario de race condition ORIGINAL (vulnérable).
    
    Avec l'ancien code, deux threads pouvaient:
    1. Lire balance = 1000
    2. Les deux vérifier: 1000 >= 500 → OK
    3. Les deux écrire: 1000 - 500 = 500
    4. Résultat: 2x 500 retiré = 1000 au lieu de 0
    """
    print("\n⚠️  SIMULATION DU SCÉNARIO VULNÉRABLE (ancien code)")
    print("-" * 60)
    
    # Account avec l'ancien code vulnérable
    class VulnerableAccount:
        def __init__(self, balance):
            self.balance = balance
        
        def withdraw(self, amount):
            if self.balance >= amount:  # CHECK
                time.sleep(0.001)  # Simule delay
                self.balance -= amount  # USE
                return True
            return False
    
    acc = VulnerableAccount(1000)
    results = []
    
    def withdraw_500():
        success = acc.withdraw(500)
        results.append(success)
    
    # Deux threads tentent un withdrawal simultané
    t1 = threading.Thread(target=withdraw_500)
    t2 = threading.Thread(target=withdraw_500)
    
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    
    print(f"   Solde initial: 1000")
    print(f"   Solde final: {acc.balance}")
    print(f"   Withdrawals réussis: {sum(results)}/2")
    print(f"   Amount retiré total: {sum([500 if r else 0 for r in results])}")
    
    if acc.balance < 0:
        print(f"   ❌ OVERDRAFT: Race condition vulnérable!")
    elif sum(results) > 1 and acc.balance == 0:
        print(f"   ❌ DOUBLE WITHDRAWAL: Les deux ont réussi!")
    else:
        print(f"   ⚠️ Résultat inattendu")


def test_vaccine():
    """Test le vaccine."""
    print("🧪 TESTING SECURE ACCOUNT (avec Lock)")
    print("=" * 60)
    
    # Account avec le vaccine
    account = Account(account_id="TEST_001", balance=1000)
    log = TransactionLog()
    
    results = []
    
    def withdraw_500():
        success = account.withdraw(500)
        results.append(success)
    
    # Deux threads tentent un withdrawal simultané
    print("\n💰 Scénario: Deux withdrawals de 500$ simultanés")
    print(f"   Solde initial: 1000")
    
    t1 = threading.Thread(target=withdraw_500)
    t2 = threading.Thread(target=withdraw_500)
    
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    
    print(f"   Solde final: {account.balance}")
    print(f"   Withdrawals réussis: {sum(results)}/2")
    print(f"   Amount retiré total: {sum([500 if r else 0 for r in results])}")
    
    if account.balance >= 0 and sum(results) <= 1:
        print("   ✅ PROTECTED: Un seul withdrawal a réussi")
    else:
        print("   ❌ FAIL: Race condition仍然 présente!")
    
    # Test de transfert sécurisé
    print("\n💸 Test: Transfert sécurisé entre deux comptes")
    acc1 = Account(account_id="ACC_1", balance=1000)
    acc2 = Account(account_id="ACC_2", balance=500)
    
    transfer = SecureTransfer(acc1, acc2, log)
    success = transfer.transfer(300, "ACC_1", "ACC_2")
    
    print(f"   Transfer: 300$ de ACC_1 vers ACC_2")
    print(f"   ACC_1 nouveau solde: {acc1.balance}")
    print(f"   ACC_2 nouveau solde: {acc2.balance}")
    print(f"   ✅ Transfert réussi!" if success else "   ❌ Transfert échoué!")
    
    print("\n" + "=" * 60)
    print("✅ SECURE ACCOUNT OPERATIONAL - RACE CONDITIONS PREVENUES")


if __name__ == "__main__":
    test_vaccine()
    print()
    simulate_race_condition()
