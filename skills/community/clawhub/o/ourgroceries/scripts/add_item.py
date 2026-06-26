#!/usr/bin/env python3
"""
OurGroceries Add Item Script
Add items to OurGroceries.com grocery lists using the unofficial Python wrapper
"""

import sys
import os
import argparse
import asyncio
from pathlib import Path

_scripts_dir = Path(__file__).resolve().parent
if str(_scripts_dir) not in sys.path:
    sys.path.insert(0, str(_scripts_dir))
import load_skill_env  # noqa: E402

load_skill_env.apply()

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "lib"))
from ourgroceries import OurGroceries

async def add_item_async(item_name, list_name=None):
    """
    Add an item to a grocery list
    
    Args:
        item_name (str): Name of the item to add
        list_name (str, optional): Name of the list to add to
    
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
        og = OurGroceries(email, password)
        
        # Login first
        await og.login()
        
        # Get lists to find the target list
        lists_result = await og.get_my_lists()
        shopping_lists = lists_result.get('lists') or lists_result.get('shoppingLists') or []
        
        target_list = None
        if list_name:
            # Find list by name
            for lst in shopping_lists:
                if lst['name'].lower() == list_name.lower():
                    target_list = lst
                    break
            if not target_list:
                print(f"[Error] List '{list_name}' not found")
                print(f"Available lists: {[lst['name'] for lst in shopping_lists]}")
                return False
        else:
            # Use first list as default
            if shopping_lists:
                target_list = shopping_lists[0]
            else:
                print("[Error] No lists found")
                return False
        
        # Add item to the list with auto-categorization
        await og.add_item_to_list(target_list['id'], item_name, auto_category=True)
        print(f"[Success] Added '{item_name}' to list '{target_list['name']}' (auto-categorized)")
        return True
        
    except Exception as e:
        print(f"[Error] Failed to add item: {str(e)}")
        return False

def add_item(item_name, list_name=None):
    """Wrapper to run the async function"""
    return asyncio.run(add_item_async(item_name, list_name))

def main():
    parser = argparse.ArgumentParser(description='Add item to OurGroceries.com list')
    parser.add_argument('item', help='Item name to add')
    parser.add_argument('-l', '--list', help='List name (optional, uses first list if not specified)')
    
    args = parser.parse_args()
    
    success = add_item(args.item, args.list)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()