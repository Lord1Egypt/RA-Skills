"""
许可证管理模块
负责查询和分配 Microsoft 365 许可证
"""
import logging

logger = logging.getLogger(__name__)


class NoAvailableLicenseError(Exception):
    """无可用许可证错误"""
    pass


class LicenseManager:
    """管理 Microsoft 365 许可证"""
    
    def __init__(self, graph_client):
        """
        初始化 LicenseManager
        
        Args:
            graph_client: GraphClient 实例
        """
        self.graph_client = graph_client
    
    def get_available_skus(self) -> list:
        """
        获取可用的 SKU 列表（consumedUnits < totalUnits）
        
        Returns:
            list: 可用 SKU 列表，每个包含 skuId, skuPartNumber, availableUnits
        """
        logger.info("查询可用的许可证 SKU")
        all_skus = self.graph_client.get_subscribed_skus()
        
        available_skus = []
        for sku in all_skus:
            consumed = sku.get('consumedUnits', 0)
            total = sku.get('prepaidUnits', {}).get('enabled', 0)
            available = total - consumed
            
            if available > 0:
                available_skus.append({
                    'skuId': sku.get('skuId'),
                    'skuPartNumber': sku.get('skuPartNumber'),
                    'availableUnits': available,
                    'totalUnits': total,
                    'consumedUnits': consumed
                })
        
        logger.info(f"找到 {len(available_skus)} 个可用许可证 SKU")
        return available_skus
    
    def find_sku_by_part_number(self, part_number: str) -> dict:
        """
        根据 SKU Part Number 查找 SKU（支持多个可能的名称）
        
        Args:
            part_number: SKU Part Number 或别名（如 "O365_BUSINESS", "BUSINESS"）
        
        Returns:
            dict: SKU 信息，包含 skuId, skuPartNumber, availableUnits
        
        Raises:
            NoAvailableLicenseError: 如果找不到指定的 SKU
        """
        logger.info(f"查找 SKU: {part_number}")
        all_skus = self.graph_client.get_subscribed_skus()
        
        # 定义可能的 SKU Part Number 映射（Microsoft 365 商业应用版）
        # 根据不同的订阅类型，可能有不同的 Part Number
        possible_part_numbers = []
        part_upper = part_number.upper()
        
        if part_upper in ['O365_BUSINESS', 'BUSINESS', 'MICROSOFT 365 商业应用版', '商业应用版']:
            possible_part_numbers = [
                'O365_BUSINESS',
                'O365_BUSINESS_ESSENTIALS',
                'O365_BUSINESS_PREMIUM',
                'MICROSOFT365_BUSINESS',
                'M365_BUSINESS_BASIC',
                'M365_BUSINESS_STANDARD',
                'M365_BUSINESS_PREMIUM'
            ]
        else:
            possible_part_numbers = [part_number]
        
        # 先尝试精确匹配
        for sku in all_skus:
            sku_part = sku.get('skuPartNumber', '').upper()
            if sku_part == part_upper:
                consumed = sku.get('consumedUnits', 0)
                total = sku.get('prepaidUnits', {}).get('enabled', 0)
                available = total - consumed
                
                if available > 0:
                    return {
                        'skuId': sku.get('skuId'),
                        'skuPartNumber': sku.get('skuPartNumber'),
                        'availableUnits': available,
                        'totalUnits': total,
                        'consumedUnits': consumed
                    }
                else:
                    raise NoAvailableLicenseError(f"SKU {sku.get('skuPartNumber')} 没有可用许可证")
        
        # 如果精确匹配失败，尝试可能的 Part Number 列表
        for possible_part in possible_part_numbers:
            for sku in all_skus:
                sku_part = sku.get('skuPartNumber', '').upper()
                if sku_part == possible_part.upper():
                    consumed = sku.get('consumedUnits', 0)
                    total = sku.get('prepaidUnits', {}).get('enabled', 0)
                    available = total - consumed
                    
                    if available > 0:
                        logger.info(f"找到匹配的 SKU: {sku.get('skuPartNumber')}")
                        return {
                            'skuId': sku.get('skuId'),
                            'skuPartNumber': sku.get('skuPartNumber'),
                            'availableUnits': available,
                            'totalUnits': total,
                            'consumedUnits': consumed
                        }
                    else:
                        raise NoAvailableLicenseError(f"SKU {sku.get('skuPartNumber')} 没有可用许可证")
        
        # 如果都找不到，列出所有可用的 SKU 供参考
        available_skus = self.get_available_skus()
        if available_skus:
            logger.warning(f"未找到 SKU: {part_number}，可用的 SKU 列表：")
            for sku in available_skus:
                logger.warning(f"  - {sku['skuPartNumber']} ({sku['skuId']})")
        
        raise NoAvailableLicenseError(f"未找到 SKU: {part_number}")
    
    def assign_license_to_user(self, user_id: str, sku_id: str = None, sku_part_number: str = None) -> dict:
        """
        为用户分配许可证
        
        Args:
            user_id: 用户 ID
            sku_id: 要分配的 SKU ID，如果为 None 则根据 sku_part_number 查找或自动选择第一个可用 SKU
            sku_part_number: SKU Part Number（如 "O365_BUSINESS"），用于查找特定许可证
        
        Returns:
            dict: 分配结果（更新后的用户对象）
        
        Raises:
            NoAvailableLicenseError: 如果没有可用的许可证
        """
        if sku_id is None:
            if sku_part_number:
                # 根据 Part Number 查找 SKU
                sku_info = self.find_sku_by_part_number(sku_part_number)
                sku_id = sku_info['skuId']
                logger.info(f"找到 SKU: {sku_id} ({sku_info['skuPartNumber']})")
            else:
                # 自动选择第一个可用 SKU
                available_skus = self.get_available_skus()
                
                if not available_skus:
                    error_msg = "没有可用的许可证 SKU"
                    logger.error(error_msg)
                    raise NoAvailableLicenseError(error_msg)
                
                sku_id = available_skus[0]['skuId']
                logger.info(f"自动选择 SKU: {sku_id} ({available_skus[0]['skuPartNumber']})")
        
        # 构建许可证分配请求
        add_licenses = [{
            'skuId': sku_id,
            'disabledPlans': []
        }]
        
        logger.info(f"为用户 {user_id} 分配许可证 {sku_id}")
        result = self.graph_client.assign_license(user_id, add_licenses)
        logger.info(f"成功为用户 {user_id} 分配许可证")
        
        return result

