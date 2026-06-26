#!/usr/bin/env python3
"""
Import Glucose Data
Import glucose readings from CSV or Excel files
"""

import argparse
import sys
import pandas as pd
from pathlib import Path
from datetime import datetime
import json

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))
from data_manager import GlucoseDataManager


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='Import glucose readings from CSV or Excel files'
    )
    
    parser.add_argument(
        '--file', '-f',
        type=str,
        required=True,
        help='Path to the data file (CSV or Excel)'
    )
    
    parser.add_argument(
        '--format',
        type=str,
        choices=['csv', 'excel', 'auto'],
        default='auto',
        help='File format (default: auto-detect from extension)'
    )
    
    parser.add_argument(
        '--sheet',
        type=str,
        help='Sheet name for Excel files (default: first sheet)'
    )
    
    parser.add_argument(
        '--date-column',
        type=str,
        default='date',
        help='Name of the date/timestamp column (default: date)'
    )
    
    parser.add_argument(
        '--time-column',
        type=str,
        help='Name of the time column (if separate from date)'
    )
    
    parser.add_argument(
        '--value-column',
        type=str,
        default='value',
        help='Name of the glucose value column (default: value)'
    )
    
    parser.add_argument(
        '--unit-column',
        type=str,
        default='unit',
        help='Name of the unit column (default: unit)'
    )
    
    parser.add_argument(
        '--default-unit',
        type=str,
        choices=['mmol/L', 'mg/dL'],
        default='mmol/L',
        help='Default unit if unit column not found (default: mmol/L)'
    )
    
    parser.add_argument(
        '--meal-context-column',
        type=str,
        help='Name of the meal context column'
    )
    
    parser.add_argument(
        '--notes-column',
        type=str,
        help='Name of the notes column'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Validate data without importing'
    )
    
    return parser.parse_args()


def detect_file_format(filepath: str) -> str:
    """Detect file format from extension"""
    ext = Path(filepath).suffix.lower()
    if ext == '.csv':
        return 'csv'
    elif ext in ['.xlsx', '.xls']:
        return 'excel'
    else:
        raise ValueError(f"Unsupported file format: {ext}")


def read_file(filepath: str, file_format: str, sheet: str = None) -> pd.DataFrame:
    """Read data from CSV or Excel file"""
    if file_format == 'csv':
        # Try different encodings
        for encoding in ['utf-8', 'utf-8-sig', 'gbk', 'gb2312', 'latin1']:
            try:
                df = pd.read_csv(filepath, encoding=encoding)
                print(f"✓ Successfully read CSV with encoding: {encoding}")
                return df
            except UnicodeDecodeError:
                continue
        raise ValueError("Unable to read CSV file with supported encodings")
    
    elif file_format == 'excel':
        if sheet:
            df = pd.read_excel(filepath, sheet_name=sheet)
        else:
            df = pd.read_excel(filepath, sheet_name=0)
        print(f"✓ Successfully read Excel file")
        return df
    
    else:
        raise ValueError(f"Unsupported format: {file_format}")


def parse_datetime(date_val, time_val=None) -> str:
    """Parse date and time values into ISO format"""
    # Handle pandas Timestamp
    if pd.isna(date_val):
        return None
    
    # If already a datetime object
    if isinstance(date_val, (pd.Timestamp, datetime)):
        return date_val.isoformat()
    
    # Try parsing string
    date_str = str(date_val)
    
    # Common date formats
    formats = [
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%d %H:%M',
        '%Y/%m/%d %H:%M:%S',
        '%Y/%m/%d %H:%M',
        '%m/%d/%Y %H:%M:%S',
        '%m/%d/%Y %H:%M',
        '%d/%m/%Y %H:%M:%S',
        '%d/%m/%Y %H:%M',
        '%Y-%m-%d',
        '%Y/%m/%d',
        '%m/%d/%Y',
        '%d/%m/%Y'
    ]
    
    if time_val and not pd.isna(time_val):
        date_str = f"{date_str} {time_val}"
    
    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.isoformat()
        except ValueError:
            continue
    
    return None


def process_row(row, args, df) -> dict:
    """Process a single row into a glucose reading"""
    reading = {}
    
    # Get glucose value
    if args.value_column not in df.columns:
        raise ValueError(f"Value column '{args.value_column}' not found")
    reading['value'] = float(row[args.value_column])
    
    # Get unit
    if args.unit_column in df.columns and not pd.isna(row[args.unit_column]):
        reading['unit'] = str(row[args.unit_column])
    else:
        reading['unit'] = args.default_unit
    
    # Parse timestamp
    if args.date_column in df.columns:
        time_val = row[args.time_column] if args.time_column and args.time_column in df.columns else None
        timestamp = parse_datetime(row[args.date_column], time_val)
        if timestamp:
            reading['timestamp'] = timestamp
    
    # Get meal context
    if args.meal_context_column and args.meal_context_column in df.columns:
        if not pd.isna(row[args.meal_context_column]):
            reading['meal_context'] = str(row[args.meal_context_column])
    
    # Get notes
    if args.notes_column and args.notes_column in df.columns:
        if not pd.isna(row[args.notes_column]):
            reading['notes'] = str(row[args.notes_column])
    
    return reading


def main():
    """Main import function"""
    args = parse_args()
    
    # Detect file format
    file_format = args.format
    if file_format == 'auto':
        file_format = detect_file_format(args.file)
    
    print(f"\nImporting glucose data from: {args.file}")
    print(f"Format: {file_format}")
    
    # Read file
    try:
        df = read_file(args.file, file_format, args.sheet)
        print(f"Found {len(df)} rows of data")
        print(f"\nColumns: {list(df.columns)}")
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
    
    # Process rows
    readings = []
    errors = []
    
    for idx, row in df.iterrows():
        try:
            reading = process_row(row, args, df)
            
            # Validate
            if 'value' not in reading:
                errors.append(f"Row {idx}: Missing glucose value")
                continue
            
            if reading['value'] <= 0 or reading['value'] > 50:  # Reasonable range check
                errors.append(f"Row {idx}: Unusual glucose value: {reading['value']}")
                continue
            
            readings.append(reading)
            
        except Exception as e:
            errors.append(f"Row {idx}: {str(e)}")
    
    # Report results
    print(f"\nProcessed {len(df)} rows:")
    print(f"  Valid readings: {len(readings)}")
    print(f"  Errors: {len(errors)}")
    
    if errors:
        print("\nErrors encountered:")
        for error in errors[:10]:  # Show first 10 errors
            print(f"  - {error}")
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more errors")
    
    if args.dry_run:
        print("\n[DRY RUN] Data validated but not imported")
        print(f"\nSample reading:")
        if readings:
            print(json.dumps(readings[0], indent=2))
        return
    
    # Import readings
    if readings:
        print(f"\nImporting {len(readings)} readings...")
        manager = GlucoseDataManager()
        
        success_count = 0
        for reading in readings:
            if manager.add_reading(reading):
                success_count += 1
        
        print(f"\n✓ Successfully imported {success_count}/{len(readings)} readings")
    else:
        print("\nNo valid readings to import")


if __name__ == "__main__":
    main()
