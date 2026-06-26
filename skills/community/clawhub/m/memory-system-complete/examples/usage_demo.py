#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Memory System Usage Examples
"""

import sys
sys.path.insert(0, '.')
from memory_system import MemorySystem

def demo_basic_operations():
    """Basic CRUD operations"""
    print("="*70)
    print("Example 1: Basic Operations")
    print("="*70)
    
    memory = MemorySystem()
    memory.initialize()
    
    # Save a memory
    memory_id = memory.save(
        type='learning',
        title='Python Context Managers',
        content='Always use context managers for file operations to ensure proper resource cleanup',
        category='programming',
        tags=['python', 'best-practices', 'files'],
        importance=8
    )
    
    print(f"\nSaved memory with ID: {memory_id}")
    
    # Query memories
    results = memory.query(type='learning', min_importance=7)
    print(f"\nFound {len(results)} high-importance learning memories")
    
    memory.close()

def demo_search():
    """Search functionality"""
    print("\n" + "="*70)
    print("Example 2: Search")
    print("="*70)
    
    memory = MemorySystem()
    memory.initialize()
    
    # Text search
    results = memory.search('python')
    print(f"\nFound {len(results)} memories related to 'python'")
    
    for i, mem in enumerate(results[:3], 1):
        print(f"{i}. {mem['title']}")
    
    memory.close()

def demo_update_delete():
    """Update and delete operations"""
    print("\n" + "="*70)
    print("Example 3: Update & Delete")
    print("="*70)
    
    memory = MemorySystem()
    memory.initialize()
    
    # Save a memory
    memory_id = memory.save(
        type='event',
        title='Test Event',
        content='This is a test',
        importance=3
    )
    
    print(f"\nCreated memory: {memory_id}")
    
    # Update it
    memory.update(memory_id, importance=7)
    print(f"Updated importance to 7")
    
    # Delete it
    memory.delete(memory_id)
    print(f"Deleted memory")
    
    memory.close()

def demo_cleanup():
    """Cleanup old memories"""
    print("\n" + "="*70)
    print("Example 4: Cleanup")
    print("="*70)
    
    memory = MemorySystem()
    memory.initialize()
    
    # Cleanup old, low-confidence memories
    deleted = memory.cleanup(min_confidence=0.3, days_old=90)
    print(f"\nCleaned up {deleted} old memories")
    
    memory.close()

def demo_stats():
    """Show statistics"""
    print("\n" + "="*70)
    print("Example 5: Statistics")
    print("="*70)
    
    memory = MemorySystem()
    memory.initialize()
    
    stats = memory.stats()
    
    print(f"\nTotal memories: {stats['total']}")
    print(f"Average importance: {stats['avg_importance']:.2f}")
    
    print("\nBy type:")
    for type_name, count in stats['by_type'].items():
        print(f"  {type_name}: {count}")
    
    memory.close()

def demo_export_import():
    """Export and import"""
    print("\n" + "="*70)
    print("Example 6: Export & Import")
    print("="*70)
    
    memory = MemorySystem()
    memory.initialize()
    
    # Export
    data = memory.export(format='json')
    print(f"\nExported {len(data)} characters of data")
    
    # Save to file
    with open('memory_export.json', 'w') as f:
        f.write(data)
    
    print("Saved to memory_export.json")
    
    memory.close()

if __name__ == "__main__":
    demo_basic_operations()
    demo_search()
    demo_update_delete()
    demo_cleanup()
    demo_stats()
    demo_export_import()
    
    print("\n" + "="*70)
    print("Examples Complete!")
    print("="*70)
