# Password Generator

Generate secure random passwords using Python's secrets module.

## Description

A secure password generator that uses Python's cryptographically secure `secrets` module to generate random passwords. Supports customizable length and character set options.

## Usage

```bash
# Generate a 16-character password with all character types
python password_generator.py --length 16

# Generate password without symbols
python password_generator.py --length 12 --no-symbols

# Generate password without numbers
python password_generator.py --length 12 --no-numbers

# Generate multiple passwords at once
python password_generator.py --length 20 --count 5
```

## Examples

```bash
# Default 16-character password
python password_generator.py

# Short password for simple use
python password_generator.py --length 8

# Long password with letters only
python password_generator.py --length 32 --no-symbols --no-numbers

# Generate 3 passwords
python password_generator.py --count 3
```

## Options

- `--length`: Password length (default: 16)
- `--no-symbols`: Exclude special symbols
- `--no-numbers`: Exclude numbers
- `--count`: Number of passwords to generate (default: 1)

## Security Note

This tool uses Python's `secrets` module, which is designed for cryptographic applications and provides secure random number generation suitable for passwords and authentication tokens.
