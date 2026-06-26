#!/usr/bin/env python3
import argparse
import math

CHAR_CATEGORIES = {
    'uppercase': r'[A-Z]',
    'lowercase': r'[a-z]',
    'digits': r'[0-9]',
    'symbols': r'[^A-Za-z0-9]'
}

def calculate_entropy(password):
    """Calculate password entropy based on character pool size."""
    pool_size = 0
    has_uppercase = any(c.isupper() for c in password)
    has_lowercase = any(c.islower() for c in password)
    has_digits = any(c.isdigit() for c in password)
    has_symbols = any(not c.isalnum() for c in password)
    
    if has_uppercase:
        pool_size += 26
    if has_lowercase:
        pool_size += 26
    if has_digits:
        pool_size += 10
    if has_symbols:
        pool_size += 32  # Approximate common symbols
    
    if pool_size == 0:
        return 0
    
    entropy = len(password) * math.log2(pool_size)
    return entropy, has_uppercase, has_lowercase, has_digits, has_symbols

def estimate_crack_time(entropy):
    """Estimate crack time based on entropy."""
    # Assuming 10 billion guesses per second (fast attacker)
    guesses_per_second = 10_000_000_000
    total_combinations = 2 ** entropy
    # Average guesses needed is half of total combinations
    avg_guesses = total_combinations / 2
    seconds = avg_guesses / guesses_per_second
    
    if seconds < 1:
        return "instantly"
    elif seconds < 60:
        return f"{int(seconds)} seconds"
    elif seconds < 3600:
        return f"{int(seconds / 60)} minutes"
    elif seconds < 86400:
        return f"{int(seconds / 3600)} hours"
    elif seconds < 31536000:
        return f"{int(seconds / 86400)} days"
    elif seconds < 31536000 * 100:
        return f"{int(seconds / 31536000)} years"
    elif seconds < 31536000 * 1000000:
        return f"{int(seconds / 31536000 / 1000)} thousand years"
    elif seconds < 31536000 * 1000000000:
        return f"{int(seconds / 31536000 / 1000000)} million years"
    else:
        return "billions of years"

def get_strength_label(entropy):
    if entropy < 28:
        return "🔴 Very Weak", "Cracked very quickly"
    elif entropy < 36:
        return "🟠 Weak", "Cracked in minutes to hours"
    elif entropy < 60:
        return "🟡 Moderate", "Cracked in days to years"
    elif entropy < 80:
        return "🟢 Strong", "Cracked in centuries"
    else:
        return "✅ Very Strong", "Practically uncrackable"

def main():
    parser = argparse.ArgumentParser(description="Check password strength")
    parser.add_argument("password", help="Password to check")
    args = parser.parse_args()
    
    entropy, has_uppercase, has_lowercase, has_digits, has_symbols = calculate_entropy(args.password)
    crack_time = estimate_crack_time(entropy)
    strength_label, description = get_strength_label(entropy)
    
    print(f"📊 Password Analysis:")
    print(f"   Length: {len(args.password)} characters")
    print(f"   Character types:")
    print(f"     • Uppercase: {'✓' if has_uppercase else '✗'}")
    print(f"     • Lowercase: {'✓' if has_lowercase else '✗'}")
    print(f"     • Digits: {'✓' if has_digits else '✗'}")
    print(f"     • Symbols: {'✓' if has_symbols else '✗'}")
    print()
    print(f"🔐 Entropy: {entropy:.2f} bits")
    print(f"💪 Strength: {strength_label}")
    print(f"⌛ Estimated time to crack (10B guesses/sec): {crack_time}")
    print(f"   {description}")

if __name__ == "__main__":
    main()
