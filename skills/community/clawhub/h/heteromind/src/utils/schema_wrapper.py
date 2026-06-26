#!/usr/bin/env python3
"""
Schema Wrapper Utilities

Extract and format primary/foreign keys from database metadata for prompts.
"""

import os
import json
import pandas as pd
from typing import Dict, List, Tuple, Any
from pathlib import Path


def wrap_primary_foreign_keys_for_db(db_data: Dict) -> Tuple[str, str]:
    """
    Extract and format primary and foreign key constraints from database metadata.
    
    Args:
        db_data (dict): Database metadata with keys:
            - db_id (str): Database identifier
            - table_names_original (list[str]): List of table names
            - column_names_original (list[tuple[int, str]]): List of (table_id, column_name)
            - primary_keys (list): Primary key column indices
            - foreign_keys (list[tuple[int, int]]): Foreign key relationships
    
    Returns:
        tuple[str, str]: (primary_keys_str, foreign_keys_str)
    """
    table_names = db_data["table_names_original"]
    column_names = db_data["column_names_original"]
    
    # Extract primary keys
    primary_keys: Dict[str, str] = {}
    for pk_id in db_data["primary_keys"]:
        if isinstance(pk_id, int):
            # Single-column primary key
            table_idx, column_name = column_names[pk_id]
            table_name = table_names[table_idx]
            primary_keys[table_name] = column_name
        elif isinstance(pk_id, list):
            # Composite primary key
            columns = []
            table_name = ""
            for col_id in pk_id:
                table_idx, column_name = column_names[col_id]
                table_name = table_names[table_idx]
                columns.append(column_name)
            primary_keys[table_name] = ", ".join(columns)
    
    # Format primary keys
    wrapped_primary_keys = [
        f"TABLE `{table_name}` PRIMARY KEY `{column_list}`"
        for table_name, column_list in primary_keys.items()
    ]
    wrapped_primary_keys_str = "\n".join(wrapped_primary_keys)
    
    # Format foreign keys
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
    Extract primary and foreign keys from knowledge graph CSV files.
    
    Args:
        box_path (str): Path to directory containing CSV files and foreign_key.json
    
    Returns:
        tuple[str, str]: (primary_keys_str, foreign_keys_str)
    """
    def get_first_column_name(csv_path: str) -> str:
        df = pd.read_csv(csv_path, nrows=0)
        return df.columns[0]
    
    # Extract primary keys (first column of each CSV)
    primary_keys: Dict[str, str] = {}
    for filename in os.listdir(box_path):
        if filename.lower().endswith(".csv"):
            table_name = os.path.splitext(filename)[0]
            first_column_name = get_first_column_name(os.path.join(box_path, filename))
            primary_keys[table_name] = first_column_name
    
    # Format primary keys
    wrapped_primary_keys = [
        f"TABLE `{table_name}` PRIMARY KEY `{column_list}`"
        for table_name, column_list in primary_keys.items()
    ]
    wrapped_primary_keys_str = "\n".join(wrapped_primary_keys)
    
    # Format foreign keys
    wrapped_foreign_keys = []
    foreign_keys_path = os.path.join(box_path, "foreign_key.json")
    
    if os.path.exists(foreign_keys_path):
        with open(foreign_keys_path) as f:
            foreign_keys = json.load(f)
        
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


def get_schema_constraints(db_data: Dict = None, box_path: str = None) -> Dict[str, Any]:
    """
    Unified interface to get schema constraints from either database metadata or KG files.
    
    Args:
        db_data (dict): Database metadata (for SQL databases)
        box_path (str): Path to KG CSV files (for knowledge graphs)
    
    Returns:
        dict: Schema constraints with keys:
            - primary_keys (str): Formatted primary key constraints
            - foreign_keys (str): Formatted foreign key constraints
            - source (str): Source type ('db' or 'kg')
    """
    if db_data is not None:
        pk_str, fk_str = wrap_primary_foreign_keys_for_db(db_data)
        return {
            "primary_keys": pk_str,
            "foreign_keys": fk_str,
            "source": "db",
        }
    elif box_path is not None:
        pk_str, fk_str = wrap_primary_foreign_keys_for_kg(box_path)
        return {
            "primary_keys": pk_str,
            "foreign_keys": fk_str,
            "source": "kg",
        }
    else:
        raise ValueError("Either db_data or box_path must be provided")


def format_schema_for_prompt(
    schema: Dict = None,
    db_data: Dict = None,
    box_path: str = None,
    include_constraints: bool = True,
) -> str:
    """
    Format complete schema information for LLM prompts.
    
    Args:
        schema (dict): Basic schema (tables, columns)
        db_data (dict): Database metadata with keys/relationships
        box_path (str): Path to KG files
        include_constraints (bool): Whether to include PK/FK constraints
    
    Returns:
        str: Formatted schema string for prompts
    """
    lines = []
    
    # Basic schema
    if schema:
        lines.append("=== Database Schema ===")
        for table in schema.get("tables", []):
            table_name = table["name"]
            columns = ", ".join(col["name"] for col in table.get("columns", []))
            desc = table.get("description", "")
            if desc:
                lines.append(f"Table: {table_name}({columns}) - {desc}")
            else:
                lines.append(f"Table: {table_name}({columns})")
        
        # Relationships
        for rel in schema.get("relationships", []):
            lines.append(
                f"Relationship: {rel['from_table']}.{rel['from_column']} -> "
                f"{rel['to_table']}.{rel['to_column']}"
            )
    
    # Constraints
    if include_constraints and (db_data or box_path):
        constraints = get_schema_constraints(db_data=db_data, box_path=box_path)
        
        if constraints["primary_keys"]:
            lines.append("\n=== Primary Keys ===")
            lines.append(constraints["primary_keys"])
        
        if constraints["foreign_keys"]:
            lines.append("\n=== Foreign Keys ===")
            lines.append(constraints["foreign_keys"])
    
    return "\n".join(lines)


# Example usage
if __name__ == "__main__":
    # Example database metadata
    example_db_data = {
        "db_id": "company",
        "table_names_original": ["employees", "departments"],
        "column_names_original": [
            (0, "emp_id"),
            (0, "name"),
            (0, "dept_id"),
            (1, "dept_id"),
            (1, "name"),
        ],
        "primary_keys": [0],  # employees.emp_id
        "foreign_keys": [(2, 3)],  # employees.dept_id -> departments.dept_id
    }
    
    pk_str, fk_str = wrap_primary_foreign_keys_for_db(example_db_data)
    
    print("Primary Keys:")
    print(pk_str)
    print("\nForeign Keys:")
    print(fk_str)
