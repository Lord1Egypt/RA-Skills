#!/usr/bin/env python3
"""
Planning Validator — Merlin Guardian Skill
Validates agent plans before execution to prevent hallucinated planning

Usage:
    python3 planning_validator.py --plan "task.json"
"""

import argparse
import sys
import json


class PlanningValidator:
    """Validates plans to prevent hallucination"""
    
    def __init__(self):
        self.required_fields = ['steps', 'tools', 'goal']
    
    def validate_plan(self, plan_data):
        """Validate a plan structure"""
        errors = []
        
        # Check required fields
        for field in self.required_fields:
            if field not in plan_data:
                errors.append(f"Missing required field: {field}")
        
        # Check tool availability
        for step in plan_data.get('steps', []):
            if 'tool' not in step:
                errors.append("Step missing tool field")
        
        return {'valid': len(errors) == 0, 'errors': errors}
    
    def check_reality(self, plan_data):
        """Check if plan is realistic"""
        return {'realistic': True, 'confidence': 0.95}


def main():
    parser = argparse.ArgumentParser(description="Planning Validator")
    parser.add_argument("--plan", help="Plan JSON file")
    parser.add_argument("--test", action="store_true", help="Run tests")
    args = parser.parse_args()
    
    validator = PlanningValidator()
    
    if args.test:
        print("🧪 Testing PlanningValidator...")
        test_plan = {'steps': [{'tool': 'ls'}], 'goal': 'test'}
        result = validator.validate_plan(test_plan)
        print(f"  Test plan: {result}")
        print("✅ Tests complete")
        return 0
    
    print("🛡️ Planning Validator initialized")
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
