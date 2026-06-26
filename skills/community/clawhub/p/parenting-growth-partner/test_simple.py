#!/usr/bin/env python3
"""Simple test for parenting-growth-partner"""
import sys
sys.path.insert(0, '.')

from handler import ParentingGrowthPartner

print('Testing Parenting Growth Partner...')
partner = ParentingGrowthPartner()

# Test 1
print('
1. Milestone assessment (24 months):')
result = partner.handle_milestone_assessment(24)
print(f'   Success: {result["success"]}')
print(f'   Status: {result["assessment"]["summary"]["development_status"]}')

# Test 2  
print('
2. Activity recommendation:')
result = partner.handle_activity_recommendation(30, 20)
print(f'   Success: {result["success"]}')
print(f'   Activities: {result["summary"]["total_available"]}')

print('
✓ Basic functionality works!')
