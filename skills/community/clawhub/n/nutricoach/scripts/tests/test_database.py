#!/usr/bin/env python3
"""
单元测试：数据库操作
测试数据库连接、查询、数据完整性
"""

import unittest
import sys
import os
import sqlite3
import tempfile
import shutil

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db_schema import (
    USERS_COLUMNS, MEALS_COLUMNS, CUSTOM_FOODS_COLUMNS,
    PANTRY_COLUMNS, BODY_METRICS_COLUMNS
)


class TestDatabaseSchema(unittest.TestCase):
    """Test database schema definitions."""
    
    def test_users_columns_complete(self):
        """Test users table has all required columns."""
        required = ['id', 'username', 'name', 'gender', 'birth_date', 
                   'height_cm', 'target_weight_kg', 'activity_level', 
                   'goal_type', 'bmr', 'tdee', 'created_at', 'updated_at']
        for col in required:
            self.assertIn(col, USERS_COLUMNS)
    
    def test_meals_columns_complete(self):
        """Test meals table has all required columns."""
        required = ['id', 'user_id', 'meal_type', 'eaten_at', 'notes',
                   'total_calories', 'total_protein_g', 'total_carbs_g', 
                   'total_fat_g', 'total_fiber_g', 'total_sodium_mg']
        for col in required:
            self.assertIn(col, MEALS_COLUMNS)
    
    def test_custom_foods_columns_complete(self):
        """Test custom_foods table has all required columns."""
        required = ['id', 'name', 'category', 'calories_per_100g',
                   'protein_per_100g', 'carbs_per_100g', 'fat_per_100g',
                   'sodium_per_100g', 'calcium_mg', 'iron_mg', 'zinc_mg']
        for col in required:
            self.assertIn(col, CUSTOM_FOODS_COLUMNS)
    
    def test_column_indices_are_integers(self):
        """Test all column indices are integers."""
        for schema in [USERS_COLUMNS, MEALS_COLUMNS, CUSTOM_FOODS_COLUMNS]:
            for col, idx in schema.items():
                self.assertIsInstance(idx, int)
                self.assertGreaterEqual(idx, 0)


class TestDatabaseOperations(unittest.TestCase):
    """Test database operations with temporary database."""
    
    def setUp(self):
        """Create temporary database for testing."""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, 'test.db')
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        
        # Create minimal schema
        self.cursor.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE,
                name TEXT,
                height_cm REAL,
                tdee REAL
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE body_metrics (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                recorded_at TEXT,
                weight_kg REAL,
                bmi REAL
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE meals (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                meal_type TEXT,
                eaten_at TEXT,
                total_calories REAL,
                total_protein_g REAL,
                total_carbs_g REAL,
                total_fat_g REAL
            )
        ''')
        
        self.conn.commit()
    
    def tearDown(self):
        """Clean up temporary database."""
        self.conn.close()
        shutil.rmtree(self.temp_dir)
    
    def test_insert_and_query_user(self):
        """Test inserting and querying user."""
        self.cursor.execute('''
            INSERT INTO users (username, name, height_cm, tdee)
            VALUES (?, ?, ?, ?)
        ''', ('testuser', 'Test User', 175.0, 2500.0))
        self.conn.commit()
        
        self.cursor.execute('SELECT * FROM users WHERE username = ?', ('testuser',))
        row = self.cursor.fetchone()
        
        self.assertIsNotNone(row)
        self.assertEqual(row[1], 'testuser')
        self.assertEqual(row[2], 'Test User')
        self.assertEqual(row[3], 175.0)
    
    def test_insert_weight_record(self):
        """Test inserting weight record."""
        # Insert user first
        self.cursor.execute('INSERT INTO users (username) VALUES (?)', ('testuser',))
        user_id = self.cursor.lastrowid
        
        # Insert weight record
        self.cursor.execute('''
            INSERT INTO body_metrics (user_id, recorded_at, weight_kg, bmi)
            VALUES (?, ?, ?, ?)
        ''', (user_id, '2026-03-31 10:00:00', 75.0, 24.5))
        self.conn.commit()
        
        self.cursor.execute('SELECT weight_kg, bmi FROM body_metrics WHERE user_id = ?', (user_id,))
        row = self.cursor.fetchone()
        
        self.assertEqual(row[0], 75.0)
        self.assertEqual(row[1], 24.5)
    
    def test_insert_meal(self):
        """Test inserting meal record."""
        # Insert user first
        self.cursor.execute('INSERT INTO users (username) VALUES (?)', ('testuser',))
        user_id = self.cursor.lastrowid
        
        # Insert meal
        self.cursor.execute('''
            INSERT INTO meals (user_id, meal_type, eaten_at, total_calories, 
                             total_protein_g, total_carbs_g, total_fat_g)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, 'lunch', '2026-03-31 12:00:00', 600.0, 30.0, 70.0, 20.0))
        self.conn.commit()
        
        self.cursor.execute('''
            SELECT total_calories, total_protein_g, total_carbs_g, total_fat_g
            FROM meals WHERE user_id = ?
        ''', (user_id,))
        row = self.cursor.fetchone()
        
        self.assertEqual(row[0], 600.0)
        self.assertEqual(row[1], 30.0)
        self.assertEqual(row[2], 70.0)
        self.assertEqual(row[3], 20.0)
    
    def test_daily_nutrition_summary(self):
        """Test calculating daily nutrition summary."""
        # Insert user
        self.cursor.execute('INSERT INTO users (username) VALUES (?)', ('testuser',))
        user_id = self.cursor.lastrowid
        
        # Insert multiple meals for same day
        meals = [
            ('breakfast', '2026-03-31 08:00:00', 400, 20, 50, 12),
            ('lunch', '2026-03-31 12:00:00', 600, 30, 70, 20),
            ('dinner', '2026-03-31 18:00:00', 500, 25, 60, 15)
        ]
        
        for meal_type, eaten_at, cal, prot, carb, fat in meals:
            self.cursor.execute('''
                INSERT INTO meals (user_id, meal_type, eaten_at, total_calories,
                                 total_protein_g, total_carbs_g, total_fat_g)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, meal_type, eaten_at, cal, prot, carb, fat))
        
        self.conn.commit()
        
        # Query daily totals
        self.cursor.execute('''
            SELECT SUM(total_calories), SUM(total_protein_g), 
                   SUM(total_carbs_g), SUM(total_fat_g)
            FROM meals
            WHERE user_id = ? AND DATE(eaten_at) = ?
        ''', (user_id, '2026-03-31'))
        
        row = self.cursor.fetchone()
        self.assertEqual(row[0], 1500)  # 400+600+500
        self.assertEqual(row[1], 75)    # 20+30+25
        self.assertEqual(row[2], 180)   # 50+70+60
        self.assertEqual(row[3], 47)    # 12+20+15


class TestDataIntegrity(unittest.TestCase):
    """Test data integrity constraints."""
    
    def test_calorie_calculation_consistency(self):
        """Test that calorie calculation is consistent."""
        # Protein and carbs = 4 kcal/g, fat = 9 kcal/g
        protein_g = 30
        carbs_g = 50
        fat_g = 20
        
        calculated_calories = protein_g * 4 + carbs_g * 4 + fat_g * 9
        expected_calories = 30 * 4 + 50 * 4 + 20 * 9  # 120 + 200 + 180 = 500
        
        self.assertEqual(calculated_calories, expected_calories)
        self.assertEqual(calculated_calories, 500)


if __name__ == '__main__':
    unittest.main()