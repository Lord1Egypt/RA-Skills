"""
Example of how AI agents can use the Twitter Skills Interface
"""

from scripts import TwitterSkillInterface
import json


def main():
    # Initialize the skill interface
    interface = TwitterSkillInterface()
    
    print("=== AI Agent Twitter Skills Demo ===\n")
    
    # 1. Discover available skills
    print("1. Discovering available skills...")
    skills = interface.get_available_skills()
    print(f"   Found {len(skills)} skills:\n")
    for skill_name, skill_info in skills.items():
        print(f"   - {skill_name}: {skill_info['description']}")
    print()
    
    # 2. Execute skills using the standardized interface
    print("2. Executing skills via interface...\n")
    
    # Example 1: Get user profile
    print("   a) Getting user profile...")
    result = interface.execute_skill(
        skill_name="get_user_profile",
        parameters={"username": "elonmusk"}
    )
    print(f"      Status: {'✓ Success' if result['success'] else '✗ Failed'}")
    if result['success']:
        print(f"      Skill: {result['skill_name']}")
        print(f"      Parameters: {result['parameters']}")
    print()
    
    # Example 2: Get user tweets
    print("   b) Getting user tweets...")
    result = interface.execute_skill(
        skill_name="get_user_tweets",
        parameters={"username": "elonmusk", "count": 5}
    )
    print(f"      Status: {'✓ Success' if result['success'] else '✗ Failed'}")
    if result['success']:
        print(f"      Retrieved: {result.get('count', 0)} tweets")
    print()
    
    # Example 3: Search tweets
    print("   c) Searching tweets...")
    result = interface.execute_skill(
        skill_name="search_tweets",
        parameters={"query": "AI technology", "count": 3}
    )
    print(f"      Status: {'✓ Success' if result['success'] else '✗ Failed'}")
    if result['success']:
        print(f"      Found: {result.get('count', 0)} tweets")
    print()
    
    # 3. Demonstrate error handling
    print("3. Testing error handling...")
    result = interface.execute_skill(
        skill_name="invalid_skill",
        parameters={}
    )
    print(f"   Status: {'✓ Success' if result['success'] else '✗ Failed (as expected)'}")
    if not result['success']:
        print(f"   Error: {result['error']}")
        print(f"   Available skills: {', '.join(result['available_skills'])}")
    print()
    
    print("=== Demo Complete ===")
    print("\nThis interface allows AI agents to:")
    print("- Discover available skills dynamically")
    print("- Execute skills with standardized parameters")
    print("- Receive structured responses with metadata")
    print("- Handle errors gracefully")


if __name__ == "__main__":
    main()
