"""
Pytest fixtures for Project Assistant tests
"""

import os
import sys
import tempfile
import shutil
import json
from pathlib import Path
from typing import Generator
import pytest


# Add tools to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'tools' / 'init'))


@pytest.fixture
def temp_project_dir() -> Generator[Path, None, None]:
    """Create a temporary project directory for testing"""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)


@pytest.fixture
def sample_python_project(temp_project_dir: Path) -> Path:
    """Create a sample Python project structure"""
    # Create basic structure
    (temp_project_dir / 'src').mkdir()
    (temp_project_dir / 'tests').mkdir()

    # Create main.py
    main_py = temp_project_dir / 'src' / 'main.py'
    main_py.write_text('''
def main():
    """Main entry point"""
    print("Hello, World!")

if __name__ == '__main__':
    main()
''')

    # Create requirements.txt
    req_txt = temp_project_dir / 'requirements.txt'
    req_txt.write_text('requests>=2.28.0\npytest>=7.0.0\n')

    # Create pyproject.toml
    pyproject = temp_project_dir / 'pyproject.toml'
    pyproject.write_text('''
[project]
name = "test-project"
version = "1.0.0"
description = "Test project"

[tool.pytest.ini_options]
testpaths = ["tests"]
''')

    return temp_project_dir


@pytest.fixture
def sample_android_project(temp_project_dir: Path) -> Path:
    """Create a sample Android project structure"""
    # Create basic structure
    app_dir = temp_project_dir / 'app' / 'src' / 'main'
    app_dir.mkdir(parents=True)
    (app_dir / 'java' / 'com' / 'example').mkdir(parents=True)

    # Create AndroidManifest.xml
    manifest = app_dir / 'AndroidManifest.xml'
    manifest.write_text('''
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.testapp">
    <application android:label="TestApp">
        <activity android:name=".MainActivity">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
''')

    # Create build.gradle
    build_gradle = temp_project_dir / 'build.gradle'
    build_gradle.write_text('''
plugins {
    id 'com.android.application'
}

android {
    compileSdk 34
    defaultConfig {
        applicationId "com.example.testapp"
        minSdk 24
        targetSdk 34
        versionCode 1
        versionName "1.0"
    }
}

dependencies {
    implementation 'androidx.appcompat:appcompat:1.6.1'
}
''')

    # Create MainActivity.kt
    main_activity = app_dir / 'java' / 'com' / 'example' / 'MainActivity.kt'
    main_activity.write_text('''
package com.example.testapp

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
    }
}
''')

    return temp_project_dir


@pytest.fixture
def sample_cmake_project(temp_project_dir: Path) -> Path:
    """Create a sample CMake project structure"""
    # Create basic structure
    (temp_project_dir / 'src').mkdir()
    (temp_project_dir / 'include').mkdir()

    # Create CMakeLists.txt
    cmake = temp_project_dir / 'CMakeLists.txt'
    cmake.write_text('''
cmake_minimum_required(VERSION 3.10)
project(TestProject VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)

add_executable(test_app
    src/main.cpp
)

target_include_directories(test_app PRIVATE include)
''')

    # Create main.cpp
    main_cpp = temp_project_dir / 'src' / 'main.cpp'
    main_cpp.write_text('''
#include <iostream>

int main() {
    std::cout << "Hello, World!" << std::endl;
    return 0;
}
''')

    return temp_project_dir


@pytest.fixture
def sample_react_project(temp_project_dir: Path) -> Path:
    """Create a sample React project structure"""
    # Create basic structure
    (temp_project_dir / 'src').mkdir()
    (temp_project_dir / 'public').mkdir()

    # Create package.json
    package_json = temp_project_dir / 'package.json'
    package_json.write_text(json.dumps({
        'name': 'test-react-app',
        'version': '1.0.0',
        'dependencies': {
            'react': '^18.2.0',
            'react-dom': '^18.2.0'
        },
        'devDependencies': {
            'typescript': '^5.0.0',
            'vite': '^5.0.0'
        },
        'scripts': {
            'dev': 'vite',
            'build': 'tsc && vite build'
        }
    }, indent=2))

    # Create tsconfig.json
    tsconfig = temp_project_dir / 'tsconfig.json'
    tsconfig.write_text(json.dumps({
        'compilerOptions': {
            'target': 'ES2020',
            'module': 'ESNext',
            'strict': True
        }
    }, indent=2))

    # Create main.tsx
    main_tsx = temp_project_dir / 'src' / 'main.tsx'
    main_tsx.write_text('''
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
''')

    return temp_project_dir