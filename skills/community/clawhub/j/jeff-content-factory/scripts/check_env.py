#!/usr/bin/env python3
"""
Load environment variables from .env file
Usage: source this in your scripts or run directly to check
"""

import os
from pathlib import Path


def load_env_file(env_path=".env"):
    """Load environment variables from .env file"""
    env_file = Path(env_path)

    if not env_file.exists():
        print(f"⚠️  .env file not found: {env_file.absolute()}")
        print(f"   Create one by copying .env.example:")
        print(f"   cp .env.example .env")
        return False

    print(f"📄 Loading environment from: {env_file.absolute()}")

    with open(env_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()

            # Skip comments and empty lines
            if not line or line.startswith('#'):
                continue

            # Parse KEY=VALUE
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()

                # Remove quotes if present
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                elif value.startswith("'") and value.endswith("'"):
                    value = value[1:-1]

                # Set environment variable
                os.environ[key] = value
                print(f"   ✅ {key} = {value[:10]}..." if len(value) > 10 else f"   ✅ {key} = {value}")

    return True


def check_required_keys():
    """Check if required API keys are set"""
    print("\n🔍 Checking API keys and credentials...")

    required_keys = {
        'GLM_API_KEY': 'GLM-Image API (required for cover generation)',
    }

    optional_keys = {
        'WECHAT_APP_ID': 'WeChat Official Account AppID (for auto-publishing)',
        'WECHAT_APP_SECRET': 'WeChat Official Account AppSecret (for auto-publishing)',
    }

    all_set = True

    # Check required keys
    print("\n📌 Required:")
    for key, description in required_keys.items():
        value = os.environ.get(key)
        if value and value != 'your-api-key-here':
            masked_value = value[:10] + "..." if len(value) > 10 else value
            print(f"   ✅ {key}: {masked_value}")
            print(f"      ({description})")
        else:
            print(f"   ❌ {key}: Not set")
            print(f"      ({description})")
            all_set = False

    # Check optional keys
    print("\n📌 Optional (for WeChat auto-publishing):")
    wechat_configured = True
    for key, description in optional_keys.items():
        value = os.environ.get(key)
        if value and value not in ['your-api-key-here', 'your-app-id-here', 'your-app-secret-here']:
            masked_value = value[:10] + "..." if len(value) > 10 else value
            print(f"   ✅ {key}: {masked_value}")
            print(f"      ({description})")
        else:
            print(f"   ⚠️  {key}: Not set")
            print(f"      ({description})")
            wechat_configured = False

    if wechat_configured:
        print("\n   ℹ️  WeChat auto-publishing is fully configured!")
    else:
        print("\n   ℹ️  WeChat credentials not set - auto-publishing will be disabled")
        print("      You can still generate cover photos and articles")

    return all_set


if __name__ == "__main__":
    print("=" * 60)
    print("🔑 Environment Configuration Checker")
    print("=" * 60)

    # Try to load from .env file
    script_dir = Path(__file__).parent.parent  # Go up to content-factory root
    env_path = script_dir / ".env"

    if env_path.exists():
        load_env_file(env_path)
    else:
        print(f"\n⚠️  No .env file found at: {env_path}")
        print(f"   Create one by copying .env.example:")
        print(f"   cd {script_dir}")
        print(f"   cp .env.example .env")
        print(f"   # Then edit .env and add your API keys")

    # Check if keys are set
    all_set = check_required_keys()

    print("\n" + "=" * 60)
    if all_set:
        print("✅ All required API keys are configured!")
        print("   You can now use the cover photo generation script.")
    else:
        print("❌ Some required API keys are missing.")
        print("\n📝 Setup instructions:")
        print("   1. Get your GLM API key from: https://open.bigmodel.cn/")
        print("   2. Copy .env.example to .env")
        print("   3. Edit .env and replace 'your-api-key-here' with your actual key")
        print("   4. Run this script again to verify")
    print("=" * 60)
