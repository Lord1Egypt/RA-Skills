#!/usr/bin/env python3
"""
Setup script for Hikaru
Initializes database and checks dependencies
"""

import sys
import sqlite3
from pathlib import Path


def setup_database(data_dir):
    """Initialize the database"""
    print("Initializing database...")

    db_path = data_dir / "relationship.db"

    # Import memory system to use its initialization
    sys.path.insert(0, str(Path(__file__).parent))
    from memory import MemorySystem

    memory = MemorySystem(data_dir)
    print(f"✓ Database initialized at {db_path}")


def check_dependencies():
    """Check if required dependencies are available"""
    print("Checking dependencies...")

    try:
        import sqlite3
        print("✓ sqlite3 available")
    except ImportError:
        print("✗ sqlite3 not available")
        return False

    return True


def create_data_directory():
    """Create data directory if it doesn't exist"""
    data_dir = Path(__file__).parent.parent / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    print(f"✓ Data directory ready at {data_dir}")
    return data_dir


def main():
    print("=" * 50)
    print("Hikaru Setup")
    print("=" * 50)
    print()

    # Check dependencies
    if not check_dependencies():
        print("\n✗ Setup failed: Missing dependencies")
        return 1

    # Create data directory
    data_dir = create_data_directory()

    # Initialize database
    setup_database(data_dir)

    print()
    print("=" * 50)
    print("✓ Setup complete!")
    print("=" * 50)
    print()
    print("You can now start talking with Hikaru:")
    print("  ./scripts/hikaru.py -i")
    print()
    print("Or send a single message:")
    print('  ./scripts/hikaru.py "Hello Hikaru"')
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
