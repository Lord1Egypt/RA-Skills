#!/usr/bin/env python3
"""
GDPR数据验证工具
提供GDPR合规性检查的验证函数
"""

import json
import datetime
from typing import Dict, List, Any, Optional, Tuple


class GDPRValidator:
    """GDPR数据验证器"""
    
    @staticmethod
    def validate_legal_basis(legal_basis: str) -> Tuple[bool, str]:
        """
        验证合法性基础是否符合GDPR Article 6
        
        Args:
            legal_basis: 合法性基础
            
        Returns:
            Tuple[是否有效, 说明]
        """
        valid_bases = [
            "consent",  # 同意
            "contract",  # 合同履行
            "legal_obligation",  # 法定义务
            "vital_interests",  # 重大利益
            "public_task",  # 公共利益任务
            "legitimate_interests"  # 合法利益
        ]
        
        if legal_basis.lower() in valid_bases:
            return True, f"合法性基础 '{legal_basis}' 符合GDPR Article 6要求"
        else:
            return False, f"合法性基础 '{legal_basis}' 不符合GDPR要求。有效的合法性基础包括: {', '.join(valid_bases)}"
    
    @staticmethod
    def validate_data_subject_rights(rights: List[str]) -> Tuple[bool, List[str]]:
        """
        验证数据主体权利是否完整
        
        Args:
            rights: 数据主体权利列表
            
        Returns:
            Tuple[是否完整, 缺失的权利列表]
        """
        required_rights = [
            "right_to_be_informed",  # 知情权 (Articles 13-14)
            "right_of_access",  # 访问权 (Article 15)
            "right_to_rectification",  # 更正权 (Article 16)
            "right_to_erasure",  # 删除权 (Article 17)
            "right_to_restrict_processing",  # 限制处理权 (Article 18)
            "right_to_data_portability",  # 数据可携权 (Article 20)
            "right_to_object",  # 反对权 (Article 21)
            "rights_related_to_automated_decision_making"  # 自动化决策相关权利 (Article 22)
        ]
        
        missing_rights = []
        for right in required_rights:
            if right not in rights:
                missing_rights.append(right)
        
        is_complete = len(missing_rights) == 0
        return is_complete, missing_rights
    
    @staticmethod
    def validate_special_category_data(data_types: List[str]) -> Tuple[bool, List[str]]:
        """
        验证特殊类别个人数据的处理
        
        Args:
            data_types: 处理的数据类型列表
            
        Returns:
            Tuple[是否包含特殊数据, 特殊数据类型列表]
        """
        special_categories = [
            "racial_or_ethnic_origin",  # 种族或民族出身
            "political_opinions",  # 政治观点
            "religious_or_philosophical_beliefs",  # 宗教或哲学信仰
            "trade_union_membership",  # 工会会员身份
            "genetic_data",  # 基因数据
            "biometric_data",  # 生物识别数据
            "health_data",  # 健康数据
            "sex_life_or_sexual_orientation"  # 性生活或性取向
        ]
        
        found_special = []
        for data_type in data_types:
            if data_type.lower() in special_categories:
                found_special.append(data_type)
        
        has_special = len(found_special) > 0
        return has_special, found_special
    
    @staticmethod
    def check_dpo_requirement(data_processing: Dict[str, Any]) -> Tuple[bool, str]:
        """
        检查是否需要指定数据保护官（DPO）
        
        Args:
            data_processing: 数据处理信息
            
        Returns:
            Tuple[是否需要DPO, 说明]
        """
        # GDPR要求DPO的情况 (Article 37)
        requires_dpo = False
        reasons = []
        
        # 1. 公共机构或机关
        if data_processing.get("is_public_authority", False):
            requires_dpo = True
            reasons.append("公共机构或机关")
        
        # 2. 核心活动涉及大规模系统化监控
        if (data_processing.get("core_activities_monitoring", False) and 
            data_processing.get("monitoring_scale", "small") in ["large", "systematic"]):
            requires_dpo = True
            reasons.append("核心活动涉及大规模系统化监控")
        
        # 3. 核心活动涉及大规模处理特殊类别数据
        special_categories = data_processing.get("special_categories_data", [])
        if (len(special_categories) > 0 and 
            data_processing.get("processing_scale", "small") in ["large", "systematic"]):
            requires_dpo = True
            reasons.append("核心活动涉及大规模处理特殊类别数据")
        
        if requires_dpo:
            return True, f"需要指定数据保护官（DPO），原因: {', '.join(reasons)}"
        else:
            return False, "不需要指定数据保护官（DPO）"
    
    @staticmethod
    def check_dpia_requirement(data_processing: Dict[str, Any]) -> Tuple[bool, str]:
        """
        检查是否需要数据保护影响评估（DPIA）
        
        Args:
            data_processing: 数据处理信息
            
        Returns:
            Tuple[是否需要DPIA, 说明]
        """
        # 需要DPIA的情况 (Article 35)
        requires_dpia = False
        reasons = []
        
        # 1. 系统化和广泛评估个人方面
        if data_processing.get("systematic_evaluation", False):
            requires_dpia = True
            reasons.append("系统化和广泛评估个人方面")
        
        # 2. 自动化决策产生法律效果
        if data_processing.get("automated_decision_making", False):
            requires_dpia = True
            reasons.append("自动化决策产生法律效果")
        
        # 3. 大规模处理特殊类别数据
        special_categories = data_processing.get("special_categories_data", [])
        if len(special_categories) > 0 and data_processing.get("processing_scale", "large"):
            requires_dpia = True
            reasons.append("大规模处理特殊类别数据")
        
        # 4. 大规模系统化监控公共区域
        if (data_processing.get("public_area_monitoring", False) and 
            data_processing.get("monitoring_scale", "small") == "large"):
            requires_dpia = True
            reasons.append("大规模系统化监控公共区域")
        
        if requires_dpia:
            return True, f"需要数据保护影响评估（DPIA），原因: {', '.join(reasons)}"
        else:
            return False, "不需要数据保护影响评估（DPIA）"
    
    @staticmethod
    def validate_data_retention_period(retention_info: Dict[str, Any]) -> Tuple[bool, str]:
        """
        验证数据保留期限是否符合GDPR要求
        
        Args:
            retention_info: 数据保留信息
            
        Returns:
            Tuple[是否合规, 说明]
        """
        period = retention_info.get("retention_period", 0)
        purpose = retention_info.get("retention_purpose", "")
        has_deletion_plan = retention_info.get("has_deletion_plan", False)
        
        # GDPR要求：数据保留期限不应超过实现目的所需时间
        if period <= 0:
            return False, "数据保留期限未指定"
        
        if period > 365 * 10:  # 超过10年
            return False, f"数据保留期限 {period} 天可能过长，需提供正当理由"
        
        if not has_deletion_plan:
            return False, "缺少数据删除计划"
        
        return True, f"数据保留期限 {period} 天似乎合理，目的: {purpose}"
    
    @staticmethod
    def check_cross_border_transfer(transfer_info: Dict[str, Any]) -> Tuple[bool, str, List[str]]:
        """
        检查跨境传输合规性
        
        Args:
            transfer_info: 跨境传输信息
            
        Returns:
            Tuple[是否合规, 说明, 建议措施]
        """
        destination = transfer_info.get("destination_country", "")
        transfer_mechanism = transfer_info.get("transfer_mechanism", "")
        data_types = transfer_info.get("data_types", [])
        
        # 充分性决定国家
        adequacy_countries = [
            "andorra", "argentina", "canada", "faroe islands", "guernsey",
            "israel", "isle of man", "japan", "jersey", "new zealand",
            "switzerland", "uruguay", "south korea", "united kingdom"
        ]
        
        recommendations = []
        
        # 检查目的地
        if destination.lower() in adequacy_countries:
            return True, f"目的地 {destination} 有充分性决定，传输合规", recommendations
        
        # 检查传输机制
        valid_mechanisms = [
            "standard_contractual_clauses",  # 标准合同条款
            "binding_corporate_rules",  # 约束性公司规则
            "approved_code_of_conduct",  # 批准的行为准则
            "approved_certification_mechanism",  # 批准的认证机制
            "derogations"  # 例外情况
        ]
        
        if transfer_mechanism not in valid_mechanisms:
            recommendations.append(f"需要建立有效的传输机制。有效机制: {', '.join(valid_mechanisms)}")
            return False, f"跨境传输到 {destination} 缺少有效机制", recommendations
        
        # 检查特殊数据
        has_special, special_types = GDPRValidator.validate_special_category_data(data_types)
        if has_special:
            recommendations.append(f"传输包含特殊类别数据: {', '.join(special_types)}，需额外保护措施")
        
        return True, f"跨境传输到 {destination} 使用 {transfer_mechanism} 机制", recommendations


def main():
    """测试函数"""
    validator = GDPRValidator()
    
    # 测试合法性基础验证
    print("1. 测试合法性基础验证:")
    result, message = validator.validate_legal_basis("consent")
    print(f"   consent: {result} - {message}")
    
    result, message = validator.validate_legal_basis("invalid")
    print(f"   invalid: {result} - {message}")
    
    # 测试数据主体权利验证
    print("\n2. 测试数据主体权利验证:")
    rights = ["right_to_be_informed", "right_of_access"]
    result, missing = validator.validate_data_subject_rights(rights)
    print(f"   权利列表: {rights}")
    print(f"   是否完整: {result}")
    print(f"   缺失权利: {missing}")
    
    # 测试DPO要求检查
    print("\n3. 测试DPO要求检查:")
    data_processing = {
        "is_public_authority": True,
        "core_activities_monitoring": False,
        "processing_scale": "small"
    }
    result, message = validator.check_dpo_requirement(data_processing)
    print(f"   数据处理: {data_processing}")
    print(f"   需要DPO: {result} - {message}")


if __name__ == "__main__":
    main()