"""
Test script for Parenting Growth Partner handler
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from handler import ParentingGrowthPartner

def test_milestone_assessment():
    """Test milestone assessment functionality"""
    print('=== Test 1: Milestone Assessment ===')
    partner = ParentingGrowthPartner()
    
    # Test with 24-month-old
    result = partner.handle_milestone_assessment(24)
    assert result['success'] == True
    print(f'✓ 24-month assessment successful')
    print(f'  Development status: {result["assessment"]["summary"]["development_status"]}')
    print(f'  Milestones checked: {result["assessment"]["total_milestones_checked"]}')
    
    # Test with observations
    result = partner.handle_milestone_assessment(
        18,
        {'language': ['says mama', 'understands no'], 'gross-motor': ['walks well']}
    )
    assert result['success'] == True
    print(f'✓ 18-month assessment with observations successful')
    
    return True

def test_activity_recommendation():
    """Test activity recommendation functionality"""
    print('
=== Test 2: Activity Recommendation ===')
    partner = ParentingGrowthPartner()
    
    # Basic recommendation
    result = partner.handle_activity_recommendation(30, 20)
    assert result['success'] == True
    print(f'✓ Basic recommendation successful')
    print(f'  Activities available: {result["summary"]["total_available"]}')
    
    # With preferred domains
    result = partner.handle_activity_recommendation(
        36, 30, ['fine-motor', 'cognitive']
    )
    assert result['success'] == True
    print(f'✓ Recommendation with domains successful')
    
    return True

def test_communication_guidance():
    """Test communication guidance functionality"""
    print('
=== Test 3: Communication Guidance ===')
    partner = ParentingGrowthPartner()
    
    # Test tantrum scenario
    result = partner.handle_communication_guidance('tantrum', 24)
    assert result['success'] == True
    print(f'✓ Tantrum guidance successful')
    print(f'  Techniques available: {len(result["guidance"]["techniques"])}')
    
    # Test bedtime scenario
    result = partner.handle_communication_guidance('bedtime')
    assert result['success'] == True
    print(f'✓ Bedtime guidance successful')
    
    return True

def test_behavior_analysis():
    """Test behavior analysis functionality"""
    print('
=== Test 4: Behavior Analysis ===')
    partner = ParentingGrowthPartner()
    
    # Test power struggle behavior
    result = partner.handle_behavior_analysis(
        '经常说"不"，拖延',
        'frequent',
        '被要求做事时',
        30
    )
    assert result['success'] == True
    print(f'✓ Behavior analysis successful')
    print(f'  Possible patterns: {len(result["analysis"]["possible_patterns"])}')
    
    return True

def test_daily_routine():
    """Test daily routine functionality"""
    print('
=== Test 5: Daily Routine ===')
    partner = ParentingGrowthPartner()
    
    # Test for 24-month-old
    result = partner.handle_daily_routine_suggestion(24)
    assert result['success'] == True
    print(f'✓ Daily routine successful')
    print(f'  Bedtime suggestion: {result["suggested_routine"]["bedtime"]}')
    
    # Test for infant
    result = partner.handle_daily_routine_suggestion(6)
    assert result['success'] == True
    print(f'✓ Infant routine successful')
    
    return True

def run_all_tests():
    """Run all tests"""
    print('Running Parenting Growth Partner tests...')
    print('=' * 50)
    
    tests = [
        test_milestone_assessment,
        test_activity_recommendation,
        test_communication_guidance,
        test_behavior_analysis,
        test_daily_routine
    ]
    
    passed = 0
    failed = 0
    
    for test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f'✗ {test_func.__name__} failed: {e}')
            failed += 1
    
    print('
' + '=' * 50)
    print(f'Test Results: {passed} passed, {failed} failed')
    
    if failed == 0:
        print('✓ All tests passed!')
        return True
    else:
        print('✗ Some tests failed')
        return False

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
