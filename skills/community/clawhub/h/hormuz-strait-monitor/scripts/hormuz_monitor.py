#!/usr/bin/env python3
"""
Hormuz Strait Monitor - Track transit data from multiple sources

This script collects shipping transit data from:
1. hormuzstraitmonitor.com - Transits (24h) and Daily Throughput
2. shipxy.com - Non-Iranian vessels exiting the strait

Requires: selenium, webdriver-manager
Install: pip install selenium webdriver-manager

Usage:
    python hormuz_monitor.py [--config CONFIG_PATH] [--channel CHANNEL]
"""

import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List
import argparse
import subprocess

# Selenium imports
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from webdriver_manager.chrome import ChromeDriverManager
except ImportError:
    print("ERROR: selenium and webdriver-manager not installed")
    print("Install: pip install selenium webdriver-manager")
    sys.exit(1)

# Default paths
DEFAULT_DATA_FILE = Path.home() / ".openclaw" / "workspace" / "memory" / "hormuz-transit-data.csv"
DEFAULT_CONFIG_FILE = Path.home() / ".openclaw" / "workspace" / "skills" / "hormuz-strait-monitor" / "references" / "config.json"

# Alert thresholds
THRESHOLDS = {
    "transits_recovery": 10,  # Transits >= 10 vessels
    "transits_percent": 0.20,  # Transits >= 20% of day normal
    "throughput_percent": 0.20,  # Daily Throughput >= 20% of avg
    "non_iranian_vessels": 10,  # Non-Iranian vessels >= 10
}


def setup_driver():
    """Setup Chrome WebDriver with headless options"""
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-notifications")
    options.add_argument("--lang=en-US")
    
    # Use installed Chrome
    options.binary_location = "/usr/bin/google-chrome"
    
    # Auto-download matching ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    return driver


def fetch_hormuzstraitmonitor(driver) -> Dict[str, Any]:
    """
    Fetch transit data from hormuzstraitmonitor.com
    
    Returns:
        dict with transits_24h, daily_throughput, day_normal, avg_throughput
    """
    url = "https://hormuzstraitmonitor.com/"
    driver.get(url)
    
    # Wait for page to load
    wait = WebDriverWait(driver, 30)
    
    result = {
        "transits_24h": None,
        "daily_throughput": None,
        "day_normal": None,
        "avg_throughput": None,
        "source": url,
        "fetched_at": datetime.now().isoformat(),
        "error": None
    }
    
    try:
        # Wait for content to render (JavaScript-heavy page)
        time.sleep(15)
        
        # Scroll to load all content
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        
        # Try to find transit count - multiple possible selectors
        # The page structure may vary, so we try different approaches
        
        # Method 1: Look for specific text patterns
        page_text = driver.page_source
        
        # Parse Transits (24h) - usually appears as "Transits (24h): X vessels"
        import re
        
        # Get page text content (not HTML source)
        visible_text = driver.find_element(By.TAG_NAME, "body").text
        
        # Split into lines for better parsing
        lines = visible_text.split('\n')
        
        # === Parse Daily Throughput ===
        # Format: "500.0K DWT" followed by "4.9% of 10.3M avg"
        for i, line in enumerate(lines):
            if 'DAILY THROUGHPUT' in line.upper():
                # Look at next few lines for the value
                for j in range(i+1, min(i+5, len(lines))):
                    next_line = lines[j].strip()
                    # Match "500.0K DWT" or similar
                    match = re.search(r'([\d.]+)([KM]?)\s*DWT', next_line, re.IGNORECASE)
                    if match:
                        value = float(match.group(1))
                        unit = match.group(2).upper() if match.group(2) else ''
                        if unit == 'K':
                            result['daily_throughput'] = value * 1000  # Convert to absolute
                        elif unit == 'M':
                            result['daily_throughput'] = value * 1000000
                        else:
                            result['daily_throughput'] = value
                        break
                    # Also try just number format
                    match2 = re.search(r'([\d.]+)[KM]\s', next_line)
                    if match2:
                        value = float(match2.group(1))
                        if 'K' in next_line:
                            result['daily_throughput'] = value * 1000
                        elif 'M' in next_line:
                            result['daily_throughput'] = value * 1000000
                        break
                
                # Also look for avg value "4.9% of 10.3M avg"
                for j in range(i+1, min(i+6, len(lines))):
                    next_line = lines[j].strip()
                    avg_match = re.search(r'([\d.]+)([KM]?)\s*avg', next_line, re.IGNORECASE)
                    if avg_match:
                        value = float(avg_match.group(1))
                        unit = avg_match.group(2).upper() if avg_match.group(2) else ''
                        if unit == 'K':
                            result['avg_throughput'] = value * 1000
                        elif unit == 'M':
                            result['avg_throughput'] = value * 1000000
                        else:
                            result['avg_throughput'] = value
                        break
                break
        
        # === Parse Transits (24h) ===
        # Format: "6 ships" followed by "5% of 60/day normal"
        for i, line in enumerate(lines):
            if 'TRANSITS' in line.upper() and '24H' in line.upper():
                # Look at next few lines
                for j in range(i+1, min(i+5, len(lines))):
                    next_line = lines[j].strip()
                    # Match "6 ships" or just number
                    match = re.search(r'(\d+)\s*ships?', next_line, re.IGNORECASE)
                    if match:
                        result['transits_24h'] = int(match.group(1))
                        break
                    # Also try just number
                    match2 = re.search(r'^\s*(\d+)\s*$', next_line)
                    if match2:
                        result['transits_24h'] = int(match2.group(1))
                        break
                
                # Look for day normal "5% of 60/day normal"
                for j in range(i+1, min(i+6, len(lines))):
                    next_line = lines[j].strip()
                    normal_match = re.search(r'(\d+)/day\s*normal', next_line, re.IGNORECASE)
                    if normal_match:
                        result['day_normal'] = int(normal_match.group(1))
                        break
                break
        
        # Fallback: use regex on full text
        if result['transits_24h'] is None:
            transits_match = re.search(r'Transits[^\d]*(\d+)[^\d]*ships?', visible_text, re.IGNORECASE)
            if transits_match:
                result['transits_24h'] = int(transits_match.group(1))
        
        # Method 2: Look for specific CSS classes/elements
        try:
            # Try to find transit elements
            elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Transit') or contains(text(), 'transit')]")
            for elem in elements:
                text = elem.text
                nums = re.findall(r'\d+', text)
                if nums and 'transit' in text.lower():
                    if result["transits_24h"] is None:
                        result["transits_24h"] = int(nums[0])
        except:
            pass
        
        # Method 3: Look for data in JSON embedded in page
        scripts = driver.find_elements(By.TAG_NAME, "script")
        for script in scripts:
            script_text = script.get_attribute("innerHTML") or ""
            if "transit" in script_text.lower() or "throughput" in script_text.lower():
                # Try to parse embedded JSON data
                json_match = re.search(r'\{[^{}]*"transit[^{}]*\}', script_text, re.IGNORECASE)
                if json_match:
                    try:
                        data = json.loads(json_match.group(0))
                        if "transits" in data:
                            result["transits_24h"] = data.get("transits", result["transits_24h"])
                        if "throughput" in data:
                            result["daily_throughput"] = data.get("throughput", result["daily_throughput"])
                    except json.JSONDecodeError:
                        pass
        
        # If we still don't have data, take a screenshot for debugging
        if result["transits_24h"] is None:
            screenshot_path = DEFAULT_DATA_FILE.parent / "hormuzstraitmonitor_debug.png"
            driver.save_screenshot(str(screenshot_path))
            result["debug_screenshot"] = str(screenshot_path)
            result["error"] = "Could not parse transit data from page"
        
    except Exception as e:
        result["error"] = str(e)
    
    return result


def fetch_shipxy(driver, max_retries=3) -> Dict[str, Any]:
    """
    Fetch non-Iranian vessel count from shipxy.com
    
    Returns:
        dict with non_iranian_vessels count
    """
    url = "https://www.shipxy.com/special/hormuz"
    
    result = {
        "non_iranian_vessels": None,
        "source": url,
        "fetched_at": datetime.now().isoformat(),
        "error": None,
        "method": None,
    }
    
    import re
    
    for attempt in range(max_retries):
        try:
            driver.get(url)
            time.sleep(20 + attempt * 5)  # Increase wait time on retries
            
            # Check for network error page
            body_text = driver.find_element(By.TAG_NAME, "body").text
            if 'connection was interrupted' in body_text.lower() or 'ERR_' in body_text:
                print(f"Network error on attempt {attempt+1}, retrying...")
                time.sleep(10)
                continue
            
            # Scroll multiple times to load all content
            for _ in range(3):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(2)
            
            visible_text = driver.find_element(By.TAG_NAME, "body").text
            page_text = driver.page_source
            
            # === Strategy 1: Parse vessel list from table ===
            # Look for "海峡进出流量与穿越明细" section and parse vessel entries
            non_iranian_count = 0
            iran_keywords = ['伊朗', 'IRAN', 'IRISL', 'Iranian', 'IRGC']
            exit_keywords = ['驶出', '出海峡', 'OUT', '出口', 'Outbound', '出湾']
            
            # Find all table rows
            vessel_rows = driver.find_elements(By.XPATH, '//tr[./td]')
            
            for row in vessel_rows:
                try:
                    row_text = row.text
                    if len(row_text) < 5:
                        continue
                    
                    # Check if row shows vessel exiting
                    is_exit = any(kw in row_text for kw in exit_keywords)
                    
                    if is_exit:
                        # Check if vessel is NOT Iranian
                        is_iranian = any(kw in row_text for kw in iran_keywords)
                        if not is_iranian:
                            non_iranian_count += 1
                except:
                    pass
            
            if non_iranian_count > 0:
                result['non_iranian_vessels'] = non_iranian_count
                result['method'] = 'table_count'
            
            # === Strategy 2: Parse from list items ===
            if result['non_iranian_vessels'] is None:
                list_items = driver.find_elements(By.XPATH, '//li | //div[contains(@class, "ship") or contains(@class, "vessel") or contains(@class, "item")]')
                
                for item in list_items:
                    try:
                        text = item.text
                        if len(text) < 5:
                            continue
                        
                        is_exit = any(kw in text for kw in exit_keywords)
                        if is_exit:
                            is_iranian = any(kw in text for kw in iran_keywords)
                            if not is_iranian:
                                non_iranian_count += 1
                    except:
                        pass
                
                if non_iranian_count > 0:
                    result['non_iranian_vessels'] = non_iranian_count
                    result['method'] = 'list_count'
            
            # === Strategy 3: Parse explicit count from text ===
            if result['non_iranian_vessels'] is None:
                cn_patterns = [
                    r'非伊朗[^\d]*(\d+)[^\d]*艘',
                    r'(\d+)[^\d]*艘[^伊]*非伊朗',
                    r'非伊朗船只[^\d]*(\d+)',
                    r'(\d+)[^\d]*非伊朗船只',
                    r'外国船只[^\d]*(\d+)',
                    r'非伊朗[^船船]*(\d+)[^船船]*船',
                    r'(\d+)[^船船]*非伊朗[^船船]*船',
                ]
                
                for pattern in cn_patterns:
                    match = re.search(pattern, visible_text)
                    if match:
                        result['non_iranian_vessels'] = int(match.group(1))
                        result['method'] = 'text_parse'
                        break
                
                # Also try HTML source
                if result['non_iranian_vessels'] is None:
                    for pattern in cn_patterns:
                        match = re.search(pattern, page_text)
                        if match:
                            result['non_iranian_vessels'] = int(match.group(1))
                            result['method'] = 'html_parse'
                            break
            
            # === Strategy 4: Parse from section header ===
            if result['non_iranian_vessels'] is None:
                sections = driver.find_elements(By.XPATH, '//*[contains(text(), "海峡进出") or contains(text(), "穿越明细") or contains(text(), "流量")]')
                
                for section in sections:
                    try:
                        parent = section.find_element(By.XPATH, '..')
                        siblings = parent.find_elements(By.XPATH, './/tr | .//li | .//div[contains(@class, "item")]')
                        
                        for sibling in siblings:
                            text = sibling.text
                            is_exit = any(kw in text for kw in exit_keywords)
                            if is_exit:
                                is_iranian = any(kw in text for kw in iran_keywords)
                                if not is_iranian:
                                    non_iranian_count += 1
                    except:
                        pass
                
                if non_iranian_count > 0:
                    result['non_iranian_vessels'] = non_iranian_count
                    result['method'] = 'section_count'
            
            # === Strategy 5: Parse 12h window ===
            if result['non_iranian_vessels'] is None:
                # Look for "12小时内" specific count
                time_patterns = [
                    r'12小时内[^\d]*(\d+)',
                    r'(\d+)[^\d]*12小时',
                    r'今日出[^\d]*(\d+)',
                ]
                
                for pattern in time_patterns:
                    match = re.search(pattern, visible_text)
                    if match:
                        potential_count = int(match.group(1))
                        if potential_count > 0 and potential_count < 200:
                            result['non_iranian_vessels'] = potential_count
                            result['method'] = 'time_parse'
                            break
            
            # If still no data, save debug files
            if result['non_iranian_vessels'] is None:
                screenshot_path = DEFAULT_DATA_FILE.parent / "shipxy_debug.png"
                driver.save_screenshot(str(screenshot_path))
                result['debug_screenshot'] = str(screenshot_path)
                
                source_path = DEFAULT_DATA_FILE.parent / "shipxy_debug.html"
                with open(source_path, 'w') as f:
                    f.write(page_text)
                result['debug_source'] = str(source_path)
                result['error'] = "Could not parse vessel data - check debug files"
            
            # Success - break retry loop
            if result['non_iranian_vessels'] is not None:
                break
                
        except Exception as e:
            result['error'] = str(e)
            if attempt < max_retries - 1:
                print(f"Error on attempt {attempt+1}: {e}, retrying...")
                time.sleep(10)
            else:
                screenshot_path = DEFAULT_DATA_FILE.parent / "shipxy_error.png"
                driver.save_screenshot(str(screenshot_path))
                result['debug_screenshot'] = str(screenshot_path)
    
    return result


def load_previous_data() -> Optional[Dict[str, Any]]:
    """Load the most recent data entry from CSV"""
    if not DEFAULT_DATA_FILE.exists():
        return None
    
    import csv
    try:
        with open(DEFAULT_DATA_FILE, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            if rows:
                return rows[-1]
    except:
        pass
    
    return None


def save_data(data: Dict[str, Any]) -> None:
    """Append data to CSV file"""
    DEFAULT_DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    import csv
    
    # Define CSV columns
    columns = [
        "timestamp",
        "transits_24h",
        "daily_throughput",
        "day_normal",
        "avg_throughput",
        "non_iranian_vessels",
        "alerts",
    ]
    
    # Check if file exists to determine if we need header
    write_header = not DEFAULT_DATA_FILE.exists()
    
    with open(DEFAULT_DATA_FILE, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        if write_header:
            writer.writeheader()
        
        # Prepare row data
        row = {
            "timestamp": data.get("timestamp", datetime.now().isoformat()),
            "transits_24h": data.get("transits_24h") or "",
            "daily_throughput": data.get("daily_throughput") or "",
            "day_normal": data.get("day_normal") or "",
            "avg_throughput": data.get("avg_throughput") or "",
            "non_iranian_vessels": data.get("non_iranian_vessels") or "",
            "alerts": data.get("alerts") or "",
        }
        writer.writerow(row)


def check_alerts(current: Dict[str, Any], previous: Optional[Dict[str, Any]]) -> List[str]:
    """
    Check if any alert conditions are met
    
    Conditions:
    a) Transits (24h) recovery: >= 10 vessels OR >= 20% of day normal
    b) Daily Throughput >= 20% of avg
    c) Non-Iranian vessels >= 10
    
    Returns list of alert messages
    """
    alerts = []
    
    transits = current.get("transits_24h")
    throughput = current.get("daily_throughput")
    day_normal = current.get("day_normal")
    avg_throughput = current.get("avg_throughput")
    non_iranian = current.get("non_iranian_vessels")
    
    # Condition a: Transits recovery
    if transits is not None:
        # Check absolute threshold
        if transits >= THRESHOLDS["transits_recovery"]:
            alerts.append(f"🚢 TRANSITS RECOVERY: {transits} vessels in 24h (>= {THRESHOLDS['transits_recovery']} threshold)")
        
        # Check relative threshold (if day_normal available)
        if day_normal is not None and day_normal > 0:
            percent = transits / day_normal
            if percent >= THRESHOLDS["transits_percent"]:
                alerts.append(f"🚢 TRANSITS RECOVERY: {transits}/{day_normal} = {percent:.1%} (>= {THRESHOLDS['transits_percent']:.0%} of day normal)")
        
        # Check significant increase from previous
        if previous and previous.get("transits_24h"):
            prev_transits = int(previous["transits_24h"]) if previous["transits_24h"] else 0
            if prev_transits > 0 and transits > prev_transits * 2:
                alerts.append(f"🚢 TRANSITS JUMP: {transits} vs previous {prev_transits} (+{transits - prev_transits} vessels)")
    
    # Condition b: Throughput recovery
    if throughput is not None and avg_throughput is not None and avg_throughput > 0:
        percent = throughput / avg_throughput
        if percent >= THRESHOLDS["throughput_percent"]:
            alerts.append(f"🛢️ THROUGHPUT RECOVERY: {throughput}/{avg_throughput} = {percent:.1%} (>= {THRESHOLDS['throughput_percent']:.0%} of avg)")
    
    # Condition c: Non-Iranian vessels
    if non_iranian is not None:
        if non_iranian >= THRESHOLDS["non_iranian_vessels"]:
            alerts.append(f"🚢 NON-IRANIAN VESSELS: {non_iranian} vessels exiting in 12h (>= {THRESHOLDS['non_iranian_vessels']} threshold)")
    
    return alerts


def format_summary(data: Dict[str, Any], alerts: List[str]) -> str:
    """Format data summary for output/notification"""
    lines = [
        "=== HORMUZ STRAIT TRANSIT MONITOR ===",
        f"Timestamp: {data.get('timestamp', 'N/A')}",
        "",
        "📊 hormuzstraitmonitor.com:",
        f"  Transits (24h): {data.get('transits_24h', 'N/A')}",
        f"  Day Normal: {data.get('day_normal', 'N/A')}",
        f"  Daily Throughput: {data.get('daily_throughput', 'N/A')}",
        f"  Avg Throughput: {data.get('avg_throughput', 'N/A')}",
        "",
        "📊 shipxy.com:",
        f"  Non-Iranian vessels (12h exit): {data.get('non_iranian_vessels', 'N/A')}",
        "",
    ]
    
    if alerts:
        lines.append("⚠️ ALERTS:")
        for alert in alerts:
            lines.append(f"  {alert}")
    else:
        lines.append("✅ No alerts - traffic remains suppressed")
    
    lines.append("")
    lines.append(f"Data file: {DEFAULT_DATA_FILE}")
    
    return "\n".join(lines)


def send_notification(message: str, channel: Optional[str] = None) -> None:
    """Send notification via configured channel"""
    if not channel:
        print(message)
        return
    
    # Use OpenClaw message tool for channel notification
    # This would be called via the skill's SKILL.md instructions
    print(f"[NOTIFICATION to {channel}]")
    print(message)


def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """Load configuration file"""
    config_file = Path(config_path) if config_path else DEFAULT_CONFIG_FILE
    
    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except:
            pass
    
    return {
        "channel": None,
        "thresholds": THRESHOLDS,
        "data_file": str(DEFAULT_DATA_FILE),
    }


def main():
    parser = argparse.ArgumentParser(description="Hormuz Strait Transit Monitor")
    parser.add_argument("--config", help="Path to config file")
    parser.add_argument("--channel", help="Notification channel (e.g., wecom, discord)")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode (keep browser open)")
    args = parser.parse_args()
    
    # Load config
    config = load_config(args.config)
    channel = args.channel or config.get("channel")
    
    print("Starting Hormuz Strait Monitor...")
    print(f"Time: {datetime.now().isoformat()}")
    
    # Setup driver
    driver = None
    try:
        driver = setup_driver()
        
        # Fetch data from both sources
        print("\nFetching hormuzstraitmonitor.com...")
        hormuz_data = fetch_hormuzstraitmonitor(driver)
        
        print("\nFetching shipxy.com...")
        shipxy_data = fetch_shipxy(driver)
        
        # Combine data
        combined = {
            "timestamp": datetime.now().isoformat(),
            "transits_24h": hormuz_data.get("transits_24h"),
            "daily_throughput": hormuz_data.get("daily_throughput"),
            "day_normal": hormuz_data.get("day_normal"),
            "avg_throughput": hormuz_data.get("avg_throughput"),
            "non_iranian_vessels": shipxy_data.get("non_iranian_vessels"),
        }
        
        # Load previous data for comparison
        previous = load_previous_data()
        
        # Check alerts
        alerts = check_alerts(combined, previous)
        combined["alerts"] = "; ".join(alerts) if alerts else ""
        
        # Save data
        save_data(combined)
        print(f"\nData saved to: {DEFAULT_DATA_FILE}")
        
        # Format and output
        summary = format_summary(combined, alerts)
        print("\n" + summary)
        
        # Send notification if alerts or channel configured
        if alerts or channel:
            send_notification(summary, channel)
        
        # Report any errors
        if hormuz_data.get("error"):
            print(f"\n⚠️ hormuzstraitmonitor.com error: {hormuz_data['error']}")
        if shipxy_data.get("error"):
            print(f"\n⚠️ shipxy.com error: {shipxy_data['error']}")
        
        if args.debug:
            print("\n[DEBUG] Keeping browser open for 60 seconds...")
            time.sleep(60)
        
    finally:
        if driver and not args.debug:
            driver.quit()
    
    return 0 if not alerts else 1  # Return 1 if alerts triggered


if __name__ == "__main__":
    sys.exit(main())