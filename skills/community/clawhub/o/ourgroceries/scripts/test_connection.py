#!/usr/bin/env python3
"""
OurGroceries Connection Test Script
Test connection to OurGroceries.com using the unofficial Python wrapper
"""

import sys
import os
import asyncio
from pathlib import Path

_scripts_dir = Path(__file__).resolve().parent
if str(_scripts_dir) not in sys.path:
    sys.path.insert(0, str(_scripts_dir))
import load_skill_env  # noqa: E402

load_skill_env.apply()

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "lib"))
from ourgroceries import OurGroceries

async def test_connection_async():
    """
    Test connection to OurGroceries.com (async version)
    
    Returns:
        bool: True if successful, False otherwise
    """
    # Get credentials from environment variables
    email = os.getenv('OURGROCERIES_EMAIL')
    password = os.getenv('OURGROCERIES_PASSWORD')
    
    if not email or not password:
        print("[Error] Please set OURGROCERIES_EMAIL and OURGROCERIES_PASSWORD environment variables")
        print("[Hint] You can set them like:")
        print("  export OURGROCERIES_EMAIL=\"your@email.com\"")
        print("  export OURGROCERIES_PASSWORD=\"yourpassword\"")
        return False
    
    try:
        # Initialize OurGroceries client
        print("[Info] Connecting to OurGroceries.com...")
        og = OurGroceries(email, password)
        
        # Login first
        await og.login()
        
        # Get lists to verify connection
        lists_result = await og.get_my_lists()
        shopping_lists = lists_result.get('lists') or lists_result.get('shoppingLists') or []
        
        print(f"[Success] Connected! Found {len(shopping_lists)} shopping list(s):")
        for lst in shopping_lists:
            print(f"  - {lst['name']} (ID: {lst['id']})")
        
        return True
        
    except Exception as e:
        print(f"[Error] Failed to connect: {str(e)}")
        return False

def test_connection():
    """Wrapper to run the async test"""
    return asyncio.run(test_connection_async())

def main():
    success = test_connection()
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()