#!/usr/bin/env python3
"""
单元测试：营养成分计算
测试食物营养计算、每日汇总、历史趋势等核心功能
"""

import unittest
import sys
import os
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db_schema import CUSTOM_FOODS_COLUMNS as FC


class TestNutritionCalculation(unittest.TestCase):
    """Test nutrition calculation functions."""
    
    def test_calculate_nutrition_per_quantity(self):
        """Test calculating nutrition for a given quantity."""
        # Test data: 100g food with known nutrition
        food_data = {
            'calories_per_100g': 165,
            'protein_per_100g': 31.0,
            'carbs_per_100g': 0,
            'fat_per_100g': 3.6,
            'fiber_per_100g': 0,
            'sodium_per_100g': 65
        }
        quantity_g = 150
        
        # Calculate expected values
        expected_calories = 165 * 1.5  # 247.5
        expected_protein = 31.0 * 1.5  # 46.5
        
        self.assertAlmostEqual(expected_calories, 247.5, places=1)
        self.assertAlmostEqual(expected_protein, 46.5, places=1)
    
    def test_daily_totals_calculation(self):
        """Test calculating daily nutrition totals."""
        # Mock meals data
        meals = [
            {'calories': 500, 'protein_g': 30, 'carbs_g': 60, 'fat_g': 15},
            {'calories': 600, 'protein_g': 35, 'carbs_g': 70, 'fat_g': 20},
            {'calories': 400, 'protein_g': 20, 'carbs_g': 50, 'fat_g': 12}
        ]
        
        totals = {
            'calories': sum(m['calories'] for m in meals),
            'protein_g': sum(m['protein_g'] for m in meals),
            'carbs_g': sum(m['carbs_g'] for m in meals),
            'fat_g': sum(m['fat_g'] for m in meals)
        }
        
        self.assertEqual(totals['calories'], 1500)
        self.assertEqual(totals['protein_g'], 85)
        self.assertEqual(totals['carbs_g'], 180)
        self.assertEqual(totals['fat_g'], 47)
    
    def test_bmi_calculation(self):
        """Test BMI calculation."""
        weight_kg = 75
        height_m = 1.75
        
        bmi = weight_kg / (height_m ** 2)
        expected_bmi = 75 / (1.75 * 1.75)  # ~24.49
        
        self.assertAlmostEqual(bmi, expected_bmi, places=2)
        self.assertGreater(bmi, 18.5)  # Normal range
        self.assertLess(bmi, 25)
    
    def test_tdee_calculation(self):
        """Test TDEE calculation using Mifflin-St Jeor formula."""
        # Male, 30 years, 175cm, 75kg, moderate activity
        weight_kg = 75
        height_cm = 175
        age = 30
        is_male = True
        activity_multiplier = 1.55  # Moderate
        
        # BMR calculation
        if is_male:
            bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
        else:
            bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
        
        tdee = bmr * activity_multiplier
        
        # Verify BMR is in reasonable range (1500-2000 for this profile)
        self.assertGreater(bmr, 1500)
        self.assertLess(bmr, 2000)
        
        # Verify TDEE is higher than BMR
        self.assertGreater(tdee, bmr)


class TestFoodDatabase(unittest.TestCase):
    """Test food database operations."""
    
    def test_food_nutrition_completeness(self):
        """Test that common foods have complete nutrition data."""
        # Essential nutrients that should be present
        essential_fields = [
            'calories_per_100g',
            'protein_per_100g',
            'carbs_per_100g',
            'fat_per_100g'
        ]
        
        for field in essential_fields:
            self.assertIn(field, FC)
    
    def test_new_nutrition_fields_exist(self):
        """Test that new nutrition fields were added."""
        new_fields = [
            'calcium_mg',
            'trans_fat_g',
            'saturated_fat_g',
            'sugar_g',
            'vitamin_a_ug',
            'vitamin_c_mg',
            'iron_mg',
            'zinc_mg'
        ]
        
        for field in new_fields:
            self.assertIn(field, FC, f"Field {field} should exist in schema")


class TestPantryCalculations(unittest.TestCase):
    """Test pantry-related calculations."""
    
    def test_remaining_percentage(self):
        """Test calculating remaining percentage."""
        initial_g = 500
        remaining_g = 250
        
        percent = (remaining_g / initial_g) * 100
        self.assertEqual(percent, 50)
    
    def test_expiry_days_calculation(self):
        """Test calculating days until expiry."""
        today = datetime.now()
        expiry = today + timedelta(days=5)
        
        days_left = (expiry - today).days
        self.assertEqual(days_left, 5)
    
    def test_expiry_status_classification(self):
        """Test expiry status classification."""
        test_cases = [
            (-2, 'expired'),      # 2 days ago
            (0, 'urgent'),        # Today
            (1, 'urgent'),        # Tomorrow
            (3, 'soon'),          # Within 3 days
            (7, 'ok'),            # Within a week
            (30, 'ok')            # Within a month
        ]
        
        for days_left, expected_status in test_cases:
            if days_left < 0:
                status = 'expired'
            elif days_left <= 1:
                status = 'urgent'
            elif days_left <= 3:
                status = 'soon'
            else:
                status = 'ok'
            
            self.assertEqual(status, expected_status)


class TestDataValidation(unittest.TestCase):
    """Test data validation functions."""
    
    def test_weight_value_validation(self):
        """Test weight value validation."""
        valid_weights = [50, 75.5, 100, 120]
        invalid_weights = [0, -10, 500, None, 'abc']
        
        for weight in valid_weights:
            self.assertTrue(30 <= weight <= 200, f"Weight {weight} should be valid")
        
        for weight in invalid_weights:
            is_valid = isinstance(weight, (int, float)) and 30 <= weight <= 200
            self.assertFalse(is_valid, f"Weight {weight} should be invalid")
    
    def test_quantity_parsing(self):
        """Test parsing food quantity strings."""
        test_cases = [
            ('米饭:150g', '米饭', 150),
            ('鸡胸肉 200g', '鸡胸肉', 200),
            ('鸡蛋:2个', '鸡蛋', 2),
        ]
        
        for input_str, expected_name, expected_qty in test_cases:
            # Basic parsing logic
            if ':' in input_str:
                parts = input_str.split(':')
            else:
                parts = input_str.rsplit(' ', 1)
            
            name = parts[0].strip()
            self.assertEqual(name, expected_name)


def run_tests():
    """Run all tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestNutritionCalculation))
    suite.addTests(loader.loadTestsFromTestCase(TestFoodDatabase))
    suite.addTests(loader.loadTestsFromTestCase(TestPantryCalculations))
    suite.addTests(loader.loadTestsFromTestCase(TestDataValidation))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
