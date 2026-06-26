# Testcontainers Guide

Comprehensive guide for using testcontainers in integration testing.

## What is Testcontainers?

Testcontainers is a library that provides lightweight, throwaway instances of databases, message brokers, web browsers, or almost anything that can run in a Docker container.

## Key Benefits

- **Real services in isolation**: Test against real dependencies, not mocks
- **Disposable environments**: Every test gets a clean, fresh environment
- **Parallel testing**: Run tests in parallel without conflicts
- **Team consistency**: Same test environment for everyone

## Installation

```bash
pip install testcontainers
```

Or with extra dependencies:

```bash
pip install testcontainers[postgresql,redis,mongodb]
```

## Common Containers

### PostgreSQL

```python
from testcontainers.postgres import PostgresContainer

def test_with_postgres():
    with PostgresContainer("postgres:15") as postgres:
        connection_url = postgres.get_connection_url()
        # Use connection_url in your tests
        # postgresql://test_user:test_pass@host:port/db_name
```

### MySQL

```python
from testcontainers.mysql import MySqlContainer

def test_with_mysql():
    with MySqlContainer("mysql:8.0") as mysql:
        connection_url = mysql.get_connection_url()
        # mysql://test_user:test_pass@host:port/db_name
```

### Redis

```python
from testcontainers.redis import RedisContainer

def test_with_redis():
    with RedisContainer("redis:7-alpine") as redis:
        host = redis.get_container_host_ip()
        port = redis.get_container_port(6379)
        # Connect to Redis at host:port
```

### MongoDB

```python
from testcontainers.mongodb import MongoDbContainer

def test_with_mongodb():
    with MongoDbContainer("mongo:6.0") as mongo:
        connection_url = mongo.get_connection_url()
        # mongodb://host:port/db_name
```

### Generic Docker Container

```python
from testcontainers.core.container import DockerContainer

def test_with_custom_image():
    with DockerContainer("nginx:latest") as nginx:
        host = nginx.get_container_host_ip()
        port = nginx.get_container_port(80)
        # Use host:port to access the container
```

## Advanced Configuration

### Custom Configuration

```python
from testcontainers.postgres import PostgresContainer

def test_custom_config():
    with PostgresContainer("postgres:15") \
            .with_name("custom-postgres") \
            .with_env("POSTGRES_PASSWORD", "custom_password") \
            .with_bind_ports(8432, 5432) \
            .with_exposed_ports(5432) as postgres:
        connection_url = postgres.get_connection_url()
```

### Volume Mounts

```python
def test_with_volume():
    with DockerContainer("nginx:latest") \
            .with_volume_mapping("./html", "/usr/share/nginx/html") \
            .with_bind_ports(8080, 80) as nginx:
        # Custom HTML content will be served
        pass
```

### Network Configuration

```python
from testcontainers.core.docker_client import DockerClient

def test_with_network():
    client = DockerClient()
    network = client.client.networks.create("test-network")
    
    with DockerContainer("nginx:latest") \
            .with_network(network.name) \
            .with_network_aliases("web") as nginx:
        # Container is in custom network
        pass
    
    network.remove()
```

## Best Practices

### 1. Always Use Context Managers

```python
# ✅ Good - automatic cleanup
with PostgresContainer("postgres:15") as postgres:
    # Use postgres
    pass

# ❌ Bad - manual cleanup required
postgres = PostgresContainer("postgres:15")
postgres.start()
try:
    # Use postgres
    pass
finally:
    postgres.stop()
```

### 2. Handle Container Startup Time

```python
import time
from testcontainers.core.container import DockerContainer

def test_with_slow_service():
    with DockerContainer("slow-service:latest") as container:
        # Wait for service to be ready
        time.sleep(5)  # Or use proper health checks
        
        # Or use wait_for_logs
        container._container.wait(until=container._container.is_running)
```

### 3. Resource Limits

```python
def test_with_resource_limits():
    with PostgresContainer("postgres:15") \
            .with_mem_limit("512m") \
            .with_cpu_quota(1024) as postgres:
        # Container has limited resources
        pass
```

### 4. Custom Images

```python
def test_with_custom_image():
    # Build custom image during tests
    from testcontainers.core.docker_client import DockerClient
    
    client = DockerClient()
    image, build_logs = client.client.images.build(
        path="./docker/",
        tag="my-custom-app:latest"
    )
    
    with DockerContainer("my-custom-app:latest") as app:
        # Use custom built image
        pass
```

## Integration with Test Frameworks

### pytest

```python
import pytest
from testcontainers.postgres import PostgresContainer

@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:15") as postgres:
        yield postgres

@pytest.fixture
def db_connection(postgres_container):
    # Create new connection for each test
    import psycopg2
    conn = psycopg2.connect(postgres_container.get_connection_url())
    yield conn
    conn.close()

def test_database_operation(db_connection):
    # Use db_connection in tests
    cursor = db_connection.cursor()
    cursor.execute("SELECT 1")
    assert cursor.fetchone()[0] == 1
```

### unittest

```python
import unittest
from testcontainers.redis import RedisContainer

class RedisIntegrationTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.redis = RedisContainer("redis:7-alpine")
        cls.redis.start()
    
    @classmethod
    def tearDownClass(cls):
        cls.redis.stop()
    
    def test_redis_connection(self):
        import redis as redis_client
        r = redis_client.Redis(
            host=self.redis.get_container_host_ip(),
            port=self.redis.get_container_port(6379)
        )
        r.set("test", "value")
        assert r.get("test") == b"value"
```

## Troubleshooting

### Container Won't Start

1. Check Docker is running: `docker ps`
2. Check logs: `docker logs <container-id>`
3. Verify image exists: `docker images`

### Port Conflicts

- Testcontainers automatically assigns available ports
- Use `get_container_port()` to get actual port
- Don't hardcode ports in tests

### Performance Issues

- Reuse containers across tests with fixtures
- Use lighter images (alpine, slim)
- Limit resource usage for heavy tests

## Further Reading

- [Official Testcontainers Python Docs](https://testcontainers-python.readthedocs.io/)
- [Testcontainers Examples](https://github.com/testcontainers/testcontainers-python/tree/master/examples)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
