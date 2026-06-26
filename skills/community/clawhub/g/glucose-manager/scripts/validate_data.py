#!/usr/bin/env python3
"""
Validate Glucose Data
Validate glucose readings for format and reasonable values
"""

import argparse
import sys
from pathlib import Path
import json

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))
from data_manager import GlucoseDataManager


def validate_reading(reading: dict) -> list:
    """
    Validate a single glucose reading
    
    Args:
        reading: Dictionary containing glucose reading
    
    Returns:
        List of validation errors (empty if valid)
    """
    errors = []
    
    # Check required fields
    if 'value' not in reading:
        errors.append("Missing 'value' field")
    elif not isinstance(reading['value'], (int, float)):
        errors.append("'value' must be a number")
    
    if 'unit' not in reading:
        errors.append("Missing 'unit' field")
    elif reading.get('unit') not in ['mmol/L', 'mg/dL']:
        errors.append(f"Invalid unit '{reading.get('unit')}'. Must be 'mmol/L' or 'mg/dL'")
    
    # Check value ranges
    if 'value' in reading and isinstance(reading['value'], (int, float)):
        value = reading['value']
        unit = reading.get('unit', 'mmol/L')
        
        # Convert to mmol/L for range checking
        if unit == 'mg/dL':
            value_mmol = value / 18.018
        else:
            value_mmol = value
        
        # Physiologically impossible ranges
        if value_mmol < 1.0:
            errors.append(f"Glucose value {value} {unit} is dangerously low (< 1.0 mmol/L)")
        elif value_mmol > 30.0:
            errors.append(f"Glucose value {value} {unit} is dangerously high (> 30.0 mmol/L)")
        elif value_mmol < 2.0:
            errors.append(f"Warning: Glucose value {value} {unit} is very low (severe hypoglycemia)")
        elif value_mmol > 25.0:
            errors.append(f"Warning: Glucose value {value} {unit} is very high (severe hyperglycemia)")
    
    # Check timestamp format
    if 'timestamp' in reading:
        try:
            from datetime import datetime
            datetime.fromisoformat(reading['timestamp'].replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            errors.append(f"Invalid timestamp format: {reading['timestamp']}")
    
    # Check meal context
    valid_contexts = ['fasting', 'pre-meal', 'post-meal', 'bedtime', 'random']
    if 'meal_context' in reading and reading['meal_context'] not in valid_contexts:
        errors.append(f"Invalid meal context '{reading['meal_context']}'. Must be one of: {valid_contexts}")
    
    return errors


def main():
    """Validate glucose data"""
    parser = argparse.ArgumentParser(description='Validate glucose readings')
    parser.add_argument('--fix', action='store_true',
                       help='Attempt to fix common issues')
    parser.add_argument('--all', action='store_true',
                       help='Show all readings, including valid ones')
    
    args = parser.parse_args()
    
    manager = GlucoseDataManager()
    data = manager.load_data()
    readings = data['readings']
    
    print(f"\nValidating {len(readings)} glucose readings...\n")
    
    valid_count = 0
    warning_count = 0
    error_count = 0
    
    for idx, reading in enumerate(readings):
        errors = validate_reading(reading)
        
        if not errors:
            valid_count += 1
            if args.all:
                print(f"✓ Reading {idx + 1}: {reading.get('value')} {reading.get('unit')} - Valid")
        else:
            # Check if warnings or errors
            has_errors = any('dangerously' in e.lower() or 'invalid' in e.lower() for e in errors)
            
            if has_errors:
                error_count += 1
                symbol = "✗"
            else:
                warning_count += 1
                symbol = "⚠"
            
            print(f"{symbol} Reading {idx + 1}: {reading.get('value', 'N/A')} {reading.get('unit', 'N/A')}")
            for error in errors:
                print(f"    - {error}")
    
    # Summary
    print("\n" + "="*60)
    print("Validation Summary:")
    print(f"  Total readings: {len(readings)}")
    print(f"  Valid: {valid_count}")
    print(f"  Warnings: {warning_count}")
    print(f"  Errors: {error_count}")
    
    if error_count > 0:
        print("\n⚠ Some readings have errors that should be reviewed")
        sys.exit(1)
    elif warning_count > 0:
        print("\n⚠ Some readings have warnings but are acceptable")
    else:
        print("\n✓ All readings are valid")


if __name__ == "__main__":
    main()
