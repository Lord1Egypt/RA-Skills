# -*- coding: utf-8 -*-
"""Proactive Intelligence - 技能管理器"""

import subprocess
import json
import os
from pathlib import Path
from datetime import datetime, timedelta

# 设置标准输出编码
import sys
sys.stdout.reconfigure(encoding='utf-8')

class SkillManager:
    def __init__(self):
        self.skills_dir = Path.home() / ".openclaw" / "workspace" / "skills"
        self.memory_dir = Path.home() / "proactive-intelligence"
        self.memory_dir.mkdir(parents=True, exist_ok=True)
    
    def run_command(self, cmd):
        """运行命令并返回输出"""
        try:
            result = subprocess.run(
                cmd, 
                shell=True, 
                capture_output=True, 
                text=True,
                encoding='utf-8'
            )
            return result.stdout.strip(), result.stderr.strip(), result.returncode
        except Exception as e:
            return "", str(e), 1
    
    def list_installed_skills(self):
        """列出已安装的技能"""
        stdout, stderr, code = self.run_command("clawhub list")
        if code == 0:
            skills = []
            for line in stdout.split('\n'):
                if line.strip() and not line.startswith('-'):
                    parts = line.split()
                    if len(parts) >= 2:
                        skills.append({
                            'name': parts[0],
                            'version': parts[1]
                        })
            return skills
        return []
    
    def check_outdated_skills(self):
        """检查过时的技能"""
        stdout, stderr, code = self.run_command("clawhub outdated")
        if code == 0:
            return stdout
        return None
    
    def check_skill_health(self, skill_name):
        """检查技能健康状态"""
        skill_path = self.skills_dir / skill_name
        if not skill_path.exists():
            return {'status': 'missing', 'path': str(skill_path)}
        
        meta_file = skill_path / "_meta.json"
        skill_file = skill_path / "SKILL.md"
        
        health = {
            'status': 'healthy',
            'path': str(skill_path),
            'has_meta': meta_file.exists(),
            'has_skill': skill_file.exists(),
            'last_modified': None
        }
        
        if skill_file.exists():
            mtime = skill_file.stat().st_mtime
            health['last_modified'] = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M')
        
        return health
    
    def analyze_usage_patterns(self):
        """分析技能使用模式"""
        # 这里可以添加更复杂的分析逻辑
        # 目前返回基本统计
        
        skills = self.list_installed_skills()
        analysis = {
            'total_skills': len(skills),
            'skills': []
        }
        
        for skill in skills:
            health = self.check_skill_health(skill['name'])
            analysis['skills'].append({
                'name': skill['name'],
                'version': skill['version'],
                'health': health['status']
            })
        
        return analysis
    
    def recommend_skills(self):
        """推荐技能"""
        # 基于当前技能推荐相关技能
        current_skills = [s['name'] for s in self.list_installed_skills()]
        recommendations = []
        
        # 检查是否缺少常用技能
        common_skills = {
            'agent-reach': '多平台搜索',
            'tavily': '网络搜索',
            'file-reader': '文件读取',
            'proactivity': '主动代理（已融合到 Proactive Intelligence）',
            'self-improving': '自我改进（已融合到 Proactive Intelligence）'
        }
        
        for skill, desc in common_skills.items():
            if skill not in current_skills and '已融合' not in desc:
                recommendations.append({
                    'name': skill,
                    'reason': desc,
                    'command': f'clawhub install {skill}'
                })
        
        return recommendations
    
    def generate_health_report(self):
        """生成健康报告"""
        report = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'installed_skills': self.list_installed_skills(),
            'analysis': self.analyze_usage_patterns(),
            'recommendations': self.recommend_skills(),
            'outdated': self.check_outdated_skills()
        }
        
        return report
    
    def save_report(self, report):
        """保存报告到文件"""
        report_file = self.memory_dir / "skill-health-report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        return report_file
    
    def print_report(self, report):
        """打印报告"""
        print(f"\n[REPORT] 技能健康报告 - {report['timestamp']}")
        print("=" * 50)
        
        print(f"\n[STATS] 已安装技能: {len(report['installed_skills'])}")
        for skill in report['installed_skills']:
            print(f"  - {skill['name']} (v{skill['version']})")
        
        print(f"\n[RECOMMEND] 推荐安装:")
        if report['recommendations']:
            for rec in report['recommendations']:
                print(f"  - {rec['name']}: {rec['reason']}")
                print(f"    安装命令: {rec['command']}")
        else:
            print("  暂无推荐")
        
        if report['outdated']:
            print(f"\n[OUTDATED] 可更新:")
            print(report['outdated'])
        else:
            print(f"\n[OK] 所有技能已是最新版本")


def main():
    """主函数"""
    print("[INIT] Proactive Intelligence - 技能管理器")
    print("=" * 50)
    
    manager = SkillManager()
    
    # 生成报告
    report = manager.generate_health_report()
    
    # 打印报告
    manager.print_report(report)
    
    # 保存报告
    report_file = manager.save_report(report)
    print(f"\n[SAVED] 报告已保存到: {report_file}")
    
    # 提供操作建议
    print("\n[ACTIONS] 建议操作:")
    print("  1. 查看推荐技能并考虑安装")
    print("  2. 更新过时的技能")
    print("  3. 清理不再使用的技能")
    print("  4. 定期运行此脚本检查健康状态")


if __name__ == "__main__":
    main()
