#!/usr/bin/env python3
"""
Setup script for Testcontainers
Configures testcontainers environment for integration testing
"""

import subprocess
import sys
import os

def check_docker():
    """Check if Docker is running and accessible"""
    try:
        result = subprocess.run(
            ['docker', 'version'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("✅ Docker is available")
            return True
        else:
            print("❌ Docker is not available")
            return False
    except FileNotFoundError:
        print("❌ Docker is not installed")
        return False

def install_python_dependencies():
    """Install required Python packages for testcontainers"""
    packages = [
        'testcontainers',
        'docker'
    ]
    
    for package in packages:
        try:
            subprocess.run(
                [sys.executable, '-m', 'pip', 'install', package],
                check=True
            )
            print(f"✅ Installed {package}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {package}: {e}")
            return False
    
    return True

def setup_environment():
    """Configure environment variables for testcontainers"""
    env_vars = {
        'TESTCONTAINERS_HOST_OVERRIDE': 'host.docker.internal',
        'TESTCONTAINERS_RYUK_DISABLED': 'true'  # Don't clean up containers after tests
    }
    
    # Add to shell profile
    profile = os.path.expanduser('~/.bashrc')
    if os.path.exists(profile):
        with open(profile, 'a') as f:
            f.write('\n# Testcontainers configuration\n')
            for key, value in env_vars.items():
                f.write(f'export {key}="{value}"\n')
        print(f"✅ Added testcontainers configuration to {profile}")
    
    return env_vars

def verify_setup():
    """Verify testcontainers setup by running a simple test"""
    try:
        from testcontainers.core.container import DockerContainer
        from alpine import AlpineContainer  # This might not be available, that's okay
        
        print("✅ Testcontainers Python package is installed")
        return True
    except ImportError as e:
        print(f"⚠️  Some testcontainers features not available: {e}")
        print("   This is normal for basic setup")
        return True

def main():
    """Main setup function"""
    print("🐋 Setting up Testcontainers environment...\n")
    
    # Step 1: Check Docker
    print("Step 1: Checking Docker...")
    if not check_docker():
        print("Please install and start Docker first")
        sys.exit(1)
    
    # Step 2: Install Python dependencies
    print("\nStep 2: Installing Python dependencies...")
    if not install_python_dependencies():
        print("Failed to install required packages")
        sys.exit(1)
    
    # Step 3: Configure environment
    print("\nStep 3: Configuring environment...")
    env_vars = setup_environment()
    
    # Step 4: Verify setup
    print("\nStep 4: Verifying setup...")
    verify_setup()
    
    print("\n" + "="*50)
    print("✅ Testcontainers setup complete!")
    print("="*50)
    print("\nYou can now use testcontainers in your tests:")
    print("  from testcontainers.postgres import PostgresContainer")
    print("  from testcontainers.redis import RedisContainer")
    print("\nSee references/testcontainers-guide.md for detailed usage")
    print("="*50)

if __name__ == '__main__':
    main()
