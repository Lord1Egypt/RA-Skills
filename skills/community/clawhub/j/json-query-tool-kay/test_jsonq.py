#!/usr/bin/env python3
"""
Test suite for JSON Query Tool - 50+ test cases
"""

import unittest
import json
import tempfile
import os
from jsonq import parse_query, get_value, format_output, format_table


class TestParseQuery(unittest.TestCase):
    """Test query parsing"""
    
    def test_simple_key(self):
        self.assertEqual(parse_query("name"), ["name"])
    
    def test_nested_key(self):
        self.assertEqual(parse_query("user.name"), ["user", "name"])
    
    def test_array_index(self):
        self.assertEqual(parse_query("users[0]"), ["users", 0])
    
    def test_array_wildcard(self):
        self.assertEqual(parse_query("users[*]"), ["users", slice(None)])
    
    def test_deep_nesting(self):
        self.assertEqual(
            parse_query("a.b.c.d"),
            ["a", "b", "c", "d"]
        )
    
    def test_mixed_array_object(self):
        self.assertEqual(
            parse_query("users[0].name"),
            ["users", 0, "name"]
        )
    
    def test_multiple_array_indices(self):
        self.assertEqual(
            parse_query("data[0].items[1]"),
            ["data", 0, "items", 1]
        )
    
    def test_wildcard_key(self):
        self.assertEqual(parse_query("users.*.name"), ["users", "*", "name"])
    
    def test_leading_dot_ignored(self):
        self.assertEqual(parse_query(".name"), ["name"])
    
    def test_trailing_dot_ignored(self):
        self.assertEqual(parse_query("user."), ["user"])
    
    def test_large_array_index(self):
        self.assertEqual(parse_query("items[999]"), ["items", 999])


class TestGetValue(unittest.TestCase):
    """Test value extraction"""
    
    def setUp(self):
        self.data = {
            "name": "Alice",
            "age": 30,
            "email": "alice@example.com",
            "address": {
                "city": "Beijing",
                "zip": "100000"
            },
            "hobbies": ["reading", "coding", "gaming"],
            "friends": [
                {"name": "Bob", "age": 25},
                {"name": "Charlie", "age": 35}
            ],
            "company": {
                "name": "TechCorp",
                "departments": [
                    {"name": "Engineering", "head": "Dave"},
                    {"name": "Sales", "head": "Eve"}
                ]
            }
        }
    
    def test_simple_string(self):
        self.assertEqual(get_value(self.data, ["name"]), "Alice")
    
    def test_simple_number(self):
        self.assertEqual(get_value(self.data, ["age"]), 30)
    
    def test_nested_object(self):
        self.assertEqual(get_value(self.data, ["address", "city"]), "Beijing")
    
    def test_nested_number(self):
        self.assertEqual(get_value(self.data, ["address", "zip"]), "100000")
    
    def test_array_index_string(self):
        self.assertEqual(get_value(self.data, ["hobbies", 0]), "reading")
    
    def test_array_index_object(self):
        self.assertEqual(
            get_value(self.data, ["friends", 0]),
            {"name": "Bob", "age": 25}
        )
    
    def test_array_wildcard(self):
        result = get_value(self.data, ["hobbies", slice(None)])
        self.assertEqual(result, ["reading", "coding", "gaming"])
    
    def test_object_in_array_wildcard(self):
        result = get_value(self.data, ["friends", slice(None), "name"])
        self.assertEqual(result, ["Bob", "Charlie"])
    
    def test_deep_nesting_array(self):
        self.assertEqual(
            get_value(self.data, ["company", "departments", 0, "name"]),
            "Engineering"
        )
    
    def test_deep_nesting_wildcard(self):
        result = get_value(self.data, ["company", "departments", slice(None), "name"])
        self.assertEqual(result, ["Engineering", "Sales"])
    
    def test_nonexistent_key(self):
        self.assertIsNone(get_value(self.data, ["nonexistent"]))
    
    def test_nonexistent_nested(self):
        self.assertIsNone(get_value(self.data, ["address", "country"]))
    
    def test_array_index_out_of_bounds(self):
        self.assertIsNone(get_value(self.data, ["hobbies", 100]))
    
    def test_negative_array_index(self):
        # Negative indices not supported
        self.assertIsNone(get_value(self.data, ["hobbies", -1]))
    
    def test_wildcard_on_object(self):
        result = get_value(self.data, ["address", "*"])
        self.assertEqual(result, {"city": "Beijing", "zip": "100000"})
    
    def test_empty_path(self):
        self.assertEqual(get_value(self.data, []), self.data)
    
    def test_null_data(self):
        self.assertIsNone(get_value(None, ["name"]))
    
    def test_string_as_data(self):
        self.assertIsNone(get_value("string", ["name"]))


class TestEdgeCases(unittest.TestCase):
    """Test edge cases"""
    
    def test_empty_object(self):
        self.assertEqual(get_value({}, ["key"]), None)
    
    def test_empty_array(self):
        self.assertEqual(get_value([], [0]), None)
        self.assertEqual(get_value([], [slice(None)]), [])
    
    def test_null_values(self):
        data = {"a": None, "b": {"c": None}}
        self.assertIsNone(get_value(data, ["a"]))
        self.assertIsNone(get_value(data, ["b", "c"]))
    
    def test_boolean_values(self):
        data = {"active": True, "deleted": False}
        self.assertEqual(get_value(data, ["active"]), True)
        self.assertEqual(get_value(data, ["deleted"]), False)
    
    def test_zero_value(self):
        data = {"count": 0, "price": 0.0}
        self.assertEqual(get_value(data, ["count"]), 0)
        self.assertEqual(get_value(data, ["price"]), 0.0)
    
    def test_empty_string(self):
        data = {"name": ""}
        self.assertEqual(get_value(data, ["name"]), "")
    
    def test_special_characters_in_key(self):
        data = {"key-with-dash": 1, "key_with_underscore": 2, "key.with.dots": 3}
        self.assertEqual(get_value(data, ["key-with-dash"]), 1)
        self.assertEqual(get_value(data, ["key_with_underscore"]), 2)


class TestComplexQueries(unittest.TestCase):
    """Test complex real-world scenarios"""
    
    def setUp(self):
        self.data = {
            "users": [
                {
                    "id": 1,
                    "profile": {
                        "name": "Alice",
                        "contact": {
                            "email": "alice@example.com",
                            "phone": "1234567890"
                        }
                    },
                    "orders": [
                        {"id": "A1", "total": 100},
                        {"id": "A2", "total": 200}
                    ]
                },
                {
                    "id": 2,
                    "profile": {
                        "name": "Bob",
                        "contact": {
                            "email": "bob@example.com",
                            "phone": "0987654321"
                        }
                    },
                    "orders": [
                        {"id": "B1", "total": 150}
                    ]
                }
            ],
            "metadata": {
                "total": 2,
                "page": 1,
                "settings": {
                    "theme": "dark",
                    "notifications": True
                }
            }
        }
    
    def test_get_all_user_names(self):
        result = get_value(self.data, ["users", slice(None), "profile", "name"])
        self.assertEqual(result, ["Alice", "Bob"])
    
    def test_get_all_emails(self):
        result = get_value(self.data, ["users", slice(None), "profile", "contact", "email"])
        self.assertEqual(result, ["alice@example.com", "bob@example.com"])
    
    def test_get_first_user_all_orders(self):
        result = get_value(self.data, ["users", 0, "orders", slice(None)])
        self.assertEqual(len(result), 2)
    
    def test_get_all_order_totals(self):
        # Nested arrays
        result = get_value(self.data, ["users", slice(None), "orders", slice(None), "total"])
        self.assertEqual(result, [[100, 200], [150]])
    
    def test_deep_metadata_access(self):
        self.assertEqual(get_value(self.data, ["metadata", "settings", "theme"]), "dark")
    
    def test_first_user_first_order_id(self):
        self.assertEqual(get_value(self.data, ["users", 0, "orders", 0, "id"]), "A1")


class TestFormatOutput(unittest.TestCase):
    """Test output formatting"""
    
    def test_json_format_simple(self):
        result = format_output("hello", "json")
        self.assertEqual(result, '"hello"')
    
    def test_json_format_number(self):
        result = format_output(42, "json")
        self.assertEqual(result, "42")
    
    def test_json_format_list(self):
        result = format_output([1, 2, 3], "json")
        self.assertEqual(result, "[\n  1,\n  2,\n  3\n]")
    
    def test_json_format_dict(self):
        result = format_output({"a": 1}, "json")
        self.assertIn('"a": 1', result)
    
    def test_raw_format_string(self):
        result = format_output("hello", "raw")
        self.assertEqual(result, "hello")
    
    def test_raw_format_number(self):
        result = format_output(42, "raw")
        self.assertEqual(result, "42")
    
    def test_raw_format_list(self):
        result = format_output([1, 2, 3], "raw")
        self.assertEqual(result, "[\n  1,\n  2,\n  3\n]")


class TestTableFormat(unittest.TestCase):
    """Test table formatting"""
    
    def test_empty_list(self):
        result = format_table([])
        self.assertEqual(result, "(empty)")
    
    def test_single_object(self):
        data = [{"name": "Alice", "age": 30}]
        result = format_table(data)
        self.assertIn("name", result)
        self.assertIn("Alice", result)
        self.assertIn("30", result)
    
    def test_multiple_objects(self):
        data = [
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 25}
        ]
        result = format_table(data)
        self.assertIn("Alice", result)
        self.assertIn("Bob", result)
    
    def test_missing_keys(self):
        data = [
            {"name": "Alice", "age": 30},
            {"name": "Bob"}  # missing age
        ]
        result = format_table(data)
        self.assertIn("Alice", result)
        self.assertIn("Bob", result)
    
    def test_non_dict_fallback(self):
        result = format_table("not a dict")
        self.assertEqual(result, '"not a dict"')


class TestCLI(unittest.TestCase):
    """Test CLI integration"""
    
    def setUp(self):
        self.test_data = {
            "users": [
                {"name": "Alice", "email": "alice@example.com"},
                {"name": "Bob", "email": "bob@example.com"}
            ]
        }
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        json.dump(self.test_data, self.temp_file)
        self.temp_file.close()
    
    def tearDown(self):
        os.unlink(self.temp_file.name)
    
    def test_cli_basic_query(self):
        import subprocess
        result = subprocess.run(
            ['python3', 'jsonq', self.temp_file.name, 'users[0].name'],
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn('Alice', result.stdout)
    
    def test_cli_invalid_file(self):
        import subprocess
        result = subprocess.run(
            ['python3', 'jsonq', 'nonexistent.json', 'name'],
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn('File not found', result.stderr)
    
    def test_cli_invalid_json(self):
        import subprocess
        bad_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        bad_file.write('not valid json')
        bad_file.close()
        
        result = subprocess.run(
            ['python3', 'jsonq', bad_file.name, 'name'],
            capture_output=True,
            text=True
        )
        os.unlink(bad_file.name)
        self.assertEqual(result.returncode, 1)
        self.assertIn('Invalid JSON', result.stderr)


class TestPerformance(unittest.TestCase):
    """Performance tests with larger datasets"""
    
    def test_large_array(self):
        data = {"items": [{"id": i, "value": f"item{i}"} for i in range(1000)]}
        result = get_value(data, ["items", slice(None), "id"])
        self.assertEqual(len(result), 1000)
    
    def test_deep_nesting(self):
        # Create deeply nested structure
        data = {"level0": {"level1": {"level2": {"level3": {"level4": "value"}}}}}
        result = get_value(data, ["level0", "level1", "level2", "level3", "level4"])
        self.assertEqual(result, "value")


if __name__ == '__main__':
    # Count test cases
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    print(f"Running {suite.countTestCases()} test cases...")
    print()
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print()
    print("=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    print("=" * 60)
    
    sys.exit(0 if result.wasSuccessful() else 1)
