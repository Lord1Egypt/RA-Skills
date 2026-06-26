#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Theory of Mind (ToM) Engine
心智模型推理引擎
"""

import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple

class ToMEngine:
    """Theory of Mind推理引擎"""
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = "memory/database/xiaozhi_memory.db"
        self.db_path = db_path
        self.conn = None
    
    def initialize(self) -> bool:
        """初始化ToM引擎"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self._create_tables()
            return True
        except Exception as e:
            print(f"Error initializing ToM engine: {e}")
            return False
    
    def _create_tables(self):
        """创建ToM相关表"""
        cursor = self.conn.cursor()
        
        # 信念表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tom_beliefs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entity TEXT NOT NULL,
                belief_type TEXT NOT NULL,
                content TEXT,
                confidence REAL DEFAULT 0.5,
                evidence TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 意图表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tom_intents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entity TEXT NOT NULL,
                intent_type TEXT NOT NULL,
                description TEXT,
                confidence REAL DEFAULT 0.5,
                context TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 情绪表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tom_emotions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entity TEXT NOT NULL,
                emotion_type TEXT NOT NULL,
                intensity REAL DEFAULT 0.5,
                cause TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()
    
    def update_belief(self, entity: str, belief_type: str, 
                     content: str, confidence: float = 0.5,
                     evidence: str = None) -> int:
        """更新信念（贝叶斯融合）"""
        cursor = self.conn.cursor()
        
        # 查找现有信念
        cursor.execute('''
            SELECT id, confidence FROM tom_beliefs
            WHERE entity = ? AND belief_type = ?
            ORDER BY updated_at DESC LIMIT 1
        ''', (entity, belief_type))
        
        row = cursor.fetchone()
        
        if row:
            # 贝叶斯融合：旧信念*0.7 + 新信念*0.3
            old_confidence = row[1]
            new_confidence = old_confidence * 0.7 + confidence * 0.3
            
            cursor.execute('''
                UPDATE tom_beliefs
                SET content = ?, confidence = ?, evidence = ?, updated_at = ?
                WHERE id = ?
            ''', (content, new_confidence, evidence, datetime.now().isoformat(), row[0]))
            
            belief_id = row[0]
        else:
            # 创建新信念
            cursor.execute('''
                INSERT INTO tom_beliefs (entity, belief_type, content, confidence, evidence)
                VALUES (?, ?, ?, ?, ?)
            ''', (entity, belief_type, content, confidence, evidence))
            
            belief_id = cursor.lastrowid
        
        self.conn.commit()
        return belief_id
    
    def infer_intent(self, entity: str, context: str) -> Dict:
        """推断意图"""
        cursor = self.conn.cursor()
        
        # 查找历史意图
        cursor.execute('''
            SELECT intent_type, description, confidence
            FROM tom_intents
            WHERE entity = ?
            ORDER BY confidence DESC
            LIMIT 5
        ''', (entity,))
        
        intents = []
        for row in cursor.fetchall():
            intents.append({
                'type': row[0],
                'description': row[1],
                'confidence': row[2]
            })
        
        # 简单意图推断逻辑
        inferred_intent = {
            'entity': entity,
            'context': context,
            'inferred_intents': intents,
            'primary_intent': intents[0] if intents else None
        }
        
        return inferred_intent
    
    def detect_emotion(self, entity: str, text: str) -> Dict:
        """检测情绪"""
        # 简单情绪检测（实际应该使用NLP模型）
        emotions = {
            'positive': ['happy', 'good', 'great', 'excellent', 'love'],
            'negative': ['bad', 'terrible', 'hate', 'angry', 'sad'],
            'neutral': ['ok', 'fine', 'normal', 'average']
        }
        
        detected = {'primary': 'neutral', 'intensity': 0.5}
        
        for emotion, keywords in emotions.items():
            for keyword in keywords:
                if keyword in text.lower():
                    detected['primary'] = emotion
                    detected['intensity'] = 0.7
                    break
        
        # 保存到数据库
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO tom_emotions (entity, emotion_type, intensity, cause)
            VALUES (?, ?, ?, ?)
        ''', (entity, detected['primary'], detected['intensity'], text))
        
        self.conn.commit()
        
        return detected
    
    def get_beliefs(self, entity: str = None) -> List[Dict]:
        """获取信念"""
        cursor = self.conn.cursor()
        
        if entity:
            cursor.execute('''
                SELECT * FROM tom_beliefs WHERE entity = ?
                ORDER BY confidence DESC
            ''', (entity,))
        else:
            cursor.execute('''
                SELECT * FROM tom_beliefs
                ORDER BY confidence DESC
            ''')
        
        beliefs = []
        for row in cursor.fetchall():
            beliefs.append({
                'id': row[0],
                'entity': row[1],
                'type': row[2],
                'content': row[3],
                'confidence': row[4],
                'evidence': row[5]
            })
        
        return beliefs
    
    def close(self):
        """关闭连接"""
        if self.conn:
            self.conn.close()


if __name__ == "__main__":
    tom = ToMEngine()
    tom.initialize()
    
    # 测试
    tom.update_belief('user', 'preference', 'Likes Python', 0.8)
    tom.detect_emotion('user', 'I am very happy with this!')
    
    beliefs = tom.get_beliefs('user')
    print(f"Beliefs: {beliefs}")
    
    tom.close()
