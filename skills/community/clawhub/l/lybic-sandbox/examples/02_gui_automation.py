"""
Example 2: GUI Automation - Click and Type

This example demonstrates:
1. Connecting to an existing sandbox
2. Taking a screenshot
3. Performing mouse clicks
4. Typing text with keyboard
5. Using hotkeys
"""

import asyncio
from lybic import LybicClient


async def main():
    sandbox_id = input("Enter your sandbox ID (e.g., SBX-xxxx): ").strip()
    
    async with LybicClient() as client:
        print(f"Connecting to sandbox {sandbox_id}...")
        
        # Verify sandbox exists
        try:
            sandbox_info = await client.sandbox.get(sandbox_id)
            print(f"✓ Connected to: {sandbox_info.name}")
        except Exception as e:
            print(f"❌ Error: {e}")
            return
        
        # Take initial screenshot
        print("\n📸 Taking screenshot...")
        url, image, _ = await client.sandbox.get_screenshot(sandbox_id)
        print(f"Screenshot URL: {url}")
        # Optionally display: image.show()
        
        # Click at screen center
        print("\n🖱️  Clicking at screen center...")
        await client.sandbox.execute_sandbox_action(
            sandbox_id,
            action={
                "type": "mouse:click",
                "x": {"type": "/", "numerator": 500, "denominator": 1000},
                "y": {"type": "/", "numerator": 500, "denominator": 1000},
                "button": 1  # Left click
            }
        )
        print("✓ Click executed")
        
        # Type some text
        print("\n⌨️  Typing text...")
        await client.sandbox.execute_sandbox_action(
            sandbox_id,
            action={
                "type": "keyboard:type",
                "content": "Hello from Lybic SDK!"
            }
        )
        print("✓ Text typed")
        
        # Press Enter
        print("\n↵ Pressing Enter...")
        await client.sandbox.execute_sandbox_action(
            sandbox_id,
            action={
                "type": "keyboard:hotkey",
                "keys": "Return"
            }
        )
        print("✓ Enter pressed")
        
        # Wait a moment
        print("\n⏳ Waiting 2 seconds...")
        await client.sandbox.execute_sandbox_action(
            sandbox_id,
            action={
                "type": "wait",
                "duration": 2000
            }
        )
        
        # Take final screenshot
        print("\n📸 Taking final screenshot...")
        url2, image2, _ = await client.sandbox.get_screenshot(sandbox_id)
        print(f"Screenshot URL: {url2}")
        
        print("\n✅ GUI automation completed!")


if __name__ == '__main__':
    asyncio.run(main())
