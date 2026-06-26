import { chromium } from 'playwright';

(async () => {
    const browser = await chromium.launch();
    const page = await browser.newPage({ viewport: { width: 1200, height: 800 } });

    // Main view
    await page.goto('http://localhost:5173/');
    await new Promise(r => setTimeout(r, 2000)); // let calendar render
    await page.screenshot({ path: 'public/screenshots/main-view.png' });

    // Click stats button
    await page.click('button[title="📊 Stats"]');
    await new Promise(r => setTimeout(r, 1000)); // let stats render and animate
    await page.screenshot({ path: 'public/screenshots/stats-view.png' });

    await browser.close();
})();
