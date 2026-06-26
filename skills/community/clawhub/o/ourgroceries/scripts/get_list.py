#!/usr/bin/env python3
"""
OurGroceries Get List Script
Retrieve items from OurGroceries.com grocery lists using the unofficial Python wrapper
"""

import sys
import os
import json
import asyncio
import argparse
from pathlib import Path

_scripts_dir = Path(__file__).resolve().parent
if str(_scripts_dir) not in sys.path:
    sys.path.insert(0, str(_scripts_dir))
import load_skill_env  # noqa: E402

load_skill_env.apply()

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "lib"))
from ourgroceries import OurGroceries

async def get_list_async(list_name=None, format_type='text'):
    """
    Get items from a grocery list
    
    Args:
        list_name (str, optional): Name of the list to retrieve
        format_type (str): Output format ('text', 'json')
    
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
        
        # Get lists
        lists_result = await og.get_my_lists()
        shopping_lists = lists_result.get('lists') or lists_result.get('shoppingLists') or []
        
        if not shopping_lists:
            print("[Info] No shopping lists found")
            return True
        
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
            target_list = shopping_lists[0]
        
        # Get items from the list
        items_result = await og.get_list_items(target_list['id'])
        # Handle different response formats
        if isinstance(items_result, dict):
            if 'value' in items_result:
                items = items_result.get('value', [])
            elif 'list' in items_result and isinstance(items_result['list'], dict) and 'value' in items_result['list']:
                items = items_result['list'].get('value', [])
            elif 'list' in items_result and isinstance(items_result['list'], dict) and 'items' in items_result['list']:
                items = items_result['list'].get('items', [])
            else:
                items = []
        else:
            items = []
        
        if format_type == 'json':
            # Output as JSON
            items_data = []
            for item in items:
                items_data.append({
                    'id': item['id'],
                    'name': item['name'],
                    'checked': item.get('crossedOff', False),
                    'note': item.get('note', ''),
                    'category': item.get('category', '')
                })
            print(json.dumps({
                'list_name': target_list['name'],
                'list_id': target_list['id'],
                'items': items_data
            }, indent=2))
        else:
            # Output as formatted text
            print(f"=== {target_list['name']} ===")
            if not items:
                print("(No items in list)")
            else:
                for i, item in enumerate(items, 1):
                    status = "[x]" if item.get('crossedOff', False) else "[ ]"
                    note = f" - {item.get('note', '')}" if item.get('note', '') else ""
                    print(f"{i}. {status} {item['name']}{note}")
            print(f"\nTotal items: {len(items)}")
        
        return True
        
    except Exception as e:
        print(f"[Error] Failed to get list: {str(e)}")
        return False

def get_list(list_name=None, format_type='text'):
    """Wrapper to run the async function"""
    return asyncio.run(get_list_async(list_name, format_type))

def main():
    parser = argparse.ArgumentParser(description='Get items from OurGroceries.com list')
    parser.add_argument('-l', '--list', help='List name (optional, uses first list if not specified)')
    parser.add_argument('-j', '--json', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    
    format_type = 'json' if args.json else 'text'
    success = get_list(args.list, format_type)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()