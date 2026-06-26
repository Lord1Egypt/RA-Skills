#!/usr/bin/env python3
"""
Batch create Notion database entries from CSV or JSON data.
"""

import csv
import json
import argparse
from typing import List, Dict, Any
from notion_client import NotionDBClient, title_property, text_property, \
    number_property, select_property, multi_select_property, \
    checkbox_property, date_property, url_property, email_property

def infer_property_type(value: Any) -> Dict:
    """Infer the Notion property type from a Python value."""
    if isinstance(value, bool):
        return checkbox_property(value)
    elif isinstance(value, (int, float)):
        return number_property(value)
    elif isinstance(value, list):
        return multi_select_property(value)
    elif value is None:
        # Return empty, let Notion handle it
        return {"rich_text": []}
    else:
        # Check if it looks like a date (YYYY-MM-DD)
        str_val = str(value)
        if len(str_val) == 10 and str_val[4] == '-' and str_val[7] == '-':
            return date_property(str_val)
        # Check if it looks like a URL
        elif str_val.startswith(('http://', 'https://')):
            return url_property(str_val)
        elif '@' in str_val and '.' in str_val:
            return email_property(str_val)
        else:
            return text_property(str_val)

def convert_csv_row_to_properties(row: Dict[str, str], schema: Dict[str, str]) -> Dict:
    """
    Convert a CSV row to Notion properties based on schema mapping.
    
    Args:
        row: CSV row (column name -> value)
        schema: Dict mapping CSV column name -> Notion property name
    """
    properties = {}
    
    for csv_col, notion_prop in schema.items():
        if csv_col not in row:
            continue
        value = row[csv_col].strip()
        
        # Try to convert to appropriate type
        if not value:
            continue
        elif value.lower() in ('true', 'yes', '1'):
            converted = checkbox_property(True)
        elif value.lower() in ('false', 'no', '0'):
            converted = checkbox_property(False)
        elif ',' in value and value.strip():
            # Assume multi-select if comma-separated
            items = [item.strip() for item in value.split(',') if item.strip()]
            converted = multi_select_property(items)
        elif value.isdigit():
            converted = number_property(int(value))
        elif '.' in value and all(c.isdigit() for c in value.replace('.', '', 1)):
            converted = number_property(float(value))
        else:
            # Default to text
            converted = text_property(value)
        
        properties[notion_prop] = converted
    
    return properties

def create_from_csv(
    api_token: str,
    database_id: str,
    csv_file: str,
    schema: Dict[str, str],
    title_column: str,
    title_property_name: str = "Name"
) -> List[Dict]:
    """
    Create multiple database entries from a CSV file.
    
    Args:
        api_token: Notion API token
        database_id: Database ID
        csv_file: Path to CSV file
        schema: Mapping CSV column -> Notion property name
        title_column: Which CSV column is the page title
        title_property_name: Name of the title property in Notion
    
    Returns:
        List of created pages
    """
    client = NotionDBClient(api_token)
    created_pages = []
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            properties = convert_csv_row_to_properties(row, schema)
            # Set the title property
            title_value = row[title_column].strip()
            properties[title_property_name] = title_property(title_value)
            
            result = client.create_page(database_id, properties)
            created_pages.append(result)
            print(f"Created page: {title_value} ({result['id']})")
    
    return created_pages

def create_from_json(
    api_token: str,
    database_id: str,
    json_file: str,
    title_key: str = "title",
    title_property_name: str = "Name"
) -> List[Dict]:
    """
    Create multiple database entries from a JSON file.
    
    JSON file should contain a list of objects:
    [
        { "title": "Page 1", "property1": "value1", ... },
        ...
    ]
    """
    client = NotionDBClient(api_token)
    created_pages = []
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for item in data:
        properties = {}
        for key, value in item.items():
            if key == title_key:
                properties[title_property_name] = title_property(str(value))
            else:
                properties[key] = infer_property_type(value)
        
        result = client.create_page(database_id, properties)
        created_pages.append(result)
        print(f"Created page: {item.get(title_key, result['id'])}")
    
    return created_pages

def main():
    parser = argparse.ArgumentParser(description='Batch create Notion database entries from CSV.')
    parser.add_argument('--api-token', help='Notion API token')
    parser.add_argument('--database-id', required=True, help='Notion database ID')
    parser.add_argument('--csv', required=True, help='CSV file to import')
    parser.add_argument('--title-column', required=True, help='Column name for page title')
    parser.add_argument('--title-property', default='Name', help='Property name for title in Notion')
    
    # Schema mapping should be in a separate JSON file
    parser.add_argument('--schema', required=True, help='JSON file with CSV column -> Notion property mapping')
    
    args = parser.parse_args()
    
    with open(args.schema, 'r') as f:
        schema = json.load(f)
    
    api_token = args.api_token or os.environ.get('NOTION_API_TOKEN')
    if not api_token:
        raise ValueError("API token required via --api-token or NOTION_API_TOKEN environment variable")
    
    created = create_from_csv(
        api_token=api_token,
        database_id=args.database_id,
        csv_file=args.csv,
        schema=schema,
        title_column=args.title_column,
        title_property_name=args.title_property
    )
    
    print(f"\nDone! Created {len(created)} pages.")

if __name__ == "__main__":
    main()
