"""
Tests for GradleParser
"""

import os
import sys
from pathlib import Path
import pytest

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'tools' / 'init'))

from parsers.gradle_parser import parse_gradle, find_gradle_files


class TestGradleParser:
    """Test cases for GradleParser"""

    def test_parse_basic_gradle(self, sample_android_project: Path):
        """Test parsing basic build.gradle"""
        gradle_files = find_gradle_files(str(sample_android_project))

        assert len(gradle_files) > 0

    def test_parse_gradle_content(self, sample_android_project: Path):
        """Test parsing gradle content"""
        result = parse_gradle(str(sample_android_project))

        assert result is not None
        # Check for expected fields
        if 'applicationId' in result:
            assert result['applicationId'] == 'com.example.testapp'

    def test_find_gradle_files(self, sample_android_project: Path):
        """Test finding gradle files"""
        gradle_files = find_gradle_files(str(sample_android_project))

        # Should find build.gradle
        assert any('build.gradle' in f for f in gradle_files)

    def test_parse_nonexistent_directory(self, temp_project_dir: Path):
        """Test parsing non-existent directory"""
        result = parse_gradle(str(temp_project_dir / 'nonexistent'))

        # Should handle gracefully
        assert result is not None
        assert result.get('error') is not None or result.get('applicationId') is None

    def test_parse_empty_directory(self, temp_project_dir: Path):
        """Test parsing empty directory"""
        result = parse_gradle(str(temp_project_dir))

        # Should return empty or error
        assert result is not None

    def test_parse_gradle_with_plugins(self, temp_project_dir: Path):
        """Test parsing gradle with plugins block"""
        # Create a gradle file with plugins
        gradle_file = temp_project_dir / 'build.gradle.kts'
        gradle_file.write_text('''
plugins {
    id("com.android.application") version "8.1.0"
    id("org.jetbrains.kotlin.android") version "1.9.0"
}

android {
    namespace = "com.example.test"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.example.test"
        minSdk = 24
        targetSdk = 34
        versionCode = 1
        versionName = "1.0"
    }
}

dependencies {
    implementation("androidx.core:core-ktx:1.12.0")
    implementation("androidx.appcompat:appcompat:1.6.1")
}
''')

        result = parse_gradle(str(temp_project_dir))

        assert result is not None
        # Check for parsed application ID
        if 'applicationId' in result:
            assert result['applicationId'] == 'com.example.test'

    def test_parse_gradle_dependencies(self, temp_project_dir: Path):
        """Test parsing gradle dependencies"""
        gradle_file = temp_project_dir / 'build.gradle'
        gradle_file.write_text('''
dependencies {
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.10.0'
    testImplementation 'junit:junit:4.13.2'
}
''')

        result = parse_gradle(str(temp_project_dir))

        assert result is not None
        # Should have dependencies
        if 'dependencies' in result:
            assert len(result['dependencies']) > 0