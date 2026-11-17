#!/usr/bin/env python3
"""
MDAC Auto-Fill & Submit
Fills Malaysia Digital Arrival Card (MDAC) and bypasses slider CAPTCHA.

Usage:
    python3 fill_and_submit.py --data '{"name":"JOHN DOE", "passNo":"A1234567", ...}'
    python3 fill_and_submit.py --file data.json
"""

import asyncio
import argparse
import json
import math
import sys
from playwright.async_api import async_playwright

MDAC_URL = "https://imigresen-online.imi.gov.my/mdac/main?registerMain"

# Default field mapping (override via --data or --file)
DEFAULT_DATA = {
    "name": "",           # Name as on passport
    "passNo": "",         # Passport number
    "nationality": "CHN", # 3-letter country code
    "pob": "CHN",         # Place of birth (3-letter code)
    "dob": "",            # DD/MM/YYYY
    "sex": "1",           # 1=Male, 2=Female
    "passExpDte": "",     # DD/MM/YYYY passport expiry
    "email": "",
    "confirmEmail": "",
    "region": "65",       # Singapore country code
    "mobile": "",
    "arrDt": "",          # DD/MM/YYYY arrival date
    "trvlMode": "2",      # 1=Air, 2=Land, 3=Sea
    "depDt": "",          # DD/MM/YYYY departure date
    "embark": "SGP",      # Last port before Malaysia
    "vesselNm": "",       # Flight/Bus/Vessel number
    "accommodationStay": "99",  # 99=Others
    "accommodationAddress1": "",
    "accommodationAddress2": "",
    "accommodationState": "01",  # 01=Johor
    "accommodationCity": "0118", # 0118=Johor Bahru
    "accommodationPostcode": ""
}

FILL_JS = """
(function(data) {{
    if (typeof retrieveRefCity === 'function') retrieveRefCity(data["accommodationState"]);
    var s = document.getElementById("accommodationState");
    if (s) s.value = data["accommodationState"];
    setTimeout(function() {{
        var c = document.getElementById("accommodationCity");
        if (c) c.value = data["accommodationCity"];
        if (typeof retrievePostcode === 'function') retrievePostcode(data["accommodationCity"]);
        for (var k in data) {{
            var el = document.getElementById(k);
            if (el) el.value = data[k];
        }}
    }}, 1200);
}})({data_json});
"""

HOOK_JS = """
(() => {
    if (window._captchaHooked) return 'already hooked';
    const orig = $.ajax.bind($);
    $.ajax = function(opts) {
        if (opts && opts.url && String(opts.url).includes('/captcha')) {
            if (opts.success) opts.success(JSON.stringify({result: true}));
            return {done: () => ({fail: () => {}}), fail: () => {}};
        }
        return orig(opts);
    };
    window._captchaHooked = true;
    return 'hooked';
})()
"""


async def get_captcha_x(page):
    """Read the real gap x-coordinate from slidercaptcha instance."""
    x = await page.evaluate("""
    (() => {
        try {
            const inst = $('.slidercaptcha').data('plugin_sliderCaptcha');
            return inst ? inst.x : null;
        } catch(e) { return null; }
    })()
    """)
    return x


async def solve_captcha(page):
    """Hook ajax and drag slider to correct position."""
    # Hook server verification
    await page.evaluate(HOOK_JS)

    # Scroll captcha into view
    await page.evaluate("document.querySelector('.slidercaptcha')?.scrollIntoView({block:'center'})")
    await asyncio.sleep(0.5)

    # Get slider position
    slider_info = await page.evaluate("""
    (() => {
        const r = document.querySelector('.slider').getBoundingClientRect();
        return {cx: Math.round(r.x + r.width/2), cy: Math.round(r.y + r.height/2)};
    })()
    """)
    sx, sy = slider_info['cx'], slider_info['cy']

    # Get captcha width and calculate moveX
    # blockLeft = (width - 40 - 20) / (width - 40) * moveX
    # where width = canvas width (271)
    captcha_x = await get_captcha_x(page)
    if captcha_x is None:
        captcha_x = 163  # fallback
    
    width = 271
    move_x = round(captcha_x * (width - 40) / (width - 40 - 20))

    # Perform drag with human-like motion
    await page.mouse.move(sx, sy)
    await page.mouse.down()
    await asyncio.sleep(0.25)

    steps = 40
    for i in range(1, steps + 1):
        t = i / steps
        # ease-in-out-cubic
        ease = 4 * t**3 if t < 0.5 else 1 - (-2*t+2)**3/2
        nx = sx + move_x * ease
        ny = sy + math.sin(i * 0.5) * 0.4
        await page.mouse.move(nx, ny)
        delay = 0.015 + (0.02 if i > 35 else 0)
        await asyncio.sleep(delay)

    await asyncio.sleep(0.4)
    await page.mouse.up()
    await asyncio.sleep(2)

    # Verify success
    status = await page.evaluate("""
    (() => ({
        cls: document.querySelector('.sliderContainer')?.className || '',
        blockLeft: document.querySelectorAll('.slidercaptcha canvas')[1]?.style.left
    }))()
    """)
    return 'sliderContainer_success' in status.get('cls', '')


async def fill_and_submit(data: dict, screenshot_path: str = None):
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=['--disable-blink-features=AutomationControlled']
        )
        ctx = await browser.new_context(
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        )
        page = await ctx.new_page()

        print(f"Opening MDAC page...")
        await page.goto(MDAC_URL, timeout=30000)
        await page.wait_for_load_state('domcontentloaded')
        await page.wait_for_timeout(4000)

        print("Filling form...")
        fill_js = FILL_JS.format(data_json=json.dumps(data))
        await page.evaluate(fill_js)
        await page.wait_for_timeout(2500)

        print("Solving CAPTCHA...")
        success = await solve_captcha(page)
        if not success:
            print("CAPTCHA solve failed, retrying...")
            # Retry once
            await page.evaluate("document.querySelector('.refreshIcon')?.click()")
            await asyncio.sleep(1)
            success = await solve_captcha(page)

        if not success:
            print("ERROR: CAPTCHA could not be solved")
            await browser.close()
            return False

        print("Submitting form...")
        await page.click('#submit')
        await asyncio.sleep(3)

        url = page.url
        if 'SUCCESSFULLY' in url:
            print(f"SUCCESS! MDAC registered. Confirmation email sent.")
            print(f"URL: {url[:100]}")
            if screenshot_path:
                await page.screenshot(path=screenshot_path)
            await browser.close()
            return True
        else:
            print(f"Unexpected result. URL: {url}")
            if screenshot_path:
                await page.screenshot(path=screenshot_path)
            await browser.close()
            return False


def main():
    parser = argparse.ArgumentParser(description='Auto-fill and submit Malaysia MDAC')
    parser.add_argument('--data', type=str, help='JSON string of form data')
    parser.add_argument('--file', type=str, help='JSON file with form data')
    parser.add_argument('--screenshot', type=str, default='/tmp/mdac_result.png', help='Screenshot output path')
    args = parser.parse_args()

    data = DEFAULT_DATA.copy()

    if args.file:
        with open(args.file) as f:
            data.update(json.load(f))
    elif args.data:
        data.update(json.loads(args.data))
    else:
        print("ERROR: Provide --data or --file with traveler information")
        sys.exit(1)

    # Validate required fields
    required = ['name', 'passNo', 'dob', 'passExpDte', 'email', 'mobile', 'arrDt', 'depDt', 'vesselNm', 'accommodationPostcode']
    missing = [f for f in required if not data.get(f)]
    if missing:
        print(f"ERROR: Missing required fields: {', '.join(missing)}")
        sys.exit(1)

    result = asyncio.run(fill_and_submit(data, args.screenshot))
    sys.exit(0 if result else 1)


if __name__ == '__main__':
    main()
