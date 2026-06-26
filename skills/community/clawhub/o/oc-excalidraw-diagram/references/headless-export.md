# Headless Export: Excalidraw → PNG

Export `.excalidraw` files to PNG using Playwright (headless Chromium).

## Prerequisites

```bash
pip install playwright
playwright install chromium
```

## Script

```python
from playwright.sync_api import sync_playwright
import json, time

def export_excalidraw_to_png(excalidraw_path, output_png_path):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        page = browser.new_page(viewport={"width": 1400, "height": 900})

        with open(excalidraw_path, "r") as f:
            content = f.read()

        page.goto("https://excalidraw.com", wait_until="networkidle", timeout=30000)
        time.sleep(5)

        # Drop file to import
        page.evaluate("""
            (jsonContent) => {
                const blob = new Blob([jsonContent], {type: 'application/json'});
                const file = new File([blob], 'diagram.excalidraw', {type: 'application/json'});
                const dt = new DataTransfer();
                dt.items.add(file);
                const target = document.querySelector('canvas').parentElement;
                target.dispatchEvent(new DragEvent('dragenter', {dataTransfer: dt, bubbles: true}));
                target.dispatchEvent(new DragEvent('dragover', {dataTransfer: dt, bubbles: true}));
                target.dispatchEvent(new DragEvent('drop', {dataTransfer: dt, bubbles: true}));
            }
        """, content)
        time.sleep(8)

        # Hide UI elements
        page.evaluate("""
            document.querySelectorAll('[class*="layer-ui"], [class*="App-menu"], [class*="sidebar"], [class*="toolbar"], [class*="HintViewer"], [class*="welcome"], [class*="WelcomeScreen"]').forEach(el => el.style.display = 'none');
        """)
        time.sleep(1)

        page.screenshot(path=output_png_path, full_page=False)
        browser.close()

# Usage
if __name__ == "__main__":
    export_excalidraw_to_png("diagram.excalidraw", "diagram.png")
    print("Exported to diagram.png")
```

## Key Notes

1. **Linux requires `--no-sandbox`** — AppImage/sandbox restrictions apply
2. **Shapes MUST have overlay text elements** (see SKILL.md Step 3.5) — embedded text in shapes does NOT render during headless export; standalone `text` elements DO render correctly
3. **wait times matter** — `time.sleep(5)` after page load, `time.sleep(8)` after file drop; reduce if network is fast, increase if export is incomplete
4. **requires network** — loads excalidraw.com; not suitable for fully offline environments

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Text not visible in PNG | Add overlay `text` elements per Step 3.5 |
| Canvas not found | Increase sleep after `page.goto` |
| Blank screenshot | Increase sleep after file drop |
| Chromium not found | Run `playwright install chromium` |
| Linux sandbox error | Ensure `--no-sandbox` arg is present |
