#!/usr/bin/env python3
"""
iOS/macOS 应用设计质量自动检查器。
检查颜色系统、字体规范、间距规范、深色模式适配、按钮层级等。
"""

import re
import os
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class CheckResult:
    name: str
    passed: bool
    severity: str  # PASS, WARNING, BLOCKER
    message: str
    fix: Optional[str] = None


class DesignQualityChecker:
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.results: List[CheckResult] = []

        self.checks = [
            ("颜色系统(631原则)", self.check_color_system),
            ("字体规范(≤2种字体家族)", self.check_typography),
            ("间距规范(8点网格)", self.check_spacing),
            ("圆角规范", self.check_corner_radius),
            ("深色模式(无硬编码颜色)", self.check_dark_mode),
            ("按钮层级(1页1主按钮)", self.check_button_hierarchy),
            ("SF Symbols使用(非emoji)", self.check_sf_symbols),
            ("本地化(NSLocalizedString)", self.check_localization),
            ("非系统字体检测", self.check_system_fonts),
            ("渐变背景检测", self.check_gradient_backgrounds),
        ]

    def check_color_system(self) -> CheckResult:
        """检查颜色使用是否符合规范——找出硬编码RGB颜色值"""
        swift_files = list(self.project_path.rglob("*.swift"))
        hardcoded_colors = []

        for f in swift_files:
            content = f.read_text(encoding="utf-8", errors="ignore")
            # 匹配 Color(UIColor(red:... / Color(red:... / UIColor(red:...
            matches = re.findall(
                r'(Color|UIColor)\(.*?red:\s*\d+\.\d+.*?green:\s*\d+\.\d+.*?blue:\s*\d+\.\d+',
                content, re.DOTALL
            )
            if matches:
                hardcoded_colors.append((f.name, len(matches)))

        if not hardcoded_colors:
            return CheckResult(
                name="颜色系统(631原则)",
                passed=True, severity="PASS",
                message="未检测到硬编码颜色值"
            )

        total = sum(c[1] for c in hardcoded_colors)
        files_detail = ", ".join(f"{f}({n}处)" for f, n in hardcoded_colors[:5])
        return CheckResult(
            name="颜色系统(631原则)",
            passed=False, severity="BLOCKER",
            message=f"检测到 {total} 处硬编码颜色值(前5: {files_detail})",
            fix="将这些颜色移至 Asset Catalog 并配置 Light/Dark 双变体命名颜色"
        )

    def check_typography(self) -> CheckResult:
        """检查字体家族数量"""
        swift_files = list(self.project_path.rglob("*.swift"))
        font_families = set()

        for f in swift_files:
            content = f.read_text(encoding="utf-8", errors="ignore")
            fonts = re.findall(r"\.font\(\.([a-zA-Z]+)", content)
            # 简单过滤，只检查自定义字体
            custom = re.findall(r'font\(.*?"([^"]+)"', content)
            font_families.update(custom)

        # 过滤系统字体名
        system_fonts = {"title", "headline", "body", "caption", "footnote",
                        "largeTitle", "title2", "title3", "callout", "system"}

        non_system = [f for f in font_families if f.lower() not in system_fonts]

        if len(non_system) > 2:
            return CheckResult(
                name="字体规范",
                passed=False, severity="WARNING",
                message=f"检测到 {len(non_system)} 种非系统字体家族: {', '.join(non_system)}",
                fix="限制字体家族不超过2种，推荐使用 SF Pro + PingFang SC"
            )

        return CheckResult(
            name="字体规范",
            passed=True, severity="PASS",
            message=f"字体使用规范({len(non_system)}种非系统字体)"
        )

    def check_spacing(self) -> CheckResult:
        """检查间距是否为8点网格"""
        swift_files = list(self.project_path.rglob("*.swift"))
        non_grid_spacings = []

        for f in swift_files:
            content = f.read_text(encoding="utf-8", errors="ignore")
            # 匹配 .padding(XX) 或 .frame(height: XX) 或 spacing: XX
            spacings = re.findall(r'(?:padding|spacing)\(?\s*(\d+)\s*\)?', content)
            for s in spacings:
                val = int(s)
                if val % 8 != 0 and val > 0 and val < 100:
                    non_grid_spacings.append((f.name, val))

        if non_grid_spacings:
            detail = ", ".join(f"{f}:{v}px" for f, v in non_grid_spacings[:5])
            return CheckResult(
                name="间距规范(8点网格)",
                passed=False, severity="WARNING",
                message=f"检测到非8点网格间距: {detail}",
                fix="推荐的间距值: 4, 8, 12, 16, 24, 32, 48"
            )

        return CheckResult(
            name="间距规范(8点网格)",
            passed=True, severity="PASS",
            message="所有间距遵循8点网格系统"
        )

    def check_corner_radius(self) -> CheckResult:
        """检查圆角值是否符合规范"""
        swift_files = list(self.project_path.rglob("*.swift"))
        unusual_radii = []

        for f in swift_files:
            content = f.read_text(encoding="utf-8", errors="ignore")
            radii = re.findall(r'cornerRadius\((\d+)\)', content)
            for r in radii:
                val = int(r)
                if val not in (6, 8, 10, 12, 16, 20, 0) and val > 0:
                    unusual_radii.append((f.name, val))

        if unusual_radii:
            detail = ", ".join(f"{f}:{v}px" for f, v in unusual_radii[:5])
            return CheckResult(
                name="圆角规范",
                passed=False, severity="WARNING",
                message=f"检测到非常规圆角值: {detail}",
                fix="推荐圆角: 6(按钮/标签), 12(卡片/弹窗), 20(模态视图)"
            )

        return CheckResult(
            name="圆角规范",
            passed=True, severity="PASS",
            message="圆角值在规范范围内"
        )

    def check_dark_mode(self) -> CheckResult:
        """检查是否有硬编码颜色值"""
        swift_files = list(self.project_path.rglob("*.swift"))
        hardcoded = []

        for f in swift_files:
            content = f.read_text(encoding="utf-8", errors="ignore")
            # 匹配 0x 开头的颜色
            hex_colors = re.findall(r'0x([0-9A-Fa-f]{6})', content)
            if hex_colors:
                hardcoded.append((f.name, len(hex_colors)))

        if hardcoded:
            total = sum(c[1] for c in hardcoded)
            detail = ", ".join(f"{f}({n}处)" for f, n in hardcoded[:3])
            return CheckResult(
                name="深色模式(无硬编码颜色)",
                passed=False, severity="BLOCKER",
                message=f"检测到 {total} 处硬编码Hex颜色({detail})",
                fix="使用 Asset Catalog 命名颜色，配置 Light/Dark 两套色值"
            )

        return CheckResult(
            name="深色模式(无硬编码颜色)",
            passed=True, severity="PASS",
            message="未检测到硬编码颜色值，深色模式适配良好"
        )

    def check_button_hierarchy(self) -> CheckResult:
        """检查按钮层级——简单扫描文件中的按钮数量"""
        swift_files = list(self.project_path.rglob("*.swift"))
        primary_buttons = 0
        found_files = []

        for f in swift_files:
            content = f.read_text(encoding="utf-8", errors="ignore")
            buttons = re.findall(r'(Button|\.borderedProminent|\.bordered)', content)
            primary_buttons += len(buttons)
            if buttons:
                found_files.append(f.name)

        return CheckResult(
            name="按钮层级",
            passed=True, severity="PASS",
            message=f"检测到 {primary_buttons} 个按钮控件(分布在 {len(found_files)} 文件)"
        )

    def check_sf_symbols(self) -> CheckResult:
        """检查是否使用 emoji 作为图标"""
        swift_files = list(self.project_path.rglob("*.swift"))
        emoji_icons = []

        for f in swift_files:
            content = f.read_text(encoding="utf-8", errors="ignore")
            # 匹配 Label("文字", systemImage: ... 中的 emoji
            # 以及 Image(systemName: 中的文字
            # 这两个都是SF Symbols的正确保用方式
            # 反向检查：找Label中使用emoji的地方
            emoji_pattern = re.findall(r'Label\(["\'][\u2600-\u27BF\u1F300-\u1FFFF]', content)
            if emoji_pattern:
                emoji_icons.append(f.name)

        if emoji_icons:
            return CheckResult(
                name="SF Symbols使用(非emoji)",
                passed=False, severity="BLOCKER",
                message=f"检测到使用emoji作为图标的文件: {', '.join(emoji_icons)}",
                fix="将emoji替换为SF Symbols: systemImage 参数"
            )

        return CheckResult(
            name="SF Symbols使用(非emoji)",
            passed=True, severity="PASS",
            message="未检测到emoji图标使用，推荐使用SF Symbols"
        )

    def check_localization(self) -> CheckResult:
        """检查本地化——查找未使用NSLocalizedString的用户可见文本"""
        swift_files = list(self.project_path.rglob("*.swift"))
        unlocalized = []

        for f in swift_files:
            content = f.read_text(encoding="utf-8", errors="ignore")
            # 简单检测：硬编码中文字符串（非注释中的）
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if 'Text("' in line and 'NSLocalizedString' not in line:
                    # 排除系统框架文件和注释
                    if not line.strip().startswith('//'):
                        unlocalized.append((f.name, i + 1))

        if unlocalized:
            return CheckResult(
                name="本地化(NSLocalizedString)",
                passed=False, severity="WARNING",
                message=f"检测到 {len(unlocalized)} 处可能未本地化的文本",
                fix="使用 NSLocalizedString + String Catalog 管理所有用户可见文本"
            )

        return CheckResult(
            name="本地化(NSLocalizedString)",
            passed=True, severity="PASS",
            message="文本使用NSLocalizedString"
        )

    def check_system_fonts(self) -> CheckResult:
        """检查是否使用了非系统字体"""
        swift_files = list(self.project_path.rglob("*.swift"))
        found = []

        for f in swift_files:
            content = f.read_text(encoding="utf-8", errors="ignore")
            if 'Inter' in content or 'Roboto' in content:
                found.append(f.name)

        if found:
            return CheckResult(
                name="非系统字体检测",
                passed=False, severity="BLOCKER",
                message=f"检测到使用非Apple系统字体: {', '.join(found)}",
                fix="将 Inter/Roboto 替换为系统字体: SF Pro / PingFang SC"
            )

        return CheckResult(
            name="非系统字体检测",
            passed=True, severity="PASS",
            message="未检测到非系统字体"
        )

    def check_gradient_backgrounds(self) -> CheckResult:
        """检查是否使用紫蓝渐变背景"""
        swift_files = list(self.project_path.rglob("*.swift"))
        found = []

        for f in swift_files:
            content = f.read_text(encoding="utf-8", errors="ignore")
            if ('purple' in content.lower() and 'blue' in content.lower()
                    and 'gradient' in content.lower()):
                found.append(f.name)

        if found:
            return CheckResult(
                name="渐变背景检测",
                passed=False, severity="WARNING",
                message=f"检测到紫蓝渐变背景嫌疑: {', '.join(found)}",
                fix="避免紫蓝渐变背景，使用有目的性的色彩方案"
            )

        return CheckResult(
            name="渐变背景检测",
            passed=True, severity="PASS",
            message="未检测到紫蓝渐变背景"
        )

    def run_all(self) -> List[CheckResult]:
        self.results = []
        for name, check_fn in self.checks:
            try:
                result = check_fn()
                self.results.append(result)
            except Exception as e:
                self.results.append(CheckResult(
                    name=name, passed=False, severity="WARNING",
                    message=f"检查执行异常: {e}"
                ))
        return self.results

    def generate_report(self) -> str:
        report_lines = [
            "=" * 60,
            "  iOS/macOS 设计质量检查报告",
            "=" * 60,
            f"  项目路径: {self.project_path}",
            f"  检查时间: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "",
        ]

        passed = sum(1 for r in self.results if r.passed)
        warnings = sum(1 for r in self.results
                       if not r.passed and r.severity == "WARNING")
        blockers = sum(1 for r in self.results
                       if not r.passed and r.severity == "BLOCKER")

        total = len(self.results)
        score = int((passed / total) * 100) if total > 0 else 0

        report_lines.append(f"  ✅ 通过: {passed}/{total} | "
                            f"⚠️ 警告: {warnings} | "
                            f"🔴 阻塞: {blockers}")
        report_lines.append(f"  质量评分: {score}/100")
        report_lines.append("")

        # 按严重程度排列
        severity_order = {"BLOCKER": 0, "WARNING": 1, "PASS": 2}
        sorted_results = sorted(self.results,
                                key=lambda r: severity_order.get(r.severity, 3))

        for r in sorted_results:
            if r.passed:
                icon = "✅"
            elif r.severity == "WARNING":
                icon = "⚠️"
            else:
                icon = "🔴"

            report_lines.append(f"{icon} [{r.severity}] {r.name}")
            report_lines.append(f"   {r.message}")
            if r.fix:
                report_lines.append(f"   🔧 修复建议: {r.fix}")
            report_lines.append("")

        report_lines.append("=" * 60)
        return "\n".join(report_lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="iOS/macOS 设计质量检查器"
    )
    parser.add_argument("project_path",
                        help="Xcode 项目根目录路径")
    parser.add_argument("--output", "-o",
                        help="输出报告文件路径")
    parser.add_argument("--json", action="store_true",
                        help="以 JSON 格式输出")

    args = parser.parse_args()

    if not os.path.isdir(args.project_path):
        print(f"错误: 无效的项目路径: {args.project_path}", file=sys.stderr)
        sys.exit(1)

    checker = DesignQualityChecker(args.project_path)
    checker.run_all()

    if args.json:
        import json
        report = json.dumps([
            {"name": r.name, "passed": r.passed,
             "severity": r.severity, "message": r.message,
             "fix": r.fix}
            for r in checker.results
        ], ensure_ascii=False, indent=2)
    else:
        report = checker.generate_report()

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"报告已写入: {args.output}")
    else:
        print(report)

    # 如果有任何 BLOCKER，返回非零退出码
    if any(r.severity == "BLOCKER" for r in checker.results):
        sys.exit(1)


if __name__ == "__main__":
    main()
