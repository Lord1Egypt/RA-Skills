# Password Generator

Generate secure passwords with configurable length, character sets, and strength analysis.

## Features
- Random password generation (8-128 chars)
- Strength analysis (entropy calculation)
- Configurable: uppercase, lowercase, digits, symbols
- Exclude similar characters option
- Batch generation

## Usage
```bash
clawdhub install king-password-generator
python3 main.py generate --length 16 --symbols
python3 main.py analyze "MyP@ssw0rd"
python3 main.py batch --count 10
```
