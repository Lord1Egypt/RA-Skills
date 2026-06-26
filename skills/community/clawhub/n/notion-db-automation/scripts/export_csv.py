#!/usr/bin/env python3
"""
Export entire Notion database to CSV file.
"""

import csv
import argparse
import os
from typing import List, Dict, Any
from notion_client import NotionDBClient

def get_property_value(result: Dict, prop_name: str) -> str:
    """Extract a human-readable value from a Notion property."""
    if prop_name not in result['properties']:
        return ""
    
    prop = result['properties'][prop_name]
    prop_type = prop['type']
    
    try:
        if prop_type == 'title':
            if not prop['title']:
                return ""
            return " ".join([t['plain_text'] for t in prop['title']])
        
        elif prop_type == 'rich_text':
            if not prop['rich_text']:
                return ""
            return " ".join([t['plain_text'] for t in prop['rich_text']])
        
        elif prop_type == 'number':
            if prop['number'] is None:
                return ""
            return str(prop['number'])
        
        elif prop_type == 'select':
            if not prop['select']:
                return ""
            return prop['select']['name']
        
        elif prop_type == 'multi_select':
            return ", ".join([item['name'] for item in prop['multi_select']])
        
        elif prop_type == 'checkbox':
            return "checked" if prop['checkbox'] else ""
        
        elif prop_type == 'date':
            if not prop['date']:
                return ""
            return prop['date'].get('start', "")
        
        elif prop_type == 'url':
            return prop['url'] or ""
        
        elif prop_type == 'email':
            return prop['email'] or ""
        
        elif prop_type == 'phone_number':
            return prop['phone_number'] or ""
        
        elif prop_type == 'created_time':
            return result.get('created_time', "")
        
        elif prop_type == 'last_edited_time':
            return result.get('last_edited_time', "")
        
        else:
            # For types like relation, rollup, people, just return something readable
            if prop_type == 'people':
                return ", ".join([p['name'] for p in prop['people'] if 'name' in p])
            return ""
    
    except Exception:
        return ""

def export_database_to_csv(
    api_token: str,
    database_id: str,
    output_file: str,
    filter: Optional[Dict] = None
) -> None:
    """Export a Notion database to CSV."""
    client = NotionDBClient(api_token)
    
    # Get database schema to know what properties we have
    schema = client.get_database_schema(database_id)
    prop_names = list(schema['properties'].keys())
    
    # Query all entries
    entries = client.query_database(database_id, filter=filter)
    
    # Write to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(prop_names)
        
        for entry in entries:
            row_values = [get_property_value(entry, prop) for prop in prop_names]
            writer.writerow(row_values)
    
    print(f"Exported {len(entries)} rows to {output_file}")

def main():
    parser = argparse.ArgumentParser(description='Export Notion database to CSV.')
    parser.add_argument('--api-token', help='Notion API token')
    parser.add_argument('--database-id', required=True, help='Notion database ID')
    parser.add_argument('--output', required=True, help='Output CSV file path')
    
    args = parser.parse_args()
    
    api_token = args.api_token or os.environ.get('NOTION_API_TOKEN')
    if not api_token:
        raise ValueError("API token required via --api-token or NOTION_API_TOKEN environment variable")
    
    export_database_to_csv(api_token, args.database_id, args.output)

if __name__ == "__main__":
    main()
