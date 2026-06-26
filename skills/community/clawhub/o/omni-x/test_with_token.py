"""
Test TwitterSkillInterface with auth_token parameter
Demonstrates the three ways to provide authentication
"""

from scripts import TwitterSkillInterface

# Replace with your actual auth_token
AUTH_TOKEN = "your_auth_token_here"

print("Testing TwitterSkillInterface with auth_token support")
print("=" * 70)

# Method 1: Initialize with auth_token (RECOMMENDED for AI Agents)
print("\n[Method 1] Initialize with auth_token in constructor")
print("-" * 70)
try:
    interface1 = TwitterSkillInterface(auth_token=AUTH_TOKEN)
    print("✓ Interface created with auth_token")
    
    # Test a skill that requires authentication
    result = interface1.execute_skill(
        skill_name="get_user_tweets",
        parameters={"username": "elonmusk", "count": 3}
    )
    
    if result["success"]:
        print(f"✓ Successfully retrieved {result.get('count', 0)} tweets")
    else:
        print(f"✗ Error: {result.get('error')}")
except Exception as e:
    print(f"✗ Failed: {e}")

# Method 2: Initialize without token, then set it
print("\n[Method 2] Set auth_token after initialization")
print("-" * 70)
try:
    interface2 = TwitterSkillInterface()
    print("✓ Interface created without auth_token")
    
    # Set auth_token later
    auth_result = interface2.set_auth_token(AUTH_TOKEN)
    if auth_result["success"]:
        print("✓ Auth token set successfully")
    else:
        print(f"✗ Auth failed: {auth_result.get('error')}")
    
    # Test a skill
    result = interface2.execute_skill(
        skill_name="get_user_profile",
        parameters={"username": "elonmusk"}
    )
    
    if result["success"]:
        print(f"✓ Successfully retrieved user profile")
    else:
        print(f"✗ Error: {result.get('error')}")
except Exception as e:
    print(f"✗ Failed: {e}")

# Method 3: Guest session (no auth_token)
print("\n[Method 3] Guest session (no auth_token)")
print("-" * 70)
try:
    interface3 = TwitterSkillInterface()
    print("✓ Interface created with guest session")
    
    # Test a skill that works without authentication
    result = interface3.execute_skill(
        skill_name="get_user_tweets",
        parameters={"username": "elonmusk", "count": 3}
    )
    
    if result["success"]:
        print(f"✓ Successfully retrieved {result.get('count', 0)} tweets (guest session)")
    else:
        print(f"✗ Error: {result.get('error')}")
        print("   Note: Some features require authentication")
except Exception as e:
    print(f"✗ Failed: {e}")

print("\n" + "=" * 70)
print("Test complete!")
print("\nRecommendation for AI Agents:")
print("  Use Method 1: TwitterSkillInterface(auth_token='your_token')")
print("  This provides immediate access to all features.")
