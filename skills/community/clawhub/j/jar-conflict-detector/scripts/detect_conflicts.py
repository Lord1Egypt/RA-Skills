#!/usr/bin/env python3
"""
JAR Conflict Detector for Spring Boot Microservices
====================================================
Detects dependency version conflicts and duplicate JARs in Maven/Gradle projects.

Usage:
    python detect_conflicts.py [--project-dir <dir>] [--output <report.html|report.txt>]
                               [--mode <maven|gradle|auto>] [--level <warn|error|all>]

Requirements:
    - Python 3.8+
    - Maven (mvn) or Gradle (gradle/gradlew) on PATH for live dependency analysis
    - No third-party Python packages required
"""

import argparse
import json
import os
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


# ─────────────────────────────────────────────
# Data Models
# ─────────────────────────────────────────────

@dataclass
class Dependency:
    group_id: str
    artifact_id: str
    version: str
    scope: str = "compile"
    source_module: str = ""
    classifier: str = ""

    @property
    def ga_key(self) -> str:
        """GroupId:ArtifactId key (version-agnostic)."""
        return f"{self.group_id}:{self.artifact_id}"

    @property
    def gav(self) -> str:
        return f"{self.group_id}:{self.artifact_id}:{self.version}"


@dataclass
class Conflict:
    artifact_key: str          # groupId:artifactId
    versions: List[str]        # all conflicting versions found
    modules: List[str]         # which modules declare them
    severity: str              # "ERROR" | "WARN" | "INFO"
    conflict_type: str         # "version_conflict" | "duplicate" | "known_incompatible"
    suggestion: str = ""       # resolution hint


@dataclass
class ScanResult:
    project_dir: str
    scan_time: str
    build_tool: str
    modules: List[str] = field(default_factory=list)
    dependencies: List[Dependency] = field(default_factory=list)
    conflicts: List[Conflict] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


# ─────────────────────────────────────────────
# Known Incompatible Pair Rules
# ─────────────────────────────────────────────

KNOWN_INCOMPATIBLE_PAIRS = [
    {
        "desc": "Spring Boot 2.x 不兼容 Spring Framework 5.0.x (需要 5.2+)",
        "pattern_a": ("org.springframework.boot", "spring-boot", lambda v: v.startswith("2.")),
        "pattern_b": ("org.springframework", "spring-core", lambda v: v.startswith("5.0.")),
        "severity": "ERROR",
        "suggestion": "升级 spring-core 至 5.2.x 或 5.3.x，或使用 Spring Boot BOM 统一管理版本"
    },
    {
        "desc": "Spring Boot 3.x 需要 Spring Framework 6.x，不兼容 5.x",
        "pattern_a": ("org.springframework.boot", "spring-boot", lambda v: v.startswith("3.")),
        "pattern_b": ("org.springframework", "spring-core", lambda v: v.startswith("5.")),
        "severity": "ERROR",
        "suggestion": "使用 Spring Boot 3.x 时，spring-core 必须为 6.x"
    },
    {
        "desc": "log4j 1.x 与 log4j2 同时存在（冗余且存在安全风险）",
        "pattern_a": ("log4j", "log4j", lambda v: True),
        "pattern_b": ("org.apache.logging.log4j", "log4j-core", lambda v: True),
        "severity": "WARN",
        "suggestion": "移除 log4j 1.x，统一使用 log4j2 或 logback"
    },
    {
        "desc": "Slf4j 多重绑定：logback-classic 与 log4j-slf4j-impl 同时存在",
        "pattern_a": ("ch.qos.logback", "logback-classic", lambda v: True),
        "pattern_b": ("org.apache.logging.log4j", "log4j-slf4j-impl", lambda v: True),
        "severity": "ERROR",
        "suggestion": "Slf4j 只能有一个绑定实现，移除其中一个"
    },
    {
        "desc": "javax.servlet 与 jakarta.servlet 同时存在（Jakarta EE 迁移冲突）",
        "pattern_a": ("javax.servlet", "javax.servlet-api", lambda v: True),
        "pattern_b": ("jakarta.servlet", "jakarta.servlet-api", lambda v: True),
        "severity": "ERROR",
        "suggestion": "Spring Boot 3.x 使用 jakarta.*，Spring Boot 2.x 使用 javax.*，不可混用"
    },
    {
        "desc": "Guava 不同版本（Android 版 vs JRE 版）混用",
        "pattern_a": ("com.google.guava", "guava", lambda v: "-android" in v),
        "pattern_b": ("com.google.guava", "guava", lambda v: "-jre" in v or ("-android" not in v and v)),
        "severity": "WARN",
        "suggestion": "统一使用 guava jre 版本，除非项目需要 Android 兼容"
    },
    {
        "desc": "Hibernate Validator 版本过低（低于 6.x）与 Spring Boot 2.3+ 不兼容",
        "pattern_a": ("org.springframework.boot", "spring-boot", lambda v: tuple(int(x) for x in v.split(".")[:2] if x.isdigit()) >= (2, 3)),
        "pattern_b": ("org.hibernate.validator", "hibernate-validator", lambda v: v.startswith("5.")),
        "severity": "ERROR",
        "suggestion": "Spring Boot 2.3+ 需要 hibernate-validator 6.x 或更高版本"
    },
]


# ─────────────────────────────────────────────
# Maven Dependency Parser
# ─────────────────────────────────────────────

NS = {"m": "http://maven.apache.org/POM/4.0.0"}


def parse_pom_xml(pom_path: Path) -> Tuple[List[Dependency], str]:
    """Parse dependencies from a pom.xml file."""
    deps = []
    module_name = pom_path.parent.name

    try:
        tree = ET.parse(pom_path)
        root = tree.getroot()

        # Try to get module artifactId
        artifact_el = root.find("m:artifactId", NS) or root.find("artifactId")
        if artifact_el is not None:
            module_name = artifact_el.text or module_name

        # Collect properties for variable substitution
        props = {}
        props_el = root.find("m:properties", NS) or root.find("properties")
        if props_el is not None:
            for prop in props_el:
                tag = prop.tag.replace("{http://maven.apache.org/POM/4.0.0}", "")
                props[tag] = prop.text or ""

        def resolve(val: Optional[str]) -> str:
            if not val:
                return ""
            # resolve ${property} references
            for k, v in props.items():
                val = val.replace(f"${{{k}}}", v)
            return val

        deps_el = root.find("m:dependencies", NS) or root.find("dependencies")
        if deps_el is not None:
            for dep_el in deps_el:
                gid = dep_el.find("m:groupId", NS) or dep_el.find("groupId")
                aid = dep_el.find("m:artifactId", NS) or dep_el.find("artifactId")
                ver = dep_el.find("m:version", NS) or dep_el.find("version")
                scope_el = dep_el.find("m:scope", NS) or dep_el.find("scope")

                if gid is not None and aid is not None:
                    version = resolve(ver.text) if ver is not None else "managed"
                    scope = scope_el.text if scope_el is not None else "compile"
                    deps.append(Dependency(
                        group_id=resolve(gid.text or ""),
                        artifact_id=resolve(aid.text or ""),
                        version=version,
                        scope=scope,
                        source_module=module_name
                    ))
    except ET.ParseError as e:
        print(f"  [WARN] 解析 {pom_path} 失败: {e}", file=sys.stderr)

    return deps, module_name


def run_mvn_dependency_tree(project_dir: Path) -> Optional[str]:
    """Run mvn dependency:tree and capture output."""
    mvn_cmd = "mvn"
    try:
        result = subprocess.run(
            [mvn_cmd, "dependency:tree", "-DoutputType=text", "--batch-mode", "-q"],
            cwd=project_dir,
            capture_output=True,
            text=True,
            timeout=300
        )
        if result.returncode == 0:
            return result.stdout
        else:
            print(f"  [WARN] mvn dependency:tree 执行失败:\n{result.stderr[:500]}", file=sys.stderr)
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        print(f"  [WARN] 无法执行 mvn: {e}", file=sys.stderr)
    return None


def parse_mvn_tree_output(tree_output: str) -> List[Dependency]:
    """Parse Maven dependency:tree text output."""
    deps = []
    current_module = "root"
    # Pattern: [INFO] groupId:artifactId:jar:version:scope
    dep_pattern = re.compile(
        r'\[INFO\]\s+[\|\\\+\- ]*([^:]+):([^:]+):(?:jar|war|pom|aar|ejb|test-jar):([^:]+):(\S+)'
    )
    module_pattern = re.compile(r'\[INFO\] Building (.+?) \[')

    for line in tree_output.splitlines():
        m_mod = module_pattern.search(line)
        if m_mod:
            current_module = m_mod.group(1).strip()
            continue
        m_dep = dep_pattern.search(line)
        if m_dep:
            deps.append(Dependency(
                group_id=m_dep.group(1),
                artifact_id=m_dep.group(2),
                version=m_dep.group(3),
                scope=m_dep.group(4),
                source_module=current_module
            ))
    return deps


# ─────────────────────────────────────────────
# Gradle Dependency Parser
# ─────────────────────────────────────────────

def run_gradle_dependencies(project_dir: Path) -> Optional[str]:
    """Run gradle dependencies and capture output."""
    gradle_cmd = "gradlew.bat" if os.name == "nt" else "./gradlew"
    gradle_path = project_dir / gradle_cmd
    if not gradle_path.exists():
        gradle_cmd = "gradle"

    try:
        result = subprocess.run(
            [str(gradle_path) if gradle_path.exists() else gradle_cmd,
             "dependencies", "--configuration", "compileClasspath"],
            cwd=project_dir,
            capture_output=True,
            text=True,
            timeout=300
        )
        if result.returncode == 0:
            return result.stdout
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        print(f"  [WARN] 无法执行 gradle: {e}", file=sys.stderr)
    return None


def parse_gradle_output(output: str, module_name: str = "root") -> List[Dependency]:
    """Parse gradle dependencies output."""
    deps = []
    # Pattern: +--- group:artifact:version (->resolved) or (*) for duplicates
    dep_pattern = re.compile(
        r'[\|+\\`\- ]+([^:\s]+):([^:\s]+):([^\s\(\*]+)'
    )
    for line in output.splitlines():
        m = dep_pattern.search(line)
        if m:
            version = m.group(3).strip().rstrip("(*)")
            if "->" in version:
                version = version.split("->")[-1].strip()
            deps.append(Dependency(
                group_id=m.group(1),
                artifact_id=m.group(2),
                version=version,
                source_module=module_name
            ))
    return deps


# ─────────────────────────────────────────────
# Conflict Detection Engine
# ─────────────────────────────────────────────

def detect_version_conflicts(deps: List[Dependency]) -> List[Conflict]:
    """Detect multiple versions of the same artifact."""
    conflicts = []
    # Group by groupId:artifactId
    ga_map: Dict[str, Dict[str, List[str]]] = defaultdict(lambda: defaultdict(list))

    for dep in deps:
        if dep.version and dep.version != "managed":
            ga_map[dep.ga_key][dep.version].append(dep.source_module or "unknown")

    for ga_key, version_map in ga_map.items():
        versions = list(version_map.keys())
        if len(versions) > 1:
            all_modules = []
            for mods in version_map.values():
                all_modules.extend(mods)

            # Determine severity by comparing major versions
            major_versions = set()
            for v in versions:
                parts = v.split(".")
                if parts[0].isdigit():
                    major_versions.add(parts[0])

            severity = "ERROR" if len(major_versions) > 1 else "WARN"

            conflicts.append(Conflict(
                artifact_key=ga_key,
                versions=versions,
                modules=list(set(all_modules)),
                severity=severity,
                conflict_type="version_conflict",
                suggestion=f"在父 POM 的 <dependencyManagement> 中统一锁定 {ga_key} 版本"
            ))
    return conflicts


def detect_known_incompatibilities(deps: List[Dependency]) -> List[Conflict]:
    """Check for known incompatible pairs."""
    conflicts = []

    def find_dep(group_id, artifact_id, version_filter):
        return [d for d in deps
                if d.group_id == group_id
                and d.artifact_id == artifact_id
                and version_filter(d.version)]

    for rule in KNOWN_INCOMPATIBLE_PAIRS:
        ga, gb = rule["pattern_a"], rule["pattern_b"]
        deps_a = find_dep(ga[0], ga[1], ga[2])
        deps_b = find_dep(gb[0], gb[1], gb[2])

        if deps_a and deps_b:
            versions_found = list(set(
                [d.version for d in deps_a] + [d.version for d in deps_b]
            ))
            modules_found = list(set(
                [d.source_module for d in deps_a + deps_b]
            ))
            conflicts.append(Conflict(
                artifact_key=f"{ga[0]}:{ga[1]} <-> {gb[0]}:{gb[1]}",
                versions=versions_found,
                modules=modules_found,
                severity=rule["severity"],
                conflict_type="known_incompatible",
                suggestion=rule["suggestion"]
            ))
    return conflicts


def detect_duplicate_classes(jar_dir: Optional[Path] = None) -> List[Conflict]:
    """Detect JARs with overlapping class paths (requires compiled output or fat jar)."""
    # This is a heuristic scan - looks for common problematic duplicate artifacts
    duplicates = []
    if jar_dir and jar_dir.exists():
        jar_files = list(jar_dir.rglob("*.jar"))
        artifact_map: Dict[str, List[Path]] = defaultdict(list)

        for jar_file in jar_files:
            # Strip version from filename: spring-core-5.3.0.jar -> spring-core
            name = jar_file.stem
            base_name = re.sub(r'-\d+[\.\d\-]*(?:RELEASE|SNAPSHOT|Final|GA|SR\d+)?$', '', name, flags=re.IGNORECASE)
            artifact_map[base_name].append(jar_file)

        for base_name, jars in artifact_map.items():
            if len(jars) > 1:
                duplicates.append(Conflict(
                    artifact_key=base_name,
                    versions=[j.name for j in jars],
                    modules=[str(j.parent) for j in jars],
                    severity="ERROR",
                    conflict_type="duplicate",
                    suggestion=f"存在重复 JAR，请检查 {base_name} 的版本管理"
                ))
    return duplicates


# ─────────────────────────────────────────────
# Project Scanner
# ─────────────────────────────────────────────

def detect_build_tool(project_dir: Path) -> str:
    if (project_dir / "pom.xml").exists():
        return "maven"
    if (project_dir / "build.gradle").exists() or (project_dir / "build.gradle.kts").exists():
        return "gradle"
    return "unknown"


def scan_project(project_dir: Path, mode: str = "auto", level: str = "all") -> ScanResult:
    result = ScanResult(
        project_dir=str(project_dir),
        scan_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        build_tool=detect_build_tool(project_dir) if mode == "auto" else mode
    )

    print(f"\n🔍 扫描项目: {project_dir}")
    print(f"   构建工具: {result.build_tool}")

    all_deps: List[Dependency] = []

    if result.build_tool == "maven":
        # Try live mvn dependency:tree first
        print("   尝试运行 mvn dependency:tree ...")
        tree_output = run_mvn_dependency_tree(project_dir)
        if tree_output:
            all_deps = parse_mvn_tree_output(tree_output)
            print(f"   ✅ 从 mvn dependency:tree 解析到 {len(all_deps)} 个依赖")
        else:
            # Fallback: parse pom.xml files statically
            print("   📄 回退到静态 pom.xml 解析 ...")
            pom_files = list(project_dir.rglob("pom.xml"))
            # Exclude common non-source directories
            pom_files = [p for p in pom_files if not any(
                part in str(p) for part in [".git", "node_modules", "target", ".m2"]
            )]
            for pom in pom_files:
                deps, module = parse_pom_xml(pom)
                all_deps.extend(deps)
                result.modules.append(module)
            print(f"   ✅ 从 {len(pom_files)} 个 pom.xml 解析到 {len(all_deps)} 个依赖")

    elif result.build_tool == "gradle":
        print("   尝试运行 gradle dependencies ...")
        gradle_output = run_gradle_dependencies(project_dir)
        if gradle_output:
            all_deps = parse_gradle_output(gradle_output)
            print(f"   ✅ 从 gradle dependencies 解析到 {len(all_deps)} 个依赖")
        else:
            result.warnings.append("无法执行 gradle 命令，请确保 gradlew 存在或 gradle 在 PATH 中")
    else:
        result.errors.append(f"未检测到 Maven 或 Gradle 构建文件，请确认项目目录: {project_dir}")

    result.dependencies = all_deps

    print("\n⚙️  分析冲突 ...")
    version_conflicts = detect_version_conflicts(all_deps)
    known_conflicts = detect_known_incompatibilities(all_deps)
    all_conflicts = version_conflicts + known_conflicts

    # Filter by level
    if level == "error":
        all_conflicts = [c for c in all_conflicts if c.severity == "ERROR"]
    elif level == "warn":
        all_conflicts = [c for c in all_conflicts if c.severity in ("ERROR", "WARN")]

    result.conflicts = all_conflicts
    print(f"   发现 {len(all_conflicts)} 个冲突 "
          f"({sum(1 for c in all_conflicts if c.severity=='ERROR')} 个 ERROR, "
          f"{sum(1 for c in all_conflicts if c.severity=='WARN')} 个 WARN)")

    return result


# ─────────────────────────────────────────────
# Report Generators
# ─────────────────────────────────────────────

def generate_text_report(result: ScanResult) -> str:
    lines = []
    lines.append("=" * 70)
    lines.append("  JAR 包冲突检测报告 - Spring Boot 微服务")
    lines.append("=" * 70)
    lines.append(f"项目路径: {result.project_dir}")
    lines.append(f"扫描时间: {result.scan_time}")
    lines.append(f"构建工具: {result.build_tool}")
    lines.append(f"依赖总数: {len(result.dependencies)}")
    lines.append(f"冲突总数: {len(result.conflicts)}")
    lines.append("")

    if not result.conflicts:
        lines.append("✅ 未发现 JAR 包冲突！")
        return "\n".join(lines)

    error_conflicts = [c for c in result.conflicts if c.severity == "ERROR"]
    warn_conflicts = [c for c in result.conflicts if c.severity == "WARN"]

    if error_conflicts:
        lines.append(f"❌ 严重冲突 ({len(error_conflicts)} 个)")
        lines.append("-" * 50)
        for c in error_conflicts:
            lines.append(f"\n  [{c.conflict_type}] {c.artifact_key}")
            lines.append(f"  版本: {', '.join(c.versions)}")
            lines.append(f"  模块: {', '.join(c.modules[:5])}")
            if c.suggestion:
                lines.append(f"  💡 建议: {c.suggestion}")

    if warn_conflicts:
        lines.append(f"\n⚠️  警告冲突 ({len(warn_conflicts)} 个)")
        lines.append("-" * 50)
        for c in warn_conflicts:
            lines.append(f"\n  [{c.conflict_type}] {c.artifact_key}")
            lines.append(f"  版本: {', '.join(c.versions)}")
            lines.append(f"  模块: {', '.join(c.modules[:5])}")
            if c.suggestion:
                lines.append(f"  💡 建议: {c.suggestion}")

    if result.warnings:
        lines.append("\n📋 扫描警告:")
        for w in result.warnings:
            lines.append(f"  - {w}")

    lines.append("\n" + "=" * 70)
    lines.append("扫描完成")
    lines.append("=" * 70)
    return "\n".join(lines)


def generate_html_report(result: ScanResult) -> str:
    error_count = sum(1 for c in result.conflicts if c.severity == "ERROR")
    warn_count = sum(1 for c in result.conflicts if c.severity == "WARN")
    status_color = "#e74c3c" if error_count > 0 else ("#f39c12" if warn_count > 0 else "#27ae60")
    status_text = "检测到严重冲突" if error_count > 0 else ("检测到警告" if warn_count > 0 else "无冲突")

    conflict_rows = ""
    for c in result.conflicts:
        badge_color = "#e74c3c" if c.severity == "ERROR" else "#f39c12"
        type_label = {"version_conflict": "版本冲突", "known_incompatible": "已知不兼容", "duplicate": "重复JAR"}.get(c.conflict_type, c.conflict_type)
        conflict_rows += f"""
        <tr>
            <td><span style="background:{badge_color};color:white;padding:2px 8px;border-radius:4px;font-size:12px">{c.severity}</span></td>
            <td><code>{c.artifact_key}</code></td>
            <td>{type_label}</td>
            <td><small>{', '.join(c.versions[:4])}</small></td>
            <td><small>{', '.join(c.modules[:3])}</small></td>
            <td><small>{c.suggestion}</small></td>
        </tr>"""

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>JAR 冲突检测报告</title>
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; margin: 0; background: #f5f7fa; color: #2c3e50; }}
  .header {{ background: linear-gradient(135deg, #2c3e50, #3498db); color: white; padding: 30px 40px; }}
  .header h1 {{ margin: 0 0 8px; font-size: 24px; }}
  .header p {{ margin: 0; opacity: 0.8; font-size: 14px; }}
  .container {{ max-width: 1100px; margin: 30px auto; padding: 0 20px; }}
  .summary {{ display: flex; gap: 16px; margin-bottom: 24px; flex-wrap: wrap; }}
  .card {{ background: white; border-radius: 10px; padding: 20px 24px; flex: 1; min-width: 160px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }}
  .card .num {{ font-size: 36px; font-weight: 700; }}
  .card .label {{ color: #7f8c8d; font-size: 13px; margin-top: 4px; }}
  .status-banner {{ background: {status_color}; color: white; padding: 12px 20px; border-radius: 8px; margin-bottom: 24px; font-weight: 600; }}
  table {{ width: 100%; border-collapse: collapse; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }}
  th {{ background: #2c3e50; color: white; padding: 12px 16px; text-align: left; font-size: 13px; font-weight: 600; }}
  td {{ padding: 12px 16px; border-bottom: 1px solid #ecf0f1; font-size: 13px; vertical-align: top; }}
  tr:last-child td {{ border-bottom: none; }}
  tr:hover td {{ background: #f8f9fa; }}
  code {{ background: #f1f3f4; padding: 2px 6px; border-radius: 4px; font-size: 12px; }}
  .footer {{ text-align: center; color: #95a5a6; font-size: 12px; margin: 30px 0; }}
  .empty {{ text-align: center; padding: 40px; color: #27ae60; font-size: 18px; }}
</style>
</head>
<body>
<div class="header">
  <h1>🔍 JAR 包冲突检测报告</h1>
  <p>Spring Boot 微服务项目 · {result.project_dir} · {result.scan_time}</p>
</div>
<div class="container">
  <div class="status-banner">{'❌' if error_count > 0 else '⚠️' if warn_count > 0 else '✅'} {status_text}</div>
  <div class="summary">
    <div class="card"><div class="num">{len(result.dependencies)}</div><div class="label">依赖总数</div></div>
    <div class="card"><div class="num" style="color:#e74c3c">{error_count}</div><div class="label">严重冲突(ERROR)</div></div>
    <div class="card"><div class="num" style="color:#f39c12">{warn_count}</div><div class="label">警告(WARN)</div></div>
    <div class="card"><div class="num">{result.build_tool.upper()}</div><div class="label">构建工具</div></div>
  </div>
  {'<p class="empty">✅ 未检测到 JAR 包冲突，项目依赖状态良好！</p>' if not result.conflicts else f"""
  <table>
    <thead><tr><th>级别</th><th>依赖</th><th>冲突类型</th><th>版本</th><th>涉及模块</th><th>解决建议</th></tr></thead>
    <tbody>{conflict_rows}</tbody>
  </table>"""}
</div>
<div class="footer">由 jar-conflict-detector skill 生成 · {result.scan_time}</div>
</body>
</html>"""


def generate_json_report(result: ScanResult) -> str:
    return json.dumps({
        "project_dir": result.project_dir,
        "scan_time": result.scan_time,
        "build_tool": result.build_tool,
        "total_dependencies": len(result.dependencies),
        "conflicts": [
            {
                "severity": c.severity,
                "type": c.conflict_type,
                "artifact": c.artifact_key,
                "versions": c.versions,
                "modules": c.modules,
                "suggestion": c.suggestion
            }
            for c in result.conflicts
        ],
        "warnings": result.warnings,
        "errors": result.errors
    }, ensure_ascii=False, indent=2)


# ─────────────────────────────────────────────
# CLI Entry Point
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="检测 Spring Boot 微服务项目中的 JAR 包冲突",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python detect_conflicts.py
  python detect_conflicts.py --project-dir /path/to/my-service
  python detect_conflicts.py --output report.html
  python detect_conflicts.py --output report.json --level error
  python detect_conflicts.py --mode maven --level warn
        """
    )
    parser.add_argument("--project-dir", "-d", default=".",
                        help="Spring Boot 项目根目录（默认: 当前目录）")
    parser.add_argument("--output", "-o", default=None,
                        help="报告输出文件（支持 .html / .txt / .json，不指定则输出到控制台）")
    parser.add_argument("--mode", choices=["maven", "gradle", "auto"], default="auto",
                        help="构建工具类型（默认: auto 自动检测）")
    parser.add_argument("--level", choices=["all", "warn", "error"], default="all",
                        help="报告级别过滤（默认: all 显示全部）")

    args = parser.parse_args()
    project_dir = Path(args.project_dir).resolve()

    if not project_dir.exists():
        print(f"❌ 项目目录不存在: {project_dir}", file=sys.stderr)
        sys.exit(1)

    result = scan_project(project_dir, mode=args.mode, level=args.level)

    # Determine output format
    output_path = args.output
    if output_path:
        ext = Path(output_path).suffix.lower()
        if ext == ".html":
            content = generate_html_report(result)
        elif ext == ".json":
            content = generate_json_report(result)
        else:
            content = generate_text_report(result)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"\n📄 报告已保存: {output_path}")
    else:
        print("\n" + generate_text_report(result))

    # Exit code: 1 if errors found
    error_count = sum(1 for c in result.conflicts if c.severity == "ERROR")
    sys.exit(1 if error_count > 0 else 0)


if __name__ == "__main__":
    main()
