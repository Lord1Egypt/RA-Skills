# LocalStack S3 Configuration Guide

Complete guide for configuring and using LocalStack S3 for AWS integration testing.

## What is LocalStack?

LocalStack provides a local AWS cloud stack that simulates AWS services. It allows you to develop and test applications without using real AWS resources, avoiding costs and ensuring reproducible test environments.

## Key Benefits

- **Cost-free testing**: No AWS charges during development/testing
- **Fast feedback**: Local development without network latency
- **Reproducible tests**: Consistent environment across all developers
- **Offline testing**: Work without internet connectivity
- **Full S3 API coverage**: Most S3 operations supported

## Installation

### Using pip

```bash
pip install localstack
```

### Using Docker

```bash
docker pull localstack/localstack:latest
```

### Using Homebrew (macOS)

```bash
brew install localstack/tap/localstack
```

## Starting LocalStack

### Command Line

```bash
# Start with default services
localstack start

# Start with specific services
localstack start --services s3,lambda,dynamodb

# Start with custom port
localstack start --port 4566

# Start with debug output
localstack start --debug
```

### Using Python

```python
from localstack import start_localstack

def start_localstack_s3():
    # Start LocalStack with S3 service
    with start_localstack(services=["s3"]) as localstack:
        print(f"LocalStack running at {localstack.endpoint_url}")
        # Use localstack.endpoint_url for AWS clients
        pass
```

## Configuring AWS Clients

### Python (boto3)

```python
import boto3
from localstack import start_localstack

def configure_boto3_for_localstack():
    with start_localstack(services=["s3"]) as localstack:
        # Configure S3 client for LocalStack
        s3_client = boto3.client(
            's3',
            endpoint_url=localstack.endpoint_url,
            aws_access_key_id='test',  # Any value works
            aws_secret_access_key='test',  # Any value works
            region_name='us-east-1'  # LocalStack default region
        )
        
        # Now use s3_client as you would with real AWS
        return s3_client
```

### AWS CLI

```bash
# Set environment variables
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
export AWS_REGION=us-east-1
export AWS_ENDPOINT_URL_S3=http://localhost:4566

# Use AWS CLI commands
aws s3 ls
aws s3 mb s3://test-bucket
aws s3 cp file.txt s3://test-bucket/
```

### Environment Variables

```bash
# .bashrc or .zshrc
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
export AWS_REGION=us-east-1
export AWS_ENDPOINT_URL_S3=http://localhost:4566

# Or use LocalStack CLI to configure
localstack configure aws
```

## S3 Operations

### Bucket Operations

```python
def test_bucket_operations():
    s3_client = configure_boto3_for_localstack()
    
    # Create bucket
    bucket_name = 'test-bucket'
    s3_client.create_bucket(Bucket=bucket_name)
    
    # List buckets
    buckets = s3_client.list_buckets()
    assert bucket_name in [b['Name'] for b in buckets['Buckets']]
    
    # Delete bucket
    s3_client.delete_bucket(Bucket=bucket_name)
```

### Object Operations

```python
def test_object_operations():
    s3_client = configure_boto3_for_localstack()
    bucket_name = 'test-bucket'
    s3_client.create_bucket(Bucket=bucket_name)
    
    # Upload object
    file_content = b'Hello, LocalStack S3!'
    s3_client.put_object(
        Bucket=bucket_name,
        Key='test-file.txt',
        Body=file_content,
        ContentType='text/plain'
    )
    
    # List objects
    objects = s3_client.list_objects_v2(Bucket=bucket_name)
    assert len(objects['Contents']) == 1
    
    # Download object
    obj = s3_client.get_object(Bucket=bucket_name, Key='test-file.txt')
    downloaded_content = obj['Body'].read()
    assert downloaded_content == file_content
    
    # Get object metadata
    metadata = s3_client.head_object(Bucket=bucket_name, Key='test-file.txt')
    assert metadata['ContentType'] == 'text/plain'
    
    # Delete object
    s3_client.delete_object(Bucket=bucket_name, Key='test-file.txt')
    s3_client.delete_bucket(Bucket=bucket_name)
```

### Large File Uploads

```python
def test_large_file_upload():
    s3_client = configure_boto3_for_localstack()
    bucket_name = 'large-files'
    s3_client.create_bucket(Bucket=bucket_name)
    
    # Use multipart upload for large files
    import os
    
    large_file_size = 100 * 1024 * 1024  # 100 MB
    large_file_content = b'x' * large_file_size
    
    # Upload with multipart
    multipart_upload = s3_client.create_multipart_upload(
        Bucket=bucket_name,
        Key='large-file.bin'
    )
    
    upload_id = multipart_upload['UploadId']
    
    # Upload in parts
    part_size = 10 * 1024 * 1024  # 10 MB parts
    parts = []
    
    for i, offset in enumerate(range(0, large_file_size, part_size), 1):
        part_data = large_file_content[offset:offset + part_size]
        part = s3_client.upload_part(
            Bucket=bucket_name,
            Key='large-file.bin',
            PartNumber=i,
            UploadId=upload_id,
            Body=part_data
        )
        parts.append({'PartNumber': i, 'ETag': part['ETag']})
    
    # Complete multipart upload
    s3_client.complete_multipart_upload(
        Bucket=bucket_name,
        Key='large-file.bin',
        UploadId=upload_id,
        MultipartUpload={'Parts': parts}
    )
    
    # Verify upload
    obj = s3_client.head_object(Bucket=bucket_name, Key='large-file.bin')
    assert obj['ContentLength'] == large_file_size
```

### Presigned URLs

```python
def test_presigned_urls():
    s3_client = configure_boto3_for_localstack()
    bucket_name = 'presigned-test'
    s3_client.create_bucket(Bucket=bucket_name)
    
    # Upload test file
    s3_client.put_object(
        Bucket=bucket_name,
        Key='public-file.txt',
        Body=b'public content'
    )
    
    # Generate presigned URL (GET)
    get_url = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket_name, 'Key': 'public-file.txt'},
        ExpiresIn=3600  # 1 hour
    )
    
    # Test presigned URL
    import requests
    response = requests.get(get_url)
    assert response.status_code == 200
    assert response.content == b'public content'
    
    # Generate presigned URL (PUT)
    put_url = s3_client.generate_presigned_url(
        'put_object',
        Params={'Bucket': bucket_name, 'Key': 'upload-file.txt'},
        ExpiresIn=3600
    )
    
    # Upload via presigned URL
    response = requests.put(put_url, data=b'uploaded content')
    assert response.status_code == 200
```

## Advanced Configuration

### Custom Port

```python
def test_custom_port():
    from localstack import start_localstack
    
    # Start LocalStack on custom port
    with start_localstack(services=["s3"], port=4567) as localstack:
        print(f"LocalStack running on port {localstack.port}")
        
        s3_client = boto3.client(
            's3',
            endpoint_url=f"http://localhost:{localstack.port}",
            aws_access_key_id='test',
            aws_secret_access_key='test',
            region_name='us-east-1'
        )
        # Use s3_client
        pass
```

### Multiple Services

```python
def test_multiple_services():
    from localstack import start_localstack
    
    # Start multiple AWS services
    with start_localstack(services=["s3", "lambda", "dynamodb"]) as localstack:
        # Configure different AWS clients
        s3_client = boto3.client(
            's3',
            endpoint_url=localstack.endpoint_url,
            aws_access_key_id='test',
            aws_secret_access_key='test',
            region_name='us-east-1'
        )
        
        dynamo_client = boto3.client(
            'dynamodb',
            endpoint_url=localstack.endpoint_url,
            aws_access_key_id='test',
            aws_secret_access_key='test',
            region_name='us-east-1'
        )
        
        # Use both clients
        pass
```

### Persistence

```python
def test_persistent_localstack():
    # Start LocalStack with persistence (Docker volume)
    # This keeps data between restarts
    import subprocess
    
    subprocess.run([
        'localstack', 'start',
        '--services', 's3',
        '--volume', '/tmp/localstack-data'
    ], check=True)
    
    # LocalStack data persists in /tmp/localstack-data
```

## Error Handling

### S3 Errors

```python
def test_s3_error_handling():
    s3_client = configure_boto3_for_localstack()
    
    # Test bucket not found
    try:
        s3_client.get_object(Bucket='nonexistent', Key='file.txt')
        assert False, "Should have raised exception"
    except s3_client.exceptions.NoSuchBucket:
        print("Correctly handled bucket not found")
    
    # Test key not found
    bucket_name = 'test-bucket'
    s3_client.create_bucket(Bucket=bucket_name)
    
    try:
        s3_client.get_object(Bucket=bucket_name, Key='nonexistent.txt')
        assert False, "Should have raised exception"
    except s3_client.exceptions.NoSuchKey:
        print("Correctly handled key not found")
    
    s3_client.delete_bucket(Bucket=bucket_name)
```

### Connection Errors

```python
def test_connection_errors():
    try:
        # Try to connect without starting LocalStack
        s3_client = boto3.client(
            's3',
            endpoint_url='http://localhost:4566',
            aws_access_key_id='test',
            aws_secret_access_key='test',
            region_name='us-east-1'
        )
        
        # This should fail if LocalStack is not running
        s3_client.list_buckets()
        
    except Exception as e:
        print(f"Connection error: {e}")
        print("Make sure LocalStack is running: localstack start")
```

## Best Practices

### 1. Use Context Managers

```python
# ✅ Good - automatic cleanup
with start_localstack(services=["s3"]) as localstack:
    s3_client = boto3.client(
        's3',
        endpoint_url=localstack.endpoint_url,
        aws_access_key_id='test',
        aws_secret_access_key='test',
        region_name='us-east-1'
    )
    # Use s3_client
    pass
```

### 2. Use Fixtures in Tests

```python
import pytest
from localstack import start_localstack

@pytest.fixture(scope="session")
def localstack_s3():
    with start_localstack(services=["s3"]) as localstack:
        yield localstack

@pytest.fixture
def s3_client(localstack_s3):
    return boto3.client(
        's3',
        endpoint_url=localstack_s3.endpoint_url,
        aws_access_key_id='test',
        aws_secret_access_key='test',
        region_name='us-east-1'
    )

def test_s3_operations(s3_client):
    # Use s3_client in tests
    pass
```

### 3. Clean Up Resources

```python
def test_cleanup():
    s3_client = configure_boto3_for_localstack()
    bucket_name = 'cleanup-test'
    
    try:
        s3_client.create_bucket(Bucket=bucket_name)
        # Perform tests
        
    finally:
        # Always cleanup, even if tests fail
        try:
            # Delete all objects
            objects = s3_client.list_objects_v2(Bucket=bucket_name)
            for obj in objects.get('Contents', []):
                s3_client.delete_object(
                    Bucket=bucket_name,
                    Key=obj['Key']
                )
        except Exception:
            pass
        
        try:
            s3_client.delete_bucket(Bucket=bucket_name)
        except Exception:
            pass
```

## Troubleshooting

### LocalStack Won't Start

1. Check Docker is running: `docker ps`
2. Check port conflicts: `netstat -an | grep 4566`
3. Check logs: `localstack logs`

### S3 Operations Fail

1. Verify endpoint URL is correct
2. Check LocalStack is running
3. Review LocalStack logs: `localstack logs`
4. Test with AWS CLI: `aws s3 ls`

### Performance Issues

- Use in-memory persistence for tests
- Avoid uploading large files unless necessary
- Restart LocalStack between test suites
- Use specific services only: `--services s3`

## Further Reading

- [Official LocalStack Documentation](https://docs.localstack.cloud/)
- [LocalStack S3 Features](https://docs.localstack.cloud/aws/s3/)
- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/)
- [Boto3 S3 Client](https://boto3.amazonaws.com/v1/documentation/api/s3.html)
