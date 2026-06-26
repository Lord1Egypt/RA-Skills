#!/usr/bin/env python3
"""Notion CLI for OpenClaw."""
import sys
import json
import argparse
from pathlib import Path

# Add parent directory to path to import lib package
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.client import NotionClient
from lib.pages import PageManager
from lib.databases import DatabaseManager
from lib.blocks import BlockManager
from lib.search import SearchManager


def main():
    parser = argparse.ArgumentParser(
        description="Notion CLI for OpenClaw",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Page commands
    page_parser = subparsers.add_parser("page", help="Page operations")
    page_subparsers = page_parser.add_subparsers(dest="action", help="Page action")
    
    # page create
    page_create = page_subparsers.add_parser("create", help="Create a new page")
    page_create.add_argument("--parent", required=True, help="Parent page ID")
    page_create.add_argument("--title", required=True, help="Page title")
    page_create.add_argument("--content", help="Initial content (paragraph)")
    
    # page get
    page_get = page_subparsers.add_parser("get", help="Get a page")
    page_get.add_argument("page_id", help="Page ID")
    
    # page update
    page_update = page_subparsers.add_parser("update", help="Update a page")
    page_update.add_argument("page_id", help="Page ID")
    page_update.add_argument("--title", help="New title")
    
    # page delete
    page_delete = page_subparsers.add_parser("delete", help="Delete (archive) a page")
    page_delete.add_argument("page_id", help="Page ID")
    
    # page list
    page_list = page_subparsers.add_parser("list", help="List child pages")
    page_list.add_argument("--parent", required=True, help="Parent page ID")
    
    # Database commands
    db_parser = subparsers.add_parser("db", help="Database operations")
    db_subparsers = db_parser.add_subparsers(dest="action", help="Database action")
    
    # db query
    db_query = db_subparsers.add_parser("query", help="Query a database")
    db_query.add_argument("db_id", help="Database ID")
    db_query.add_argument("--filter", help="Filter as key=value")
    db_query.add_argument("--sort", help="Sort as key:asc or key:desc")
    
    # db add
    db_add = db_subparsers.add_parser("add", help="Add page to database")
    db_add.add_argument("db_id", help="Database ID")
    db_add.add_argument("--props", required=True, help="Properties as JSON")
    
    # db list
    db_list = db_subparsers.add_parser("list", help="List all databases")
    
    # Block commands
    block_parser = subparsers.add_parser("block", help="Block operations")
    block_subparsers = block_parser.add_subparsers(dest="action", help="Block action")
    
    # block append
    block_append = block_subparsers.add_parser("append", help="Append a block")
    block_append.add_argument("block_id", help="Block/Page ID")
    block_append.add_argument("--type", required=True, 
                             choices=["paragraph", "todo", "heading1", "heading2", "heading3", "code"],
                             help="Block type")
    block_append.add_argument("--text", required=True, help="Block text content")
    block_append.add_argument("--checked", action="store_true", help="For todo: mark as checked")
    block_append.add_argument("--language", help="For code: programming language")
    
    # block children
    block_children = block_subparsers.add_parser("children", help="List child blocks")
    block_children.add_argument("block_id", help="Block ID")
    
    # Search command
    search_parser = subparsers.add_parser("search", help="Search workspace")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument("--type", choices=["page", "database"], help="Filter by object type")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        client = NotionClient()
        
        if args.command == "page":
            page_manager = PageManager(client)
            
            if args.action == "create":
                result = page_manager.create(args.parent, args.title, args.content)
                print(json.dumps(result, indent=2))
            
            elif args.action == "get":
                result = page_manager.get(args.page_id)
                print(json.dumps(result, indent=2))
            
            elif args.action == "update":
                result = page_manager.update(args.page_id, args.title)
                print(json.dumps(result, indent=2))
            
            elif args.action == "delete":
                result = page_manager.delete(args.page_id)
                print(json.dumps(result, indent=2))
            
            elif args.action == "list":
                result = page_manager.list_children(args.parent)
                print(json.dumps(result, indent=2))
            
            else:
                page_parser.print_help()
                return 1
        
        elif args.command == "db":
            db_manager = DatabaseManager(client)
            
            if args.action == "query":
                filter_dict = None
                sort_list = None
                
                if args.filter:
                    # Simple filter: key=value
                    key, value = args.filter.split("=", 1)
                    filter_dict = {
                        "property": key,
                        "rich_text": {"contains": value}
                    }
                
                if args.sort:
                    # Simple sort: key:asc or key:desc
                    key, direction = args.sort.split(":", 1)
                    sort_list = [{"property": key, "direction": direction}]
                
                result = db_manager.query(args.db_id, filter_dict, sort_list)
                print(json.dumps(result, indent=2))
            
            elif args.action == "add":
                props = json.loads(args.props)
                result = db_manager.add_page(args.db_id, props)
                print(json.dumps(result, indent=2))
            
            elif args.action == "list":
                result = db_manager.list_all()
                print(json.dumps(result, indent=2))
            
            else:
                db_parser.print_help()
                return 1
        
        elif args.command == "block":
            block_manager = BlockManager(client)
            
            if args.action == "append":
                # Normalize block type
                block_type_map = {
                    "todo": "to_do",
                    "heading1": "heading_1",
                    "heading2": "heading_2",
                    "heading3": "heading_3"
                }
                block_type = block_type_map.get(args.type, args.type)
                
                result = block_manager.append(
                    args.block_id,
                    block_type,
                    args.text,
                    checked=args.checked,
                    language=args.language
                )
                print(json.dumps(result, indent=2))
            
            elif args.action == "children":
                result = block_manager.get_children(args.block_id)
                print(json.dumps(result, indent=2))
            
            else:
                block_parser.print_help()
                return 1
        
        elif args.command == "search":
            search_manager = SearchManager(client)
            result = search_manager.search(args.query, args.type)
            print(json.dumps(result, indent=2))
        
        return 0
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
