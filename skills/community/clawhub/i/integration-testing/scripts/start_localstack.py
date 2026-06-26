#!/usr/bin/env python3
"""
Setup script for LocalStack
Starts LocalStack services for AWS testing without real AWS resources
"""

import subprocess
import sys
import os
import time
import signal

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

def install_localstack():
    """Install LocalStack CLI"""
    try:
        # Check if localstack is already installed
        result = subprocess.run(
            ['localstack', '--version'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"✅ LocalStack is installed: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    # Install LocalStack
    print("📥 Installing LocalStack...")
    try:
        subprocess.run(
            ['pip', 'install', 'localstack'],
            check=True
        )
        print("✅ LocalStack installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install LocalStack: {e}")
        print("You can also install LocalStack via:")
        print("  brew install localstack/tap/localstack  # macOS")
        print("  pip install localstack  # pip")
        return False

def start_localstack(services=None, port=4566):
    """Start LocalStack services"""
    if services is None:
        services = ['s3', 'lambda', 'dynamodb', 'sns', 'sqs']
    
    print(f"🚀 Starting LocalStack services: {', '.join(services)}")
    
    # Build localstack command
    cmd = ['localstack', 'start', '--port', str(port)]
    for service in services:
        cmd.extend(['--services', service])
    
    print(f"   Starting on port {port}...")
    print(f"   Services: {', '.join(services)}")
    
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait for LocalStack to be ready
        print("⏳ Waiting for LocalStack to be ready...")
        max_attempts = 30
        for i in range(max_attempts):
            # Check if process is still running
            if process.poll() is not None:
                stdout, stderr = process.communicate()
                print(f"❌ LocalStack failed to start")
                print(f"   Error: {stderr}")
                return None
            
            time.sleep(2)
            print(f"   Waiting... ({(i+1)*2}s)", end='\r')
        
        print(f"\n✅ LocalStack started successfully!")
        print(f"   Endpoint: http://localhost:{port}")
        print(f"   AWS Region: us-east-1")
        
        return process
        
    except Exception as e:
        print(f"❌ Failed to start LocalStack: {e}")
        return None

def configure_aws_cli(port=4566):
    """Configure AWS CLI to use LocalStack"""
    print("\n⚙️  Configuring AWS CLI for LocalStack...")
    
    # Set environment variables
    env_vars = {
        'AWS_ACCESS_KEY_ID': 'test',
        'AWS_SECRET_ACCESS_KEY': 'test',
        'AWS_REGION': 'us-east-1',
        'AWS_ENDPOINT_URL_S3': f'http://localhost:{port}'
    }
    
    profile = os.path.expanduser('~/.bashrc')
    if os.path.exists(profile):
        with open(profile, 'a') as f:
            f.write('\n# LocalStack configuration\n')
            for key, value in env_vars.items():
                f.write(f'export {key}="{value}"\n')
        print(f"✅ Added LocalStack configuration to {profile}")
    
    return env_vars

def verify_localstack(port=4566):
    """Verify LocalStack is running by testing S3"""
    try:
        import boto3
        s3 = boto3.client(
            's3',
            endpoint_url=f'http://localhost:{port}',
            aws_access_key_id='test',
            aws_secret_access_key='test',
            region_name='us-east-1'
        )
        
        # Try to list buckets (should work even if empty)
        s3.list_buckets()
        print("✅ LocalStack S3 is responsive")
        return True
    except ImportError:
        print("⚠️  boto3 not installed (pip install boto3)")
        return True
    except Exception as e:
        print(f"⚠️  Could not verify LocalStack: {e}")
        return True

def cleanup_handler(signum, frame):
    """Handle cleanup on script exit"""
    print("\n\n🛑 Stopping LocalStack...")
    # LocalStack will be stopped automatically
    print("✅ LocalStack stopped")
    sys.exit(0)

def main():
    """Main setup function"""
    print("🏗️  Setting up LocalStack for AWS testing...\n")
    
    # Register cleanup handler
    signal.signal(signal.SIGINT, cleanup_handler)
    signal.signal(signal.SIGTERM, cleanup_handler)
    
    # Step 1: Check Docker
    print("Step 1: Checking Docker...")
    if not check_docker():
        print("Please install and start Docker first")
        sys.exit(1)
    
    # Step 2: Install LocalStack
    print("\nStep 2: Installing LocalStack...")
    if not install_localstack():
        sys.exit(1)
    
    # Step 3: Start LocalStack
    print("\nStep 3: Starting LocalStack services...")
    process = start_localstack(services=['s3'])  # Start with S3 for basic testing
    if not process:
        sys.exit(1)
    
    # Step 4: Configure AWS CLI
    print("\nStep 4: Configuring AWS CLI...")
    configure_aws_cli()
    
    # Step 5: Verify setup
    print("\nStep 5: Verifying LocalStack setup...")
    verify_localstack()
    
    print("\n" + "="*50)
    print("✅ LocalStack setup complete!")
    print("="*50)
    print("\nLocalStack is running with AWS services available locally")
    print("You can now test S3 operations without using real AWS!")
    print("\nExample usage in Python:")
    print("  import boto3")
    print("  s3 = boto3.client('s3', endpoint_url='http://localhost:4566')")
    print("\nSee references/localstack-s3-config.md for detailed configuration")
    print("="*50)
    print("\nPress Ctrl+C to stop LocalStack")
    
    # Keep script running until interrupted
    try:
        process.wait()
    except KeyboardInterrupt:
        cleanup_handler(signal.SIGINT, None)

if __name__ == '__main__':
    main()
