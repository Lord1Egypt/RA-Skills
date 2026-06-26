import re

def parse_kplc_sms(text):
    """
    Parses a KPLC SMS message to extract token, units, and amount.
    """
    # Regex patterns for various parts of the KPLC message
    token_pattern = r"Token:\s*([\d-]+)"
    units_pattern = r"Units:\s*([\d.]+)"
    amount_pattern = r"(?:Amount|Amt):\s*([\d,.]+)"

    token_match = re.search(token_pattern, text, re.IGNORECASE)
    units_match = re.search(units_pattern, text, re.IGNORECASE)
    amount_match = re.search(amount_pattern, text, re.IGNORECASE)

    if token_match and units_match:
        token_raw = token_match.group(1)
        token = token_raw.replace("-", "")
        units = float(units_match.group(1))
        
        # Amount is sometimes formatted with commas or missing entirely in some alerts
        amount = 0.0
        if amount_match:
            amount_str = amount_match.group(1).replace(",", "")
            try:
                amount = float(amount_str)
            except ValueError:
                pass
                
        return {
            "token": token,
            "token_display": token_raw,
            "units": units,
            "amount": amount,
            "success": True
        }
    
    # Alternate format: "token is 1234-5678-... for 12.5 units"
    alt = re.search(r'token\s+is\s+([\d-]+)\s+for\s+([\d.]+)\s+units', text, re.IGNORECASE)
    if alt:
        return {
            "token": alt.group(1).replace("-", ""),
            "token_display": alt.group(1),
            "units": float(alt.group(2)),
            "amount": 0.0,
            "success": True
        }

    return {"success": False, "error": "Could not find token or units in the message."}

# Testing the parser
if __name__ == "__main__":
    test_messages = [
        "Accept Token: 1234-5678-9012-3456-7890 Units: 34.5 Amount: 1000.00",
        "Token: 9876-5432-1098-7654-3210 Units: 15.2 Amt: 500.0",
        "Your token is 1111-2222-3333-4444-5555 for 12.5 units."
    ]
    
    for msg in test_messages:
        print(f"Parsing: {msg}")
        print(parse_kplc_sms(msg))
        print("-" * 20)
