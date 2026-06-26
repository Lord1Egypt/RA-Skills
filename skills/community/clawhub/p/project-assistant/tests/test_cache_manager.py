"""
Tests for CacheManager
"""

import os
import sys
import json
import time
from pathlib import Path
import pytest

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'tools' / 'init'))

from utils.cache_manager import CacheManager, CacheConfig, CacheEntry


class TestCacheManager:
    """Test cases for CacheManager"""

    def test_load_empty_cache(self, temp_project_dir: Path):
        """Test loading cache when it doesn't exist"""
        manager = CacheManager(str(temp_project_dir))
        cache = manager.load()

        assert cache.timestamp == ''
        assert cache.version == '1.0'

    def test_save_and_load_cache(self, temp_project_dir: Path):
        """Test saving and loading cache"""
        manager = CacheManager(str(temp_project_dir))

        # Save cache
        cache = manager.load()
        cache.timestamp = '2024-01-01T00:00:00'
        manager._dirty = True
        manager.save()

        # Load again
        manager2 = CacheManager(str(temp_project_dir))
        loaded_cache = manager2.load()

        assert loaded_cache.timestamp == '2024-01-01T00:00:00'

    def test_clear_cache(self, temp_project_dir: Path):
        """Test clearing cache"""
        manager = CacheManager(str(temp_project_dir))

        # Create and save cache
        manager.load()
        manager._dirty = True
        manager.save()

        # Clear cache
        manager.clear()

        # Cache file should be gone
        assert not manager.cache_path.exists()

    def test_compute_file_hash(self, temp_project_dir: Path):
        """Test file hash computation"""
        # Create a test file
        test_file = temp_project_dir / 'test.txt'
        test_file.write_text('test content')

        manager = CacheManager(str(temp_project_dir))
        hash1 = manager.compute_file_hash(test_file)
        hash2 = manager.compute_file_hash(test_file)

        assert hash1 == hash2
        assert len(hash1) == 32  # MD5 hex length

    def test_compute_project_hashes(self, sample_python_project: Path):
        """Test project hashes computation"""
        manager = CacheManager(str(sample_python_project))
        hashes = manager.compute_project_hashes()

        # Should have hashes for existing config files
        assert 'requirements.txt' in hashes or 'pyproject.toml' in hashes

    def test_check_validity_no_cache(self, temp_project_dir: Path):
        """Test validity check when no cache exists"""
        manager = CacheManager(str(temp_project_dir))
        result = manager.check_validity()

        assert result['cache_exists'] is False
        assert result['needs_update'] is True

    def test_check_validity_quick_mode(self, sample_python_project: Path):
        """Test quick validity check"""
        manager = CacheManager(str(sample_python_project))

        # Create cache
        manager.update()

        # Quick check
        result = manager.check_validity(quick=True)

        assert result['cache_exists'] is True

    def test_update_cache(self, sample_python_project: Path):
        """Test cache update"""
        manager = CacheManager(str(sample_python_project))

        cache = manager.update()

        assert cache.timestamp != ''
        assert len(cache.file_hashes) > 0

    def test_analysis_cache(self, temp_project_dir: Path):
        """Test analysis cache operations"""
        manager = CacheManager(str(temp_project_dir))

        # Set analysis cache
        manager.set_analysis_cache('test_key', {'data': 'value'})

        # Get analysis cache
        value = manager.get_analysis_cache('test_key')

        assert value == {'data': 'value'}

    def test_metadata_operations(self, temp_project_dir: Path):
        """Test metadata operations"""
        manager = CacheManager(str(temp_project_dir))

        # Set metadata
        manager.set_metadata('project_name', 'TestProject')
        manager.set_metadata('version', '1.0.0')

        # Get metadata
        assert manager.get_metadata('project_name') == 'TestProject'
        assert manager.get_metadata('version') == '1.0.0'

    def test_subsystem_cache(self, temp_project_dir: Path):
        """Test subsystem cache management"""
        manager = CacheManager(str(temp_project_dir))

        # Mark subsystem as analyzed
        manager.mark_subsystem_analyzed('vehicle')

        # Check if analyzed
        assert manager.is_subsystem_analyzed('vehicle') is True
        assert manager.is_subsystem_analyzed('infotainment') is False

    def test_process_cache(self, temp_project_dir: Path):
        """Test process cache management"""
        manager = CacheManager(str(temp_project_dir))

        # Mark process as analyzed
        manager.mark_process_analyzed('main_process')

        cache = manager.load()
        assert 'main_process' in cache.processes

    def test_incremental_update(self, sample_python_project: Path):
        """Test incremental cache update"""
        manager = CacheManager(str(sample_python_project))

        # Initial update
        manager.set_analysis_cache('old_key', 'old_value')
        manager.save()

        # Incremental update
        manager.update(analysis_data={'new_key': 'new_value'}, incremental=True)

        # Both keys should exist
        assert manager.get_analysis_cache('old_key') == 'old_value'
        assert manager.get_analysis_cache('new_key') == 'new_value'


class TestCacheConfig:
    """Test cases for CacheConfig"""

    def test_default_config(self):
        """Test default configuration"""
        config = CacheConfig()

        assert config.default_ttl == 3600
        assert config.max_cache_size == 100 * 1024 * 1024
        assert config.lazy_check is True
        assert config.incremental_update is True

    def test_custom_config(self):
        """Test custom configuration"""
        config = CacheConfig(
            default_ttl=7200,
            max_cache_size=200 * 1024 * 1024,
            lazy_check=False
        )

        assert config.default_ttl == 7200
        assert config.max_cache_size == 200 * 1024 * 1024
        assert config.lazy_check is False


class TestCacheEntry:
    """Test cases for CacheEntry"""

    def test_default_values(self):
        """Test default values of CacheEntry"""
        entry = CacheEntry()

        assert entry.version == '1.0'
        assert entry.timestamp == ''
        assert entry.project_hash == ''
        assert entry.file_hashes == {}
        assert entry.scale == 'small'

    def test_custom_values(self):
        """Test custom values of CacheEntry"""
        entry = CacheEntry(
            version='2.0',
            timestamp='2024-01-01T00:00:00',
            scale='large',
            subsystems=['vehicle', 'infotainment']
        )

        assert entry.version == '2.0'
        assert entry.scale == 'large'
        assert 'vehicle' in entry.subsystems