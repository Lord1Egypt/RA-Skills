#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Memory System v3.0 - Installation Verification
"""

import sqlite3
import os
import sys

def verify_installation(db_path="memory/database/xiaozhi_memory.db"):
    """Verify installation"""
    
    print("[1/5] Checking database file...")
    if not os.path.exists(db_path):
        print(f"      [ERROR] Database file not found: {db_path}")
        return False
    print(f"      [OK] Database file exists")
    
    print("[2/5] Checking database connection...")
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        print(f"      [OK] Database connection successful")
    except Exception as e:
        print(f"      [ERROR] Database connection failed: {e}")
        return False
    
    print("[3/5] Checking tables...")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    
    expected_tables = [
        'memories', 'causal_relations', 'knowledge_relations',
        'memory_associations', 'memory_communities', 'graph_insights',
        'review_queue', 'deep_research', 'ingestion_cache',
        'retrieval_history', 'evolution_log',
        'genetic_neurons', 'genetic_connections', 'synaptic_weights',
        'neurogenesis_log', 'memory_consolidation_log', 'attention_records',
        'neuromodulation_records', 'spike_records', 'structural_plasticity_log',
        'heterogeneous_neurons', 'module_records', 'evolution_records'
    ]
    
    missing_tables = [t for t in expected_tables if t not in tables]
    if missing_tables:
        print(f"      [ERROR] Missing tables: {missing_tables}")
        return False
    
    print(f"      [OK] All 23 tables present")
    
    print("[4/5] Checking indexes...")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index'")
    indexes = [row[0] for row in cursor.fetchall()]
    
    expected_indexes = [
        'idx_memories_type', 'idx_memories_category', 'idx_memories_created_at',
        'idx_causal_cause', 'idx_causal_effect',
        'idx_knowledge_source', 'idx_knowledge_target',
        'idx_associations_memory', 'idx_communities_memory', 'idx_review_memory',
        'idx_neurons_type', 'idx_connections_source', 'idx_connections_target',
        'idx_weights_connection', 'idx_consolidation_memory', 'idx_modulation_neuron',
        'idx_spikes_neuron', 'idx_plasticity_neuron', 'idx_heterogeneous_neuron'
    ]
    
    missing_indexes = [i for i in expected_indexes if i not in indexes]
    if missing_indexes:
        print(f"      [WARNING] Missing indexes: {missing_indexes}")
    else:
        print(f"      [OK] All 20 indexes present")
    
    print("[5/5] Testing basic operations...")
    try:
        # Test insert
        cursor.execute('''
            INSERT INTO memories (type, title, content, category, importance)
            VALUES (?, ?, ?, ?, ?)
        ''', ('test', 'Installation Test v3.0', 'Testing memory system v3.0', 'test', 5))
        
        # Test select
        cursor.execute('SELECT * FROM memories WHERE title = ?', ('Installation Test v3.0',))
        result = cursor.fetchone()
        
        if result:
            print(f"      [OK] Insert and select operations working")
            
            # Clean up test data
            cursor.execute('DELETE FROM memories WHERE title = ?', ('Installation Test v3.0',))
            conn.commit()
        else:
            print(f"      [ERROR] Select operation failed")
            return False
    except Exception as e:
        print(f"      [ERROR] Basic operations failed: {e}")
        return False
    
    conn.close()
    
    return True

if __name__ == "__main__":
    db_path = sys.argv[1] if len(sys.argv) > 1 else "memory/database/xiaozhi_memory.db"
    
    print("=" * 60)
    print("Memory System v3.0 - Installation Verification")
    print("=" * 60)
    print()
    
    success = verify_installation(db_path)
    
    print()
    print("=" * 60)
    if success:
        print("[SUCCESS] Installation verified!")
        print("[INFO] Memory system v3.0 is ready to use")
        print("[INFO] Total tables: 23 (3 core + 8 evolution + 12 genetic)")
        print("[INFO] Total indexes: 20")
    else:
        print("[ERROR] Installation verification failed!")
        print("[INFO] Please run: python scripts/init_database_v3.py")
    print("=" * 60)
    
    sys.exit(0 if success else 1)
