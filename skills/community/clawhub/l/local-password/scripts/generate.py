#!/usr/bin/env python3
import argparse
import secrets
import string

DEFAULT_LENGTH = 16
CHARSETS = {
    'uppercase': string.ascii_uppercase,
    'lowercase': string.ascii_lowercase,
    'digits': string.digits,
    'symbols': '!@#$%^&*()_-+=[]{}|;:,.<>?`~'
}
AMBIGUOUS = '0O1lI'

def generate_password(length=DEFAULT_LENGTH, use_uppercase=True, use_lowercase=True, use_digits=True, use_symbols=True, exclude_ambiguous=False):
    # Build character pool
    pool = ''
    if use_uppercase:
        pool += CHARSETS['uppercase']
    if use_lowercase:
        pool += CHARSETS['lowercase']
    if use_digits:
        pool += CHARSETS['digits']
    if use_symbols:
        pool += CHARSETS['symbols']
    
    if not pool:
        print("❌ Error: At least one character type must be enabled")
        return None
    
    # Exclude ambiguous characters if requested
    if exclude_ambiguous:
        pool = ''.join([c for c in pool if c not in AMBIGUOUS])
    
    if not pool:
        print("❌ Error: No characters left after excluding ambiguous characters")
        return None
    
    # Generate password
    password = ''.join([secrets.choice(pool) for _ in range(length)])
    return password

def main():
    parser = argparse.ArgumentParser(description="Generate secure random password")
    parser.add_argument("--length", type=int, default=DEFAULT_LENGTH, help=f"Password length (default: {DEFAULT_LENGTH})")
    parser.add_argument("--no-uppercase", action="store_true", help="Exclude uppercase letters")
    parser.add_argument("--no-lowercase", action="store_true", help="Exclude lowercase letters")
    parser.add_argument("--no-digits", action="store_true", help="Exclude digits")
    parser.add_argument("--no-symbols", action="store_true", help="Exclude symbols")
    parser.add_argument("--no-ambiguous", action="store_true", help="Exclude ambiguous characters (0O1lI)")
    args = parser.parse_args()
    
    password = generate_password(
        length=args.length,
        use_uppercase=not args.no_uppercase,
        use_lowercase=not args.no_lowercase,
        use_digits=not args.no_digits,
        use_symbols=not args.no_symbols,
        exclude_ambiguous=args.no_ambiguous
    )
    
    if password:
        print(f"🔒 Generated password:")
        print(password)

if __name__ == "__main__":
    main()
