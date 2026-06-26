"""
映射器工厂
根据目标系统自动选择合适的映射器
"""

from typing import Optional, Dict, List
from functools import lru_cache

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from mappers.base_mapper import BaseMapper
from mappers.bipv5_mapper import BIPV5Mapper
from mappers.eas_yxh_mapper import EasYxhMapper
from mappers.fingard_mapper import FingardMapper
from mappers.nstc_mapper import NstcMapper
from mappers.yyncc_mapper import YynccMapper


class MapperFactory:
    """映射器工厂"""

    # 支持的映射器注册表
    _mappers: Dict[str, BaseMapper] = {}

    @classmethod
    def register_mapper(cls, target_system: str, mapper: BaseMapper):
        """注册映射器"""
        cls._mappers[target_system.upper()] = mapper

    @classmethod
    def get_mapper(cls, target_system: str) -> BaseMapper:
        """
        根据目标系统获取映射器

        Args:
            target_system: 目标系统名称

        Returns:
            映射器实例

        Raises:
            ValueError: 没有找到匹配的映射器
        """
        target_upper = target_system.upper()

        if not cls._mappers:
            cls._register_default_mappers()

        if target_upper not in cls._mappers:
            supported = list(cls._mappers.keys())
            raise ValueError(
                f"不支持的目标系统: {target_system}",
                f"支持的系统: {', '.join(supported)}"
            )

        return cls._mappers[target_upper]

    @classmethod
    def _register_default_mappers(cls):
        """注册默认映射器"""
        cls.register_mapper('BIPV5', BIPV5Mapper())
        cls.register_mapper('EAS_YXH', EasYxhMapper())
        cls.register_mapper('FINGARD', FingardMapper())
        cls.register_mapper('NSTC', NstcMapper())
        cls.register_mapper('YYNCC', YynccMapper())

    @classmethod
    def supported_systems(cls) -> List[str]:
        """获取支持的目标系统列表"""
        if not cls._mappers:
            cls._register_default_mappers()
        return list(cls._mappers.keys())


@lru_cache(maxsize=8)
def get_mapper(target_system: str) -> BaseMapper:
    """
    获取映射器的便捷函数

    Args:
        target_system: 目标系统名称

    Returns:
        映射器实例
    """
    return MapperFactory.get_mapper(target_system)


def create_mapper(target_system: str, **kwargs) -> Optional[BaseMapper]:
    """
    根据目标系统创建映射器

    Args:
        target_system: 目标系统名称
        **kwargs: 传递给映射器的额外参数

    Returns:
        映射器实例，如果没有匹配的格式返回 None
    """
    if not MapperFactory._mappers:
        MapperFactory._register_default_mappers()

    target_upper = target_system.upper()

    if target_upper == 'BIPV5':
        return BIPV5Mapper(kwargs.get('config_path'))
    elif target_upper == 'EAS_YXH':
        return EasYxhMapper(kwargs.get('template_path'))
    elif target_upper == 'FINGARD':
        return FingardMapper(kwargs.get('template_path'))
    elif target_upper == 'NSTC':
        return NstcMapper(kwargs.get('template_path'))
    elif target_upper == 'YYNCC':
        return YynccMapper(kwargs.get('template_path'))

    return None
