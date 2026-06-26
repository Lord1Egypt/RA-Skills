from playwright.sync_api import sync_playwright
import os

html_file_path = os.path.abspath('path/to/your/file.html')
file_url = f'file://{html_file_path}'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1920, 'height': 1080})
    page.goto(file_url)
    page.screenshot(path='/tmp/static_page.png', full_page=True)
    browser.close()

print('本地 HTML 自动化执行完成！')
