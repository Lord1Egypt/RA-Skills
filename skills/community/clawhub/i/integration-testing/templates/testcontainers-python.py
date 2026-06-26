"""
Testcontainers Python Template
Basic example for integration testing with PostgreSQL using testcontainers

⚠️ SECURITY WARNING: This code is for INTEGRATION TESTING ONLY
- Containers are isolated and destroyed after testing
- Never expose test containers to untrusted networks
- Use official Docker images only
- Monitor resource usage in CI/CD environments
"""

from testcontainers.postgres import PostgresContainer
import psycopg2
from psycopg2 import sql

def test_database_integration():
    """Example: Test application with real PostgreSQL container"""
    
    # Start PostgreSQL container
    with PostgresContainer("postgres:15") as postgres:
        # Get connection string from container
        connection_url = postgres.get_connection_url()
        
        # Test database operations
        conn = psycopg2.connect(connection_url)
        cursor = conn.cursor()
        
        # Create test table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL
            )
        """)
        
        # Insert test data
        cursor.execute(
            "INSERT INTO users (name, email) VALUES (%s, %s)",
            ("Test User", "test@example.com")
        )
        
        # Query test data
        cursor.execute("SELECT * FROM users WHERE name = %s", ("Test User",))
        result = cursor.fetchone()
        
        assert result[1] == "Test User"
        assert result[2] == "test@example.com"
        
        # Cleanup
        cursor.close()
        conn.close()
        print("✅ Database integration test passed!")

# Usage in pytest:
# def test_with_postgres(test_database_integration):
#     test_database_integration()
