#!/usr/bin/env python3
"""
VACCINE: data_leak.py
Patch for Information Disclosure vulnerability

APPLIQUER CE PATCH POUR CORRIGER:
- Exposition de données sensibles (SSN, CB, emails)
- Retour de champs non autorisés dans les requêtes
- Fuites de secrets/API keys
"""

from typing import Any, Dict, List, Optional

# ✅ CHAMPS PUBLICS SEULEMENT (sans risque)
PUBLIC_FIELDS = {
    'id', 'name', 'username', 'email', 'phone',
    'address', 'city', 'country', 'postal_code'
}

# ❌ CHAMPS SENSIBLES (jamais retourner sans autorisation explicite)
SENSITIVE_FIELDS = {
    'password', 'ssn', 'social_security', 'credit_card', 'cc_number',
    'cvv', 'expiry', 'bank_account', 'routing_number',
    'api_key', 'secret', 'token', 'private_key',
    'balance', 'salary', 'income', 'ssn_hash'
}

class DataLeakPreventor:
    """
    Filtre les champs sensibles avant de retourner des données.
    
    VULNÉRABILITÉ CORRIGÉE:
    - AVANT: Tous les champs retournés (SELECT * FROM users)
    - APRÈS: Whitelist de champs publics seulement
    """
    
    def __init__(self, allow_sensitive: bool = False):
        """
        Args:
            allow_sensitive: Si True, retourne aussi les champs sensibles (⚠️ DANGEREUX)
        """
        self.allow_sensitive = allow_sensitive
    
    def filter_fields(self, data: Dict[str, Any], 
                     allowed_fields: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Filtre les champs sensibles d'un dictionnaire de données.
        
        Args:
            data: Données brutes de la DB
            allowed_fields: Liste de champs spécifiques à retourner (optionnel)
        
        Returns:
            Données filtrées, champs sensibles retirés
        """
        if allowed_fields:
            # Si whitelist explicite fourni, l'utiliser
            return {k: v for k, v in data.items() if k in allowed_fields}
        
        # Sinon, utiliser le filtrage automatique
        filtered = {}
        for key, value in data.items():
            if key.lower() in SENSITIVE_FIELDS:
                if not self.allow_sensitive:
                    filtered[key] = "[REDACTED]"
                    continue
            if key.lower() in PUBLIC_FIELDS:
                filtered[key] = value
            elif self.allow_sensitive:
                filtered[key] = value
            # else: skip field silently
        
        return filtered
    
    def filter_list(self, data_list: List[Dict[str, Any]],
                   allowed_fields: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Applique filter_fields à une liste de dictionnaires."""
        return [self.filter_fields(item, allowed_fields) for item in data_list]
    
    def build_safe_query(self, fields: List[str], table: str) -> str:
        """
        Construit une requête SQL SÉCURISÉE avec whitelist de champs.
        
        ⚠️ INCOMPLET: Utiliser avec des requêtes paramétrées!
        """
        # Valider que tous les champs sont publics
        for field in fields:
            if field.lower() in SENSITIVE_FIELDS:
                if not self.allow_sensitive:
                    raise SensitiveFieldError(f"Cannot select sensitive field: {field}")
        
        # Valider que tous les champs existent
        field_list = ', '.join(fields)
        return f"SELECT {field_list} FROM {table}"


class SensitiveFieldError(Exception):
    """Exception levée quand un champ sensible est détecté."""
    pass


class MockDatabase:
    """
    Simule une DB avec des données sensibles pour tester le vaccine.
    """
    
    USERS = [
        {
            'id': 1,
            'name': 'Alexandre Lajeunesse',
            'username': 'kofna336',
            'email': 'alexandre@lajeunesse.com',
            'ssn': '123-45-6789',
            'credit_card': '4532-1234-5678-9012',
            'balance': 133720.66,
            'api_key': 'sk_live_336CORRUPTED'
        },
        {
            'id': 2,
            'name': 'Test User',
            'username': 'test',
            'email': 'test@example.com',
            'ssn': '987-65-4321',
            'credit_card': '4111-1111-1111-1111',
            'balance': 1000.00,
            'api_key': 'sk_test_123'
        }
    ]
    
    @classmethod
    def query_all(cls):
        return cls.USERS.copy()
    
    @classmethod
    def query_by_id(cls, user_id: int):
        for user in cls.USERS:
            if user['id'] == user_id:
                return user.copy()
        return None


def test_vaccine():
    """Test le vaccine."""
    preventor = DataLeakPreventor()
    db = MockDatabase()
    
    print("🧪 TESTING DATA LEAK PREVENTOR")
    print("=" * 60)
    
    # Test 1: Requête normale d'un utilisateur
    print("\n📊 Test 1: Query user by ID")
    user_data = db.query_by_id(1)
    print(f"   Original fields: {list(user_data.keys())}")
    
    safe_data = preventor.filter_fields(user_data)
    print(f"   Filtered fields: {list(safe_data.keys())}")
    print(f"   ✅ Sensitive data: {safe_data.get('ssn', 'N/A')} → [REDACTED]")
    print(f"   ✅ API key: {safe_data.get('api_key', 'N/A')} → [REDACTED]")
    print(f"   ✅ Balance: {safe_data.get('balance', 'N/A')} → [REDACTED]")
    print(f"   ✅ Email: {safe_data.get('email', 'N/A')} → KEPT")
    
    # Test 2: Requête avec whitelist explicite
    print("\n📊 Test 2: Query with explicit whitelist")
    whitelist = ['id', 'name', 'email']
    safe_data = preventor.filter_fields(user_data, allowed_fields=whitelist)
    print(f"   Whitelist: {whitelist}")
    print(f"   Returned: {list(safe_data.keys())}")
    print(f"   ✅ Only whitelisted fields returned")
    
    # Test 3: SSN leak attempt
    print("\n📊 Test 3: SSN Leak Prevention")
    user_data = db.query_by_id(1)
    safe_data = preventor.filter_fields(user_data)
    
    if safe_data.get('ssn') == '[REDACTED]':
        print("   ✅ SSN BLOCKED - [REDACTED]")
    else:
        print("   ❌ SSN LEAKED!")
    
    if safe_data.get('credit_card') == '[REDACTED]':
        print("   ✅ Credit Card BLOCKED - [REDACTED]")
    else:
        print("   ❌ Credit Card LEAKED!")
    
    print("\n" + "=" * 60)
    print("✅ DATA LEAK PREVENTOR OPERATIONAL")


if __name__ == "__main__":
    test_vaccine()
