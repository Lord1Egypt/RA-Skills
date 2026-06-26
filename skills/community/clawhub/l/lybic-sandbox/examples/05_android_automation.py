"""
Example 5: Android Mobile Automation

This example demonstrates:
1. Connecting to an Android sandbox
2. Using touch gestures
3. Managing Android apps
4. Navigating with system buttons
"""

import asyncio
from lybic import LybicClient


async def main():
    sandbox_id = input("Enter your Android sandbox ID (e.g., SBX-xxxx): ").strip()
    
    async with LybicClient() as client:
        print(f"Connecting to Android sandbox {sandbox_id}...")
        
        # Verify sandbox
        try:
            sandbox_info = await client.sandbox.get(sandbox_id)
            print(f"✓ Connected to: {sandbox_info.name}")
        except Exception as e:
            print(f"❌ Error: {e}")
            return
        
        # Take initial screenshot
        print("\n📸 Taking screenshot...")
        url, _, _ = await client.sandbox.get_screenshot(sandbox_id)
        print(f"Screenshot: {url}")
        
        # List installed apps
        print("\n📱 Listing installed apps...")
        try:
            result = await client.sandbox.execute_sandbox_action(
                sandbox_id,
                action={"type": "os:listApps"}
            )
            print("✓ Apps listed (check actionResult for details)")
        except Exception as e:
            print(f"⚠️ Could not list apps: {e}")
        
        # Tap at screen center
        print("\n👆 Tapping at screen center...")
        await client.sandbox.execute_sandbox_action(
            sandbox_id,
            action={
                "type": "touch:tap",
                "x": {"type": "/", "numerator": 500, "denominator": 1000},
                "y": {"type": "/", "numerator": 500, "denominator": 1000}
            }
        )
        print("✓ Tap executed")
        
        # Swipe up (like scrolling)
        print("\n👆 Swiping up...")
        await client.sandbox.execute_sandbox_action(
            sandbox_id,
            action={
                "type": "touch:swipe",
                "x": {"type": "/", "numerator": 500, "denominator": 1000},
                "y": {"type": "/", "numerator": 750, "denominator": 1000},
                "direction": "up",
                "distance": {"type": "px", "value": 300}
            }
        )
        print("✓ Swipe executed")
        
        # Type text (for input fields)
        print("\n⌨️  Typing text...")
        await client.sandbox.execute_sandbox_action(
            sandbox_id,
            action={
                "type": "keyboard:type",
                "content": "Hello from Lybic!"
            }
        )
        print("✓ Text typed")
        
        # Press Android back button
        print("\n◀️  Pressing back button...")
        await client.sandbox.execute_sandbox_action(
            sandbox_id,
            action={"type": "android:back"}
        )
        print("✓ Back pressed")
        
        # Press home button
        print("\n🏠 Pressing home button...")
        await client.sandbox.execute_sandbox_action(
            sandbox_id,
            action={"type": "android:home"}
        )
        print("✓ Home pressed")
        
        # Example: Start Chrome browser
        start_app = input("\nStart Chrome browser? (y/n): ").strip().lower()
        if start_app == 'y':
            print("\n🌐 Starting Chrome...")
            try:
                await client.sandbox.execute_sandbox_action(
                    sandbox_id,
                    action={
                        "type": "os:startApp",
                        "packageName": "com.android.chrome"
                    }
                )
                print("✓ Chrome started")
                
                # Wait and take screenshot
                await asyncio.sleep(3)
                print("\n📸 Taking final screenshot...")
                url2, _, _ = await client.sandbox.get_screenshot(sandbox_id)
                print(f"Screenshot: {url2}")
            except Exception as e:
                print(f"❌ Error starting Chrome: {e}")
        
        print("\n✅ Android automation completed!")


if __name__ == '__main__':
    asyncio.run(main())
