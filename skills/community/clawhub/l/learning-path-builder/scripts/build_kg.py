#!/usr/bin/env python3
"""
权威知识图谱构建器 - 主构建脚本
基于国家标准文档生成结构化知识图谱
"""

import json
import yaml
import os
import sys
from datetime import datetime
from pathlib import Path

class AuthoritativeKnowledgeGraphBuilder:
    """权威知识图谱构建器"""
    
    def __init__(self, config_path=None):
        """初始化构建器"""
        self.config = self._load_config(config_path)
        self.knowledge_graph = None
        self.build_report = {
            "start_time": datetime.now().isoformat(),
            "stages": [],
            "errors": [],
            "warnings": []
        }
    
    def _load_config(self, config_path):
        """加载配置文件"""
        default_config = {
            "authoritative_sources": {
                "mooc_platforms": [
                    {"name": "中国大学MOOC", "url": "https://www.icourse163.org", "priority": 1},
                    {"name": "学堂在线", "url": "https://www.xuetangx.com", "priority": 2}
                ],
                "government_data": [
                    {"name": "国家数据", "url": "http://data.stats.gov.cn", "priority": 1},
                    {"name": "北京市政务数据", "url": "https://data.beijing.gov.cn", "priority": 2}
                ],
                "academic_databases": [
                    {"name": "中国知网", "url": "https://www.cnki.net", "priority": 1},
                    {"name": "万方数据", "url": "https://www.wanfangdata.com.cn", "priority": 2}
                ],
                "official_docs": [
                    {"name": "技能人才评价工作网（国家职业标准查询系统）", "url": "https://www.osta.org.cn", "priority": 1},
                    {"name": "国家标准全文公开系统", "url": "https://openstd.samr.gov.cn", "priority": 1},
                    {"name": "工信部技术标准", "url": "https://www.miit.gov.cn", "priority": 2}
                ]
            },
            "avoided_sources": [
                "个人博客", "非技术论坛", "社交媒体", 
                "未经验证的教程", "商业推广内容", "过时技术资料"
            ],
            "quality_thresholds": {
                "authoritative_coverage": 0.85,
                "structure_coherence": 0.90,
                "source_reliability": 0.95,
                "learning_progression": 0.85,
                "practical_relevance": 0.80
            },
            "hour_allocation_rules": {
                "foundation_knowledge": 0.25,
                "development_skills": 0.40,
                "testing_skills": 0.15,
                "operations_skills": 0.20
            }
        }
        
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    user_config = yaml.safe_load(f)
                    # 合并配置
                    default_config.update(user_config)
            except Exception as e:
                print(f"警告: 加载配置文件失败: {e}, 使用默认配置")
        
        return default_config
    
    def build_occupational_skill_knowledge_graph(self, total_hours=80, target_level="初级"):
        """构建职业技能知识图谱"""
        print("=" * 60)
        print(f"🏗️  构建职业技能知识图谱")
        print(f"📊 总学时: {total_hours}小时 ({target_level}级)")
        print("=" * 60)
        
        self._add_stage("开始构建", "初始化知识图谱")
        
        # 计算学习单元数
        total_units = total_hours * 2  # 每小时2个单元
        
        # 构建知识图谱
        self.knowledge_graph = {
            "metadata": self._build_metadata(total_hours, total_units, target_level),
            "learning_domains": self._build_learning_domains(total_hours),
            "knowledge_nodes": self._build_knowledge_nodes(),
            "learning_paths": self._build_learning_paths(target_level),
            "authoritative_resources": self._collect_authoritative_resources(),
            "quality_metrics": self._calculate_quality_metrics()
        }
        
        self._add_stage("构建完成", "知识图谱构建完成")
        
        return self.knowledge_graph
    
    def _build_metadata(self, total_hours, total_units, target_level):
        """构建元数据"""
        return {
            "title": f"职业技能工程技术人员知识图谱（{target_level}版）",
            "version": "authoritative-1.0",
            "total_hours": total_hours,
            "total_learning_units": total_units,
            "unit_duration_minutes": 25,
            "target_level": target_level,
            "authoritative_sources": self.config["authoritative_sources"],
            "avoided_sources": self.config["avoided_sources"],
            "build_time": datetime.now().isoformat(),
            "quality_assurance": "权威资源优先，避免非权威信息"
        }
    
    def _build_learning_domains(self, total_hours):
        """构建学习领域"""
        # 使用occupational_skill规则集
        rule_set = self.config["hour_allocation_rules"].get("occupational_skill", {
            "foundation_knowledge": 0.25,
            "development_skills": 0.40,
            "testing_skills": 0.15,
            "operations_skills": 0.20
        })
        
        """构建学习领域"""
        domains = [
            {
                "id": "foundation",
                "name": "基础知识",
                "description": "计算机和职业技能基础概念",
                "hours": int(total_hours * rule_set["foundation_knowledge"]),
                "units": int(total_hours * rule_set["foundation_knowledge"] * 2),
                "authoritative_sources": ["中国大学MOOC", "国家标准"],
                "nodes": ["计算机基础", "职业技能基础", "安全基础"]
            },
            {
                "id": "development",
                "name": "开发技能",
                "description": "职业技能应用开发相关技能",
                "hours": int(total_hours * rule_set["development_skills"]),
                "units": int(total_hours * rule_set["development_skills"] * 2),
                "authoritative_sources": ["学堂在线", "官方技术文档"],
                "nodes": ["技术组件开发", "应用系统开发", "开发工具"]
            },
            {
                "id": "testing",
                "name": "测试技能",
                "description": "职业技能系统测试和验证",
                "hours": int(total_hours * rule_set["testing_skills"]),
                "units": int(total_hours * rule_set["testing_skills"] * 2),
                "authoritative_sources": ["国家标准", "学术数据库"],
                "nodes": ["安全测试", "性能测试", "功能测试"]
            },
            {
                "id": "operations",
                "name": "运维技能",
                "description": "职业技能系统部署和运维",
                "hours": int(total_hours * rule_set["operations_skills"]),
                "units": int(total_hours * rule_set["operations_skills"] * 2),
                "authoritative_sources": ["政府数据", "行业标准"],
                "nodes": ["系统部署", "监控运维", "故障处理"]
            }
        ]
        
        self._add_stage("构建学习领域", f"创建了{len(domains)}个学习领域")
        return domains
    
    def _build_knowledge_nodes(self):
        """构建知识节点"""
        nodes = [
            {
                "id": "node_foundation_occupational_skill",
                "name": "职业技能基础",
                "domain": "foundation",
                "hours": 12,
                "units": 24,
                "description": "职业技能概念、原理、架构",
                "authoritative_resources": [
                    {"source": "中国大学MOOC", "course": "职业技能技术与应用", "institution": "清华大学"},
                    {"source": "国家标准", "name": "职业技能和系统架构记账技术 参考架构", "number": "GB/T XXXXX-XXXX"}
                ],
                "learning_units": [
                    {"id": "unit_001", "name": "职业技能定义与特点", "duration": 25},
                    {"id": "unit_002", "name": "系统架构账本原理", "duration": 25},
                    {"id": "unit_003", "name": "协调算法介绍", "duration": 25}
                ]
            },
            {
                "id": "node_dev_smart_contract",
                "name": "技术组件开发",
                "domain": "development",
                "hours": 18,
                "units": 36,
                "description": "ProgrammingLanguage语言、合约编写、测试部署",
                "authoritative_resources": [
                    {"source": "学堂在线", "course": "ProgrammingLanguage技术组件开发", "institution": "北京大学"},
                    {"source": "官方文档", "name": "官方技术平台官方文档", "url": "https://official.techplatform.org/docs"}
                ],
                "learning_units": [
                    {"id": "unit_101", "name": "ProgrammingLanguage语法基础", "duration": 25},
                    {"id": "unit_102", "name": "合约编写实践", "duration": 25},
                    {"id": "unit_103", "name": "安全注意事项", "duration": 25}
                ]
            }
        ]
        
        self._add_stage("构建知识节点", f"创建了{len(nodes)}个知识节点")
        return nodes
    
    def _build_learning_paths(self, target_level):
        """构建学习路径"""
        if target_level == "初级":
            paths = [
                {
                    "id": "path_beginner",
                    "name": "初学者完整路径",
                    "description": "从零开始系统学习职业技能技术",
                    "total_weeks": 16,
                    "weekly_hours": 5,
                    "node_sequence": ["node_foundation_occupational_skill", "node_dev_smart_contract"],
                    "authoritative_resources": {
                        "foundation": "中国大学MOOC-职业技能入门课程",
                        "development": "学堂在线-ProgrammingLanguage开发课程"
                    }
                }
            ]
        else:
            paths = []
        
        self._add_stage("构建学习路径", f"创建了{len(paths)}条学习路径")
        return paths
    
    def _collect_authoritative_resources(self):
        """收集权威资源
        
        注意：这是一个框架方法，实际实现应该：
        1. 根据职业技能领域搜索相关MOOC课程
        2. 搜索国家职业标准（osta.org.cn）
        3. 搜索相关学术论文（知网等）
        4. 搜索官方技术文档
        5. 所有资源应通过实际搜索获取，而非硬编码
        """
        resources = {
            "mooc_courses": [],      # 应通过搜索中国大学MOOC等平台动态获取
            "national_standards": [], # 应通过搜索osta.org.cn等平台动态获取
            "academic_papers": [],    # 应通过搜索知网等学术数据库动态获取
            "official_documentation": [] # 应通过搜索官方技术平台动态获取
        }
        
        self._add_stage("收集权威资源", "权威资源收集框架已初始化（需实现具体搜索逻辑）")
        return resources
    
    def _calculate_quality_metrics(self):
        """计算质量指标
        
        注意：这是一个框架方法，实际实现应该：
        1. 基于实际收集的资源计算权威覆盖率
        2. 基于知识图谱结构计算结构一致性
        3. 基于学习路径计算学习渐进性
        4. 基于实际内容计算实践相关性
        5. 基于来源可靠性计算来源可信度
        """
        # 返回占位符值，实际应该基于数据分析计算
        metrics = {
            "authoritative_coverage": 0.0,  # 应根据权威资源占比计算
            "structure_coherence": 0.0,     # 应根据知识图谱结构计算
            "learning_progression": 0.0,    # 应根据学习路径合理性计算
            "practical_relevance": 0.0,     # 应根据实践内容占比计算
            "source_reliability": 0.0       # 应根据来源权威性计算
        }
        
        self._add_warning("质量指标计算为占位符值，需实现具体计算逻辑")
        self._add_stage("计算质量指标", "质量指标计算完成（占位符值）")
        
        return metrics
    
    def _add_stage(self, stage_name, description):
        """添加构建阶段"""
        stage = {
            "name": stage_name,
            "description": description,
            "time": datetime.now().isoformat()
        }
        self.build_report["stages"].append(stage)
        print(f"  🔹 {stage_name}: {description}")
    
    def _add_error(self, error_message):
        """添加错误"""
        self.build_report["errors"].append({
            "message": error_message,
            "time": datetime.now().isoformat()
        })
        print(f"  ❌ 错误: {error_message}")
    
    def _add_warning(self, warning_message):
        """添加警告"""
        self.build_report["warnings"].append({
            "message": warning_message,
            "time": datetime.now().isoformat()
        })
        print(f"  ⚠️  警告: {warning_message}")
    
    def save_knowledge_graph(self, output_path):
        """保存知识图谱"""
        if not self.knowledge_graph:
            print("错误: 知识图谱未构建")
            return False
        
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # 保存知识图谱
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(self.knowledge_graph, f, ensure_ascii=False, indent=2)
            
            print(f"💾 知识图谱已保存到: {output_path}")
            
            # 生成构建报告
            self.build_report["end_time"] = datetime.now().isoformat()
            self.build_report["output_file"] = output_path
            
            report_path = output_path.replace('.json', '_build_report.md')
            self._generate_build_report(report_path)
            
            return True
            
        except Exception as e:
            self._add_error(f"保存知识图谱失败: {e}")
            return False
    
    def _generate_build_report(self, report_path):
        """生成构建报告"""
        report_content = f"""# 知识图谱构建报告

## 基本信息
- **构建时间**: {self.build_report['start_time']} - {self.build_report.get('end_time', '进行中')}
- **输出文件**: {self.build_report.get('output_file', '未保存')}
- **构建状态**: {'完成' if 'end_time' in self.build_report else '进行中'}

## 构建阶段
"""
        
        for stage in self.build_report["stages"]:
            report_content += f"- **{stage['name']}**: {stage['description']} ({stage['time']})\n"
        
        if self.build_report["warnings"]:
            report_content += "\n## 警告\n"
            for warning in self.build_report["warnings"]:
                report_content += f"- ⚠️ {warning['message']} ({warning['time']})\n"
        
        if self.build_report["errors"]:
            report_content += "\n## 错误\n"
            for error in self.build_report["errors"]:
                report_content += f"- ❌ {error['message']} ({error['time']})\n"
        
        if self.knowledge_graph:
            metadata = self.knowledge_graph["metadata"]
            report_content += f"""
## 知识图谱摘要
- **标题**: {metadata['title']}
- **总学时**: {metadata['total_hours']}小时
- **学习单元**: {metadata['total_learning_units']}个
- **单元时长**: {metadata['unit_duration_minutes']}分钟
- **目标级别**: {metadata.get('target_level', '未指定')}

## 质量指标
"""
            metrics = self.knowledge_graph["quality_metrics"]
            for metric, value in metrics.items():
                report_content += f"- **{metric}**: {value*100:.0f}%\n"
            
            report_content += f"""
## 学习领域
"""
            domains = self.knowledge_graph["learning_domains"]
            for domain in domains:
                report_content += f"- **{domain['name']}**: {domain['hours']}小时, {domain['units']}单元\n"
        
        report_content += f"""
## 构建配置
- **权威资源类型**: {len(self.config['authoritative_sources'])}类
- **避免资源类型**: {len(self.config['avoided_sources'])}类
- **质量阈值**: {len(self.config['quality_thresholds'])}个指标

## 建议
1. 验证权威资源的可用性
2. 检查知识结构的合理性
3. 根据实际需求调整学时分配
4. 定期更新权威资源

---
*报告生成时间: {datetime.now().isoformat()}*
*生成工具: 权威知识图谱构建器 v1.0.0*
"""
        
        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(report_content)
            print(f"📝 构建报告已保存到: {report_path}")
        except Exception as e:
            print(f"警告: 生成构建报告失败: {e}")
    
    def print_summary(self):
        """打印构建摘要"""
        if not self.knowledge_graph:
            print("知识图谱未构建")
            return
        
        metadata = self.knowledge_graph["metadata"]
        domains = self.knowledge_graph["learning_domains"]
        nodes = self.knowledge_graph["knowledge_nodes"]
        metrics = self.knowledge_graph["quality_metrics"]
        
        print("\n" + "=" * 60)
        print("📈 知识图谱构建摘要")
        print("=" * 60)
        
        print(f"📊 基本信息:")
        print(f"  • 标题: {metadata['title']}")
        print(f"  • 总学时: {metadata['total_hours']}小时")
        print(f"  • 学习单元: {metadata['total_