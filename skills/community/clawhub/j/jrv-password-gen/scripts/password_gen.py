#!/usr/bin/env python3
"""Secure password and passphrase generator with customizable rules.

Features:
- Random passwords with configurable length, character sets, and exclusions
- Passphrase generation using EFF word lists (bundled or downloaded)
- Entropy estimation
- Batch generation
- PIN generation
- Password strength analysis

No external dependencies required (uses Python stdlib only).
"""

import argparse
import math
import os
import random
import secrets
import string
import sys
import json
import hashlib
import urllib.request
import tempfile

# --- Word list for passphrases ---

# A compact built-in word list (200 common words) for offline passphrase generation.
# For higher quality, the script can download the EFF long word list.
BUILTIN_WORDS = [
    "abandon", "ability", "able", "about", "above", "absent", "absorb", "abstract",
    "absurd", "abuse", "access", "accident", "account", "accuse", "achieve", "acid",
    "acoustic", "acquire", "across", "action", "actor", "actual", "adapt", "address",
    "adjust", "admit", "adult", "advance", "advice", "aerobic", "affair", "afford",
    "afraid", "again", "agent", "agree", "ahead", "aim", "air", "airport",
    "alarm", "album", "alcohol", "alert", "alien", "allow", "almost", "alone",
    "alpha", "already", "also", "alter", "always", "amateur", "amazing", "among",
    "amount", "amused", "anchor", "ancient", "anger", "angle", "animal", "answer",
    "anxiety", "apart", "apology", "appear", "apple", "approve", "arctic", "area",
    "arena", "argue", "armor", "army", "arrange", "arrest", "arrive", "arrow",
    "artist", "artwork", "aspect", "atom", "audit", "august", "aunt", "author",
    "average", "avocado", "avoid", "awake", "aware", "awesome", "bacon", "badge",
    "balance", "balcony", "bamboo", "banana", "banner", "barely", "barrel", "basket",
    "battle", "beach", "beauty", "become", "believe", "benefit", "bicycle", "blanket",
    "blossom", "bottle", "bounce", "breeze", "bridge", "bright", "bronze", "bubble",
    "buffalo", "burden", "butter", "cabin", "cactus", "camera", "campus", "candle",
    "canyon", "captain", "carbon", "carpet", "castle", "catalog", "caught", "ceiling",
    "celery", "cement", "center", "cereal", "chair", "chalk", "change", "chapter",
    "cherry", "chicken", "chimney", "circle", "citizen", "cliff", "climb", "clock",
    "cluster", "coach", "coconut", "coffee", "collect", "column", "comfort", "comic",
    "company", "concert", "connect", "control", "cookie", "copper", "corner", "cotton",
    "country", "couple", "cousin", "cover", "cradle", "craft", "crane", "crater",
    "credit", "cricket", "crisis", "crisp", "cross", "crucial", "crystal", "curtain",
    "custom", "cycle", "damage", "dance", "danger", "dawn", "decade", "deliver",
    "demand", "deposit", "design", "diamond", "dinner", "dolphin", "dragon", "dream",
]

EFF_WORDLIST_URL = "https://www.eff.org/files/2016/07/18/eff_large_wordlist.txt"
EFF_CACHE_PATH = os.path.join(tempfile.gettempdir(), "eff_large_wordlist.txt")


def load_eff_wordlist():
    """Download and cache the EFF large word list. Falls back to built-in list."""
    if os.path.exists(EFF_CACHE_PATH):
        words = []
        with open(EFF_CACHE_PATH, "r") as f:
            for line in f:
                parts = line.strip().split("\t")
                if len(parts) == 2:
                    words.append(parts[1])
        if len(words) > 1000:
            return words

    try:
        urllib.request.urlretrieve(EFF_WORDLIST_URL, EFF_CACHE_PATH)
        return load_eff_wordlist()
    except Exception:
        return BUILTIN_WORDS


def calculate_entropy(length, charset_size):
    """Calculate entropy in bits."""
    if charset_size <= 0 or length <= 0:
        return 0.0
    return length * math.log2(charset_size)


def strength_label(entropy):
    """Return a human-readable strength label."""
    if entropy < 28:
        return "Very Weak"
    elif entropy < 36:
        return "Weak"
    elif entropy < 60:
        return "Moderate"
    elif entropy < 80:
        return "Strong"
    elif entropy < 128:
        return "Very Strong"
    else:
        return "Excellent"


def generate_password(length=16, uppercase=True, lowercase=True, digits=True,
                      symbols=True, exclude="", must_include=None):
    """Generate a cryptographically secure random password."""
    charset = ""
    required = []

    if uppercase:
        chars = string.ascii_uppercase
        for c in exclude:
            chars = chars.replace(c, "")
        charset += chars
        if chars:
            required.append(secrets.choice(chars))

    if lowercase:
        chars = string.ascii_lowercase
        for c in exclude:
            chars = chars.replace(c, "")
        charset += chars
        if chars:
            required.append(secrets.choice(chars))

    if digits:
        chars = string.digits
        for c in exclude:
            chars = chars.replace(c, "")
        charset += chars
        if chars:
            required.append(secrets.choice(chars))

    if symbols:
        chars = string.punctuation
        for c in exclude:
            chars = chars.replace(c, "")
        charset += chars
        if chars:
            required.append(secrets.choice(chars))

    if not charset:
        print("Error: No characters available after applying exclusions.", file=sys.stderr)
        sys.exit(1)

    if must_include:
        for c in must_include:
            required.append(c)
            if c not in charset:
                charset += c

    if length < len(required):
        length = len(required)

    remaining = length - len(required)
    password_chars = required + [secrets.choice(charset) for _ in range(remaining)]

    # Shuffle to avoid predictable positions
    random_inst = secrets.SystemRandom()
    random_inst.shuffle(password_chars)

    password = "".join(password_chars)
    entropy = calculate_entropy(length, len(set(charset)))
    return password, entropy


def generate_passphrase(words=4, separator="-", capitalize=False, add_number=False):
    """Generate a passphrase from random words."""
    wordlist = load_eff_wordlist()
    chosen = [secrets.choice(wordlist) for _ in range(words)]

    if capitalize:
        chosen = [w.capitalize() for w in chosen]

    parts = chosen
    if add_number:
        parts.append(str(secrets.randbelow(100)))

    passphrase = separator.join(parts)
    entropy = words * math.log2(len(wordlist))
    if add_number:
        entropy += math.log2(100)

    return passphrase, entropy


def generate_pin(length=6):
    """Generate a numeric PIN."""
    pin = "".join(secrets.choice(string.digits) for _ in range(length))
    entropy = calculate_entropy(length, 10)
    return pin, entropy


def analyze_password(password):
    """Analyze an existing password's strength."""
    length = len(password)
    has_upper = any(c in string.ascii_uppercase for c in password)
    has_lower = any(c in string.ascii_lowercase for c in password)
    has_digit = any(c in string.digits for c in password)
    has_symbol = any(c in string.punctuation for c in password)

    charset_size = 0
    if has_upper:
        charset_size += 26
    if has_lower:
        charset_size += 26
    if has_digit:
        charset_size += 10
    if has_symbol:
        charset_size += 32

    entropy = calculate_entropy(length, charset_size)

    # Check for common patterns
    issues = []
    if length < 8:
        issues.append("Too short (< 8 characters)")
    if not has_upper:
        issues.append("No uppercase letters")
    if not has_lower:
        issues.append("No lowercase letters")
    if not has_digit:
        issues.append("No digits")
    if not has_symbol:
        issues.append("No symbols")

    # Check for sequential characters
    for i in range(len(password) - 2):
        if ord(password[i]) + 1 == ord(password[i+1]) == ord(password[i+2]) - 1:
            issues.append("Contains sequential characters")
            break

    # Check for repeated characters
    for i in range(len(password) - 2):
        if password[i] == password[i+1] == password[i+2]:
            issues.append("Contains repeated characters (3+)")
            break

    return {
        "length": length,
        "charset_size": charset_size,
        "entropy_bits": round(entropy, 1),
        "strength": strength_label(entropy),
        "has_uppercase": has_upper,
        "has_lowercase": has_lower,
        "has_digits": has_digit,
        "has_symbols": has_symbol,
        "issues": issues,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Secure password and passphrase generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  %(prog)s                          Generate a 16-char password
  %(prog)s -l 32                    Generate a 32-char password
  %(prog)s -l 20 --no-symbols       No special characters
  %(prog)s --passphrase             Generate a 4-word passphrase
  %(prog)s --passphrase -w 6        Generate a 6-word passphrase
  %(prog)s --pin                    Generate a 6-digit PIN
  %(prog)s --pin -l 4               Generate a 4-digit PIN
  %(prog)s --analyze 'MyP@ss123'    Analyze password strength
  %(prog)s -n 5                     Generate 5 passwords
  %(prog)s --json                   Output as JSON
"""
    )
    parser.add_argument("-l", "--length", type=int, default=16,
                        help="Password length (default: 16)")
    parser.add_argument("-n", "--count", type=int, default=1,
                        help="Number of passwords to generate (default: 1)")
    parser.add_argument("--no-uppercase", action="store_true",
                        help="Exclude uppercase letters")
    parser.add_argument("--no-lowercase", action="store_true",
                        help="Exclude lowercase letters")
    parser.add_argument("--no-digits", action="store_true",
                        help="Exclude digits")
    parser.add_argument("--no-symbols", action="store_true",
                        help="Exclude symbols/punctuation")
    parser.add_argument("--exclude", type=str, default="",
                        help="Exclude specific characters (e.g., 'lI1O0')")
    parser.add_argument("--must-include", type=str, default=None,
                        help="Characters that must appear in the password")
    parser.add_argument("--passphrase", action="store_true",
                        help="Generate a passphrase instead of a password")
    parser.add_argument("-w", "--words", type=int, default=4,
                        help="Number of words in passphrase (default: 4)")
    parser.add_argument("--separator", type=str, default="-",
                        help="Word separator for passphrase (default: -)")
    parser.add_argument("--capitalize", action="store_true",
                        help="Capitalize passphrase words")
    parser.add_argument("--add-number", action="store_true",
                        help="Append a random number to passphrase")
    parser.add_argument("--pin", action="store_true",
                        help="Generate a numeric PIN")
    parser.add_argument("--analyze", type=str, default=None,
                        help="Analyze an existing password's strength")
    parser.add_argument("--json", action="store_true",
                        help="Output as JSON")

    args = parser.parse_args()

    # Analyze mode
    if args.analyze is not None:
        result = analyze_password(args.analyze)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"Password:      {'*' * len(args.analyze)} ({result['length']} chars)")
            print(f"Entropy:       {result['entropy_bits']} bits")
            print(f"Strength:      {result['strength']}")
            print(f"Charset size:  {result['charset_size']}")
            print(f"Uppercase:     {'Yes' if result['has_uppercase'] else 'No'}")
            print(f"Lowercase:     {'Yes' if result['has_lowercase'] else 'No'}")
            print(f"Digits:        {'Yes' if result['has_digits'] else 'No'}")
            print(f"Symbols:       {'Yes' if result['has_symbols'] else 'No'}")
            if result['issues']:
                print(f"Issues:        {', '.join(result['issues'])}")
            else:
                print("Issues:        None detected")
        return

    results = []

    for _ in range(args.count):
        if args.passphrase:
            value, entropy = generate_passphrase(
                words=args.words,
                separator=args.separator,
                capitalize=args.capitalize,
                add_number=args.add_number,
            )
            mode = "passphrase"
        elif args.pin:
            value, entropy = generate_pin(length=args.length if args.length != 16 else 6)
            mode = "pin"
        else:
            value, entropy = generate_password(
                length=args.length,
                uppercase=not args.no_uppercase,
                lowercase=not args.no_lowercase,
                digits=not args.no_digits,
                symbols=not args.no_symbols,
                exclude=args.exclude,
                must_include=args.must_include,
            )
            mode = "password"

        results.append({
            "value": value,
            "mode": mode,
            "entropy_bits": round(entropy, 1),
            "strength": strength_label(entropy),
        })

    if args.json:
        if len(results) == 1:
            print(json.dumps(results[0], indent=2))
        else:
            print(json.dumps(results, indent=2))
    else:
        for r in results:
            print(f"{r['value']}  ({r['entropy_bits']} bits, {r['strength']})")


if __name__ == "__main__":
    main()
