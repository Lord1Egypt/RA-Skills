import os
import re
from datetime import datetime
import requests

# ─── Configuration ───────────────────────────────────────────────
# Set these as environment variables before running:
#   export NOTION_API_KEY="your_notion_api_key_here"
#   export EXPENSE_DATABASE_ID="your_database_id_here"
#
# To get your Notion API key:
#   1. Go to https://www.notion.so/my-integrations
#   2. Create a new integration and copy the token
#   3. Share your expense database with the integration
#
# To get your database ID:
#   1. Open your Notion expense database in a browser
#   2. The URL looks like: notion.so/{workspace}/{database_id}?v=...
#   3. Copy the 32-character database_id (remove dashes)
# ─────────────────────────────────────────────────────────────────

NOTION_API_KEY = os.getenv('NOTION_API_KEY')
DATABASE_ID = os.getenv('EXPENSE_DATABASE_ID')

if not NOTION_API_KEY or not DATABASE_ID:
    raise EnvironmentError(
        "Missing required environment variables.\n"
        "Please set NOTION_API_KEY and EXPENSE_DATABASE_ID.\n"
        "See comments above for instructions."
    )

# Bank aliases — maps user input to display name
BANK_ALIASES = {
    'ocbc': 'OCBC',
    'dbs': 'DBS',
    'trust': 'TRUST',
    'revolut': 'Revolut',
    '支付宝': '支付宝',
    'alipay': '支付宝',
    '微信': '微信',
    'wechat': '微信',
    'ocbc business': 'OCBC BUSINESS',
}

# Category keywords for auto-classification
CATEGORY_KEYWORDS = {
    'Food': ['food', 'rice', 'noodle', 'lunch', 'dinner', 'breakfast', 'coffee', 'tea',
             'meal', 'restaurant', 'cafe', 'bakery', 'chicken', 'beef', 'pork', 'fish',
             'snack', 'porridge', 'bingsu', 'starbucks', 'breadtalk', 'foodpanda',
             '咖啡', '奶茶', '牛肉干'],
    'Transport': ['transport', 'taxi', 'bus', 'train', 'mrt', 'grab', 'tada',
                  'commute', '打车', '火车票'],
    'shopping': ['shopping', 'clothes', 'shoes', 'taobao', 'shopee', 'lazada',
                 'perfume', 'gift', '鞋子', '内衣', '公仔'],
    'Groceries': ['fairprice', 'ntuc', 'groceries', 'shampoo', 'household', '饮料'],
    'Leisure': ['movie', 'netflix', 'spotify', 'steam', 'game', 'concert', 'bilibili',
                'swimming', 'pottery', 'vpn', '游戏'],
    'Bills': ['bill', 'subscription', 'insurance', 'icloud', 'gym membership',
              'phone bill', 'm1 bill'],
    'business': ['notion labs', 'claude ai', 'website', 'marketing', 'carou',
                 'elementor', 'bluehost', 'delivery fee'],
    'medical': ['medical', 'clinic', 'doctor', 'lactoguard', 'pharmacy'],
    'investment': ['webull', 'stocks', 'investment', 's&p'],
    'Education': ['driving school', 'driving test', 'driving class', 'course',
                  'tuition', '3d printing'],
}


def get_category_from_text(text):
    """Auto-categorise based on keyword matching."""
    text_lower = text.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in text_lower for keyword in keywords):
            return category
    return 'other'


def extract_amount_and_category(text):
    """Extract the expense amount and auto-detect category from message text."""
    amount_pattern = r'(\d+(?:\.\d+)?)'
    amounts = re.findall(amount_pattern, text)

    if amounts:
        # Take the last number as the amount (handles "2 coffee 9" → amount=9)
        amount = float(amounts[-1])
        text_no_amount = text
        # Remove the matched amount from text for cleaner category detection
        for i, m in enumerate(re.finditer(amount_pattern, text)):
            if i == len(amounts) - 1:
                text_no_amount = text[:m.start()] + text[m.end():]
        category = get_category_from_text(text_no_amount)
    else:
        amount = 0.0
        category = get_category_from_text(text)

    return round(amount, 2), category


def extract_bank_name(text):
    """Detect payment method from message text. Defaults to OCBC."""
    text_lower = text.lower()
    # Check longer aliases first to avoid partial matches
    for alias in sorted(BANK_ALIASES.keys(), key=len, reverse=True):
        if alias in text_lower:
            return BANK_ALIASES[alias]
    return 'OCBC'


def get_item_name(text, amount, bank):
    """Extract the item description by removing amount and bank from the message."""
    item = text
    # Remove amount
    item = re.sub(r'\$?\d+(?:\.\d+)?', '', item, count=1)
    # Remove bank name if detected
    if bank != 'OCBC':  # Don't strip default
        for alias in BANK_ALIASES:
            item = re.sub(re.escape(alias), '', item, flags=re.IGNORECASE)
    # Remove category overrides and clean up
    item = re.sub(r'\b(food|transport|shopping|business|bills|medical|leisure|groceries|investment|education)\b',
                  '', item, flags=re.IGNORECASE)
    item = re.sub(r'\s+', ' ', item).strip()
    return item if item else text


def log_expense(text):
    """
    Log an expense to Notion database.

    Args:
        text: Natural language expense like "chicken rice 5" or "grab home 15 OCBC"

    Returns:
        dict with status, message, amount, category, bank
    """
    try:
        amount, category = extract_amount_and_category(text)
        bank = extract_bank_name(text)
        item = get_item_name(text, amount, bank)
        current_date = datetime.now().strftime("%Y-%m-%d")

        # Check for explicit category override in the message
        text_lower = text.lower()
        for cat in CATEGORY_KEYWORDS:
            if cat.lower() in text_lower.split():
                category = cat
                break

        headers = {
            "Authorization": f"Bearer {NOTION_API_KEY}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }

        payload = {
            "parent": {"database_id": DATABASE_ID},
            "properties": {
                "Name": {"title": [{"text": {"content": item}}]},
                "Amount": {"number": amount},
                "Category": {"select": {"name": category}},
                "Bank Name": {"select": {"name": bank}},
                "Transaction Date": {"date": {"start": current_date}}
            }
        }

        response = requests.post(
            "https://api.notion.com/v1/pages",
            headers=headers,
            json=payload,
            timeout=30
        )

        if response.status_code == 200:
            return {
                "status": "success",
                "message": f"✅ Logged: {item} — SGD {amount:.2f}\n📂 {category} | 🏦 {bank} | 📅 {current_date}",
                "amount": amount,
                "category": category,
                "bank": bank
            }
        else:
            return {
                "status": "error",
                "message": f"Failed to log expense: {response.status_code} - {response.text}",
                "amount": amount,
                "category": category,
                "bank": bank
            }

    except requests.exceptions.Timeout:
        return {"status": "error", "message": "Notion API timed out. Try again."}
    except requests.exceptions.ConnectionError:
        return {"status": "error", "message": "Could not connect to Notion API. Check your internet."}
    except Exception as e:
        return {"status": "error", "message": f"Error: {str(e)}"}


if __name__ == "__main__":
    test_expenses = [
        "chicken rice 5",
        "咖啡 3.50 支付宝",
        "grab to school 12.50",
        "notion labs 33 revolut",
        "dinner with jy 57 trust",
        "driving class 90",
        "steam game 35",
    ]

    for expense in test_expenses:
        print(f"Input:  {expense}")
        amount, cat = extract_amount_and_category(expense)
        bank = extract_bank_name(expense)
        item = get_item_name(expense, amount, bank)
        print(f"Parsed: item={item}, amount={amount}, category={cat}, bank={bank}")
        print("---")
