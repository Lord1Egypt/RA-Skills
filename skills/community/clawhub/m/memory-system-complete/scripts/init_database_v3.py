#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Memory System v3.0 - Database Initialization
"""

import sqlite3
import os
from pathlib import Path

def init_database(db_path="memory/database/xiaozhi_memory.db"):
    """Initialize database with all tables"""
    
    # Create database directory
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Core tables (3)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            category TEXT,
            tags TEXT,
            importance INTEGER DEFAULT 5,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS causal_relations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cause_id INTEGER NOT NULL,
            effect_id INTEGER NOT NULL,
            causal_type TEXT NOT NULL,
            strength REAL DEFAULT 0.5,
            confidence REAL DEFAULT 0.5,
            evidence TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (cause_id) REFERENCES memories(id),
            FOREIGN KEY (effect_id) REFERENCES memories(id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS knowledge_relations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_id INTEGER NOT NULL,
            target_id INTEGER NOT NULL,
            relation_type TEXT NOT NULL,
            strength REAL DEFAULT 0.5,
            direction TEXT DEFAULT 'bidirectional',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (source_id) REFERENCES memories(id),
            FOREIGN KEY (target_id) REFERENCES memories(id)
        )
    ''')
    
    # Evolution tables (8)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS memory_associations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            memory_id INTEGER NOT NULL,
            associated_id INTEGER NOT NULL,
            association_type TEXT,
            strength REAL DEFAULT 0.5,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (memory_id) REFERENCES memories(id),
            FOREIGN KEY (associated_id) REFERENCES memories(id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS memory_communities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            community_id INTEGER NOT NULL,
            memory_id INTEGER NOT NULL,
            membership_strength REAL DEFAULT 0.5,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (memory_id) REFERENCES memories(id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS graph_insights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            insight_type TEXT NOT NULL,
            description TEXT,
            related_memories TEXT,
            confidence REAL DEFAULT 0.5,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS review_queue (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            memory_id INTEGER NOT NULL,
            action_type TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            assigned_to TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,
            FOREIGN KEY (memory_id) REFERENCES memories(id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS deep_research (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT NOT NULL,
            results TEXT,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ingestion_cache (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content_hash TEXT NOT NULL,
            processed_content TEXT,
            metadata TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS retrieval_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT NOT NULL,
            results TEXT,
            retrieval_method TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS evolution_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT NOT NULL,
            description TEXT,
            metadata TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Genetic neuron tables (12)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS genetic_neurons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            neuron_type TEXT NOT NULL,
            activation_threshold REAL DEFAULT 0.5,
            activation_function TEXT DEFAULT 'sigmoid',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS genetic_connections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_id INTEGER NOT NULL,
            target_id INTEGER NOT NULL,
            weight REAL DEFAULT 0.5,
            connection_type TEXT DEFAULT 'excitatory',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (source_id) REFERENCES genetic_neurons(id),
            FOREIGN KEY (target_id) REFERENCES genetic_neurons(id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS synaptic_weights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            connection_id INTEGER NOT NULL,
            weight REAL DEFAULT 0.5,
            learning_rate REAL DEFAULT 0.01,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (connection_id) REFERENCES genetic_connections(id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS neurogenesis_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            neuron_id INTEGER NOT NULL,
            neurogenesis_type TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (neuron_id) REFERENCES genetic_neurons(id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS memory_consolidation_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            memory_id INTEGER NOT NULL,
            consolidation_strength REAL DEFAULT 0.5,
            consolidation_type TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (memory_id) REFERENCES memories(id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attention_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT NOT NULL,
            attention_weights TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS neuromodulation_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            neuron_id INTEGER NOT NULL,
            dopamine REAL DEFAULT 0.0,
            serotonin REAL DEFAULT 0.0,
            norepinephrine REAL DEFAULT 0.0,
            acetylcholine REAL DEFAULT 0.0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (neuron_id) REFERENCES genetic_neurons(id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS spike_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            neuron_id INTEGER NOT NULL,
            spike_times TEXT,
            spike_count INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (neuron_id) REFERENCES genetic_neurons(id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS structural_plasticity_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            neuron_id INTEGER NOT NULL,
            plasticity_type TEXT,
            structural_change TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (neuron_id) REFERENCES genetic_neurons(id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS heterogeneous_neurons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            neuron_id INTEGER NOT NULL,
            neuron_subtype TEXT,
            properties TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (neuron_id) REFERENCES genetic_neurons(id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS module_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            module_id INTEGER NOT NULL,
            module_type TEXT,
            module_function TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS evolution_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            generation INTEGER NOT NULL,
            fitness REAL DEFAULT 0.0,
            population_size INTEGER DEFAULT 0,
            best_individual TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create indexes
    indexes = [
        ('idx_memories_type', 'memories', 'type'),
        ('idx_memories_category', 'memories', 'category'),
        ('idx_memories_created_at', 'memories', 'created_at'),
        ('idx_causal_cause', 'causal_relations', 'cause_id'),
        ('idx_causal_effect', 'causal_relations', 'effect_id'),
        ('idx_knowledge_source', 'knowledge_relations', 'source_id'),
        ('idx_knowledge_target', 'knowledge_relations', 'target_id'),
        ('idx_associations_memory', 'memory_associations', 'memory_id'),
        ('idx_communities_memory', 'memory_communities', 'memory_id'),
        ('idx_review_memory', 'review_queue', 'memory_id'),
        ('idx_neurons_type', 'genetic_neurons', 'neuron_type'),
        ('idx_connections_source', 'genetic_connections', 'source_id'),
        ('idx_connections_target', 'genetic_connections', 'target_id'),
        ('idx_weights_connection', 'synaptic_weights', 'connection_id'),
        ('idx_consolidation_memory', 'memory_consolidation_log', 'memory_id'),
        ('idx_modulation_neuron', 'neuromodulation_records', 'neuron_id'),
        ('idx_spikes_neuron', 'spike_records', 'neuron_id'),
        ('idx_plasticity_neuron', 'structural_plasticity_log', 'neuron_id'),
        ('idx_heterogeneous_neuron', 'heterogeneous_neurons', 'neuron_id'),
    ]
    
    for index_name, table, column in indexes:
        cursor.execute(f'CREATE INDEX IF NOT EXISTS {index_name} ON {table}({column})')
    
    # Commit changes
    conn.commit()
    conn.close()
    
    print(f"[OK] Database initialized: {db_path}")
    print(f"[OK] Total tables: 23 (3 core + 8 evolution + 12 genetic)")
    print(f"[OK] Total indexes: 20")
    
    return True

if __name__ == "__main__":
    import sys
    
    db_path = sys.argv[1] if len(sys.argv) > 1 else "memory/database/xiaozhi_memory.db"
    
    print("=" * 60)
    print("Memory System v3.0 - Database Initialization")
    print("=" * 60)
    print()
    
    success = init_database(db_path)
    
    if success:
        print()
        print("=" * 60)
        print("[SUCCESS] Database initialization completed!")
        print("=" * 60)
    else:
        print()
        print("=" * 60)
        print("[ERROR] Database initialization failed!")
        print("=" * 60)
