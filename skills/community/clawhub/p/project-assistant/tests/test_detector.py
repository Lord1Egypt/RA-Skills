"""
Tests for ProjectDetector
"""

import os
import sys
import json
from pathlib import Path
import pytest

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'tools' / 'init'))

from detector import ProjectDetector, DetectionResult


class TestProjectDetector:
    """Test cases for ProjectDetector"""

    def test_detect_python_project(self, sample_python_project: Path):
        """Test detection of Python project"""
        detector = ProjectDetector(str(sample_python_project))
        result = detector.detect()

        assert result['language'] == 'python'
        assert result['build_system'] in ['pip', 'poetry']
        assert 'requirements.txt' in result['config_files'] or 'pyproject.toml' in result['config_files']

    def test_detect_android_project(self, sample_android_project: Path):
        """Test detection of Android project"""
        detector = ProjectDetector(str(sample_android_project))
        result = detector.detect()

        assert result['project_type'] == 'android-app'
        assert result['language'] == 'kotlin'
        assert result['build_system'] == 'gradle'

    def test_detect_cmake_project(self, sample_cmake_project: Path):
        """Test detection of CMake project"""
        detector = ProjectDetector(str(sample_cmake_project))
        result = detector.detect()

        assert result['project_type'] == 'cmake'
        assert result['language'] in ['cpp', 'c']
        assert result['build_system'] == 'cmake'

    def test_detect_react_project(self, sample_react_project: Path):
        """Test detection of React project"""
        detector = ProjectDetector(str(sample_react_project))
        result = detector.detect()

        assert result['project_type'] == 'react'
        assert result['language'] == 'typescript'
        assert result['build_system'] == 'npm'

    def test_detect_nonexistent_directory(self, temp_project_dir: Path):
        """Test detection on non-existent directory"""
        detector = ProjectDetector(str(temp_project_dir / 'nonexistent'))
        result = detector.detect()

        assert 'error' in result
        assert 'not found' in result['error'].lower()

    def test_detect_empty_directory(self, temp_project_dir: Path):
        """Test detection on empty directory"""
        detector = ProjectDetector(str(temp_project_dir))
        result = detector.detect()

        # Should return unknown for empty directory
        assert result['project_type'] == 'unknown'

    def test_cache_mechanism(self, sample_python_project: Path):
        """Test that caching works"""
        detector = ProjectDetector(str(sample_python_project))

        # First call
        result1 = detector.detect()

        # Second call should return cached result
        result2 = detector.detect()

        assert result1 == result2

    def test_clear_cache(self, sample_python_project: Path):
        """Test cache clearing"""
        detector = ProjectDetector(str(sample_python_project))

        # First call to populate cache
        detector.detect()

        # Clear cache
        ProjectDetector.clear_cache()

        # Cache should be empty
        assert not detector._cache

    def test_entry_points_detection(self, sample_python_project: Path):
        """Test entry points detection"""
        detector = ProjectDetector(str(sample_python_project))
        result = detector.detect()

        assert len(result['entry_points']) > 0

    def test_config_files_detection(self, sample_python_project: Path):
        """Test config files detection"""
        detector = ProjectDetector(str(sample_python_project))
        result = detector.detect()

        assert len(result['config_files']) > 0

    def test_target_platform_detection(self, sample_android_project: Path):
        """Test target platform detection"""
        detector = ProjectDetector(str(sample_android_project))
        result = detector.detect()

        assert result['target_platform'] == 'android'

    def test_scale_detection_small(self, sample_python_project: Path):
        """Test scale detection for small project"""
        detector = ProjectDetector(str(sample_python_project))
        result = detector.detect()

        assert result['scale'] == 'small'

    def test_get_subskill_path(self, sample_android_project: Path):
        """Test subskill path mapping"""
        detector = ProjectDetector(str(sample_android_project))
        subskill = detector.get_subskill_path()

        assert subskill == 'mobile/android.md'


class TestDetectionResult:
    """Test cases for DetectionResult dataclass"""

    def test_default_values(self):
        """Test default values of DetectionResult"""
        result = DetectionResult()

        assert result.project_type == 'unknown'
        assert result.language == 'unknown'
        assert result.build_system == 'unknown'
        assert result.entry_points == []
        assert result.config_files == []
        assert result.dependencies == []
        assert result.confidence == 0.0

    def test_custom_values(self):
        """Test custom values of DetectionResult"""
        result = DetectionResult(
            project_type='android-app',
            language='kotlin',
            build_system='gradle',
            confidence=0.95
        )

        assert result.project_type == 'android-app'
        assert result.language == 'kotlin'
        assert result.build_system == 'gradle'
        assert result.confidence == 0.95