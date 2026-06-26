#!/usr/bin/env python3
"""
Blood Glucose Data Manager
Handles storage, retrieval, and backup of glucose reading data
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import shutil


class GlucoseDataManager:
    """Manages blood glucose data storage and retrieval"""
    
    def __init__(self, data_dir: Optional[str] = None):
        """
        Initialize the data manager.
        
        Args:
            data_dir: Custom data directory path. If None, uses default location.
        """
        if data_dir:
            self.data_dir = Path(data_dir)
        else:
            self.data_dir = Path.home() / '.workbuddy' / 'data'
        
        self.data_file = self.data_dir / 'glucose_readings.json'
        self.backup_dir = self.data_dir / 'backups'
        
        # Initialize directories
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Create necessary directories if they don't exist"""
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
    
    def _create_backup(self):
        """Create a backup of the current data file"""
        if self.data_file.exists():
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_file = self.backup_dir / f'glucose_readings_{timestamp}.json'
            shutil.copy2(self.data_file, backup_file)
            
            # Keep only last 10 backups
            backups = sorted(self.backup_dir.glob('glucose_readings_*.json'))
            if len(backups) > 10:
                for old_backup in backups[:-10]:
                    old_backup.unlink()
    
    def load_data(self) -> Dict:
        """
        Load glucose readings data from file.
        
        Returns:
            Dictionary containing glucose readings and metadata
        """
        if not self.data_file.exists():
            return {
                'readings': [],
                'metadata': {
                    'created': datetime.now().isoformat(),
                    'last_updated': datetime.now().isoformat(),
                    'version': '1.0'
                }
            }
        
        with open(self.data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save_data(self, data: Dict):
        """
        Save glucose readings data to file with backup.
        
        Args:
            data: Dictionary containing glucose readings and metadata
        """
        self._create_backup()
        
        data['metadata']['last_updated'] = datetime.now().isoformat()
        
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def add_reading(self, reading: Dict) -> bool:
        """
        Add a new glucose reading.
        
        Args:
            reading: Dictionary containing reading data
                Required keys: value, unit
                Optional keys: timestamp, meal_context, notes, tags
        
        Returns:
            True if successful, False otherwise
        """
        try:
            data = self.load_data()
            
            # Validate required fields
            if 'value' not in reading or 'unit' not in reading:
                print("Error: Missing required fields (value, unit)")
                return False
            
            # Add timestamp if not provided
            if 'timestamp' not in reading:
                reading['timestamp'] = datetime.now().isoformat()
            
            # Add reading ID
            reading['id'] = datetime.now().strftime('%Y%m%d%H%M%S%f')
            
            # Add to readings list
            data['readings'].append(reading)
            
            # Sort by timestamp
            data['readings'].sort(key=lambda x: x['timestamp'])
            
            # Save
            self.save_data(data)
            
            print(f"✓ Added reading: {reading['value']} {reading['unit']} at {reading['timestamp']}")
            return True
            
        except Exception as e:
            print(f"Error adding reading: {e}")
            return False
    
    def get_readings(self, 
                     start_date: Optional[str] = None,
                     end_date: Optional[str] = None,
                     limit: Optional[int] = None) -> List[Dict]:
        """
        Retrieve glucose readings with optional filters.
        
        Args:
            start_date: Start date filter (ISO format string)
            end_date: End date filter (ISO format string)
            limit: Maximum number of readings to return
        
        Returns:
            List of glucose readings
        """
        data = self.load_data()
        readings = data['readings']
        
        # Apply date filters
        if start_date:
            readings = [r for r in readings if r['timestamp'] >= start_date]
        
        if end_date:
            readings = [r for r in readings if r['timestamp'] <= end_date]
        
        # Apply limit
        if limit:
            readings = readings[-limit:]
        
        return readings
    
    def update_reading(self, reading_id: str, updates: Dict) -> bool:
        """
        Update an existing glucose reading.
        
        Args:
            reading_id: ID of the reading to update
            updates: Dictionary of fields to update
        
        Returns:
            True if successful, False otherwise
        """
        try:
            data = self.load_data()
            
            # Find reading
            for reading in data['readings']:
                if reading['id'] == reading_id:
                    reading.update(updates)
                    self.save_data(data)
                    print(f"✓ Updated reading {reading_id}")
                    return True
            
            print(f"Error: Reading {reading_id} not found")
            return False
            
        except Exception as e:
            print(f"Error updating reading: {e}")
            return False
    
    def delete_reading(self, reading_id: str) -> bool:
        """
        Delete a glucose reading.
        
        Args:
            reading_id: ID of the reading to delete
        
        Returns:
            True if successful, False otherwise
        """
        try:
            data = self.load_data()
            
            # Find and remove reading
            original_count = len(data['readings'])
            data['readings'] = [r for r in data['readings'] if r['id'] != reading_id]
            
            if len(data['readings']) < original_count:
                self.save_data(data)
                print(f"✓ Deleted reading {reading_id}")
                return True
            else:
                print(f"Error: Reading {reading_id} not found")
                return False
                
        except Exception as e:
            print(f"Error deleting reading: {e}")
            return False
    
    def get_statistics(self, 
                       start_date: Optional[str] = None,
                       end_date: Optional[str] = None) -> Dict:
        """
        Calculate statistics for glucose readings.
        
        Args:
            start_date: Start date filter (ISO format string)
            end_date: End date filter (ISO format string)
        
        Returns:
            Dictionary containing statistics
        """
        readings = self.get_readings(start_date, end_date)
        
        if not readings:
            return {
                'count': 0,
                'message': 'No readings found for the specified period'
            }
        
        values = [r['value'] for r in readings]
        
        # Calculate statistics
        import statistics
        
        stats = {
            'count': len(values),
            'mean': statistics.mean(values),
            'median': statistics.median(values),
            'min': min(values),
            'max': max(values),
            'std_dev': statistics.stdev(values) if len(values) > 1 else 0,
        }
        
        # Calculate coefficient of variation
        if stats['mean'] > 0:
            stats['cv'] = (stats['std_dev'] / stats['mean']) * 100
        else:
            stats['cv'] = 0
        
        # Calculate time in ranges (assuming mmol/L)
        # Normal range: 4.0-7.0 mmol/L (fasting), 4.0-10.0 mmol/L (post-meal)
        # For simplicity, using 4.0-10.0 as general target range
        in_range = sum(1 for v in values if 4.0 <= v <= 10.0)
        below_range = sum(1 for v in values if v < 4.0)
        above_range = sum(1 for v in values if v > 10.0)
        
        stats['time_in_range'] = {
            'in_range': (in_range / len(values)) * 100,
            'below_range': (below_range / len(values)) * 100,
            'above_range': (above_range / len(values)) * 100
        }
        
        return stats


def main():
    """Example usage"""
    manager = GlucoseDataManager()
    
    # Add a test reading
    test_reading = {
        'value': 7.2,
        'unit': 'mmol/L',
        'meal_context': 'post-meal',
        'notes': 'Test reading'
    }
    
    manager.add_reading(test_reading)
    
    # Get statistics
    stats = manager.get_statistics()
    print("\nStatistics:")
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
