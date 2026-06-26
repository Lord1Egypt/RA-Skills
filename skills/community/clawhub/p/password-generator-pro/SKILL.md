---
name: password-generator-pro
description: Generate secure random passwords using Python's secrets module with customizable length and character set options.

tags: password-generator, security, cryptography
---

# Password Generator Pro

## Usage Scenarios

### Scenario 1: Generate a Default Secure Password
**User input:** "Generate a secure password for my new account"
**Expected output:** The tool outputs a randomly generated 16-character password using mixed case letters, digits, and special symbols, along with the command used.

### Scenario 2: Create a Custom-Length Password
**User input:** "I need a 32-character password with all character types"
**Expected output:** The tool generates a 32-character password with symbols and numbers included, using `--length 32` option.

### Scenario 3: Generate Multiple Passwords at Once
**User input:** "Generate 5 passwords for my team's new service accounts"
**Expected output:** The tool outputs 5 separate passwords each 16 characters long, using `--count 5` option, suitable for bulk account creation.

Generate secure random passwords using Python's secrets module.
### Scenario 4: 生成一个安全又好记的密码
**User input:** "我要注册一个新的银行App，需要设置登录密码，要求大小写+数字+特殊字符，帮我生成一个。"
**Expected output:** 生成一个强密码模板：采用'三段式'原则（熟悉词+数字+符号），如'dog$Running!2026#'。或者使用口令式（4个随机单词组合确保长度和复杂度）。同时建议用户开启银行App的指纹/面部识别和双因素认证（如短信验证码+动态口令）。不建议在多个重要的账号使用相同的密码。如果用户记不住，推荐使用苹果iCloud钥匙串或1Password。

## Description

A secure password generator that uses Python's cryptographically secure `secrets` module to generate random passwords. Supports customizable length and character set options.

## Usage

```bash
# Generate a 16-character password with all character types
python ~/.openclaw/skills/password-generator-pro/password_generator.py --length 16

# Generate password without symbols
python ~/.openclaw/skills/password-generator-pro/password_generator.py --length 12 --no-symbols

# Generate password without numbers
python ~/.openclaw/skills/password-generator-pro/password_generator.py --length 12 --no-numbers

# Generate multiple passwords at once
python ~/.openclaw/skills/password-generator-pro/password_generator.py --length 20 --count 5
```

## Examples

```bash
# Default 16-character password
python ~/.openclaw/skills/password-generator-pro/password_generator.py

# Short password for simple use
python ~/.openclaw/skills/password-generator-pro/password_generator.py --length 8

# Long password with letters only
python ~/.openclaw/skills/password-generator-pro/password_generator.py --length 32 --no-symbols --no-numbers

# Generate 3 passwords
python ~/.openclaw/skills/password-generator-pro/password_generator.py --count 3
```

## Options

- `--length`: Password length (default: 16)
- `--no-symbols`: Exclude special symbols
- `--no-numbers`: Exclude numbers
- `--count`: Number of passwords to generate (default: 1)

## Security Note

This tool uses Python's `secrets` module, which is designed for cryptographic applications and provides secure random number generation suitable for passwords and authentication tokens.
