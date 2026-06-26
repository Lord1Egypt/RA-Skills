#!/usr/bin/env python3
"""
DATA LEAK SYSTEM — For Morgana Testing
Intentional vulnerability: Information disclosure through error messages
"""

import traceback

# Sensitive data that should NEVER be exposed
SECRETS = {
    "api_key": "sk_live_336CORRUPTED",
    "db_password": "ServerRootPass2026!",
    "private_key": "-----BEGIN RSA PRIVATE KEY-----\nMIIEpQIBAAKCAQ...\n[FAKE KEY DATA]",
    "admin_email": "alexandre@axioma-stellaris.cluster",
}

USER_DATA = {
    "alexandre": {
        "email": "alexandre@lajeunesse.com",
        "ssn": "123-45-6789",
        "credit_card": "4532-1234-5678-9012",
        "balance": 133720.66,
    }
}

def get_user_info(username, requesting_user="guest"):
    """
    VULNERABILITY: No access control!
    Any user can request any other user's data
    """
    if username in USER_DATA:
        # FLAWED - no check if requesting_user == username or has admin rights
        return {"success": True, "data": USER_DATA[username]}
    return {"success": False, "error": "User not found"}

def get_secret(secret_name):
    """
    VULNERABILITY: No authentication required!
    Anyone can request any secret
    """
    if secret_name in SECRETS:
        # FLAWED - should require admin authentication
        return {"success": True, "secret": SECRETS[secret_name]}
    return {"success": False, "error": "Secret not found"}

def search_data(query):
    """
    VULNERABILITY: No rate limiting or access control!
    Could be used for data enumeration
    """
    results = []
    
    # Search user data
    for username, data in USER_DATA.items():
        for key, value in data.items():
            if query.lower() in str(value).lower():
                results.append({"type": "user_data", "user": username, "field": key, "value": value})
    
    # Search secrets (SHOULD NOT HAPPEN!)
    for name, value in SECRETS.items():
        if query.lower() in value.lower():
            results.append({"type": "secret", "name": name, "value": value})
    
    return {"success": True, "results": results, "count": len(results)}

def error_handler(func):
    """
    VULNERABILITY: Detailed error messages leak internals!
    Should show generic errors to users
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # FLAWED - exposing internal details
            return {
                "error": str(e),
                "type": type(e).__name__,
                "traceback": traceback.format_exc(),
                "hint": "This error reveals system internals - security risk!"
            }
    return wrapper

@error_handler
def divide_by_zero():
    return 1/0

@error_handler
def access_undefined_key():
    data = {"key": "value"}
    return data["nonexistent_key"]

if __name__ == "__main__":
    print("=== Data Leak Test ===")
    print(get_user_info("alexandre"))
    print(get_secret("api_key"))
    print(search_data("336"))
