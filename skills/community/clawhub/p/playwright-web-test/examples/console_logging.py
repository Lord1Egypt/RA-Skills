from playwright.sync_api import sync_playwright

url = 'http://localhost:5173'
console_logs = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1920, 'height': 1080})

    def handle_console_message(msg):
        log = f"[{msg.type}] {msg.text}"
        console_logs.append(log)
        print(f"控制台日志：{log}")

    page.on("console", handle_console_message)
    page.goto(url)
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(1000)
    browser.close()

log_path = '/tmp/console.log'
with open(log_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(console_logs))

print(f"日志已保存到：{log_path}")
