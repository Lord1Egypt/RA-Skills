"""
LocalStack S3 Testing Template
Example for testing S3 integration without using real AWS resources

⚠️ SECURITY WARNING: This code is for INTEGRATION TESTING ONLY
- LocalStack services run locally and are isolated
- Never use for production data storage
- Use actual AWS services or managed alternatives for production
- Follow AWS security best practices in production environments
"""

import boto3
from localstack import start_localstack
import os

def test_s3_operations():
    """Example: Test S3 operations using LocalStack"""
    
    # Start LocalStack with S3 service
    with start_localstack(services=["s3"]) as localstack:
        # Configure S3 client to use LocalStack
        s3_client = boto3.client(
            's3',
            endpoint_url=localstack.endpoint_url,
            aws_access_key_id='test',
            aws_secret_access_key='test',
            region_name='us-east-1'
        )
        
        # Create test bucket
        bucket_name = 'test-bucket'
        s3_client.create_bucket(Bucket=bucket_name)
        
        # Upload test file
        test_content = b'Hello, LocalStack S3!'
        s3_client.put_object(
            Bucket=bucket_name,
            Key='test-file.txt',
            Body=test_content
        )
        
        # List objects
        objects = s3_client.list_objects_v2(Bucket=bucket_name)
        assert len(objects['Contents']) == 1
        assert objects['Contents'][0]['Key'] == 'test-file.txt'
        
        # Download and verify
        obj = s3_client.get_object(Bucket=bucket_name, Key='test-file.txt')
        downloaded_content = obj['Body'].read()
        assert downloaded_content == test_content
        
        # Delete object
        s3_client.delete_object(Bucket=bucket_name, Key='test-file.txt')
        
        # Delete bucket
        s3_client.delete_bucket(Bucket=bucket_name)
        
        print("✅ S3 integration test passed!")

def test_s3_file_operations():
    """Example: Test more complex S3 file operations"""
    
    with start_localstack(services=["s3"]) as localstack:
        s3_client = boto3.client(
            's3',
            endpoint_url=localstack.endpoint_url,
            aws_access_key_id='test',
            aws_secret_access_key='test',
            region_name='us-east-1'
        )
        
        bucket_name = 'file-operations-bucket'
        s3_client.create_bucket(Bucket=bucket_name)
        
        # Upload multiple files
        test_files = {
            'file1.txt': b'Content 1',
            'file2.txt': b'Content 2',
            'subdir/file3.txt': b'Content 3'
        }
        
        for key, content in test_files.items():
            s3_client.put_object(
                Bucket=bucket_name,
                Key=key,
                Body=content
            )
        
        # List all objects (including subdirectory)
        all_objects = s3_client.list_objects_v2(Bucket=bucket_name)
        assert len(all_objects['Contents']) == 3
        
        # Test pagination
        paginator = s3_client.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=bucket_name)
        total_count = sum(1 for page in pages for _ in page['Contents'])
        assert total_count == 3
        
        # Cleanup
        for key in test_files.keys():
            s3_client.delete_object(Bucket=bucket_name, Key=key)
        s3_client.delete_bucket(Bucket=bucket_name)
        
        print("✅ S3 file operations test passed!")
