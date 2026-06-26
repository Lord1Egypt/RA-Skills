#!/usr/bin/env python3
"""
项目类型探测器
快速识别项目类型，返回结构化JSON数据

特性：
- 结果缓存机制
- 并行文件搜索
- 置信度排序
- 多项目类型支持
"""

import os
import sys
import json
import re
import time
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Set
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field

# 添加日志支持
try:
    from utils.logger import get_logger
    logger = get_logger(__name__)
except ImportError:
    import logging
    logger = logging.getLogger(__name__)

# 导入统一常量
try:
    from constants import EXCLUDE_DIRS
except ImportError:
    EXCLUDE_DIRS = {
        '.git', '.svn', '.hg', '.idea', '.vscode',
        'node_modules', 'dist', 'build', 'out', 'bin', 'obj',
        '__pycache__', '.pytest_cache', '.mypy_cache',
        'target', 'vendor', 'CMakeFiles', '_deps',
        'Output', 'Listings', 'Objects', 'DebugConfig', 'RTE',
        '.gradle', '.idea', 'out', 'Pods', 'DerivedData',
        'venv', '.venv', 'env', '.env',
    }


@dataclass
class ProjectTypeRule:
    """项目类型规则"""
    patterns: List[str]
    project_type: str
    language: str = 'unknown'
    priority: int = 0  # 越高越优先
    build_system: str = 'unknown'


@dataclass
class DetectionResult:
    """探测结果"""
    project_type: str = 'unknown'
    language: str = 'unknown'
    build_system: str = 'unknown'
    entry_points: List[str] = field(default_factory=list)
    config_files: List[str] = field(default_factory=list)
    dependencies: List[Dict[str, str]] = field(default_factory=list)
    modules: List[str] = field(default_factory=list)
    target_platform: str = 'unknown'
    confidence: float = 0.0
    secondary_types: List[str] = field(default_factory=list)
    detection_time: str = ''
    # 大型项目支持
    scale: str = 'small'  # small/medium/large
    subsystems: List[str] = field(default_factory=list)
    processes: List[str] = field(default_factory=list)
    ipc_protocols: List[str] = field(default_factory=list)


class ProjectDetector:
    """项目类型探测器"""

    # 项目类型识别规则
    RULES = [
        # Android (高优先级)
        ProjectTypeRule(['AndroidManifest.xml'], 'android-app', 'kotlin', 100, 'gradle'),
        ProjectTypeRule(['build.gradle', 'app/src/main'], 'android-app', 'kotlin', 90, 'gradle'),
        ProjectTypeRule(['build.gradle.kts', 'app/src/main'], 'android-app', 'kotlin', 90, 'gradle'),
        ProjectTypeRule(['Android.mk', 'jni'], 'android-ndk', 'c', 80, 'ndk-build'),
        ProjectTypeRule(['Android.bp'], 'aosp', 'java', 85, 'soong'),
        ProjectTypeRule(['frameworks', 'system', 'hardware'], 'aosp', 'java', 70, 'soong'),

        # iOS
        ProjectTypeRule(['*.xcodeproj'], 'ios', 'swift', 100, 'xcode'),
        ProjectTypeRule(['*.xcworkspace'], 'ios', 'swift', 100, 'xcode'),
        ProjectTypeRule(['Podfile'], 'ios', 'swift', 85, 'cocoapods'),
        ProjectTypeRule(['Package.swift'], 'swift', 'swift', 80, 'spm'),

        # Embedded MCU
        ProjectTypeRule(['*.ioc'], 'stm32', 'c', 95, 'stm32cubeide'),
        ProjectTypeRule(['*.uvprojx', '*.uvproj'], 'keil', 'c', 95, 'keil'),
        ProjectTypeRule(['*.ewp'], 'iar', 'c', 95, 'iar'),
        ProjectTypeRule(['platformio.ini'], 'platformio', 'c', 90, 'platformio'),
        ProjectTypeRule(['pico_sdk_import.cmake'], 'pico', 'c', 90, 'cmake'),
        ProjectTypeRule(['sdkconfig', 'CMakeLists.txt'], 'esp32', 'c', 85, 'cmake'),

        # Embedded RTOS
        ProjectTypeRule(['FreeRTOSConfig.h'], 'freertos', 'c', 90, 'make'),
        ProjectTypeRule(['Kconfig', 'CMakeLists.txt', 'zephyr'], 'zephyr', 'c', 85, 'cmake'),
        ProjectTypeRule(['rtconfig.h'], 'rt-thread', 'c', 90, 'scons'),

        # Embedded Linux
        ProjectTypeRule(['defconfig', 'Kbuild'], 'embedded-linux', 'c', 80, 'make'),
        ProjectTypeRule(['*.dts', '*.dtsi'], 'embedded-linux', 'dts', 75, 'dtc'),
        ProjectTypeRule(['Buildroot', 'Config.in'], 'buildroot', 'make', 85, 'make'),
        ProjectTypeRule(['meta-', 'recipes-'], 'yocto', 'python', 85, 'bitbake'),
        ProjectTypeRule(['poky', 'bitbake'], 'yocto', 'python', 80, 'bitbake'),
        ProjectTypeRule(['feeds.conf', 'openwrt'], 'openwrt', 'c', 80, 'make'),

        # QNX
        ProjectTypeRule(['QNX_TARGET'], 'qnx', 'c', 90, 'make'),
        ProjectTypeRule(['*.build', 'startup-'], 'qnx', 'c', 75, 'make'),

        # Web Frontend
        ProjectTypeRule(['package.json', 'src/index.tsx'], 'react', 'typescript', 85, 'npm'),
        ProjectTypeRule(['package.json', 'src/main.tsx'], 'react', 'typescript', 85, 'npm'),
        ProjectTypeRule(['nuxt.config.js'], 'nuxt', 'javascript', 90, 'npm'),
        ProjectTypeRule(['nuxt.config.ts'], 'nuxt', 'typescript', 90, 'npm'),
        ProjectTypeRule(['next.config.js'], 'nextjs', 'javascript', 90, 'npm'),
        ProjectTypeRule(['next.config.ts'], 'nextjs', 'typescript', 90, 'npm'),
        ProjectTypeRule(['vue.config.js'], 'vue', 'javascript', 90, 'npm'),
        ProjectTypeRule(['angular.json'], 'angular', 'typescript', 95, 'npm'),
        ProjectTypeRule(['svelte.config.js'], 'svelte', 'javascript', 90, 'npm'),

        # Web Backend
        ProjectTypeRule(['manage.py', 'settings.py'], 'django', 'python', 95, 'pip'),
        ProjectTypeRule(['main.py', 'requirements.txt', 'fastapi'], 'fastapi', 'python', 80, 'pip'),
        ProjectTypeRule(['app.py', 'requirements.txt'], 'flask', 'python', 80, 'pip'),
        ProjectTypeRule(['pom.xml'], 'maven', 'java', 95, 'maven'),
        ProjectTypeRule(['build.gradle', 'src/main/java'], 'gradle-java', 'java', 90, 'gradle'),
        ProjectTypeRule(['go.mod'], 'go', 'go', 95, 'go-mod'),
        ProjectTypeRule(['Cargo.toml'], 'rust', 'rust', 95, 'cargo'),

        # Desktop
        ProjectTypeRule(['*.pro'], 'qt', 'cpp', 85, 'qmake'),
        ProjectTypeRule(['package.json', 'electron'], 'electron', 'javascript', 80, 'npm'),
        ProjectTypeRule(['pubspec.yaml', 'lib/main.dart'], 'flutter', 'dart', 95, 'flutter'),

        # System/Native
        ProjectTypeRule(['CMakeLists.txt'], 'cmake', 'cpp', 70, 'cmake'),
        ProjectTypeRule(['Makefile'], 'makefile', 'c', 70, 'make'),
        ProjectTypeRule(['meson.build'], 'meson', 'c', 80, 'meson'),
        ProjectTypeRule(['BUILD', 'WORKSPACE'], 'bazel', 'java', 90, 'bazel'),

        # AI/ML
        ProjectTypeRule(['requirements.txt', 'torch'], 'pytorch', 'python', 75, 'pip'),
        ProjectTypeRule(['requirements.txt', 'tensorflow'], 'tensorflow', 'python', 75, 'pip'),
        ProjectTypeRule(['*.ipynb'], 'jupyter', 'python', 70, 'pip'),

        # Game
        ProjectTypeRule(['Assets', 'ProjectSettings'], 'unity', 'csharp', 95, 'unity'),
        ProjectTypeRule(['*.uproject', 'Source'], 'unreal', 'cpp', 95, 'unreal'),
        ProjectTypeRule(['project.godot'], 'godot', 'gdscript', 95, 'godot'),
    ]

    # 类缓存
    _cache: Dict[str, Dict[str, Any]] = {}
    _cache_ttl: int = 300  # 5分钟缓存

    def __init__(self, target_dir: str, max_workers: int = 4):
        self.target_dir = Path(target_dir).resolve()
        self.max_workers = max_workers
        self._files_cache: Optional[List[str]] = None
        self._dirs_cache: Optional[List[str]] = None

    def detect(self) -> Dict[str, Any]:
        """执行探测"""
        start_time = time.time()
        logger.debug(f"开始探测项目: {self.target_dir}")

        # 检查缓存
        cache_key = self._get_cache_key()
        if cache_key in self._cache:
            cached = self._cache[cache_key]
            if time.time() - cached['timestamp'] < self._cache_ttl:
                logger.debug("使用缓存结果")
                return cached['result']

        if not self.target_dir.exists():
            logger.error(f"目录不存在: {self.target_dir}")
            return {'error': f'Directory not found: {self.target_dir}'}

        # 执行探测
        result = self._do_detect()

        # 缓存结果
        self._cache[cache_key] = {
            'result': result,
            'timestamp': time.time(),
        }

        elapsed = time.time() - start_time
        result['detection_time'] = f"{elapsed:.2f}s"

        return result

    def _get_cache_key(self) -> str:
        """获取缓存键"""
        return str(self.target_dir)

    def _do_detect(self) -> Dict[str, Any]:
        """执行实际探测"""
        # 并行收集文件和目录
        files, dirs = self._collect_files_and_dirs()

        # 1. 检测项目类型
        project_types = self._detect_project_types(files, dirs)

        # 2. 检测语言
        language = self._detect_language(files)

        # 3. 检测构建系统
        build_system = self._detect_build_system(files)

        # 4. 查找入口点
        entry_points = self._find_entry_points(files)

        # 5. 查找配置文件
        config_files = self._find_config_files(files)

        # 6. 扫描模块目录
        modules = self._scan_modules(dirs)

        # 7. 提取依赖
        dependencies = self._extract_dependencies(files)

        return {
            'project_type': project_types[0] if project_types else 'unknown',
            'secondary_types': project_types[1:] if len(project_types) > 1 else [],
            'language': language,
            'build_system': build_system,
            'entry_points': entry_points,
            'config_files': config_files,
            'dependencies': dependencies,
            'modules': modules,
            'target_platform': self._detect_target_platform(project_types),
            'confidence': 1.0 if project_types else 0.0,
            'scale': self._detect_scale(files, dirs),
            'subsystems': self._detect_subsystems(dirs),
            'processes': self._detect_processes(files),
            'ipc_protocols': self._detect_ipc_protocols(files),
        }

    def _collect_files_and_dirs(self, max_depth: int = 3) -> Tuple[List[str], List[str]]:
        """并行收集文件和目录"""
        files = []
        dirs = []

        try:
            for root, dirnames, filenames in os.walk(self.target_dir):
                # 排除特定目录
                dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]

                rel_root = os.path.relpath(root, self.target_dir)
                depth = 0 if rel_root == '.' else rel_root.count(os.sep) + 1

                if depth > max_depth:
                    dirnames[:] = []
                    continue

                for f in filenames:
                    if rel_root == '.':
                        files.append(f)
                    else:
                        files.append(os.path.join(rel_root, f).replace('\\', '/'))

                for d in dirnames:
                    if rel_root == '.':
                        dirs.append(d)
                    else:
                        dirs.append(os.path.join(rel_root, d).replace('\\', '/'))
        except PermissionError:
            pass

        return files, dirs

    def _detect_project_types(self, files: List[str], dirs: List[str]) -> List[str]:
        """检测项目类型（支持多类型）"""
        matches: List[Tuple[ProjectTypeRule, float]] = []

        files_set = set(files)
        dirs_set = set(dirs)

        for rule in self.RULES:
            score = 0
            matched_patterns = 0

            for pattern in rule.patterns:
                if pattern.startswith('*.'):
                    # 通配符匹配
                    ext = pattern[1:]  # .xxx
                    if any(f.endswith(ext) for f in files):
                        score += 1
                        matched_patterns += 1
                elif pattern in files_set or pattern in dirs_set:
                    score += 1.5  # 精确匹配得分更高
                    matched_patterns += 1
                elif self._content_contains(pattern, files[:20]):
                    score += 0.5  # 内容匹配
                    matched_patterns += 0.5

            if matched_patterns > 0:
                # 计算置信度
                confidence = matched_patterns / len(rule.patterns)
                total_score = score * (1 + rule.priority / 100) * confidence
                matches.append((rule, total_score))

        # 按分数排序
        matches.sort(key=lambda x: x[1], reverse=True)

        # 返回项目类型列表
        types = []
        for rule, score in matches:
            if score >= 0.5:  # 置信度阈值
                types.append(rule.project_type)

        # 去重，保持顺序
        seen = set()
        unique_types = []
        for t in types:
            if t not in seen:
                seen.add(t)
                unique_types.append(t)

        return unique_types[:3]  # 最多返回3个类型

    def _content_contains(self, pattern: str, files: List[str]) -> bool:
        """检查文件内容是否包含模式"""
        # 对于某些关键字，检查文件内容
        keywords = ['fastapi', 'torch', 'tensorflow', 'electron', 'zephyr', 'rtthread']

        if pattern.lower() not in keywords:
            return False

        for f in files[:20]:
            if not f.endswith(('.py', '.js', '.ts', '.json', '.h', '.c', '.cpp', '.md')):
                continue

            try:
                filepath = self.target_dir / f
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as fp:
                    content = fp.read().lower()
                    if pattern.lower() in content:
                        return True
            except (IOError, OSError):
                continue

        return False

    def _detect_language(self, files: List[str]) -> str:
        """检测主要语言"""
        lang_map = {
            '.kt': ('kotlin', 10),
            '.java': ('java', 8),
            '.swift': ('swift', 10),
            '.m': ('objective-c', 8),
            '.mm': ('objective-cpp', 8),
            '.c': ('c', 5),
            '.cpp': ('cpp', 6),
            '.cc': ('cpp', 6),
            '.cxx': ('cpp', 6),
            '.h': ('c-header', 2),
            '.hpp': ('cpp-header', 2),
            '.py': ('python', 8),
            '.js': ('javascript', 6),
            '.mjs': ('javascript', 6),
            '.cjs': ('javascript', 6),
            '.ts': ('typescript', 8),
            '.tsx': ('typescript-react', 9),
            '.jsx': ('javascript-react', 7),
            '.go': ('go', 10),
            '.rs': ('rust', 10),
            '.rb': ('ruby', 8),
            '.php': ('php', 8),
            '.cs': ('csharp', 10),
            '.dart': ('dart', 10),
            '.scala': ('scala', 10),
            '.groovy': ('groovy', 8),
            '.lua': ('lua', 8),
            '.r': ('r', 8),
            '.vue': ('vue', 9),
            '.svelte': ('svelte', 9),
        }

        extensions: Dict[str, int] = {}

        for f in files:
            ext = Path(f).suffix.lower()
            if ext in lang_map:
                lang, weight = lang_map[ext]
                # 根据路径深度调整权重
                depth = f.count('/')
                adjusted_weight = weight * (1.0 - depth * 0.1)
                extensions[lang] = extensions.get(lang, 0) + adjusted_weight

        if extensions:
            # 排除头文件的影响
            code_exts = {k: v for k, v in extensions.items()
                        if not k.endswith('-header')}
            if code_exts:
                main_lang = max(code_exts, key=code_exts.get)
                return main_lang

        return 'unknown'

    def _detect_build_system(self, files: List[str]) -> str:
        """检测构建系统"""
        build_files = [
            ('build.gradle.kts', 'gradle'),
            ('build.gradle', 'gradle'),
            ('settings.gradle.kts', 'gradle'),
            ('settings.gradle', 'gradle'),
            ('pom.xml', 'maven'),
            ('CMakeLists.txt', 'cmake'),
            ('Makefile', 'make'),
            ('makefile', 'make'),
            ('Android.mk', 'ndk-build'),
            ('Android.bp', 'soong'),
            ('package.json', 'npm'),
            ('pnpm-lock.yaml', 'pnpm'),
            ('yarn.lock', 'yarn'),
            ('Cargo.toml', 'cargo'),
            ('go.mod', 'go-mod'),
            ('requirements.txt', 'pip'),
            ('pyproject.toml', 'poetry'),
            ('poetry.lock', 'poetry'),
            ('meson.build', 'meson'),
            ('BUILD', 'bazel'),
            ('WORKSPACE', 'bazel'),
            ('platformio.ini', 'platformio'),
            ('*.uvprojx', 'keil'),
            ('*.ewp', 'iar'),
            ('*.pro', 'qmake'),
            ('pubspec.yaml', 'flutter'),
            ('Podfile', 'cocoapods'),
            ('Gemfile', 'bundler'),
            ('composer.json', 'composer'),
        ]

        files_set = set(files)

        for pattern, build_system in build_files:
            if pattern.startswith('*'):
                ext = pattern[1:]
                if any(f.endswith(ext) for f in files):
                    return build_system
            elif pattern in files_set:
                return build_system

        return 'unknown'

    def _find_entry_points(self, files: List[str]) -> List[str]:
        """查找入口点文件"""
        entry_patterns = [
            # 通用入口
            'main.c', 'main.cpp', 'main.py', 'main.go', 'main.rs',
            'Main.kt', 'MainActivity.kt', 'MainActivity.java',
            'index.js', 'index.ts', 'main.tsx', 'index.tsx',
            'app.py', 'run.py', '__main__.py',
            'Program.cs', 'main.dart',

            # 嵌入式入口
            'app_main.c', 'app_main.cpp',
            'main_task.c', 'main_loop.c',
            'application_main.c',

            # Web入口
            'server.js', 'server.ts', 'app.js', 'app.ts',
            'index.php', 'index.rb',

            # Android
            'Application.java', 'Application.kt',

            # iOS
            'AppDelegate.swift', 'AppDelegate.m',
            'main.m', 'main.swift',
        ]

        entry_points = []
        for pattern in entry_patterns:
            for f in files:
                if f.endswith('/' + pattern) or f == pattern:
                    entry_points.append(f)

        # 去重
        return list(dict.fromkeys(entry_points))

    def _find_config_files(self, files: List[str]) -> List[str]:
        """查找配置文件"""
        config_patterns = [
            'AndroidManifest.xml',
            'build.gradle', 'build.gradle.kts',
            'settings.gradle', 'settings.gradle.kts',
            'CMakeLists.txt', 'Makefile',
            'package.json', 'package-lock.json',
            'Cargo.toml', 'Cargo.lock',
            'go.mod', 'go.sum',
            'pom.xml',
            'requirements.txt', 'pyproject.toml', 'poetry.lock',
            'Android.mk', 'Android.bp', 'Application.mk',
            'sdkconfig', 'Kconfig', 'defconfig',
            '.config',
            'pubspec.yaml', 'pubspec.lock',
            'Podfile', 'Podfile.lock',
            'Gemfile', 'Gemfile.lock',
            'composer.json', 'composer.lock',
            'vite.config.js', 'vite.config.ts',
            'webpack.config.js',
            'tsconfig.json',
            '.eslintrc.js', '.eslintrc.json',
            '.prettierrc', '.prettierrc.json',
            'tailwind.config.js', 'tailwind.config.ts',
            'next.config.js', 'next.config.ts',
            'nuxt.config.js', 'nuxt.config.ts',
            'vue.config.js',
            'angular.json',
        ]

        config_files = []

        # 通配符模式
        wildcard_patterns = ['*.ioc', '*.dts', '*.dtsi', '*.uvprojx', '*.ewp', '*.pro']

        files_set = set(files)

        for pattern in config_patterns:
            if pattern in files_set:
                config_files.append(pattern)

        for pattern in wildcard_patterns:
            ext = pattern[1:]
            for f in files:
                if f.endswith(ext):
                    config_files.append(f)

        return config_files[:20]  # 限制数量

    def _scan_modules(self, dirs: List[str]) -> List[str]:
        """扫描模块目录"""
        common_modules = {
            'src', 'lib', 'app', 'core', 'internal', 'cmd',
            'components', 'pages', 'hooks', 'store', 'api', 'utils',
            'controllers', 'services', 'models', 'routes', 'middleware',
            'drivers', 'hal', 'bsp', 'kernel', 'frameworks',
            'features', 'modules', 'packages', 'domains',
            'entities', 'usecases', 'repositories',
            'presentation', 'data', 'di',
            'public', 'private', 'test', 'tests', 'spec',
        }

        modules = []
        for d in dirs:
            name = Path(d).name
            if name in common_modules:
                modules.append(d)

        return sorted(modules)

    def _extract_dependencies(self, files: List[str]) -> List[Dict[str, str]]:
        """提取依赖信息"""
        dependencies = []
        files_set = set(files)

        # package.json
        if 'package.json' in files_set:
            try:
                with open(self.target_dir / 'package.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for dep_type in ['dependencies', 'devDependencies']:
                        if dep_type in data:
                            for name, version in data[dep_type].items():
                                dependencies.append({
                                    'name': name,
                                    'version': version,
                                    'type': dep_type,
                                    'source': 'package.json'
                                })
            except (IOError, OSError, json.JSONDecodeError):
                pass

        # requirements.txt
        if 'requirements.txt' in files_set:
            try:
                with open(self.target_dir / 'requirements.txt', 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            # 解析包名和版本
                            match = re.match(r'^([a-zA-Z0-9_-]+)\s*([<>=!]+.*)?$', line)
                            if match:
                                dependencies.append({
                                    'name': match.group(1),
                                    'version': match.group(2) or '',
                                    'type': 'dependency',
                                    'source': 'requirements.txt'
                                })
            except (IOError, OSError):
                pass

        # Cargo.toml
        if 'Cargo.toml' in files_set:
            try:
                content = (self.target_dir / 'Cargo.toml').read_text(encoding='utf-8')
                # 简单解析 [dependencies]
                in_deps = False
                for line in content.split('\n'):
                    line = line.strip()
                    if line == '[dependencies]':
                        in_deps = True
                        continue
                    if line.startswith('['):
                        in_deps = False
                    if in_deps and '=' in line:
                        name, version = line.split('=', 1)
                        dependencies.append({
                            'name': name.strip(),
                            'version': version.strip().strip('"'),
                            'type': 'dependency',
                            'source': 'Cargo.toml'
                        })
            except (IOError, OSError):
                pass

        return dependencies[:50]  # 限制数量

    def _detect_target_platform(self, project_types: List[str]) -> str:
        """检测目标平台"""
        platform_map = {
            # Mobile
            'android-app': 'android',
            'android-ndk': 'android',
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
            'qnx': 'embedded',
            'aosp': 'embedded',

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

            # Desktop
            'electron': 'desktop',
            'qt': 'desktop',

            # System
            'cmake': 'native',
            'makefile': 'native',
            'go': 'cross-platform',
            'rust': 'cross-platform',
        }

        for ptype in project_types:
            if ptype in platform_map:
                return platform_map[ptype]

        return 'unknown'

    def _detect_scale(self, files: List[str], dirs: List[str]) -> str:
        """检测项目规模"""
        file_count = len(files)
        dir_count = len(dirs)

        # 检测是否有多进程特征
        has_multiple_processes = self._has_multiple_processes(files)

        if file_count > 5000 or dir_count > 500 or has_multiple_processes:
            return 'large'
        elif file_count > 500 or dir_count > 50:
            return 'medium'
        return 'small'

    def _has_multiple_processes(self, files: List[str]) -> bool:
        """检测是否有多进程"""
        # 检测多进程特征文件
        process_indicators = [
            'AndroidManifest.xml',  # Android 多进程
            '.aidl',  # Binder IPC
            'system/', 'frameworks/',  # AOSP
            'vehicle/', 'infotainment/', 'adas/',  # 智能座舱常见目录
        ]

        for f in files:
            for indicator in process_indicators:
                if indicator in f:
                    return True

        # 检测多个 main 函数
        main_files = [f for f in files if 'main.' in f.lower()]
        if len(main_files) > 3:
            return True

        return False

    def _detect_subsystems(self, dirs: List[str]) -> List[str]:
        """检测子系统"""
        # 常见子系统目录名
        subsystem_patterns = {
            'vehicle', 'infotainment', 'adas', 'cluster',
            'tbox', 'hud', 'ivi', 'autonomous',
            'frameworks', 'system', 'hardware', 'packages',
            'services', 'apps', 'core', 'common',
        }

        subsystems = []
        for d in dirs:
            name = Path(d).name.lower()
            if name in subsystem_patterns:
                subsystems.append(name)
            # 也检查一级目录
            parts = d.split('/')
            if len(parts) == 1 and parts[0] in subsystem_patterns:
                if parts[0] not in subsystems:
                    subsystems.append(parts[0])

        return list(set(subsystems))[:10]

    def _detect_processes(self, files: List[str]) -> List[str]:
        """检测进程（通过 main 文件推断）"""
        processes = []

        # 查找 main 文件作为进程入口
        main_patterns = ['main.cpp', 'main.c', 'main.py', 'main.go', 'main.rs']

        for f in files:
            fname = Path(f).name.lower()
            if fname in main_patterns:
                # 从路径推断进程名
                parts = f.split('/')
                if len(parts) > 1:
                    process_name = parts[-2]  # 父目录名
                    if process_name not in processes:
                        processes.append(process_name)

        return processes[:20]

    def _detect_ipc_protocols(self, files: List[str]) -> List[str]:
        """检测 IPC 协议"""
        protocols = set()

        ipc_indicators = {
            '.aidl': 'binder',
            '.hal': 'hwbinder',
            '.proto': 'grpc',
            'dbus': 'dbus',
            'someip': 'someip',
            'vsomeip': 'someip',
            'commonapi': 'someip',
        }

        for f in files:
            f_lower = f.lower()
            for indicator, protocol in ipc_indicators.items():
                if indicator in f_lower:
                    protocols.add(protocol)

        # 检查文件名中的 IPC 关键字
        ipc_keywords = ['binder', 'dbus', 'socket', 'grpc', 'someip']
        for f in files:
            f_lower = f.lower()
            for kw in ipc_keywords:
                if kw in f_lower:
                    protocols.add(kw)

        return list(protocols)

    def get_subskill_path(self) -> Optional[str]:
        """获取对应的子skill路径"""
        project_type = self.detect().get('project_type', 'unknown')

        skill_map = {
            'android-app': 'mobile/android.md',
            'android-ndk': 'embedded/android-native.md',
            'aosp': 'embedded/android-native.md',
            'ios': 'mobile/ios.md',
            'stm32': 'embedded/mcu.md',
            'esp32': 'embedded/mcu.md',
            'pico': 'embedded/mcu.md',
            'keil': 'embedded/mcu.md',
            'iar': 'embedded/mcu.md',
            'freertos': 'embedded/rtos.md',
            'zephyr': 'embedded/rtos.md',
            'rt-thread': 'embedded/rtos.md',
            'embedded-linux': 'embedded/linux.md',
            'buildroot': 'embedded/linux.md',
            'yocto': 'embedded/linux.md',
            'qnx': 'embedded/qnx.md',
            'react': 'web/frontend.md',
            'vue': 'web/frontend.md',
            'angular': 'web/frontend.md',
            'svelte': 'web/frontend.md',
            'nextjs': 'web/frontend.md',
            'nuxt': 'web/frontend.md',
            'django': 'web/backend.md',
            'fastapi': 'web/backend.md',
            'flask': 'web/backend.md',
            'electron': 'desktop/desktop.md',
            'qt': 'desktop/desktop.md',
            'cmake': 'system/native.md',
            'makefile': 'system/native.md',
            'go': 'system/native.md',
            'rust': 'system/native.md',
            'flutter': 'desktop/desktop.md',
        }

        return skill_map.get(project_type)

    @classmethod
    def clear_cache(cls):
        """清除缓存"""
        cls._cache.clear()


def main():
    if len(sys.argv) < 2:
        target_dir = os.getcwd()
    else:
        target_dir = sys.argv[1]

    # 解析参数
    force_refresh = '--force' in sys.argv
    verbose = '--verbose' in sys.argv

    if force_refresh:
        ProjectDetector.clear_cache()

    detector = ProjectDetector(target_dir)
    result = detector.detect()

    if verbose:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        # 简洁输出
        output = {
            'project_type': result['project_type'],
            'language': result['language'],
            'build_system': result['build_system'],
            'entry_points': result['entry_points'][:5],
            'config_files': result['config_files'][:10],
            'scale': result.get('scale', 'small'),
        }
        if result.get('secondary_types'):
            output['secondary_types'] = result['secondary_types']
        # 大型项目额外信息
        if result.get('scale') == 'large':
            output['subsystems'] = result.get('subsystems', [])[:5]
            output['processes'] = len(result.get('processes', []))
            output['ipc_protocols'] = result.get('ipc_protocols', [])
        print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()