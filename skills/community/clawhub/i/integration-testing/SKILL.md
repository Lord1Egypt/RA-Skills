---
name: integration-testing
description: Automated integration testing with external services using testcontainers, wiremock, localstack. Use when developer needs to set up integration tests for testing with real services in Docker containers via testcontainers, mocking HTTP APIs with WireMock, testing AWS S3 with LocalStack, SFTP integration testing, or setting up complex integration test environments with external dependencies.
---

# Integration Testing with External Services

## Quick Start

This skill helps you set up integration tests with external services:

- **Testcontainers**: Run real services in Docker containers for testing
- **WireMock**: Mock HTTP services and APIs
- **LocalStack**: Local AWS services (S3) for testing without AWS dependency
- **SFTP**: Integration testing with SFTP servers

## When to Use This Skill

Use this skill when you need to:
- Set up integration tests with external services
- Test applications against real databases/message queues in isolation
- Mock HTTP APIs for reliable testing
- Test S3 integration without using real AWS resources
- Configure automated integration test environments

## Setup Options

### Testcontainers Setup

For integration tests with real services:

```python
# Basic testcontainers example
from testcontainers.postgres import PostgresContainer

def test_with_postgres():
    with PostgresContainer("postgres:15") as postgres:
        connection_string = postgres.get_connection_url()
        # Run tests with real PostgreSQL
```

See [testcontainers-guide.md](references/testcontainers-guide.md) for detailed setup.

### WireMock Setup

For mocking HTTP services:

```python
# WireMock configuration example
from wiremock import WireMockServer

def test_with_wiremock():
    with WireMockServer() as wiremock:
        wiremock.stub_for(
            request_method="GET",
            request_url="/api/users",
            response_body='{"users": []}'
        )
        # Test against mocked API
```

See [wiremock-patterns.md](references/wiremock-patterns.md) for common patterns.

### LocalStack Setup

For testing S3 without AWS:

```python
# LocalStack S3 testing example
import boto3
from localstack import start_localstack

def test_s3_with_localstack():
    with start_localstack(services=["s3"]) as localstack:
        s3 = boto3.client('s3', endpoint_url=localstack.endpoint_url)
        # Test S3 operations locally
```

See [localstack-s3-config.md](references/localstack-s3-config.md) for S3 configuration.

### SFTP Integration Testing

For testing SFTP connectivity and operations:

```python
# SFTP integration test example
from paramiko import SSHClient

def test_sftp_operations():
    with SSHClient() as ssh:
        ssh.connect('sftp-server', username='test', password='test')
        sftp = ssh.open_sftp()
        # Test SFTP file operations
```

## Available Templates

Ready-to-use test templates for common scenarios:

- `templates/testcontainers-python.py` - Python testcontainers setup
- `templates/wiremock-http-tests.py` - WireMock HTTP API tests
- `templates/localstack-s33-tests.py` - LocalStack S3 integration tests
- `templates/sftp-integration-tests.py` - SFTP integration testing

## Helper Scripts

Setup scripts to initialize test environments:

- `scripts/setup_testcontainers.py` - Configure testcontainers environment
- `scripts/init_wiremock.py` - Initialize WireMock server
- `scripts/start_localstack.py` - Start LocalStack services

## Best Practices

1. **Container Management**: Always use context managers for container lifecycle
2. **Port Conflicts**: Configure ports to avoid conflicts with local services
3. **Cleanup**: Ensure proper cleanup of resources in test teardown
4. **Environment Variables**: Use env vars for configuration, avoid hardcoded values
5. **Parallel Testing**: Design tests to run in parallel where possible

## Getting Help

For detailed setup and patterns, see:
- [Testcontainers Guide](references/testcontainers-guide.md)
- [WireMock Patterns](references/wiremock-patterns.md)  
- [LocalStack S3 Config](references/localstack-s3-config.md)

## Security & Compliance

This skill is designed **SOLELY for legitimate integration testing purposes** in isolated development environments.

### ⚠️ Important Security Notes

- **Development Use Only**: Never deploy test containers or services to production networks
- **Isolated Environments**: All services run locally and are destroyed after testing
- **Educational Purpose**: Designed to teach proper testing methodologies
- **Full Transparency**: Source code is fully visible and auditable

For detailed security information, see [SECURITY.md](SECURITY.md)
