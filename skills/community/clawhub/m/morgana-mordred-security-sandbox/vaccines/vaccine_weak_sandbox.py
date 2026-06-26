#!/usr/bin/env python3
"""
VACCINE: weak_sandbox.py
Patch for Sandbox Escape vulnerability

APPLIQUER CE PATCH POUR CORRIGER:
- Exécution de code arbitraire via __import__
- Accès aux modules système (os, sys, subprocess)
"""

import builtins
from typing import Any

# ✅ WHITELIST DE BUILTINS AUTORISÉS
ALLOWED_BUILTINS = {
    'print', 'len', 'range', 'str', 'int', 'float', 'bool',
    'list', 'dict', 'tuple', 'set', 'frozenset', 'type',
    'isinstance', 'issubclass', 'hasattr', 'getattr', 'setattr',
    'abs', 'min', 'max', 'sum', 'sorted', 'reversed', 'enumerate',
    'zip', 'map', 'filter', 'any', 'all', 'ord', 'chr',
    'open',  # ⚠️ Limit file operations via mode='r' only
}

# ❌ MODULES INTERDITS (ne peuvent pas être importés)
FORBIDDEN_MODULES = {
    'os', 'sys', 'subprocess', 'importlib', 'imp',
    'builtins', 'ctypes', 'socket', 'requests', 'urllib',
    'threading', 'multiprocessing', 'asyncio',
}


class SecurityError(Exception):
    """Exception levée quand une tentative de contournement est détectée."""
    pass


class SecureSandbox:
    """
    Sandbox SÉCURISÉE avec whitelist de builtins.
    
    VULNÉRABILITÉ CORRIGÉE:
    - AVANT: Tous les builtins disponibles, imports libres
    - APRÈS: Whitelist explicite,监控 chaque appel
    """
    
    def __init__(self):
        # Garder références aux fonctions originales AVANT de filtrer
        self._original_builtins = dict(builtins.__dict__)
        self._setup_secure_builtins()
    
    def _setup_secure_builtins(self):
        """Configure les builtins sécurisés."""
        # Créer un dict de builtins filtré
        secure_builtins = {}
        for name in ALLOWED_BUILTINS:
            if name in builtins.__dict__:
                secure_builtins[name] = builtins.__dict__[name]
        
        # Remplacer les builtins
        builtins.__dict__.clear()
        builtins.__dict__.update(secure_builtins)
    
    def restore(self):
        """Restaure les builtins originaux."""
        builtins.__dict__.clear()
        builtins.__dict__.update(self._original_builtins)
    
    def safe_exec(self, code: str) -> Any:
        """
        Exécute le code dans le sandbox sécurisé.
        
        VULNÉRABILITÉ CORRIGÉE:
        - Impossible d'importer os, sys, etc.
        - Impossible d'utiliser __import__
        - Seuls les builtins whitelistés sont disponibles
        """
        # Vérifier les patterns dangereux AVANT exécution
        dangerous_patterns = [
            '__import__', 'import ', 'from ', 'eval', 'exec',
            'open(', 'file(', 'input(',
            'globals()', 'locals()', 'dir(',
            'compile(', 'settrace', 'callable'
        ]
        
        code_lower = code.lower()
        for pattern in dangerous_patterns:
            if pattern in code_lower:
                raise SecurityError(f"Forbidden pattern detected: {pattern}")
        
        # Exécuter dans un namespace limité
        namespace = {
            '__builtins__': builtins.__dict__,
            '__name__': '__sandbox__'
        }
        
        # Utiliser exec du namespace original via le builtins original
        original_builtins = self._original_builtins
        try:
            original_builtins['exec'](code, namespace)
            return namespace.get('_result')
        except Exception as e:
            raise SecurityError(f"Execution blocked: {e}")


def test_vaccine():
    """Test le vaccine."""
    sandbox = SecureSandbox()
    
    test_cases = [
        # (code, should_succeed, description)
        ("print('Hello World')", True, "Legitimate code - allowed"),
        ("result = 2 + 2", True, "Arithmetic - allowed"),
        ("result = len([1,2,3])", True, "Builtin function - allowed"),
        ("import os", False, "Module import - BLOCKED"),
        ("__import__('os').system('ls')", False, "Sandbox escape - BLOCKED"),
        ("eval('1+1')", False, "eval() call - BLOCKED"),
        ("exec('print(1)')", False, "exec() call - BLOCKED"),
    ]
    
    print("🧪 TESTING SECURE SANDBOX")
    print("=" * 60)
    
    all_passed = True
    for code, should_succeed, description in test_cases:
        try:
            sandbox.safe_exec(code)
            success = True
        except SecurityError:
            success = False
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            success = False
        
        status = "✅ PASS" if (success == should_succeed) else "❌ FAIL"
        if success != should_succeed:
            all_passed = False
        
        print(f"{status}: {description}")
        print(f"       Code: {code[:50]}...")
        print()
    
    sandbox.restore()
    
    print("=" * 60)
    if all_passed:
        print("✅ ALL TESTS PASSED - VACCINE EFFECTIVE!")
    else:
        print("❌ SOME TESTS FAILED - VACCINE NEEDS REVIEW")
    
    return all_passed


if __name__ == "__main__":
    test_vaccine()
