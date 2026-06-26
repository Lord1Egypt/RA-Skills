#!/usr/bin/env python3
"""
项目常量定义
统一管理项目中使用的常量，避免重复定义
"""

# 排除目录 - 用于文件遍历时跳过
# 这些目录通常包含构建产物、依赖包、IDE配置等，不需要分析
EXCLUDE_DIRS = {
    # 版本控制
    '.git', '.svn', '.hg',

    # IDE 和编辑器
    '.idea', '.vscode', '.settings', '.project', '.classpath',

    # Node.js
    'node_modules', 'npm-cache', '.npm', 'yarn-cache',

    # Python
    '__pycache__', '.pytest_cache', '.mypy_cache', '.tox',
    'venv', '.venv', 'env', '.env', 'site-packages',
    '*.egg-info', 'dist-info', '.eggs',

    # Java/Kotlin
    '.gradle', 'target', 'out', '.kotlin',

    # iOS/macOS
    'Pods', 'DerivedData', '.build', 'build',

    # C/C++
    'build', 'cmake-build-*', 'CMakeFiles', '_deps',
    'bin', 'obj', 'lib', 'libs',

    # Rust
    'target',

    # Go
    'vendor',

    # Embedded
    'Output', 'Listings', 'Objects', 'DebugConfig', 'RTE',
    'Core', 'Drivers', 'Middlewares',  # STM32CubeIDE generated

    # Web
    'dist', '.next', '.nuxt', '.cache',

    # 通用
    'logs', 'tmp', 'temp', 'cache', '.cache',
}

# 文件扩展名映射到语言
FILE_EXTENSION_LANG_MAP = {
    # 前端
    '.js': 'javascript',
    '.mjs': 'javascript',
    '.cjs': 'javascript',
    '.jsx': 'javascript-react',
    '.ts': 'typescript',
    '.tsx': 'typescript-react',
    '.vue': 'vue',
    '.svelte': 'svelte',
    '.html': 'html',
    '.css': 'css',
    '.scss': 'scss',
    '.less': 'less',

    # 后端/脚本
    '.py': 'python',
    '.pyw': 'python',
    '.rb': 'ruby',
    '.php': 'php',
    '.go': 'go',
    '.rs': 'rust',
    '.lua': 'lua',
    '.r': 'r',

    # 移动端
    '.kt': 'kotlin',
    '.kts': 'kotlin',
    '.java': 'java',
    '.swift': 'swift',
    '.m': 'objective-c',
    '.mm': 'objective-cpp',
    '.dart': 'dart',

    # 系统/嵌入式
    '.c': 'c',
    '.h': 'c-header',
    '.cpp': 'cpp',
    '.cc': 'cpp',
    '.cxx': 'cpp',
    '.hpp': 'cpp-header',
    '.hxx': 'cpp-header',
    '.rs': 'rust',
    '.zig': 'zig',

    # 配置/数据
    '.json': 'json',
    '.yaml': 'yaml',
    '.yml': 'yaml',
    '.toml': 'toml',
    '.xml': 'xml',
    '.ini': 'ini',
    '.conf': 'conf',
    '.cfg': 'conf',
    '.env': 'env',
    '.md': 'markdown',

    # IPC/接口
    '.aidl': 'aidl',
    '.proto': 'protobuf',
    '.thrift': 'thrift',
    '.hal': 'hal',

    # Shell
    '.sh': 'shell',
    '.bash': 'shell',
    '.zsh': 'shell',
    '.bat': 'batch',
    '.ps1': 'powershell',

    # 其他
    '.cs': 'csharp',
    '.scala': 'scala',
    '.groovy': 'groovy',
    '.sql': 'sql',
    '.graphql': 'graphql',
    '.ex': 'elixir',
    '.exs': 'elixir',
    '.erl': 'erlang',
}

# 关键配置文件列表
KEY_CONFIG_FILES = [
    # JavaScript/TypeScript
    'package.json',
    'package-lock.json',
    'yarn.lock',
    'pnpm-lock.yaml',

    # Rust
    'Cargo.toml',
    'Cargo.lock',

    # Go
    'go.mod',
    'go.sum',

    # Python
    'requirements.txt',
    'pyproject.toml',
    'poetry.lock',
    'Pipfile.lock',
    'setup.py',
    'setup.cfg',

    # Java/Kotlin
    'pom.xml',
    'build.gradle',
    'build.gradle.kts',
    'settings.gradle',
    'settings.gradle.kts',

    # C/C++
    'CMakeLists.txt',
    'Makefile',
    'meson.build',
    'BUILD',
    'WORKSPACE',

    # Android
    'AndroidManifest.xml',
    'gradle.properties',
    'Android.mk',
    'Android.bp',
    'Application.mk',

    # Flutter/Dart
    'pubspec.yaml',
    'pubspec.lock',

    # iOS
    'Podfile',
    'Podfile.lock',
    'Gemfile',
    'Gemfile.lock',
    'Cartfile',
    'Cartfile.resolved',

    # Embedded
    '.ioc',
    'sdkconfig',
    'Kconfig',
    'defconfig',
    'prj.conf',
    'platformio.ini',

    # Config
    '.env',
    '.env.local',
    '.env.development',
    '.env.production',

    # Web
    'vite.config.js',
    'vite.config.ts',
    'webpack.config.js',
    'tsconfig.json',
    'jsconfig.json',
    '.eslintrc.js',
    '.eslintrc.json',
    '.prettierrc',
    'tailwind.config.js',
    'tailwind.config.ts',
    'next.config.js',
    'next.config.ts',
    'nuxt.config.js',
    'nuxt.config.ts',
    'vue.config.js',
    'angular.json',
]

# 项目类型到目标平台的映射
PROJECT_TYPE_PLATFORM_MAP = {
    # Mobile
    'android-app': 'android',
    'android-ndk': 'android',
    'aosp': 'android',
    'ios': 'ios',
    'flutter': 'cross-platform',
    'react-native': 'cross-platform',

    # Embedded
    'stm32': 'embedded',
    'esp32': 'embedded',
    'pico': 'embedded',
    'keil': 'embedded',
    'iar': 'embedded',
    'freertos': 'embedded',
    'zephyr': 'embedded',
    'rt-thread': 'embedded',
    'embedded-linux': 'embedded',
    'buildroot': 'embedded',
    'yocto': 'embedded',
    'openwrt': 'embedded',
    'qnx': 'embedded',

    # Web
    'react': 'web',
    'vue': 'web',
    'angular': 'web',
    'svelte': 'web',
    'nextjs': 'web',
    'nuxt': 'web',
    'django': 'web',
    'fastapi': 'web',
    'flask': 'web',
    'spring': 'web',

    # Desktop
    'electron': 'desktop',
    'qt': 'desktop',
    'tauri': 'desktop',

    # System
    'cmake': 'native',
    'makefile': 'native',
    'go': 'cross-platform',
    'rust': 'cross-platform',

    # Game
    'unity': 'game',
    'unreal': 'game',
    'godot': 'game',
}

# IPC 协议指示器
IPC_INDICATORS = {
    '.aidl': 'binder',
    '.hal': 'hwbinder',
    '.proto': 'grpc',
    'dbus': 'dbus',
    'someip': 'someip',
    'vsomeip': 'someip',
    'commonapi': 'someip',
}

# 常见模块目录名
COMMON_MODULE_DIRS = {
    'src', 'lib', 'app', 'core', 'internal', 'cmd',
    'components', 'pages', 'hooks', 'store', 'api', 'utils',
    'controllers', 'services', 'models', 'routes', 'middleware',
    'drivers', 'hal', 'bsp', 'kernel', 'frameworks',
    'features', 'modules', 'packages', 'domains',
    'entities', 'usecases', 'repositories',
    'presentation', 'data', 'di',
    'public', 'private', 'test', 'tests', 'spec',
}

# 常见子系统目录名（大型项目）
SUBSYSTEM_PATTERNS = {
    'vehicle', 'infotainment', 'adas', 'cluster',
    'tbox', 'hud', 'ivi', 'autonomous',
    'frameworks', 'system', 'hardware', 'packages',
    'services', 'apps', 'core', 'common',
}

__all__ = [
    'EXCLUDE_DIRS',
    'FILE_EXTENSION_LANG_MAP',
    'KEY_CONFIG_FILES',
    'PROJECT_TYPE_PLATFORM_MAP',
    'IPC_INDICATORS',
    'COMMON_MODULE_DIRS',
    'SUBSYSTEM_PATTERNS',
]