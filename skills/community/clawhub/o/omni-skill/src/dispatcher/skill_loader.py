"""
最近最少使用缓存与延迟加载器 (LRU Cache & Lazy Loader)
"""
import importlib
from collections import OrderedDict
from typing import Any, Optional
import config.settings as settings

class SkillLazyLoader:
    """带有 LRU 淘汰机制的技能延迟加载器"""
    def __init__(self, capacity: int = settings.CACHE_CAPACITY):
        self.capacity = capacity # 最大缓存实例数
        self.cache = OrderedDict() # LRU 缓存字典

    def load_skill(self, skill_id: str, module_path: str, class_name: str) -> Optional[Any]:
        """延迟加载技能实例"""
        # 若已在缓存中，则置于最前 (刷新 LRU 状态)
        if skill_id in self.cache:
            self.cache.move_to_end(skill_id)
            return self.cache[skill_id]

        # 缓存若满，触发 LRU 淘汰机制
        if len(self.cache) >= self.capacity:
            self.cache.popitem(last=False)

        # 动态导入模块
        try:
            # 引入模块
            module = importlib.import_module(module_path)
            skill_class = getattr(module, class_name)
            skill_instance = skill_class() # 实例化技能

            # 存入缓存
            self.cache[skill_id] = skill_instance
            return skill_instance
        except ImportError as e:
            # 模块加载失败
            print(f"[警告] 加载技能 {skill_id} 失败，未找到路径: {str(e)}")
            return None
        except AttributeError as e:
            # 类名不存在
            print(f"[警告] 加载技能 {skill_id} 失败，未找到类名: {str(e)}")
            return None
        except Exception as e:
            # 其他异常
            print(f"[警告] 加载技能 {skill_id} 发生异常: {str(e)}")
            return None