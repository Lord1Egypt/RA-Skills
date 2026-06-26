"""
HeteroMind - Schema Utilities

Utilities for extracting and formatting primary/foreign keys
from database and knowledge graph metadata.
"""

import os
import json
import pandas as pd
from pathlib import Path
from typing import Dict, List, Tuple

from utils.file_utils import read_json


def wrap_primary_foreign_keys_for_db(db_data: dict) -> Tuple[str, str]:
    """
    Extract and format primary and foreign key constraints from database metadata.
    
    Args:
        db_data (dict): Database metadata dictionary with keys:
            - db_id (str): Database identifier
            - table_names_original (list[str]): List of table names
            - column_names_original (list[tuple[int, str]]): List of (table_id, column_name) tuples
            - primary_keys (list): Primary key column indices
            - foreign_keys (list[tuple[int, int]]): Foreign key relationships
    
    Returns:
        tuple[str, str]: (wrapped_primary_keys, wrapped_foreign_keys)
    """
    table_names = db_data["table_names_original"]
    column_names = db_data["column_names_original"]
    
    # Extract primary keys
    primary_keys: Dict[str, str] = {}
    for pk_id in db_data["primary_keys"]:
        if isinstance(pk_id, int):
            table_idx, column_name = column_names[pk_id]
            table_name = table_names[table_idx]
            primary_keys[table_name] = column_name
        elif isinstance(pk_id, list):
            columns = []
            table_name = ""
            for col_id in pk_id:
                table_idx, column_name = column_names[col_id]
                table_name = table_names[table_idx]
                columns.append(column_name)
            primary_keys[table_name] = ", ".join(columns)
    
    wrapped_primary_keys = [
        f"TABLE `{table_name}` PRIMARY KEY `{column_list}`"
        for table_name, column_list in primary_keys.items()
    ]
    wrapped_primary_keys_str = "\n".join(wrapped_primary_keys)
    
    # Extract foreign keys
    wrapped_foreign_keys = []
    for from_col_id, to_col_id in db_data["foreign_keys"]:
        from_table_idx, from_column_name = column_names[from_col_id]
        from_table_name = table_names[from_table_idx]
        
        to_table_idx, to_column_name = column_names[to_col_id]
        to_table_name = table_names[to_table_idx]
        
        wrapped_foreign_keys.append(
            f"FOREIGN KEY {from_table_name}['{from_column_name}'] REFERENCES {to_table_name}['{to_column_name}']"
        )
    wrapped_foreign_keys_str = "\n".join(wrapped_foreign_keys)
    
    return wrapped_primary_keys_str, wrapped_foreign_keys_str


def wrap_primary_foreign_keys_for_kg(box_path: str) -> Tuple[str, str]:
    """
    Extract primary and foreign keys from knowledge graph box schema.
    
    Args:
        box_path (str): Path to KG box schema directory
    
    Returns:
        tuple[str, str]: (wrapped_primary_keys, wrapped_foreign_keys)
    """
    def get_first_column_name(csv_path: str) -> str:
        df = pd.read_csv(csv_path, nrows=0)
        return df.columns[0]
    
    primary_keys: Dict[str, str] = {}
    
    for filename in os.listdir(box_path):
        if filename.lower().endswith(".csv"):
            table_name = os.path.splitext(filename)[0].split(".")[-1]
            first_column_name = get_first_column_name(os.path.join(box_path, filename))
            primary_keys[table_name] = first_column_name
    
    wrapped_primary_keys = [
        f"TABLE `{table_name}` PRIMARY KEY `{column_list}`"
        for table_name, column_list in primary_keys.items()
    ]
    wrapped_primary_keys_str = "\n".join(wrapped_primary_keys)
    
    # Extract foreign keys
    wrapped_foreign_keys = []
    foreign_keys_file = os.path.join(box_path, "foreign_key.json")
    
    if os.path.exists(foreign_keys_file):
        foreign_keys = read_json(foreign_keys_file)
        
        for from_col, to_col in foreign_keys:
            from_table_name, from_column_name = from_col.split("-")
            from_table_name = from_table_name.split(".")[-1]
            
            to_table_name, to_column_name = to_col.split("-")
            to_table_name = to_table_name.split(".")[-1]
            
            wrapped_foreign_keys.append(
                f"FOREIGN KEY {from_table_name}['{from_column_name}'] REFERENCES {to_table_name}['{to_column_name}']"
            )
    
    wrapped_foreign_keys_str = "\n".join(wrapped_foreign_keys)
    
    return wrapped_primary_keys_str, wrapped_foreign_keys_str


def load_db_schema_with_keys(schema_path: str) -> dict:
    """
    Load database schema and extract primary/foreign keys.
    
    Args:
        schema_path (str): Path to schema JSON file
    
    Returns:
        dict: Schema with formatted keys
    """
    with open(schema_path, 'r') as f:
        db_data = json.load(f)
    
    primary_keys, foreign_keys = wrap_primary_foreign_keys_for_db(db_data)
    
    return {
        "schema": db_data,
        "primary_keys": primary_keys,
        "foreign_keys": foreign_keys,
    }


def load_kg_schema_with_keys(box_path: str) -> dict:
    """
    Load KG box schema and extract primary/foreign keys.
    
    Args:
        box_path (str): Path to KG box directory
    
    Returns:
        dict: Schema with formatted keys
    """
    primary_keys, foreign_keys = wrap_primary_foreign_keys_for_kg(box_path)
    
    return {
        "box_path": box_path,
        "primary_keys": primary_keys,
        "foreign_keys": foreign_keys,
    }
