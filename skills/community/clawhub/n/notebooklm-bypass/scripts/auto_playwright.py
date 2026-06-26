from playwright.sync_api import sync_playwright
import json
import os
import subprocess
import sys

def main():
    # Automatically get the user's home directory so this works on ANY computer
    user_home = os.path.expanduser("~")
    profile_dir = os.path.join(user_home, ".notebooklm", "browser_profile")
    state_path = os.path.join(user_home, ".notebooklm", "storage_state.json")
    payload_path = os.path.join(user_home, ".notebooklm", "auth_payload.json")
    
    print("1. Launching Playwright with NotebookLM persistent profile...")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch_persistent_context(
                user_data_dir=profile_dir,
                headless=False,
            )
            
            page = browser.pages[0]
            print("2. Navigating to NotebookLM...")
            page.goto("https://notebooklm.google.com/", wait_until="networkidle")
            
            print("3. Waiting 5 seconds to ensure cookies are refreshed...")
            page.wait_for_timeout(5000)
            
            print("4. Extracting cookies...")
            state = browser.storage_state()
            
            # Format SameSite exactly as expected by the CLI API
            for c in state.get("cookies", []):
                samesite = str(c.get("sameSite", "Lax")).capitalize()
                if samesite == "None":
                    samesite = "None"
                c["sameSite"] = samesite
                
            print(f"5. Found {len(state.get('cookies', []))} cookies. Saving to disk...")
            
            # Ensure the .notebooklm folder exists
            os.makedirs(os.path.dirname(state_path), exist_ok=True)
            
            with open(state_path, "w") as f:
                json.dump(state, f)
                
            env_json = json.dumps({"cookies": state.get("cookies", [])})
            with open(payload_path, "w") as f:
                f.write(env_json)
                
            print(f"Saved auth payload to {payload_path}")
            
            # Automatically apply to Windows User Environment Variable to bypass the Playwright browser lock bug
            if sys.platform == "win32":
                print("Injecting cookies into Windows Environment Variable NOTEBOOKLM_AUTH_JSON...")
                subprocess.run([
                    "powershell", "-Command", 
                    f'[Environment]::SetEnvironmentVariable("NOTEBOOKLM_AUTH_JSON", \'{env_json}\', "User")'
                ], check=True)
            else:
                print("Non-Windows OS detected. To complete bypass, manually export NOTEBOOKLM_AUTH_JSON using the contents of auth_payload.json")
                
            browser.close()
            print("6. Done! Cookies successfully extracted and applied.")
            
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Playwright error: {e}")

if __name__ == "__main__":
    main()
