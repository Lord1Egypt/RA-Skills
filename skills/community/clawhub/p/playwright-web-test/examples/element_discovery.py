from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    url = 'http://localhost:5173'
    page.goto(url)
    page.wait_for_load_state('networkidle')

    buttons = page.locator('button').all()
    print(f"共发现 {len(buttons)} 个按钮")
    for i, button in enumerate(buttons):
        try:
            text = button.inner_text().strip() if button.is_visible() else '[隐藏]'
        except Exception:
            text = '[无法获取]'
        print(f"[{i}] {text}")

    browser.close()
