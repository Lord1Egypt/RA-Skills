#!/usr/bin/env python3
"""
Setup script for WireMock
Initializes and starts WireMock server for API mocking
"""

import subprocess
import sys
import os
import time
import requests

def check_java():
    """Check if Java is available (WireMock requires Java)"""
    try:
        result = subprocess.run(
            ['java', '-version'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("✅ Java is available")
            return True
        else:
            print("❌ Java is not available")
            return False
    except FileNotFoundError:
        print("❌ Java is not installed")
        return False

def download_wiremock():
    """Download WireMock standalone JAR if not present"""
    wiremock_version = "3.5.2"  # Latest stable version
    wiremock_jar = f"wiremock-standalone-{wiremock_version}.jar"
    wiremock_url = f"https://repo1.maven.org/maven2/org/wiremock/wiremock-standalone/{wiremock_version}/{wiremock_jar}"
    
    if os.path.exists(wiremock_jar):
        print(f"✅ WireMock JAR already exists: {wiremock_jar}")
        return wiremock_jar
    
    print(f"📥 Downloading WireMock {wiremock_version}...")
    try:
        subprocess.run(
            ['curl', '-L', '-o', wiremock_jar, wiremock_url],
            check=True
        )
        print(f"✅ Downloaded {wiremock_jar}")
        return wiremock_jar
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to download WireMock: {e}")
        return None

def start_wiremock(jar_path, port=8080):
    """Start WireMock server"""
    print(f"🚀 Starting WireMock server on port {port}...")
    
    # Check if port is already in use
    try:
        response = requests.get(f"http://localhost:{port}/__admin")
        print(f"⚠️  Port {port} is already in use")
        return None
    except requests.exceptions.ConnectionError:
        pass  # Port is available
    
    # Start WireMock
    try:
        process = subprocess.Popen(
            ['java', '-jar', jar_path, '--port', str(port)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for server to start
        max_attempts = 10
        for i in range(max_attempts):
            try:
                response = requests.get(f"http://localhost:{port}/__admin")
                if response.status_code == 200:
                    print(f"✅ WireMock server started on port {port}")
                    print(f"   Admin UI: http://localhost:{port}/__admin")
                    return process
            except requests.exceptions.ConnectionError:
                time.sleep(0.5)
        
        print(f"❌ WireMock failed to start within {max_attempts * 0.5} seconds")
        process.terminate()
        return None
        
    except Exception as e:
        print(f"❌ Failed to start WireMock: {e}")
        return None

def verify_wiremock(port=8080):
    """Verify WireMock is running"""
    try:
        response = requests.get(f"http://localhost:{port}/__admin/mappings")
        if response.status_code == 200:
            print("✅ WireMock API is responsive")
            return True
        return False
    except requests.exceptions.ConnectionError:
        return False

def main():
    """Main initialization function"""
    print("🔧 Setting up WireMock for API mocking...\n")
    
    # Step 1: Check Java
    print("Step 1: Checking Java...")
    if not check_java():
        print("Please install Java first (WireMock requires Java 8+)")
        sys.exit(1)
    
    # Step 2: Download WireMock
    print("\nStep 2: Downloading WireMock...")
    jar_path = download_wiremock()
    if not jar_path:
        sys.exit(1)
    
    # Step 3: Start WireMock
    print("\nStep 3: Starting WireMock server...")
    process = start_wiremock(jar_path)
    if not process:
        sys.exit(1)
    
    # Step 4: Verify setup
    print("\nStep 4: Verifying WireMock setup...")
    if verify_wiremock():
        print("\n" + "="*50)
        print("✅ WireMock setup complete!")
        print("="*50)
        print("\nWireMock server is running at http://localhost:8080")
        print("Admin UI available at http://localhost:8080/__admin")
        print("\nYou can now use WireMock in your tests:")
        print("  from wiremock import WireMockServer")
        print("\nSee references/wiremock-patterns.md for usage examples")
        print("="*50)
        print("\nPress Ctrl+C to stop the WireMock server")
        
        try:
            # Keep script running until interrupted
            process.wait()
        except KeyboardInterrupt:
            print("\n\n🛑 Stopping WireMock server...")
            process.terminate()
            process.wait()
            print("✅ WireMock server stopped")
    else:
        print("❌ WireMock verification failed")
        process.terminate()
        sys.exit(1)

if __name__ == '__main__':
    main()
