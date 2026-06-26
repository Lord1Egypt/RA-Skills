#!/usr/bin/env python3
"""Password Generator - Secure password generator using Python's secrets module."""

import argparse
import secrets
import string


def generate_password(length: int = 16, include_symbols: bool = True, include_numbers: bool = True) -> str:
    """Generate a secure random password."""
    # Build character set
    chars = string.ascii_letters  # Always include letters
    
    if include_numbers:
        chars += string.digits
    
    if include_symbols:
        chars += string.punctuation
    
    # Generate password ensuring at least one of each required type
    password = []
    
    # Always add at least one lowercase and one uppercase letter
    password.append(secrets.choice(string.ascii_lowercase))
    password.append(secrets.choice(string.ascii_uppercase))
    
    if include_numbers:
        password.append(secrets.choice(string.digits))
    
    if include_symbols:
        password.append(secrets.choice(string.punctuation))
    
    # Fill remaining length with random characters
    remaining = length - len(password)
    if remaining > 0:
        password.extend(secrets.choice(chars) for _ in range(remaining))
    
    # Shuffle to avoid predictable pattern
    secrets.SystemRandom().shuffle(password)
    
    return ''.join(password[:length])


def main():
    parser = argparse.ArgumentParser(description='Generate secure random passwords')
    parser.add_argument('--length', '-l', type=int, default=16, help='Password length (default: 16)')
    parser.add_argument('--no-symbols', action='store_true', help='Exclude special symbols')
    parser.add_argument('--no-numbers', action='store_true', help='Exclude numbers')
    parser.add_argument('--count', '-c', type=int, default=1, help='Number of passwords to generate')
    
    args = parser.parse_args()
    
    # Validate length
    min_length = 2 + (0 if args.no_numbers else 1) + (0 if args.no_symbols else 1)
    if args.length < min_length:
        print(f"Error: Minimum length for selected options is {min_length}")
        return 1
    
    # Generate passwords
    for i in range(args.count):
        password = generate_password(
            length=args.length,
            include_symbols=not args.no_symbols,
            include_numbers=not args.no_numbers
        )
        if args.count > 1:
            print(f"{i + 1}: {password}")
        else:
            print(password)
    
    return 0


if __name__ == '__main__':
    exit(main())
