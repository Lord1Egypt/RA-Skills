#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
规范驱动开发工具

提供规范初始化、分析和更新功能
"""

import os
import json
import argparse
from typing import Dict, List, Optional

class SpecTools:
    """
    规范驱动开发工具类
    """
    
    def __init__(self, project_root: str = "."):
        """
        初始化工具
        
        Args:
            project_root: 项目根目录
        """
        self.project_root = project_root
        self.spec_dir = os.path.join(project_root, "docs", "spec")
    
    def init(self) -> bool:
        """
        初始化规范环境
        
        Returns:
            bool: 初始化是否成功
        """
        try:
            # 创建规范目录
            os.makedirs(self.spec_dir, exist_ok=True)
            
            # 创建规范模板文件
            templates = {
                "CONSTITUTION.md": self._get_constitution_template(),
                "SPEC.md": self._get_spec_template(),
                "SPEC_ANALYSIS.md": self._get_spec_analysis_template(),
                "PROJECT_STRUCTURE.md": self._get_project_structure_template()
            }
            
            for filename, content in templates.items():
                file_path = os.path.join(self.spec_dir, filename)
                if not os.path.exists(file_path):
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(content)
                    print(f"Created template: {file_path}")
                else:
                    print(f"Template already exists: {file_path}")
            
            print("Spec environment initialized successfully!")
            return True
        except Exception as e:
            print(f"Error initializing spec environment: {e}")
            return False
    
    def analyze(self, spec_file: Optional[str] = None) -> Dict:
        """
        规范一致性分析
        
        Args:
            spec_file: 规范文件路径，默认分析所有规范文件
            
        Returns:
            Dict: 分析结果
        """
        try:
            analysis_result = {
                "status": "success",
                "files": {},
                "issues": []
            }
            
            # 分析指定文件或所有规范文件
            if spec_file:
                files_to_analyze = [spec_file]
            else:
                files_to_analyze = [
                    os.path.join(self.spec_dir, "CONSTITUTION.md"),
                    os.path.join(self.spec_dir, "SPEC.md"),
                    os.path.join(self.spec_dir, "SPEC_ANALYSIS.md"),
                    os.path.join(self.spec_dir, "PROJECT_STRUCTURE.md")
                ]
            
            for file_path in files_to_analyze:
                if os.path.exists(file_path):
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    # 简单的分析逻辑
                    analysis_result["files"][os.path.basename(file_path)] = {
                        "exists": True,
                        "size": len(content),
                        "has_content": len(content.strip()) > 0
                    }
                    
                    if not analysis_result["files"][os.path.basename(file_path)]["has_content"]:
                        analysis_result["issues"].append({
                            "file": os.path.basename(file_path),
                            "type": "empty_file",
                            "message": "File is empty"
                        })
                else:
                    analysis_result["files"][os.path.basename(file_path)] = {
                        "exists": False
                    }
                    analysis_result["issues"].append({
                        "file": os.path.basename(file_path),
                        "type": "missing_file",
                        "message": "File does not exist"
                    })
            
            print("Spec analysis completed!")
            print(json.dumps(analysis_result, indent=2, ensure_ascii=False))
            return analysis_result
        except Exception as e:
            print(f"Error analyzing spec: {e}")
            return {"status": "error", "message": str(e)}
    
    def update(self, spec_file: str, content: Optional[str] = None) -> bool:
        """
        更新规范文档
        
        Args:
            spec_file: 规范文件路径
            content: 新内容，如果不提供则使用默认模板
            
        Returns:
            bool: 更新是否成功
        """
        try:
            file_path = os.path.join(self.spec_dir, spec_file)
            
            if not content:
                # 使用默认模板
                templates = {
                    "CONSTITUTION.md": self._get_constitution_template(),
                    "SPEC.md": self._get_spec_template(),
                    "SPEC_ANALYSIS.md": self._get_spec_analysis_template(),
                    "PROJECT_STRUCTURE.md": self._get_project_structure_template()
                }
                
                if spec_file in templates:
                    content = templates[spec_file]
                else:
                    print(f"Unknown spec file: {spec_file}")
                    return False
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            
            print(f"Updated spec file: {file_path}")
            return True
        except Exception as e:
            print(f"Error updating spec file: {e}")
            return False
    
    def _get_constitution_template(self) -> str:
        """
        获取项目宪法模板
        """
        template_path = os.path.join(self.spec_dir, "CONSTITUTION_TEMPLATE.md")
        return self._read_template(template_path, "# 项目宪法\n\n## 1. 项目信息\n\n| 项目名称 | 版本 | 负责人 | 最后更新 |\n|---------|------|--------|----------|\n| 项目名称 | v1.0.0 | 团队 | YYYY-MM-DD |\n\n## 2. 不可协商项\n\n### 2.1 核心原则\n- **原则1**: [描述核心原则1]\n- **原则2**: [描述核心原则2]\n- **原则3**: [描述核心原则3]\n\n### 2.2 技术栈\n- **语言**: [如：Java、Python、JavaScript等]\n- **框架**: [如：Spring Boot、React、Django等]\n- **数据库**: [如：MySQL、PostgreSQL、MongoDB等]\n- **工具**: [如：Git、Docker、CI/CD等]\n\n### 2.3 开发规范\n- **代码风格**: [如：Google Java Style、PEP 8等]\n- **命名规范**: [如：驼峰命名、下划线命名等]\n- **文档规范**: [如：JSDoc、JavaDoc等]\n- **版本控制**: [如：Git Flow、GitHub Flow等]\n\n### 2.4 质量要求\n- **测试覆盖率**: [如：≥80%]\n- **代码审查**: [如：必须通过代码审查]\n- **CI/CD**: [如：必须通过CI测试]\n- **性能要求**: [如：响应时间≤100ms]\n\n## 3. 决策流程\n\n### 3.1 重大决策\n- **决策机制**: [如：团队投票、技术评审等]\n- **决策记录**: [如：决策日志、会议记录等]\n- **变更流程**: [如：变更申请、审批流程等]\n\n### 3.2 紧急决策\n- **应急机制**: [如：紧急决策流程]\n- **责任分工**: [如：紧急决策负责人]\n- **事后评估**: [如：紧急决策评估]\n\n## 4. 团队协作\n\n### 4.1 沟通机制\n- **沟通工具**: [如：Slack、钉钉、企业微信等]\n- **会议规范**: [如：每日站会、周会等]\n- **文档共享**: [如：Wiki、Confluence等]\n\n### 4.2 角色与职责\n- **角色1**: [职责描述]\n- **角色2**: [职责描述]\n- **角色3**: [职责描述]\n\n### 4.3 冲突解决\n- **冲突类型**: [如：技术冲突、需求冲突等]\n- **解决机制**: [如：协商、仲裁等]\n- **升级流程**: [如：冲突升级流程]\n\n## 5. 项目管理\n\n### 5.1 迭代周期\n- **迭代长度**: [如：2周、1个月等]\n- **迭代计划**: [如：迭代计划制定流程]\n- **迭代评审**: [如：迭代评审流程]\n\n### 5.2 风险管理\n- **风险识别**: [如：风险识别方法]\n- **风险评估**: [如：风险评估标准]\n- **风险应对**: [如：风险应对策略]\n\n### 5.3 交付标准\n- **交付物**: [如：代码、文档、测试等]\n- **验收标准**: [如：功能验收、性能验收等]\n- **发布流程**: [如：发布审批、灰度发布等]\n\n## 6. 附录\n\n### 6.1 术语定义\n\n| 术语 | 解释 |\n|------|------|\n| 术语1 | 解释 |\n| 术语2 | 解释 |\n\n### 6.2 参考文档\n\n- [参考文档1]\n- [参考文档2]\n""")
    
    def _get_spec_template(self) -> str:
        """
        获取项目规范模板
        """
        template_path = os.path.join(self.spec_dir, "SPEC_TEMPLATE.md")
        return self._read_template(template_path, "# 项目规范\n\n## 1. 项目信息\n\n| 项目名称 | 版本 | 负责人 | 最后更新 |\n|---------|------|--------|----------|\n| 项目名称 | v1.0.0 | 团队 | YYYY-MM-DD |\n\n## 2. 功能需求\n\n### 2.1 功能模块\n\n| 模块名称 | 功能描述 | 优先级 | 备注 |\n|---------|---------|--------|------|\n| 模块1 | 功能描述 | P0/P1/P2 | 备注 |\n| 模块2 | 功能描述 | P0/P1/P2 | 备注 |\n| 模块3 | 功能描述 | P0/P1/P2 | 备注 |\n\n### 2.2 详细功能\n\n#### 2.2.1 模块1\n- **功能点1**: [功能描述]\n- **功能点2**: [功能描述]\n- **功能点3**: [功能描述]\n\n#### 2.2.2 模块2\n- **功能点1**: [功能描述]\n- **功能点2**: [功能描述]\n\n## 3. 非功能需求\n\n### 3.1 性能要求\n- **响应时间**: [如：95%的请求在100ms内完成]\n- **并发处理**: [如：支持1000QPS]\n- **资源使用**: [如：内存使用不超过2GB]\n\n### 3.2 可靠性要求\n- **可用性**: [如：99.9%]\n- **容错能力**: [如：支持单点故障自动恢复]\n- **数据一致性**: [如：最终一致性]\n\n### 3.3 安全性要求\n- **认证方式**: [如：JWT认证]\n- **授权机制**: [如：基于角色的访问控制]\n- **数据加密**: [如：传输加密、存储加密]\n\n### 3.4 可扩展性要求\n- **水平扩展**: [如：支持集群部署]\n- **模块化设计**: [如：插件化架构]\n- **配置管理**: [如：外部化配置]\n\n## 4. 技术实现\n\n### 4.1 技术栈\n- **前端**: [如：React、Vue、Angular等]\n- **后端**: [如：Spring Boot、Node.js、Flask等]\n- **数据库**: [如：MySQL、PostgreSQL、MongoDB等]\n- **中间件**: [如：Redis、Kafka、RabbitMQ等]\n\n### 4.2 架构设计\n- **架构风格**: [如：微服务架构、单体应用、分层架构等]\n- **模块划分**: [模块划分描述]\n- **核心流程**: [核心流程描述]\n\n### 4.3 数据设计\n- **数据模型**: [数据模型描述]\n- **数据库结构**: [数据库结构描述]\n- **数据迁移**: [数据迁移策略]\n\n### 4.4 API设计\n- **API风格**: [如：RESTful、GraphQL等]\n- **接口规范**: [接口规范描述]\n- **版本管理**: [API版本管理策略]\n\n## 5. 验收标准\n\n### 5.1 功能验收\n- **验收项1**: [验收标准]\n- **验收项2**: [验收标准]\n- **验收项3**: [验收标准]\n\n### 5.2 性能验收\n- **验收项1**: [验收标准]\n- **验收项2**: [验收标准]\n\n### 5.3 安全验收\n- **验收项1**: [验收标准]\n- **验收项2**: [验收标准]\n\n## 6. 项目计划\n\n### 6.1 开发周期\n- **总周期**: [如：3个月]\n- **里程碑**: [如：需求确认、设计完成、开发完成、测试完成、上线]\n\n### 6.2 资源需求\n- **人力资源**: [如：前端开发2人、后端开发2人、测试1人]\n- **设备资源**: [如：服务器、测试环境]\n- **工具资源**: [如：开发工具、测试工具]\n\n## 7. 风险评估\n\n| 风险点 | 影响程度 | 可能性 | 应对措施 |\n|-------|---------|--------|----------|\n| 风险1 | 影响程度 | 可能性 | 应对措施 |\n| 风险2 | 影响程度 | 可能性 | 应对措施 |\n\n## 8. 附录\n\n### 8.1 术语定义\n\n| 术语 | 解释 |\n|------|------|\n| 术语1 | 解释 |\n| 术语2 | 解释 |\n\n### 8.2 参考文档\n\n- [参考文档1]\n- [参考文档2]\n""")
    
    def _get_spec_analysis_template(self) -> str:
        """
        获取规范分析报告模板
        """
        template_path = os.path.join(self.spec_dir, "SPEC_ANALYSIS_TEMPLATE.md")
        return self._read_template(template_path, "# 规范分析报告\n\n## 1. 分析信息\n\n| 项目名称 | 版本 | 分析人 | 分析日期 |\n|---------|------|--------|----------|\n| 项目名称 | v1.0.0 | 架构师 | YYYY-MM-DD |\n\n## 2. 规范完整性分析\n\n### 2.1 功能需求完整性\n- **覆盖度**: [如：90%]\n- **缺失功能**: [缺失功能列表]\n- **冗余功能**: [冗余功能列表]\n\n### 2.2 非功能需求完整性\n- **覆盖度**: [如：85%]\n- **缺失需求**: [缺失需求列表]\n- **冗余需求**: [冗余需求列表]\n\n### 2.3 技术实现完整性\n- **覆盖度**: [如：95%]\n- **缺失技术**: [缺失技术列表]\n- **冗余技术**: [冗余技术列表]\n\n## 3. 规范一致性分析\n\n### 3.1 需求一致性\n- **内部一致性**: [如：无冲突]\n- **外部一致性**: [如：与PRD一致]\n- **冲突点**: [冲突点列表]\n\n### 3.2 技术一致性\n- **架构一致性**: [如：架构设计与技术栈一致]\n- **实现一致性**: [如：技术实现与规范要求一致]\n- **冲突点**: [冲突点列表]\n\n### 3.3 验收一致性\n- **验收标准一致性**: [如：验收标准与需求一致]\n- **测试覆盖一致性**: [如：测试用例与验收标准一致]\n- **冲突点**: [冲突点列表]\n\n## 4. 规范可行性分析\n\n### 4.1 技术可行性\n- **技术成熟度**: [如：技术栈成熟]\n- **技术风险**: [技术风险列表]\n- **应对措施**: [应对措施列表]\n\n### 4.2 时间可行性\n- **开发周期**: [如：符合预期]\n- **时间风险**: [时间风险列表]\n- **应对措施**: [应对措施列表]\n\n### 4.3 资源可行性\n- **人力资源**: [如：资源充足]\n- **设备资源**: [如：资源充足]\n- **资源风险**: [资源风险列表]\n- **应对措施**: [应对措施列表]\n\n## 5. 规范质量评估\n\n### 5.1 清晰度\n- **描述清晰度**: [如：清晰]\n- **歧义点**: [歧义点列表]\n- **改进建议**: [改进建议列表]\n\n### 5.2 可执行性\n- **可理解性**: [如：易于理解]\n- **可实现性**: [如：易于实现]\n- **改进建议**: [改进建议列表]\n\n### 5.3 可维护性\n- **结构合理性**: [如：结构合理]\n- **文档完整性**: [如：文档完整]\n- **改进建议**: [改进建议列表]\n\n## 6. 分析结论\n\n### 6.1 总体评估\n- **规范质量**: [如：优秀、良好、一般、差]\n- **主要问题**: [主要问题列表]\n- **改进建议**: [改进建议列表]\n\n### 6.2 风险评估\n- **高风险项**: [高风险项列表]\n- **中风险项**: [中风险项列表]\n- **低风险项**: [低风险项列表]\n\n### 6.3 建议行动\n- **立即行动**: [立即行动列表]\n- **短期行动**: [短期行动列表]\n- **长期行动**: [长期行动列表]\n\n## 7. 附录\n\n### 7.1 分析方法\n- **分析工具**: [使用的分析工具]\n- **分析流程**: [分析流程描述]\n\n### 7.2 参考文档\n- [参考文档1]\n- [参考文档2]\n""")
    
    def _get_project_structure_template(self) -> str:
        """
        获取项目结构模板
        """
        template_path = os.path.join(self.spec_dir, "PROJECT_STRUCTURE_TEMPLATE.md")
        return self._read_template(template_path, "# 项目结构")
    
    def _read_template(self, template_path: str, default_content: str) -> str:
        """
        从模板文件中读取内容，如果文件不存在则返回默认内容
        
        Args:
            template_path: 模板文件路径
            default_content: 默认内容
            
        Returns:
            str: 模板内容
        """
        if os.path.exists(template_path):
            try:
                with open(template_path, "r", encoding="utf-8") as f:
                    return f.read()
            except Exception as e:
                print(f"Error reading template file: {e}")
                return default_content
        else:
            print(f"Template file not found: {template_path}")
            return default_content

def main():
    """
    主函数
    """
    parser = argparse.ArgumentParser(description="Spec Tools")
    parser.add_argument("command", choices=["init", "analyze", "update"], help="Command to execute")
    parser.add_argument("--project-path", default=".", help="Project root path")
    parser.add_argument("--spec-file", help="Spec file path")
    parser.add_argument("--content", help="Content for update command")
    
    args = parser.parse_args()
    
    spec_tools = SpecTools(args.project_path)
    
    if args.command == "init":
        spec_tools.init()
    elif args.command == "analyze":
        spec_tools.analyze(args.spec_file)
    elif args.command == "update":
        if not args.spec_file:
            print("Error: --spec-file is required for update command")
            return
        spec_tools.update(args.spec_file, args.content)

if __name__ == "__main__":
    main()