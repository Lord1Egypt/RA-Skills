"""
SFTP Integration Testing Template
Example for testing SFTP server connectivity and file operations

⚠️ SECURITY WARNING: This code is for INTEGRATION TESTING ONLY
- Never use in production environments
- Never use hardcoded credentials in real applications
- These patterns are strictly for isolated testing environments
- Use environment variables or secret management for credentials in production
"""

import paramiko
import tempfile
import os

def test_sftp_basic_operations():
    """Example: Test basic SFTP connectivity and operations"""
    
    # Note: This assumes a test SFTP server is available
    # In production, you might want to use a containerized SFTP server
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        # Connect to SFTP server
        ssh.connect(
            hostname='sftp-test-server',
            port=2222,
            username='testuser',
            password='testpass',
            timeout=10
        )
        
        # Open SFTP channel
        sftp = ssh.open_sftp()
        
        # Create test directory
        test_dir = '/test/integration_test'
        try:
            sftp.mkdir(test_dir)
        except IOError:
            pass  # Directory might already exist
        
        # Create and upload test file
        test_file = os.path.join(test_dir, 'test_file.txt')
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
            tmp.write('Test SFTP content')
            tmp_path = tmp.name
        
        try:
            sftp.put(tmp_path, test_file)
            
            # Verify file exists
            file_attrs = sftp.stat(test_file)
            assert file_attrs.st_size > 0
            
            # Download and verify content
            with tempfile.NamedTemporaryFile(mode='w', delete=False) as download_tmp:
                download_path = download_tmp.name
            
            sftp.get(test_file, download_path)
            
            with open(download_path, 'r') as f:
                content = f.read()
                assert content == 'Test SFTP content'
            
            # List files in test directory
            files = sftp.listdir(test_dir)
            assert 'test_file.txt' in files
            
            # Delete test file
            sftp.remove(test_file)
            
            # Delete test directory
            sftp.rmdir(test_dir)
            
            print("✅ SFTP basic operations test passed!")
            
        finally:
            # Cleanup temp files
            os.unlink(tmp_path)
            if os.path.exists(download_path):
                os.unlink(download_path)
                
    finally:
        ssh.close()

def test_sftp_error_handling():
    """Example: Test error handling for SFTP operations"""
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        # Test connection failure handling
        try:
            ssh.connect(
                hostname='invalid-host',
                port=2222,
                username='testuser',
                password='testpass',
                timeout=5
            )
            assert False, "Should have failed to connect"
        except (paramiko.AuthenticationException, 
                paramiko.SSHException, 
                TimeoutError):
            print("✅ Connection error handling test passed!")
            
    finally:
        if ssh.get_transport() is not None:
            ssh.close()

# Setup script for test SFTP server (using docker)
# This can be used in CI/CD pipelines
def setup_test_sftp_server():
    """
    Setup a test SFTP server using Docker
    Example for CI/CD integration
    """
    import subprocess
    
    # Start test SFTP server container
    cmd = [
        'docker', 'run', '-d',
        '--name', 'test-sftp-server',
        '-p', '2222:22',
        '-e', 'SFTP_USER=testuser',
        '-e', 'SFTP_PASSWORD=testpass',
        'atmoz/sftp:alpine'
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("✅ Test SFTP server started!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start SFTP server: {e}")
        return False
