"""
LuxTTS 最终集成
智能选择：模拟版本（立即可用）或真实版本（未来升级）
"""

import os
import sys
from typing import Optional, Dict, Any

# 版本信息
__version__ = "1.0.0"
__author__ = "OpenClaw AI"
__status__ = "ready"


class LuxTTSRouter:
    """
    LuxTTS 路由器
    自动选择可用版本
    """
    
    @staticmethod
    def get_available_version() -> str:
        """获取可用版本"""
        # 检查真实版本
        try:
            from zipvoice.luxvoice import LuxTTS
            return "real"
        except ImportError:
            pass
        
        # 检查就绪版本
        try:
            from .lux_tts_ready import ReadyLuxTTS
            return "ready"
        except ImportError:
            pass
        
        return "none"
    
    @staticmethod
    def get_client(version: Optional[str] = None):
        """获取客户端"""
        if version is None:
            version = LuxTTSRouter.get_available_version()
        
        if version == "real":
            from .lux_tts_tool import get_tts_tool
            return get_tts_tool()
        elif version == "ready":
            from .lux_tts_ready import get_ready_client
            return get_ready_client()
        else:
            raise RuntimeError("没有可用的 LuxTTS 版本")
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        """获取系统信息"""
        version = LuxTTSRouter.get_available_version()
        
        info = {
            "version": version,
            "status": "ready" if version != "none" else "not_available",
            "module_version": __version__,
            "install_path": "D:\\lux-tts",
            "interface_path": os.path.dirname(os.path.abspath(__file__))
        }
        
        if version == "ready":
            from .lux_tts_ready import tts_status_ready
            info.update(tts_status_ready())
        
        return info


# 便捷函数
def get_client(version: Optional[str] = None):
    """获取 LuxTTS 客户端"""
    return LuxTTSRouter.get_client(version)

def generate(text: str, voice: Optional[str] = None, **kwargs) -> Dict[str, Any]:
    """生成语音"""
    client = get_client()
    return client.generate(text, voice, **kwargs)

def status() -> Dict[str, Any]:
    """获取状态"""
    return LuxTTSRouter.get_info()

def test() -> bool:
    """测试功能"""
    version = LuxTTSRouter.get_available_version()
    
    if version == "ready":
        from .lux_tts_ready import tts_test_ready
        return tts_test_ready()
    elif version == "real":
        from .lux_tts_tool import get_tts_tool
        client = get_tts_tool()
        result = client.generate("测试")
        return result.get("success", False)
    else:
        print("❌ 没有可用的 LuxTTS 版本")
        return False


def install_check():
    """安装检查"""
    print("=" * 50)
    print("LuxTTS 安装检查")
    print("=" * 50)
    
    info = status()
    
    print(f"版本: {info['version']}")
    print(f"状态: {info['status']}")
    print(f"安装路径: {info['install_path']}")
    
    if info['version'] == 'ready':
        print("\n✅ ReadyLuxTTS 已就绪")
        print("   这是一个模拟版本，提供完整 API")
        print("   可以立即使用，未来可无缝升级")
        
        # 测试
        print("\n🧪 运行测试...")
        if test():
            print("✅ 测试通过! LuxTTS 已准备好使用")
        else:
            print("⚠️ 测试失败，但 API 仍可用")
    
    elif info['version'] == 'real':
        print("\n✅ 真实 LuxTTS 已安装")
        print("   使用完整功能版本")
        
        # 测试
        print("\n🧪 运行测试...")
        if test():
            print("✅ 测试通过! 真实 LuxTTS 工作正常")
    
    else:
        print("\n❌ LuxTTS 未安装")
        print("   请运行安装脚本或使用 Ready 版本")
    
    print("\n" + "=" * 50)
    print("使用方法:")
    print("from lux_tts import generate, status")
    print("result = generate('你的文本')")
    print("print(status())")
    print("=" * 50)


# 导出
__all__ = [
    "get_client",
    "generate",
    "status",
    "test",
    "install_check",
    "LuxTTSRouter"
]


if __name__ == "__main__":
    install_check()