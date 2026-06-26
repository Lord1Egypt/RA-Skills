#!/usr/bin/env python3
"""
OurGroceries Remove Item Script
Remove items from OurGroceries.com grocery lists using the unofficial Python wrapper
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


def _items_from_list_payload(items_result):
    """Normalize get_list_items() response to a list of item dicts."""
    if not isinstance(items_result, dict):
        return []
    if 'value' in items_result:
        return items_result.get('value') or []
    lst = items_result.get('list')
    if isinstance(lst, dict):
        if 'value' in lst:
            return lst.get('value') or []
        if 'items' in lst:
            return lst.get('items') or []
    return []

async def remove_item_async(item_name, list_name=None):
    """
    Remove an item from a grocery list
    
    Args:
        item_name (str): Name of the item to remove
        list_name (str, optional): Name of the list to remove from
    
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
        if not await og.login():
            print("[Error] Login failed - check your credentials")
            return False
        
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
        
        # Get items from the list to find the item to remove
        items_raw = await og.get_list_items(target_list['id'])
        items = _items_from_list_payload(items_raw)

        target_item = None
        for item in items:
            if (item.get('name') or '').lower() == item_name.lower():
                target_item = item
                break

        if not target_item:
            print(f"[Error] Item '{item_name}' not found in list '{target_list['name']}'")
            print(f"Available items: {[item.get('name') for item in items]}")
            return False

        # Remove item from the list
        await og.remove_item_from_list(target_list['id'], target_item['id'])
        print(f"[Success] Removed '{item_name}' from list '{target_list['name']}'")
        return True
        
    except Exception as e:
        print(f"[Error] Failed to remove item: {str(e)}")
        return False

def remove_item(item_name, list_name=None):
    """Wrapper to run the async function"""
    return asyncio.run(remove_item_async(item_name, list_name))

def main():
    parser = argparse.ArgumentParser(description='Remove item from OurGroceries.com list')
    parser.add_argument('item', help='Item name to remove')
    parser.add_argument('-l', '--list', help='List name (optional, uses first list if not specified)')
    
    args = parser.parse_args()
    
    success = remove_item(args.item, args.list)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()