#!/usr/bin/env python3
"""
GDPR模板引擎
提供GDPR合规文档的模板生成功能
"""

import json
import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path


class GDPRTemplateEngine:
    """GDPR模板引擎"""
    
    def __init__(self, template_dir: Optional[str] = None):
        """
        初始化模板引擎
        
        Args:
            template_dir: 模板目录路径
        """
        if template_dir:
            self.template_dir = Path(template_dir)
        else:
            self.template_dir = Path(__file__).parent.parent.parent / "assets" / "templates"
        
        # 确保模板目录存在
        self.template_dir.mkdir(parents=True, exist_ok=True)
        
        # 预定义模板
        self.templates = {
            "privacy_notice": self._get_privacy_notice_template(),
            "data_processing_agreement": self._get_dpa_template(),
            "data_breach_notification": self._get_breach_notification_template(),
            "dpia_report": self._get_dpia_template(),
            "consent_form": self._get_consent_form_template(),
            "data_subject_request_form": self._get_dsr_form_template()
        }
    
    def _get_privacy_notice_template(self) -> str:
        """获取隐私通知模板"""
        return """
# 隐私通知 (Privacy Notice)
## 根据欧盟《通用数据保护条例》(GDPR)要求

### 1. 数据处理控制者信息
**公司名称**: {company_name}
**地址**: {company_address}
**数据保护官(DPO)**: {dpo_name} ({dpo_email})
**联系方式**: {contact_email}

### 2. 处理目的和合法性基础
我们处理您的个人数据用于以下目的：

| 处理目的 | 合法性基础 | 数据类别 | 保留期限 |
|---------|-----------|---------|---------|
{processing_purposes}

### 3. 数据主体权利
根据GDPR，您拥有以下权利：
- **知情权** (Articles 13-14): 了解我们如何处理您的数据
- **访问权** (Article 15): 获取您的个人数据副本
- **更正权** (Article 16): 更正不准确的数据
- **删除权** (Article 17): 要求删除您的数据
- **限制处理权** (Article 18): 限制数据处理
- **数据可携权** (Article 20): 获取结构化、常用格式的数据副本
- **反对权** (Article 21): 反对基于合法利益的数据处理
- **自动化决策相关权利** (Article 22): 不受仅基于自动化处理的决定约束

### 4. 数据接收方
您的数据可能被以下接收方处理：
{data_recipients}

### 5. 跨境数据传输
{data_transfers}

### 6. 投诉权利
如果您认为我们对您个人数据的处理违反了GDPR，您有权向监管机构投诉。
**监管机构**: {supervisory_authority}
**联系方式**: {supervisory_contact}

### 7. 联系信息
如有任何问题或行使您的权利，请联系：
**数据保护官**: {dpo_name}
**邮箱**: {dpo_email}
**电话**: {dpo_phone}

**最后更新**: {update_date}
"""
    
    def _get_dpa_template(self) -> str:
        """获取数据处理协议模板"""
        return """
# 数据处理协议 (Data Processing Agreement)
## 根据GDPR Article 28要求

### 协议双方
**数据控制者 (Controller)**:
- 名称: {controller_name}
- 地址: {controller_address}
- 代表: {controller_representative}

**数据处理者 (Processor)**:
- 名称: {processor_name}
- 地址: {processor_address}
- 代表: {processor_representative}

### 1. 处理目的和范围
**处理目的**: {processing_purpose}
**数据类别**: {data_categories}
**数据主体类别**: {data_subject_categories}
**处理期限**: {processing_duration}

### 2. 数据处理者的义务
根据GDPR Article 28，数据处理者同意：

#### 2.1 处理指令
仅根据数据控制者的书面指令处理个人数据。

#### 2.2 保密义务
确保处理个人数据的人员承担保密义务。

#### 2.3 安全措施
实施适当的技术和组织措施确保安全水平。

#### 2.4 分包处理
如使用其他处理者，需获得数据控制者事先授权。

#### 2.5 协助义务
协助数据控制者履行GDPR义务。

#### 2.6 数据泄露通知
发现数据泄露后72小时内通知数据控制者。

#### 2.7 删除或返还数据
处理结束后删除或返还所有个人数据。

### 3. 安全措施
双方同意的安全措施包括：
{security_measures}

### 4. 审计权利
数据控制者有权审计数据处理者的合规性。

### 5. 责任和赔偿
{liability_provisions}

### 6. 协议期限和终止
**生效日期**: {effective_date}
**期限**: {agreement_term}
**终止条款**: {termination_clauses}

### 签字
**数据控制者**: ___________________________
**日期**: {signature_date}

**数据处理者**: ___________________________
**日期**: {signature_date}
"""
    
    def _get_breach_notification_template(self) -> str:
        """获取数据泄露通知模板"""
        return """
# 数据泄露通知 (Data Breach Notification)
## 根据GDPR Article 33要求

### 1. 泄露基本信息
**泄露发现时间**: {breach_discovery_time}
**通知时间**: {notification_time} (应在发现后72小时内)
**泄露类型**: {breach_type}
**影响数据类别**: {affected_data_categories}
**估计受影响人数**: {estimated_affected_individuals}

### 2. 泄露描述
**发生时间**: {breach_occurrence_time}
**持续时间**: {breach_duration}
**泄露原因**: {breach_cause}
**泄露方式**: {breach_method}

### 3. 影响评估
**数据类别影响**:
{data_category_impact}

**数据主体影响**:
{data_subject_impact}

**风险评估**:
{risk_assessment}

### 4. 已采取措施
**立即响应措施**:
{immediate_measures}

**技术措施**:
{technical_measures}

**组织措施**:
{organizational_measures}

### 5. 后续计划
**补救措施**:
{remedial_measures}

**预防措施**:
{preventive_measures}

**沟通计划**:
{communication_plan}

### 6. 联系人信息
**数据保护官(DPO)**: {dpo_name}
**联系方式**: {dpo_contact}
**监管机构**: {supervisory_authority}
**监管联系方式**: {supervisory_contact}

### 7. 附件
{attachments}
"""
    
    def _get_dpia_template(self) -> str:
        """获取DPIA报告模板"""
        return """
# 数据保护影响评估报告 (DPIA Report)
## 根据GDPR Article 35要求

### 项目信息
**项目名称**: {project_name}
**评估日期**: {assessment_date}
**评估版本**: {assessment_version}
**负责人**: {responsible_person}

### 1. 处理活动描述
**处理目的**: {processing_purpose}
**合法性基础**: {legal_basis}
**数据类别**: {data_categories}
**数据来源**: {data_sources}
**数据接收方**: {data_recipients}
**保留期限**: {retention_period}

### 2. 必要性和比例性评估
**处理必要性**:
{processing_necessity}

**比例性评估**:
{proportionality_assessment}

**替代方案**:
{alternatives_considered}

### 3. 风险评估
#### 3.1 对数据主体权利和自由的风险
{rights_risks}

#### 3.2 可能性评估
{likelihood_assessment}

#### 3.3 影响程度评估
{impact_assessment}

#### 3.4 总体风险等级
{overall_risk_level}

### 4. 拟采取措施
#### 4.1 技术措施
{technical_measures}

#### 4.2 组织措施
{organizational_measures}

#### 4.3 合同措施
{contractual_measures}

### 5. DPO咨询意见
{dpo_opinion}

### 6. 处理者咨询
{processor_consultation}

### 7. 监管机构咨询
{supervisory_consultation}

### 8. 批准和监控
**批准人**: {approver_name}
**批准日期**: {approval_date}
**监控计划**: {monitoring_plan}

### 9. 附件
{attachments}
"""
    
    def _get_consent_form_template(self) -> str:
        """获取同意表格模板"""
        return """
# 数据处理同意表格 (Consent Form)
## 根据GDPR要求

### 数据处理信息
**数据处理者**: {data_controller}
**处理目的**: {processing_purpose}
**数据类别**: {data_categories}
**数据接收方**: {data_recipients}
**保留期限**: {retention_period}

### 您的权利
根据GDPR，您拥有以下权利：
1. **撤回同意权**: 您有权随时撤回同意，不影响撤回前处理的合法性
2. **访问权**: 获取您的个人数据副本
3. **更正权**: 更正不准确的数据
4. **删除权**: 要求删除您的数据
5. **限制处理权**: 限制数据处理
6. **数据可携权**: 获取结构化、常用格式的数据副本
7. **反对权**: 反对基于合法利益的数据处理
8. **投诉权**: 向监管机构投诉

### 同意声明
我，{data_subject_name}，确认：

1. □ 我已阅读并理解上述信息
2. □ 我了解我可以随时撤回同意
3. □ 我了解我的GDPR权利
4. □ 我自愿同意上述数据处理活动

### 签字
**数据主体**: ___________________________
**日期**: {consent_date}
**联系方式**: {contact_information}

### 数据处理者确认
**确认接收**: ___________________________
**确认日期**: {acknowledgement_date}
**联系方式**: {controller_contact}
"""
    
    def _get_dsr_form_template(self) -> str:
        """获取数据主体权利请求表格模板"""
        return """
# 数据主体权利请求表格 (Data Subject Request Form)
## 根据GDPR要求

### 请求人信息
**姓名**: {requester_name}
**地址**: {requester_address}
**联系方式**: {requester_contact}
**身份证明**: {id_proof} (如身份证复印件)

### 请求类型 (请选择一项)
□ **访问权** (Article 15) - 获取我的个人数据副本
□ **更正权** (Article 16) - 更正不准确的数据
□ **删除权** (Article 17) - 删除我的数据
□ **限制处理权** (Article 18) - 限制数据处理
□ **数据可携权** (Article 20) - 获取结构化格式的数据
□ **反对权** (Article 21) - 反对基于合法利益的处理
□ **撤回同意** - 撤回之前给予的同意

### 请求详细信息
**涉及的数据处理活动**: {processing_activity}
**具体请求内容**: {request_details}
**相关时间范围**: {relevant_time_period}

### 数据处理者响应
**收到请求日期**: {receipt_date}
**响应截止日期**: {response_deadline} (应在收到后1个月内)
**响应状态**: {response_status}
**响应内容**: {response_content}

### 请求处理记录
**处理人**: {handler_name}
**处理日期**: {handling_date}
**采取的措施**: {measures_taken}
**备注**: {notes}

### 投诉信息
如对响应不满意，您有权向监管机构投诉：
**监管机构**: {supervisory_authority}
**联系方式**: {supervisory_contact}
**投诉截止日期**: {complaint_deadline}
"""
    
    def generate_document(self, template_name: str, data: Dict[str, Any]) -> str:
        """
        生成文档
        
        Args:
            template_name: 模板名称
            data: 模板数据
            
        Returns:
            生成的文档内容
        """
        if template_name not in self.templates:
            available = ", ".join(self.templates.keys())
            raise ValueError(f"模板 '{template_name}' 不存在。可用模板: {available}")
        
        template = self.templates[template_name]
        
        # 添加默认值
        default_data = {
            "update_date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "effective_date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "signature_date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "consent_date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "receipt_date": datetime.datetime.now().strftime("%Y-%m-%d"),
        }
        
        # 合并数据
        merged_data = {**default_data, **data}
        
        # 格式化模板
        try:
            document = template.format(**merged_data)
            return document
        except KeyError as e:
            missing_key = str(e).strip("'")
            raise ValueError(f"模板数据缺少必要的键: {missing_key}")
    
    def save_document(self, template_name: str, data: Dict[str, Any], 
                     output_path: str, format: str = "txt") -> str:
        """
        生成并保存文档
        
        Args:
            template_name: 模板名称
            data: 模板数据
            output_path: 输出路径
            format: 输出格式 (txt, md, json)
            
        Returns:
            保存的文件路径
        """
        document = self.generate_document(template_name, data)
        
        output_file = Path(output_path)
        
        if format == "json":
            # 将文档结构化为JSON
            doc_data = {
                "template": template_name,
                "generated_date": datetime.datetime.now().isoformat(),
                "content": document,
                "metadata": data
            }
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(doc_data, f, ensure_ascii=False, indent=2)
        else:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(document)
        
        return str(output_file.absolute())


def main():
    """测试函数"""
    engine = GDPRTemplateEngine()
    
    # 测试隐私通知生成
    print("测试隐私通知生成:")
    privacy_data = {
        "company_name": "示例公司",
        "company_address": "示例地址",
        "dpo_name": "张三",
        "dpo_email": "dpo@example.com",
        "contact_email": "contact@example.com",
        "processing_purposes": "| 营销 | 同意 | 姓名、邮箱 | 2年 |",
        "data_recipients": "- 内部部门\n- 服务提供商",
        "data_transfers": "无跨境传输",
        "supervisory_authority": "示例监管机构",
        "supervisory_contact": "supervisory@example.com",
        "dpo_phone": "+1234567890"
    }
    
    try:
        document = engine.generate_document("privacy_notice", privacy_data)
        print("✅ 隐私通知生成成功")
        print(f"文档长度: {len(document)} 字符")
        
        # 保存测试
        saved_path = engine.save_document("privacy_notice", privacy_data, 
                                         "test_privacy_notice.md", "md")
        print(f"✅ 文档已保存到: {saved_path}")
        
    except Exception as e:
        print(f"❌ 生成失败: {e}")


if __name__ == "__main__":
    main()