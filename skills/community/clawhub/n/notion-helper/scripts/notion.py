#!/usr/bin/env python3
"""
Notion Integration - Work with Notion API
Requires: pip install notion-client
"""

import os
import sys
import json
import argparse

NOTION_TOKEN = os.environ.get('NOTION_TOKEN')

def check_token():
    if not NOTION_TOKEN:
        print("Error: NOTION_TOKEN not set")
        print("Set it with: export NOTION_TOKEN='secret_xxx'")
        return False
    return True


def query_database(database_id):
    """Query a Notion database."""
    try:
        from notion_client import Client
        notion = Client(auth=NOTION_TOKEN)
        results = notion.databases.query(database_id=database_id)
        return results
    except ImportError:
        print("Error: notion-client not installed")
        print("Install with: pip install notion-client")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def create_page(database_id, title, properties=None):
    """Create a new page in a database."""
    try:
        from notion_client import Client
        notion = Client(auth=NOTION_TOKEN)
        
        props = {"Name": {"title": [{"text": {"content": title}}]}}
        if properties:
            props.update(properties)
        
        result = notion.pages.create(parent={"database_id": database_id}, properties=props)
        return result
    except ImportError:
        print("Error: notion-client not installed")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def get_page(page_id):
    """Get page content."""
    try:
        from notion_client import Client
        notion = Client(auth=NOTION_TOKEN)
        result = notion.pages.retrieve(page_id=page_id)
        return result
    except ImportError:
        print("Error: notion-client not installed")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def update_page(page_id, properties):
    """Update page properties."""
    try:
        from notion_client import Client
        notion = Client(auth=NOTION_TOKEN)
        result = notion.pages.update(page_id=page_id, properties=properties)
        return result
    except ImportError:
        print("Error: notion-client not installed")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def main():
    if not check_token():
        return 1
    
    parser = argparse.ArgumentParser(description='Notion Integration CLI')
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Query command
    query_parser = subparsers.add_parser('query', help='Query a database')
    query_parser.add_argument('--database-id', required=True, help='Database ID')
    
    # Create page command
    create_parser = subparsers.add_parser('create-page', help='Create a page')
    create_parser.add_argument('--database-id', required=True, help='Database ID')
    create_parser.add_argument('--title', required=True, help='Page title')
    
    # Get page command
    get_parser = subparsers.add_parser('get-page', help='Get page content')
    get_parser.add_argument('--page-id', required=True, help='Page ID')
    
    # Update page command
    update_parser = subparsers.add_parser('update-page', help='Update page')
    update_parser.add_argument('--page-id', required=True, help='Page ID')
    update_parser.add_argument('--properties', help='JSON properties')
    
    args = parser.parse_args()
    
    if args.command == 'query':
        result = query_database(args.database_id)
    elif args.command == 'create-page':
        result = create_page(args.database_id, args.title)
    elif args.command == 'get-page':
        result = get_page(args.page_id)
    elif args.command == 'update-page':
        props = json.loads(args.properties) if args.properties else {}
        result = update_page(args.page_id, props)
    else:
        parser.print_help()
        return 0
    
    if result:
        print(json.dumps(result, indent=2))
        return 0
    return 1


if __name__ == '__main__':
    sys.exit(main())
