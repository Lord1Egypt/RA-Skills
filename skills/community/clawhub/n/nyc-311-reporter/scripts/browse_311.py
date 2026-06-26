#!/usr/bin/env python3
"""Browse NYC 311 portal and submit complaints using Playwright."""

import asyncio
import json
import sys
from playwright.async_api import async_playwright


async def scrape_categories():
    """Scrape all complaint categories from 311 portal."""
    categories = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            await page.goto('https://portal.311.nyc.gov/', wait_until='networkidle')
            await page.wait_for_timeout(2000)
            
            # Find all links that might be complaint categories
            links = await page.query_selector_all('a')
            
            for link in links:
                href = await link.get_attribute('href')
                text = await link.inner_text()
                
                if text and len(text.strip()) > 2:
                    text_clean = text.strip()
                    # Filter for complaint/report related links
                    if any(keyword in text_clean.lower() for keyword in ['complaint', 'report', 'request', 'parking', 'hydrant', 'illegal']):
                        url = href if href and href.startswith('http') else f"https://portal.311.nyc.gov{href}"
                        categories.append({
                            'name': text_clean,
                            'url': url,
                            'id': text_clean.lower().replace(' ', '-')[:50]
                        })
            
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
        finally:
            await browser.close()
    
    return categories


async def find_fire_hydrant_form():
    """Find the fire hydrant complaint form."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            # Start at main page
            await page.goto('https://portal.311.nyc.gov/', wait_until='networkidle')
            await page.wait_for_timeout(2000)
            
            # Look for Illegal Parking or Fire Hydrant links
            links = await page.query_selector_all('a')
            
            target_url = None
            for link in links:
                text = await link.inner_text()
                href = await link.get_attribute('href')
                
                if text and ('fire hydrant' in text.lower() or 'illegal parking' in text.lower()):
                    target_url = href if href and href.startswith('http') else f"https://portal.311.nyc.gov{href}"
                    break
            
            if not target_url:
                # Try direct URL
                target_url = 'https://portal.311.nyc.gov/report-problems/'
            
            return {'url': target_url, 'found': target_url is not None}
            
        except Exception as e:
            return {'error': str(e)}
        finally:
            await browser.close()


async def fill_fire_hydrant_complaint(location, vehicle, duration, reporter_name, reporter_email, reporter_phone, dry_run=True):
    """Fill and optionally submit fire hydrant complaint."""
    
    result = {
        'status': 'pending',
        'dry_run': dry_run,
        'fields_filled': [],
        'errors': []
    }
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            # Navigate to 311 portal
            await page.goto('https://portal.311.nyc.gov/', wait_until='networkidle')
            await page.wait_for_timeout(2000)
            
            # Look for and click on Illegal Parking or Report Problems
            links = await page.query_selector_all('a')
            report_link = None
            
            for link in links:
                text = await link.inner_text()
                if text and ('illegal parking' in text.lower() or 'report problems' in text.lower()):
                    report_link = link
                    break
            
            if report_link:
                await report_link.click()
                await page.wait_for_load_state('networkidle')
                await page.wait_for_timeout(2000)
            
            # Take screenshot of current state
            await page.screenshot(path='/tmp/311_step1.png')
            result['screenshot_1'] = '/tmp/311_step1.png'
            
            # Look for fire hydrant specific option
            page_text = await page.content()
            
            if 'fire hydrant' in page_text.lower():
                # Try to find and click fire hydrant option
                hydrant_links = await page.query_selector_all('a, button')
                for elem in hydrant_links:
                    text = await elem.inner_text()
                    if text and 'fire hydrant' in text.lower():
                        await elem.click()
                        await page.wait_for_load_state('networkidle')
                        break
            
            # Check if we're on a form
            form_fields = await page.query_selector_all('input, textarea, select')
            
            if len(form_fields) > 0:
                result['form_found'] = True
                result['field_count'] = len(form_fields)
                
                # Try to fill fields based on common patterns
                for field in form_fields:
                    try:
                        name = await field.get_attribute('name') or await field.get_attribute('id') or ''
                        field_type = await field.get_attribute('type') or 'text'
                        
                        if any(x in name.lower() for x in ['location', 'address', 'street']):
                            await field.fill(location)
                            result['fields_filled'].append('location')
                        elif any(x in name.lower() for x in ['vehicle', 'car', 'description']):
                            await field.fill(f"{vehicle} blocking fire hydrant")
                            result['fields_filled'].append('vehicle_description')
                        elif any(x in name.lower() for x in ['duration', 'time', 'how long']):
                            await field.fill(duration)
                            result['fields_filled'].append('duration')
                        elif any(x in name.lower() for x in ['name', 'reporter']):
                            await field.fill(reporter_name)
                            result['fields_filled'].append('reporter_name')
                        elif any(x in name.lower() for x in ['email']):
                            await field.fill(reporter_email)
                            result['fields_filled'].append('reporter_email')
                        elif any(x in name.lower() for x in ['phone', 'tel']):
                            await field.fill(reporter_phone)
                            result['fields_filled'].append('reporter_phone')
                            
                    except Exception as e:
                        result['errors'].append(f"Field fill error: {str(e)}")
                
                # Take screenshot of filled form
                await page.screenshot(path='/tmp/311_filled.png')
                result['screenshot_filled'] = '/tmp/311_filled.png'
                
                if not dry_run:
                    # Look for submit button
                    submit_btn = await page.query_selector('button[type="submit"], input[type="submit"], button:has-text("Submit")')
                    if submit_btn:
                        await submit_btn.click()
                        await page.wait_for_load_state('networkidle')
                        await page.wait_for_timeout(3000)
                        
                        await page.screenshot(path='/tmp/311_submitted.png')
                        result['screenshot_submitted'] = '/tmp/311_submitted.png'
                        result['status'] = 'submitted'
                        
                        # Try to extract confirmation
                        content = await page.content()
                        if 'confirmation' in content.lower() or 'submitted' in content.lower():
                            result['confirmation'] = True
                    else:
                        result['status'] = 'error'
                        result['error'] = 'Submit button not found'
                else:
                    result['status'] = 'dry_run_complete'
                    result['message'] = 'Form filled successfully. Review screenshot and run with --submit to actually submit.'
            else:
                result['form_found'] = False
                result['status'] = 'error'
                result['error'] = 'No form found on page'
                
        except Exception as e:
            result['status'] = 'error'
            result['error'] = str(e)
        finally:
            await browser.close()
    
    return result


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='NYC 311 Browser Automation')
    parser.add_argument('command', choices=['scrape', 'find', 'submit'])
    parser.add_argument('--location', default='726 DeKalb Avenue, Brooklyn, NY')
    parser.add_argument('--vehicle', default='Gray Nissan Micra')
    parser.add_argument('--duration', default='10 hours')
    parser.add_argument('--name', default='Ricardo Díaz')
    parser.add_argument('--email', default='ricardo@example.com')
    parser.add_argument('--phone', default='+19299990000')
    parser.add_argument('--submit', action='store_true', help='Actually submit the form')
    
    args = parser.parse_args()
    
    if args.command == 'scrape':
        categories = asyncio.run(scrape_categories())
        print(json.dumps(categories, indent=2))
    
    elif args.command == 'find':
        result = asyncio.run(find_fire_hydrant_form())
        print(json.dumps(result, indent=2))
    
    elif args.command == 'submit':
        result = asyncio.run(fill_fire_hydrant_complaint(
            location=args.location,
            vehicle=args.vehicle,
            duration=args.duration,
            reporter_name=args.name,
            reporter_email=args.email,
            reporter_phone=args.phone,
            dry_run=not args.submit
        ))
        print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
