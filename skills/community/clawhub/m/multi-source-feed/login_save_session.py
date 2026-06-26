from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # Connect to the user's already-open Chrome via CDP
    browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    context = browser.contexts[0]

    # Save the login session/cookies to a file
    context.storage_state(path="x_session.json")
    print("Login session saved to x_session.json")

    browser.close()
