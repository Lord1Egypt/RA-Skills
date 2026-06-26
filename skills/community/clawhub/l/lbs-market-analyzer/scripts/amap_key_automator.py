import asyncio
import os
from playwright.async_api import async_playwright

# Configuration
USER_DATA_DIR = "./amap_session"  # Directory to save login state
AMAP_CONSOLE_URL = "https://console.amap.com/dev/key/app"

async def automate_amap_key():
    async with async_playwright() as p:
        # Launch browser with persistent context to keep you logged in
        context = await p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=False,  # Set to True once login is stable
            args=["--start-maximized"]
        )
        
        page = await context.new_page()
        print(f"Navigating to {AMAP_CONSOLE_URL}...")
        try:
            # timeout=0 means wait indefinitely
            await page.goto(AMAP_CONSOLE_URL, wait_until="domcontentloaded", timeout=0)
        except Exception as e:
            print(f"Navigation warning: {e}")

        # Step 1: Wait for Dashboard or Login/Verification
        print("Waiting for dashboard to load (handling potential logins or verifications)...")
        while True:
            # Check for the dashboard button which indicates we are in
            if await page.locator("text='创建新应用'").count() > 0:
                # Ensure the button is actually visible (not hidden by an overlay)
                if await page.locator("text='创建新应用'").first.is_visible():
                    print("Dashboard loaded.")
                    break
            
            # Detect Login or Verification keywords
            # Added "验证" (Verification) to the detection list
            url = page.url.lower()
            content = await page.content()
            
            if "/user/permission" in url or "/user/info" in url or "?from=" in url:
                print("Landed on user settings/permission page. Navigating to My Applications...")
                try:
                    my_app_menu = page.locator("text='我的应用'").first
                    if not await my_app_menu.is_visible():
                        manage_menu = page.locator("text='应用管理'").first
                        if await manage_menu.is_visible():
                            await manage_menu.click()
                            await page.wait_for_timeout(1000)
                    
                    if await my_app_menu.is_visible():
                        await my_app_menu.click()
                    else:
                        await page.goto(AMAP_CONSOLE_URL)
                except Exception as e:
                    print(f"Fallback to direct navigation: {e}")
                    await page.goto(AMAP_CONSOLE_URL)
            elif "login" in url or "passport" in url or "验证" in content or "登录" in content:
                print("Action Required: Please complete the Login or Verification process in the browser...")
            
            await page.wait_for_timeout(3000)

        # Step 2: Create Application (if force new)
        create_app_btn = page.locator("text='创建新应用'").first
        print("Creating a new application...")
        await create_app_btn.click()
            
        # Wait a moment for the dialog animation to complete
        await page.wait_for_timeout(2000)
        
        try:
            # Based on the user's HTML, the input has id="productName"
            input_locator = page.locator("input#productName")
            await input_locator.fill("lbs-ca", timeout=5000)
            print("Successfully filled application name.")
        except Exception as e:
            print(f"Failed to find or fill the input field: {e}")

        # Select an industry type (often required, id="industryId")
        try:
            await page.locator("#industryId").click(timeout=3000)
            await page.wait_for_timeout(500)
            # ant-design typically renders select options in a global dropdown
            await page.locator(".ant-select-dropdown-menu-item").first.click(timeout=3000)
            print("Selected an industry type.")
        except Exception:
            pass # Ignore if it works without it

        try:
            # The submit button seems to have text like '新 建' and class 'ant-btn-primary'
            await page.locator(".ant-modal-footer .ant-btn-primary").click(timeout=3000)
            print("Clicked confirm button.")
        except Exception as e:
            print(f"Failed to click confirm button: {e}")
        
        await page.wait_for_timeout(2000)

        # Step 3: Add Key to the App
        print("Adding a new Web Service Key...")
        try:
            # The page might reload or take time to show the new app, so wait longer (15s)
            add_key_btn = page.locator("button:has-text('添加Key')").first
            await add_key_btn.click(timeout=15000)
            await page.wait_for_timeout(1000)
            
            # Fill Key Name
            await page.locator("input#keyName").fill("lbs-ca-key", timeout=5000)
            
            # Select 'Web服务' (Crucial for LBS API)
            await page.locator("label:has-text('Web服务')").click()
            
            # Check the terms checkbox
            await page.locator("input#agreement").check()
                
            # Submit
            await page.locator(".aesFormKeyCreate .ant-modal-footer .ant-btn-primary").click()
            print("Key creation submitted.")
        except Exception as e:
            print(f"Failed to create the Key: {e}")

        # Step 4: Extract the Key
        await page.wait_for_timeout(3000)
        try:
            # Locate the key by finding the row with our key name
            row_locator = page.locator("tr", has=page.locator("text='lbs-ca-key'")).first
            # The key is in the second td of that row
            key_value = await row_locator.locator("td").nth(1).inner_text()
            key_value = key_value.strip()
            
            print(f"Success: Extracted AMAP Key: {key_value}")
            
            # Save to .env (Project Root)
            script_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(script_dir)
            env_path = os.path.join(project_root, ".env")
            with open(env_path, "a", encoding="utf-8") as f:
                f.write(f"\nAMAP_KEY={key_value}\n")
            print(f"Saved key to {env_path}")
            
        except Exception as e:
            print(f"Could not automatically extract key string: {e}")

        await asyncio.sleep(5) # Let user see the result
        await context.close()

if __name__ == "__main__":
    if not os.path.exists(USER_DATA_DIR):
        os.makedirs(USER_DATA_DIR)
    
    print("Starting AMAP Key Automator...")
    asyncio.run(automate_amap_key())