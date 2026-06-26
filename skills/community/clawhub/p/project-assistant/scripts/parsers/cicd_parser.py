#!/usr/bin/env python3
"""
CI/CD 配置解析器
解析 GitHub Actions、GitLab CI、Jenkinsfile 等配置
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field

# 添加日志支持
try:
    from utils.logger import get_logger
    logger = get_logger(__name__)
except ImportError:
    import logging
    logger = logging.getLogger(__name__)

# 尝试导入 yaml
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False
    logger.warning("PyYAML not installed, YAML parsing will be limited")


@dataclass
class Pipeline:
    """CI/CD 流水线"""
    name: str
    platform: str  # github, gitlab, jenkins, circleci, azure
    triggers: List[str] = field(default_factory=list)
    stages: List[str] = field(default_factory=list)
    jobs: List[Dict[str, Any]] = field(default_factory=list)
    env_vars: Dict[str, str] = field(default_factory=dict)
    secrets: List[str] = field(default_factory=list)


class CICDParser:
    """CI/CD 配置解析器"""

    # CI/CD 配置文件路径
    CONFIG_PATHS = {
        'github': ['.github/workflows/*.yml', '.github/workflows/*.yaml'],
        'gitlab': ['.gitlab-ci.yml'],
        'jenkins': ['Jenkinsfile', 'jenkinsfile'],
        'circleci': ['.circleci/config.yml'],
        'azure': ['azure-pipelines.yml', 'azure-pipelines.yaml', '.azure-pipelines.yml'],
        'travis': ['.travis.yml'],
        'drone': ['.drone.yml'],
        'bitbucket': ['bitbucket-pipelines.yml'],
    }

    def __init__(self, project_dir: str):
        self.project_dir = Path(project_dir).resolve()
        self.pipelines: List[Pipeline] = []

    def parse(self) -> Dict[str, Any]:
        """解析所有 CI/CD 配置"""
        logger.info(f"开始解析 CI/CD 配置: {self.project_dir}")

        self._parse_github_actions()
        self._parse_gitlab_ci()
        self._parse_jenkinsfile()
        self._parse_other_cicd()

        return self._generate_report()

    def _parse_github_actions(self) -> None:
        """解析 GitHub Actions"""
        workflows_dir = self.project_dir / '.github' / 'workflows'

        if not workflows_dir.exists():
            return

        for workflow_file in workflows_dir.glob('*.yml'):
            self._parse_github_workflow(workflow_file)

        for workflow_file in workflows_dir.glob('*.yaml'):
            self._parse_github_workflow(workflow_file)

    def _parse_github_workflow(self, file_path: Path) -> None:
        """解析单个 GitHub Actions workflow"""
        if not HAS_YAML:
            self._parse_yaml_fallback(file_path, 'github')
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)

            if not data:
                return

            workflow_name = data.get('name', file_path.stem)
            triggers = []

            # 解析触发器
            on_config = data.get('on', {})
            if isinstance(on_config, dict):
                triggers = list(on_config.keys())
            elif isinstance(on_config, list):
                triggers = on_config
            elif isinstance(on_config, str):
                triggers = [on_config]

            # 解析 jobs
            jobs = []
            jobs_config = data.get('jobs', {})
            for job_name, job_data in jobs_config.items():
                if isinstance(job_data, dict):
                    steps = job_data.get('steps', [])
                    jobs.append({
                        'name': job_name,
                        'runs_on': job_data.get('runs-on', ''),
                        'steps_count': len(steps),
                        'env': job_data.get('env', {}),
                    })

            # 提取 secrets
            secrets = self._extract_secrets(data)

            self.pipelines.append(Pipeline(
                name=workflow_name,
                platform='github',
                triggers=triggers,
                jobs=jobs,
                secrets=secrets,
            ))

        except Exception as e:
            logger.debug(f"解析 GitHub workflow 失败 {file_path}: {e}")

    def _parse_gitlab_ci(self) -> None:
        """解析 GitLab CI"""
        gitlab_ci = self.project_dir / '.gitlab-ci.yml'

        if not gitlab_ci.exists():
            return

        if not HAS_YAML:
            self._parse_yaml_fallback(gitlab_ci, 'gitlab')
            return

        try:
            with open(gitlab_ci, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)

            if not data:
                return

            # 提取 stages
            stages = data.get('stages', ['build', 'test', 'deploy'])

            # 提取 jobs
            jobs = []
            for key, value in data.items():
                if isinstance(value, dict) and 'script' in value:
                    jobs.append({
                        'name': key,
                        'stage': value.get('stage', ''),
                        'script': value.get('script', [])[:5],  # 限制输出
                    })

            # 提取变量
            env_vars = data.get('variables', {})

            # 提取 secrets
            secrets = self._extract_secrets(data)

            self.pipelines.append(Pipeline(
                name='GitLab CI',
                platform='gitlab',
                stages=stages,
                jobs=jobs,
                env_vars=env_vars if isinstance(env_vars, dict) else {},
                secrets=secrets,
            ))

        except Exception as e:
            logger.debug(f"解析 GitLab CI 失败: {e}")

    def _parse_jenkinsfile(self) -> None:
        """解析 Jenkinsfile"""
        for jenkinsfile_name in ['Jenkinsfile', 'jenkinsfile']:
            jenkinsfile = self.project_dir / jenkinsfile_name

            if not jenkinsfile.exists():
                continue

            try:
                with open(jenkinsfile, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                # 简单解析 Jenkinsfile (Groovy 语法)
                stages = re.findall(r'stage\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)', content)

                # 检测触发器
                triggers = []
                if 'pipeline' in content or 'pipeline {' in content:
                    triggers.append('pipeline')
                if 'multibranch' in content.lower():
                    triggers.append('multibranch')

                # 检测 agent
                agent_match = re.search(r'agent\s*\{([^}]+)\}', content)
                agent = agent_match.group(1).strip() if agent_match else 'any'

                self.pipelines.append(Pipeline(
                    name='Jenkins',
                    platform='jenkins',
                    triggers=triggers,
                    stages=stages,
                    jobs=[{'name': 'pipeline', 'agent': agent}],
                ))

            except Exception as e:
                logger.debug(f"解析 Jenkinsfile 失败: {e}")

    def _parse_other_cicd(self) -> None:
        """解析其他 CI/CD 配置"""
        # CircleCI
        circleci_config = self.project_dir / '.circleci' / 'config.yml'
        if circleci_config.exists() and HAS_YAML:
            try:
                with open(circleci_config, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)

                jobs = []
                for job_name, job_data in (data.get('jobs', {}) or {}).items():
                    if isinstance(job_data, dict):
                        jobs.append({'name': job_name})

                self.pipelines.append(Pipeline(
                    name='CircleCI',
                    platform='circleci',
                    jobs=jobs,
                ))
            except Exception:
                pass

        # Azure Pipelines
        for azure_file in ['azure-pipelines.yml', '.azure-pipelines.yml']:
            azure_path = self.project_dir / azure_file
            if azure_path.exists() and HAS_YAML:
                try:
                    with open(azure_path, 'r', encoding='utf-8') as f:
                        data = yaml.safe_load(f)

                    stages = [s.get('stage', '') for s in (data.get('stages', []) or [])]

                    self.pipelines.append(Pipeline(
                        name='Azure Pipelines',
                        platform='azure',
                        stages=stages,
                    ))
                except Exception:
                    pass

    def _parse_yaml_fallback(self, file_path: Path, platform: str) -> None:
        """YAML 解析回退方法（无 PyYAML 时）"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 简单提取
            name_match = re.search(r'^name:\s*(.+)$', content, re.MULTILINE)
            name = name_match.group(1).strip() if name_match else file_path.stem

            self.pipelines.append(Pipeline(
                name=name,
                platform=platform,
            ))

        except Exception as e:
            logger.debug(f"YAML 回退解析失败 {file_path}: {e}")

    def _extract_secrets(self, data: Dict) -> List[str]:
        """提取 secrets 引用"""
        secrets = set()

        def find_secrets(obj):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if key == 'secrets' and isinstance(value, dict):
                        secrets.update(value.keys())
                    elif isinstance(value, str) and '${{ secrets.' in value:
                        # 提取 ${{ secrets.SECRET_NAME }}
                        match = re.search(r'\$\{\{\s*secrets\.(\w+)', value)
                        if match:
                            secrets.add(match.group(1))
                    else:
                        find_secrets(value)
            elif isinstance(obj, list):
                for item in obj:
                    find_secrets(item)

        find_secrets(data)
        return list(secrets)

    def _generate_report(self) -> Dict[str, Any]:
        """生成报告"""
        return {
            'summary': {
                'platforms': list(set(p.platform for p in self.pipelines)),
                'total_pipelines': len(self.pipelines),
                'total_secrets': len(set(s for p in self.pipelines for s in p.secrets)),
            },
            'pipelines': [
                {
                    'name': p.name,
                    'platform': p.platform,
                    'triggers': p.triggers,
                    'stages': p.stages,
                    'jobs_count': len(p.jobs),
                    'secrets': p.secrets,
                }
                for p in self.pipelines
            ],
        }

    @classmethod
    def find_cicd_files(cls, project_dir: str) -> List[str]:
        """查找 CI/CD 配置文件"""
        files = []
        project_path = Path(project_dir)

        for platform, patterns in cls.CONFIG_PATHS.items():
            for pattern in patterns:
                if '*' in pattern:
                    for f in project_path.glob(pattern):
                        files.append(str(f.relative_to(project_path)))
                else:
                    file_path = project_path / pattern
                    if file_path.exists():
                        files.append(pattern)

        return files


def main():
    import sys

    if len(sys.argv) < 2:
        print("Usage: cicd_parser.py <project_dir> [--find-files]")
        print("\nOptions:")
        print("  --find-files    Find CI/CD config files only")
        sys.exit(1)

    project_dir = sys.argv[1]
    find_files_only = '--find-files' in sys.argv

    if find_files_only:
        files = CICDParser.find_cicd_files(project_dir)
        print(json.dumps({'files': files}, indent=2))
    else:
        parser = CICDParser(project_dir)
        result = parser.parse()
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()