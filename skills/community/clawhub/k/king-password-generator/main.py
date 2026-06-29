#!/usr/bin/env python3
"""Password Generator & Strength Analyzer."""
import sys, secrets, string, math

VERSION = "1.0.0"

def generate(length=16, use_upper=True, use_lower=True, use_digits=True, use_special=True):
    chars = ''
    if use_upper: chars += string.ascii_uppercase
    if use_lower: chars += string.ascii_lowercase
    if use_digits: chars += string.digits
    if use_special: chars += '!@#$%^&*()_+-=[]{}|;:,.<>?'
    return ''.join(secrets.choice(chars) for _ in range(length))

def strength(password):
    length = len(password)
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)
    charset_size = 0
    if has_upper: charset_size += 26
    if has_lower: charset_size += 26
    if has_digit: charset_size += 10
    if has_special: charset_size += 32
    entropy = length * math.log2(max(charset_size, 1))
    score = min(100, int(entropy / 8 * 10))
    label = "Very Strong" if score >= 80 else "Strong" if score >= 60 else "Medium" if score >= 40 else "Weak"
    return score, round(entropy, 1), label

if __name__ == '__main__':
    if "--version" in sys.argv: print(VERSION); sys.exit(0)
    if "--check" in sys.argv:
        idx = sys.argv.index("--check") + 1
        if idx < len(sys.argv):
            s, e, l = strength(sys.argv[idx])
            print(json.dumps({"score": s, "entropy": e, "label": l, "password": sys.argv[idx]}))
    else:
        length = 16
        if "--length" in sys.argv:
            idx = sys.argv.index("--length") + 1
            if idx < len(sys.argv): length = int(sys.argv[idx])
        pwd = generate(length)
        s, e, l = strength(pwd)
        print(json.dumps({"password": pwd, "score": s, "entropy": e, "strength": l}))
