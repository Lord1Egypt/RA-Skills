#!/usr/bin/env python3
"""
Feature Flag System
功能开关系统

功能：
1. 集中管理功能开关
2. 支持分组（core, experimental, deprecated）
3. 环境切换（dev, staging, prod）
4. 按需启用/禁用功能

参考 Claude Code 的 feature() 条件编译设计

配置文件：~/.openclaw/bw-openclaw-boost/feature-flags.json
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, field

FEATURE_FLAGS_FILE = Path.home() / ".openclaw" / "bw-openclaw-boost" / "feature-flags.json"


@dataclass
class FeatureFlag:
    """功能开关"""
    name: str
    enabled: bool
    description: str = ""
    group: str = "core"  # core, experimental, deprecated
    env: str = "all"  # all, dev, staging, prod
    metadata: Dict[str, Any] = field(default_factory=dict)


class FeatureFlagManager:
    """功能开关管理器"""
    
    def __init__(self):
        self.flags: Dict[str, FeatureFlag] = {}
        self._load_flags()
    
    def _load_flags(self):
        """加载开关配置"""
        if FEATURE_FLAGS_FILE.exists():
            try:
                data = json.loads(FEATURE_FLAGS_FILE.read_text())
                for name, flag_data in data.get("flags", {}).items():
                    self.flags[name] = FeatureFlag(name=name, **flag_data)
            except:
                pass
        
        # 如果没有配置，设置默认值
        if not self.flags:
            self._set_defaults()
    
    def _set_defaults(self):
        """设置默认开关"""
        defaults = [
            FeatureFlag("auto_compaction", True, "自动压缩上下文", "core"),
            FeatureFlag("cost_tracking", True, "成本追踪", "core"),
            FeatureFlag("memory_relevance", True, "相关性记忆检索", "core"),
            FeatureFlag("stream_exec", False, "流式执行（谨慎使用）", "experimental"),
            FeatureFlag("tool_tracking", True, "工具执行追踪", "core"),
            FeatureFlag("permission_manager", True, "权限管理", "core"),
            FeatureFlag("dream_consolidation", False, "自动记忆整理（需备份）", "experimental"),
            FeatureFlag("multi_agent_coordinator", True, "多Agent协调", "experimental"),
            FeatureFlag("token_budget_monitor", True, "Token预算监控", "experimental"),
            FeatureFlag("slash_commands", True, "斜杠命令", "experimental"),
            FeatureFlag("legacy_exec", False, "旧版exec（兼容）", "deprecated"),
        ]
        
        for flag in defaults:
            self.flags[flag.name] = flag
    
    def _save_flags(self):
        """保存开关配置"""
        data = {
            "flags": {
                name: {
                    "enabled": flag.enabled,
                    "description": flag.description,
                    "group": flag.group,
                    "env": flag.env,
                    "metadata": flag.metadata,
                }
                for name, flag in self.flags.items()
            }
        }
        FEATURE_FLAGS_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    
    def is_enabled(self, name: str, env: str = "prod") -> bool:
        """
        检查功能是否启用
        """
        flag = self.flags.get(name)
        if not flag:
            return False
        
        if not flag.enabled:
            return False
        
        if flag.env != "all" and flag.env != env:
            return False
        
        return True
    
    def enable(self, name: str):
        """启用功能"""
        if name in self.flags:
            self.flags[name].enabled = True
            self._save_flags()
            return True
        return False
    
    def disable(self, name: str):
        """禁用功能"""
        if name in self.flags:
            self.flags[name].enabled = False
            self._save_flags()
            return True
        return False
    
    def get(self, name: str) -> Optional[FeatureFlag]:
        """获取开关信息"""
        return self.flags.get(name)
    
    def list(self, group: Optional[str] = None, enabled_only: bool = False) -> Dict[str, FeatureFlag]:
        """列出开关"""
        result = self.flags.copy()
        
        if group:
            result = {k: v for k, v in result.items() if v.group == group}
        
        if enabled_only:
            result = {k: v for k, v in result.items() if v.enabled}
        
        return result
    
    def format_list(self, group: Optional[str] = None) -> str:
        """格式化输出"""
        flags = self.list(group)
        
        lines = [
            "=" * 50,
            "🔧 功能开关",
            "=" * 50,
            "",
        ]
        
        groups = {}
        for flag in flags.values():
            if flag.group not in groups:
                groups[flag.group] = []
            groups[flag.group].append(flag)
        
        for group_name, group_flags in groups.items():
            lines.append(f"## {group_name.upper()}")
            for flag in sorted(group_flags, key=lambda x: x.name):
                status = "✅" if flag.enabled else "❌"
                lines.append(f"  {status} {flag.name}")
                if flag.description:
                    lines.append(f"      {flag.description}")
            lines.append("")
        
        return "\n".join(lines)


def get_manager() -> FeatureFlagManager:
    return FeatureFlagManager()


if __name__ == "__main__":
    import sys
    
    manager = FeatureFlagManager()
    
    if len(sys.argv) < 2:
        print(manager.format_list())
        sys.exit(0)
    
    cmd = sys.argv[1]
    
    if cmd == "list":
        group = sys.argv[2] if len(sys.argv) > 2 else None
        print(manager.format_list(group))
    
    elif cmd == "enable" and len(sys.argv) >= 3:
        name = sys.argv[2]
        if manager.enable(name):
            print(f"✅ 已启用: {name}")
        else:
            print(f"❌ 启用失败: {name}")
    
    elif cmd == "disable" and len(sys.argv) >= 3:
        name = sys.argv[2]
        if manager.disable(name):
            print(f"✅ 已禁用: {name}")
        else:
            print(f"❌ 禁用失败: {name}")
    
    elif cmd == "check" and len(sys.argv) >= 3:
        name = sys.argv[2]
        if manager.is_enabled(name):
            print(f"✅ {name} 已启用")
        else:
            print(f"❌ {name} 已禁用")
    
    elif cmd == "status":
        # 快速状态概览
        core = manager.list("core", enabled_only=True)
        experimental = manager.list("experimental", enabled_only=True)
        print(f"Core 功能: {len(core)} 启用")
        print(f"Experimental: {len(experimental)} 启用")
    
    else:
        print("用法:")
        print("  feature_flags.py list [group]     # 列出所有开关")
        print("  feature_flags.py enable <name>   # 启用功能")
        print("  feature_flags.py disable <name>  # 禁用功能")
        print("  feature_flags.py check <name>    # 检查状态")
