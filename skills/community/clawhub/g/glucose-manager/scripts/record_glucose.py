#!/usr/bin/env python3
"""
Record Blood Glucose Reading
Command-line tool to manually record glucose readings
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path

# Add parent directory to path to import data_manager
sys.path.insert(0, str(Path(__file__).parent))
from data_manager import GlucoseDataManager


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='Record a blood glucose reading'
    )
    
    parser.add_argument(
        '--value', '-v',
        type=float,
        required=True,
        help='Glucose value'
    )
    
    parser.add_argument(
        '--unit', '-u',
        type=str,
        choices=['mmol/L', 'mg/dL'],
        default='mmol/L',
        help='Glucose unit (default: mmol/L)'
    )
    
    parser.add_argument(
        '--time', '-t',
        type=str,
        help='Timestamp of reading (ISO format, e.g., "2026-03-24 08:00")'
    )
    
    parser.add_argument(
        '--meal-context', '-m',
        type=str,
        choices=['fasting', 'pre-meal', 'post-meal', 'bedtime', 'random'],
        help='Meal context for the reading'
    )
    
    parser.add_argument(
        '--notes', '-n',
        type=str,
        help='Additional notes for this reading'
    )
    
    parser.add_argument(
        '--tags',
        type=str,
        nargs='+',
        help='Tags for categorizing this reading (e.g., exercise sick stress)'
    )
    
    return parser.parse_args()


def main():
    """Main function to record glucose reading"""
    args = parse_args()
    
    # Create reading dictionary
    reading = {
        'value': args.value,
        'unit': args.unit
    }
    
    # Parse timestamp
    if args.time:
        try:
            # Support multiple formats
            for fmt in ['%Y-%m-%d %H:%M', '%Y-%m-%d %H:%M:%S', '%Y-%m-%dT%H:%M', '%Y-%m-%dT%H:%M:%S']:
                try:
                    dt = datetime.strptime(args.time, fmt)
                    reading['timestamp'] = dt.isoformat()
                    break
                except ValueError:
                    continue
            else:
                print(f"Error: Unable to parse timestamp '{args.time}'")
                print("Supported formats: 'YYYY-MM-DD HH:MM' or 'YYYY-MM-DDTHH:MM'")
                sys.exit(1)
        except Exception as e:
            print(f"Error parsing timestamp: {e}")
            sys.exit(1)
    
    # Add optional fields
    if args.meal_context:
        reading['meal_context'] = args.meal_context
    
    if args.notes:
        reading['notes'] = args.notes
    
    if args.tags:
        reading['tags'] = args.tags
    
    # Save reading
    manager = GlucoseDataManager()
    success = manager.add_reading(reading)
    
    if success:
        print("\nReading recorded successfully!")
        
        # Show recent statistics
        stats = manager.get_statistics(limit=10)
        if stats['count'] > 0:
            print(f"\nRecent readings summary (last {stats['count']} readings):")
            print(f"  Average: {stats['mean']:.1f} {args.unit}")
            print(f"  Range: {stats['min']:.1f} - {stats['max']:.1f} {args.unit}")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
